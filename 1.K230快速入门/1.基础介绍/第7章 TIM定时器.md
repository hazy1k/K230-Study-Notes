# 第七章 TIM定时器

## 1. TIM基础配置

K230 内部集成了 6 个 Timer 硬件模块，最小定时周期为 1 毫秒（ms）。

Timer 类位于 `machine` 模块中。

### 1.1 构造函数

```python
timer = Timer(index, mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, arg=None)
```

#### 1.1.1 参数

- `index`: 定时器模块编号，取值范围为 `[-1, 5]`。
  - `-1` 表示软件定时器。
  - `0~5` 为硬件定时器编号，【但当前不可用】。
- `mode`: 定时器运行模式，可选 `Timer.ONE_SHOT` 或 `Timer.PERIODIC`。
  - `ONE_SHOT`：定时器在触发一次回调后自动停止。
  - `PERIODIC`：定时器在触发回调后会自动重置周期，持续周期性触发。
- `freq`: 定时器频率（Hz），可以为浮点数。如果设置了 `freq`，则定时器的时间间隔由频率决定，`freq` 优先级高于 `period`。例如，`freq=1` 相当于 `period=1000ms`。
- `period`: 定时器周期，单位为毫秒（ms），如果未设置 `freq`，则以 `period` 为准。
- `callback`: 超时回调函数。当定时器计数完成后自动调用该函数，函数至少应包含一个参数（接收定时器自身对象或关联参数）。
- `arg`: 超时回调函数的参数（可选）。如果提供了 `arg`，在回调函数中将可以通过传入的参数获取额外信息。

**注意：** **硬件定时器 [0-5] 暂不可用。**

### 1.2 init方法

```python
Timer.init(mode=Timer.PERIODIC, freq=-1, period=-1, callback=None, arg=None)
```

用于初始化或重新配置定时器的参数。参数与构造函数相同。

### 1.3 deinit方法

```py
Timer.deinit()
```

## 2. TIM基础使用示例

```python
from machine import FPIOA, Pin, Timer
import time

RGB = FPIOA()
RGB.set_function(62, FPIOA.GPIO62)
RGB.set_function(20, FPIOA.GPIO20)
RGB.set_function(63, FPIOA.GPIO63)
R = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
G = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
B = Pin(63, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
R.high()
G.high()
B.high()
# 颜色状态
color_state = 0  # 0红1绿2蓝


# 中断回调函数
def led_toggle(timer):
    global color_state
    R.high()
    G.high()
    B.high()
    if color_state == 0:
        R.low()
    elif color_state == 1:
        G.low()
    elif color_state == 2:
        B.low()

    color_state = (color_state + 1) % 3  # 切换颜色


# 创建软件定时器-1
tim = Timer(-1)
# 初始化定时器，每隔500ms调用一次回调函数
tim.init(period=500, mode=Timer.PERIODIC, callback=led_toggle)

while True:
    time.sleep(1)

```

通过在IDE中运行上面的代码，我们可以直观地看到定时器带来的异步定时执行效果：即使主循环在空转（什么都不做），RGB LED 依然会按照定时器设定的周期不断轮换颜色。
