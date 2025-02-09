# 第三章 PWM控制

## 1. PWM介绍

PWM（Pulse Width Modulation，脉宽调制）是一种在嵌入式系统中常用的技术，它可以用来模拟信号，控制设备的功率输出或者实现对设备的精确控制。PWM信号是一种类似于方波的信号，具有固定的频率，但脉冲宽度（占空比）可以调整。在一定频率下，我们可以通过调整这个占空比来改变他的有效电压，在一定程度上可以实现D/A转换（数字量转模拟量，不过一般来说都是用DAC，本开发板K230的DAC已经被连接到了3.5mm耳机孔上面了，可以用来播放音频）。

- 频率（Frequency）：指PWM信号在一秒内循环的次数。频率是周期的倒数，单位是赫兹（Hz）。
- 周期（Period）：指一个完整的PWM信号的时间长度，与频率成反比。单位是秒（s）。
- 脉宽（Pulse Width）：指PWM信号中高电平（通常为1）的时间长度。单位是秒（s）或毫秒（ms）。
- 占空比(Duty Ratio)：表示在一个完整的PWM信号周期内，高电平（通常为1）所占的时间比例。占空比 = （脉宽 / 周期）x 100%。
- 上升沿（Rising Edge）：PWM信号从低电平跳变到高电平的瞬间，通常用来作为触发事件。
- 下降沿（Falling Edge）：PWM信号从高电平跳变到低电平的瞬间，也常被用作触发事件。
- 正脉冲宽度（Positive Pulse Width）：PWM信号中高电平的持续时间，一般情况下的脉宽指的就是这个。
- 负脉冲宽度（Negative Pulse Width）：PWM信号中低电平的持续时间。

## 2. 开发板上的PWM

![](https://wiki.lckfb.com/storage/images/zh-hans/lushan-pi-k230/basic/pwm/pwm_20241024_140755.png)

| 排针引脚号 | 芯片引脚号   | PWM通道号 |
| ----- | ------- | ------ |
| 12    | GPIO 47 | PWM3   |
| 26    | GPIO 61 | PWM1   |
| 32    | GPIO 46 | PWM2   |
| 33    | GPIO 52 | PWM4   |
| 35    | GPIO 42 | PWM0   |

## 3. PWM基础配置

### 3.1 引脚复用为PWM模式

先用`FPIOA`的`set_function`方法把对应GPIO配置为PWM模式。如下所示：

```python
from machine import FPIOA

test = FPIOA()

test.set_function(47, FPIOA.PWM3)
test.set_function(61, FPIOA.PWM1)
test.set_function(46, FPIOA.PWM2)
test.set_function(52, FPIOA.PWM4)
test.set_function(42, FPIOA.PWM0)
```

### 3.2 配置PWM模块

#### 3.2.1 导入模块

```python
from machine import PWM
```

#### 3.2.2 构造函数

用于构造pin对象，可同时对引脚进行初始化。

```python
pwm = PWM(channel, freq, duty=50, enable=False)
```

##### 3.2.2.1 参数

- `channel`: PWM 通道号，取值范围为 [0, 5]。
- `freq`: PWM 通道输出频率。单位为Hz。
- `duty`: PWM 通道输出占空比，表示高电平在整个周期中的百分比，取值范围为 [0, 100]，支持小数点。可选参数，默认值为 50。
- `enable`: PWM 通道输出是否立即使能，可选参数，默认值为 False。

#### 3.2.3 freq方法

```python
pwm.freq(freq)
```

获取或设置 PWM 通道的输出频率。

##### 3.2.3.1 参数

- `freq`: PWM 通道输出频率，可选参数。如果不传入参数，则返回当前频率。

##### 3.2.3.2 返回值

返回当前 PWM 通道的输出频率或空。

#### 3.2.4 duty方法

```python
pwm.duty(duty)
```

获取或设置 PWM 通道的输出占空比。

##### 3.2.4.1 参数

- `duty`: PWM 通道输出占空比，可选参数。支持小数点。如果不传入参数，则返回当前占空比。

##### 3.2.4.2 返回值

返回当前 PWM 通道的输出占空比或空

#### 3.2.5 enable方法

```python
pwm.enable(enable)
```

使能或禁用 PWM 通道的输出。

##### 3.2.5.1 参数

- `enable`: 是否使能 PWM 通道输出。
  - `True`：`1`
  - `False`：`0`

#### 3.2.6 deinit方法

```python
pwm.deinit()
```

释放 PWM 通道的资源。

## 4. PWM基础使用

### 4.1 控制引脚输出PWM信号

```python
from machine import PWM, FPIOA
# 配置PWM输出引脚
pwm = FPIOA()
pwm.set_function(47, FPIOA.PWM3)
# 初始化PWM
pwm_start = PWM(3, 2000, 50, enable = True) # 通道3,频率2KHz,占空比50%,立即使能
```

### 4.2 控制蜂鸣器

下面代码的主要功能就是让蜂鸣器发出一个短暂的4kHz（50%占空比）声音，然后在50毫秒后关闭。

```python
from machine import PWM, FPIOA
import time

beep = FPIOA()
beep.set_function(43, FPIOA.PWM1)
beep_pwm = PWM(1, 4000, 50, enable = False) # PWM1,4000KHz,50%,禁止立即输出使能
beep_pwm.enable(1) # 使能PWM输出
time.sleep_ms(50)
beep_pwm.enable(0) # 关闭PWM
beep_pwm.deinit() # 释放PWM
```

开头就是导入`time`库用来延时，PWM用来控制引脚输出PWM信号，FPIOA用来将引脚复用为PWM功能。

接下来实例化FPIOA，设置蜂鸣器的驱动脚`GPIO43`为PWM通道1输出模式。设置频率为4KHz，占空比为50%，`enable=False`表示初始化时关闭PWM输出，即默认状态下蜂鸣器不发声。接下来调用`beep_pwm.enable(1)`让蜂鸣器开始发出4Khz的声音，延时50ms后先关闭PWM输出，来停止蜂鸣器的发声，最后释放一下PWM通道资源，防止在不断电的情况下继续运行其他程序造成的资源占用。
