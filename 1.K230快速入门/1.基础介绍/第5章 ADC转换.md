# 第五章 ADC转换

## 1. ADC转换基本步骤

模拟信号是一个随时间连续变化的量（例如传感器的电压输出），而数字信号只在有限的离散时间点上取值，并且每个取值只能表示在一定量化精度下的数字代码。ADC 的作用就是定时（或在特定触发下）对模拟电压进行采样，并将每个采样点的电压值经过量化和编码后输出一个数字值。

**一般步骤**：

1. **采样**：在每个采样时刻使用采样保持电路对输入模拟信号进行快速捕捉，获得瞬间电压值。
2. **量化**：将采样后的电压值映射到有限离散的电平（量化等级）。例如，一个 10-bit 的 ADC 可以将输入电压范围（0V 到基准电压 Vref）分成 2^10 = 1024 个离散电平。一般单片机最常见的是12bit的分辨率，我们的庐山派使用的主控芯片K230的ADC分辨率是12位的。
3. **编码**：将量化结果转换为对应的数字二进制码。例如，输入电压接近满量程的一半时，10-bit ADC 输出约为 512（0x200）。

## 2. 开发板上的ADC

虽然K230芯片支持六个通道，但是板子上能用的只有四个，原理图和在板子上的实际位置如下：

原理图：

![](https://wiki.lckfb.com/storage/images/zh-hans/lushan-pi-k230/basic/adc/adc_20241206_155227.png)

实际位置:

![](https://wiki.lckfb.com/storage/images/zh-hans/lushan-pi-k230/basic/adc/adc_20241206_155542.png)

## 3. ADC基础配置

K230 处理器内部集成了一个 ADC（模数转换）硬件模块，提供 6 个独立通道。该模块的采样分辨率为 12 位，即输出范围为 0-4095，采样速率为 1 MHz。

ADC 类属于 `machine` 模块。

### 3.1 构造函数

```python
adc = ADC(channel)
```

#### 3.1.1 参数

- `channel`: 表示要使用的 ADC 通道号，范围为 [0, 5]。

### 3.2 read_u16方法

```python
ADC.read_u16()
```

获取指定通道的当前采样值。

#### 3.2.1 返回值

返回该 ADC 通道的采样值，范围为 [0, 4095]。

### 3.3 read_uv方法

```python
ADC.read_uv()
```

获取指定通道的当前电压值 (微伏)。

#### 3.3.1 返回值

返回该 ADC 通道的电压值，单位为微伏（uV），范围为 [0, 1800000] 微伏。

## 4. ADC基础使用示例

```python
from machine import ADC
import time
# 初始化ADC通道0
adc = ADC(0)
while True:
    # 获取ADC通道0的采样值
    adc_value = adc.read_u16()
    # 获取ADX通道0的电压值
    adc_voltage = adc.read_uv()
    # ADC转换
    adc_v = adc_voltage/(1000*1000) # 转换成电压V
    print("ADC Value: %d, Voltage: %d uV, %.6f V" % (adc_value, adc_voltage, adc_v)) # 采集值，转换微伏，计算伏
    time.sleep_ms(100)
```
