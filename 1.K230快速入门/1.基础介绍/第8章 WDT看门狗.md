# 第八章 WDT看门狗

## 1. 看门狗的工作原理

1. **初始化看门狗：** 系统启动后，首先初始化看门狗定时器，并设置一个超时时间（喂狗时间）。
2. **定时复位看门狗：** 在正常运行中，系统需要定期向看门狗发送信号（称为“喂狗”），重置看门狗的计时器。
3. **触发复位：** 如果系统未能及时“喂狗”，看门狗计时器超时会触发硬件复位操作，将系统恢复到初始状态。

## 2. 看门狗基础配置

K230 内部包含两个 WDT（看门狗定时器）硬件模块，主要用于在应用程序崩溃或进入不可恢复状态时重启系统。一旦启动 WDT，如果在设定的超时时间内没有进行“喂狗”操作，系统将自动复位。

WDT 类位于 `machine` 模块中。

### 2.1 构造函数

```python
wdt = WDT(id=1, timeout=5)
```

#### 2.1.1 参数

- `id`: WDT 模块编号，取值范围为 [0, 1]，默认为 1。
- `timeout`: 超时值，单位为秒（s），默认为 5。

**注意：** WDT0 暂不可用。

### 2.2 feed方法

```python
WDT.feed()
```

执行喂狗操作。

## 3. 看门狗使用举例

```python
from machine import FPIOA, Pin, WDT
import time

gpio = FPIOA()
gpio.set_function(62, FPIOA.GPIO62)
gpio.set_function(20, FPIOA.GPIO20)
gpio.set_function(63, FPIOA.GPIO63)
gpio.set_function(53, FPIOA.GPIO53)
R = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
G = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
B = Pin(63, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
key = Pin(53, Pin.IN, Pin.PULL_DOWN)
R.high()
G.high()
B.high()
color_state = 0 # 颜色状态
# 初始化看门狗，通道1，喂狗时间10s
wwdg = WDT(1, 10)
wwdg.feed() # 先喂狗
while True:
    R.high()
    G.high()
    B.high()
    if color_state == 0:
        R.low()
    elif color_state == 1:
        G.low()
    elif color_state == 2:
        B.low()

    color_state = (color_state + 1) % 3

    if key.value() == 1:
        wwdg.feed() # 进行喂狗
        print("已经成功喂狗啦")
        time.sleep(0.2)

    time.sleep(1)
    
```

看门狗（WDT）的主要作用是就是**监控系统是否正常运行**，并在系统出现异常时触发复位，上面例程并不是真实的使用场景，大家根据自己的时间项目自由设置。
