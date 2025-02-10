# 第四章 UART串口通讯

## 1. 开发板上使用的串口

![](https://wiki.lckfb.com/storage/images/zh-hans/lushan-pi-k230/basic/pwm/pwm_20241024_140755.png)

从上图中可以看到在排针处可以使用`串口1`，`串口2`，`串口3`，`串口4`。

| 排针引脚号 | 芯片引脚号   | 串口功能号     | 备注                                        |
| ----- | ------- | --------- | ----------------------------------------- |
| 03    | GPIO 49 | UART4_RXD | 同时连入摄像头2（CSI2）用作IIC通讯，板子内部有4.7K的电阻上拉至3.3V |
| 05    | GPIO 48 | UART4_TXD | 同时连入摄像头2（CSI2）用作IIC通讯，板子内部有4.7K的电阻上拉至3.3V |
| 08    | GPIO 03 | UART1_TXD | Na                                        |
| 10    | GPIO 04 | UART1_RXD | Na                                        |
| 11    | GPIO 05 | UART2_TXD | Na                                        |
| 13    | GPIO 06 | UART2_RXD | Na                                        |
| 27    | GPIO 41 | UART1_RXD | 同时连入摄像头1（CSI1）用作IIC通讯，板子内部有4.7K的电阻上拉至3.3V |
| 28    | GPIO 40 | UART1_TXD | 同时连入摄像头1（CSI1）用作IIC通讯，板子内部有4.7K的电阻上拉至3.3V |
| 29    | GPIO 36 | UART4_TXD | Na                                        |
| 31    | GPIO 37 | UART4_RXD | Na                                        |
| 37    | GPIO 32 | UART3_TXD | Na                                        |
| 40    | GPIO 33 | UART3_RXD | Na                                        |

## 2. UART基础配置

K230 内部集成了五个 UART（通用异步收发传输器）硬件模块，串口3（当前固件没被占用，但如果使用的是Linux+RT-Smart SDK就会被小核占用，如果用最新的CanMV固件则用户可以使用）；串口0（被RT-Smart占用，最新的CanMV K230固件中只在大核中运行了RT-Smart），剩下的串口1，2，3，4均可被用户正常调用。

### 2.1 导入模块

```python
from machine import UART, FPIOA

K230 = FPIOA()

K230.set_function(11, FPIOA.UART2_TXD)
K230.set_function(12, FPIOA.UART2_RXD)
```

### 2.2 构造函数

```python
uart = UART(id, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
```

#### 2.2.1 参数

- `id`: UART 模块编号，有效值为 `UART.UART1`、`UART.UART2`、`UART.UART3`、`UART.UART4`。
- `baudrate`: UART 波特率，可选参数，默认值为 115200。
- `bits`: 每个字符的数据位数，有效值为 `UART.FIVEBITS`、`UART.SIXBITS`、`UART.SEVENBITS`、`UART.EIGHTBITS`，可选参数，默认值为 `UART.EIGHTBITS`。
- `parity`: 奇偶校验，有效值为 `UART.PARITY_NONE`、`UART.PARITY_ODD`、`UART.PARITY_EVEN`，可选参数，默认值为 `UART.PARITY_NONE`。
- `stop`: 停止位数，有效值为 `UART.STOPBITS_ONE`、`UART.STOPBITS_TWO`，可选参数，默认值为 `UART.STOPBITS_ONE`。

### 2.3 init方法

```python
uart.init(baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
```

配置 UART 参数。

### 2.4 read方法

```python
uart.read(nbytes)
```

读取字符。如果指定了 `nbytes`，则最多读取该数量的字节；否则，将尽可能多地读取数据。

#### 2.4.1 参数

- `nbytes`: 最多读取的字节数，可选参数。

#### 2.4.2 返回值

返回一个包含读取字节的字节对象。

### 2.5 readline方法

```python
uart.readline()
```

读取一行数据，并以换行符结束。

#### 2.5.1 返回值

返回一个包含读取字节的字节对象。

### 2.6 readinto方法

```python
uart.readinto(buf, nbytes)
```

将字节读取到 `buf` 中。如果指定了 `nbytes`，则最多读取该数量的字节；否则，最多读取 `len(buf)` 数量的字节。

#### 2.6.1 参数

- `buf`: 一个缓冲区对象。
- `nbytes`: 最多读取的字节数，可选参数。

#### 2.6.2 返回值

返回读取并存入 `buf` 的字节数。

### 2.7 write方法

```python
uart.write(buf)
```

将字节缓冲区写入 UART。

#### 2.7.1 参数

- `buf`: 一个缓冲区对象。

#### 2.7.2 返回值

返回写入的字节数。

### 2.8 deinit方法

```python
uart.deinit()
```

释放 UART 资源。

## 3. UART基础使用示例

### 3.1 串口发送数据

#### 3.1.1 基本发送

```python
from machine import FPIOA, UART
import time
k230 = FPIOA()
k230.set_function(11, FPIOA.UART2_TXD)
k230.set_function(12, FPIOA.UART2_RXD)
# 初始化UART2，波特率115200，8位数据位，无效验位，1位停止位
uart = UART(UART.UART2, baudrate = 115200, bits = UART.EIGHTBITS, parity = UART.PARITY_NONE, stop = UART.STOPBITS_ONE)
# 要发送的信息
ifo = "hello, k230\n"
while True:
    uart.write(ifo)
    time.sleep(1)
```

- **引脚配置**：使用 `FPIOA` 将 GPIO11 和 GPIO12 配置为 UART2 的 TXD 和 RXD 功能。
- **初始化UART**：创建一个 UART2 实例，设置波特率为 115200，8 位数据位，无校验，1 位停止位。
- **发送数据**：使用 `uart.write()` 方法将数据发送出去。
- **资源释放**：操作完成后，使用 `uart.deinit()` 方法释放 UART 资源。

#### 3.1.2 发送字节数组

有时，我们需要和其他外部设备比如STM32进行通讯就需要发送二进制数据，比如各种传感器的原始数据。可以使用字节数组或 `bytes` 类型的数据。

```python
from machine import FPIOA, UART
import time
k230 = FPIOA()
k230.set_function(11, FPIOA.UART2_TXD)
k230.set_function(12, FPIOA.UART2_RXD)
# 初始化UART2，波特率115200，8位数据位，无效验位，1位停止位
uart = UART(UART.UART2, baudrate = 115200, bits = UART.EIGHTBITS, parity = UART.PARITY_NONE, stop = UART.STOPBITS_ONE)
# 要发送的信息
data = bytes([0x01, 0x02, 0x03, 0x04])
while True:
    uart.write(data)
    time.sleep(1)
```

基本操作和上面类似，不过如果你还是连入串口助手进行查看数据的话，记得把串口工具的显示格式从**字符串**改为**十六进制**显示，如果连线配置等正常，你就可以在屏幕上看到`01 02 03 04`这些数据了。

#### 3.1.3 连续发送数据

```python
from machine import FPIOA, UART
import time
k230 = FPIOA()
k230.set_function(11, FPIOA.UART2_TXD)
k230.set_function(12, FPIOA.UART2_RXD)
# 初始化UART2，波特率115200，8位数据位，无效验位，1位停止位
uart = UART(UART.UART2, baudrate = 115200, bits = UART.EIGHTBITS, parity = UART.PARITY_NONE, stop = UART.STOPBITS_ONE)
# 获取传感器的数据
value = 0 
while True:
    ifo = "Value:{}\n".format(value)
    uart.write(ifo)
    value = value + 1
    time.sleep(1)
```

### 3.2 串口接收数据

#### 3.2.1 基础接收

```python
from machine import FPIOA, UART

k230 = FPIOA()
k230.set_function(11, FPIOA.UART2_TXD)
k230.set_function(12, FPIOA.UART2_RXD)
# 初始化UART2，波特率115200，8位数据位，无效验位，1位停止位
uart = UART(UART.UART2, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
# 接收到的数据
re_data = None
while re_data == None:
    re_data = uart.read()  # 读取数据

uart.write("UART2 Received:{}\n".format(re_data))
uart.deinit()
```

#### 3.2.2 使用readline方法

```python
from machine import UART
from machine import FPIOA

# 配置引脚
fpioa = FPIOA()
fpioa.set_function(11, FPIOA.UART2_TXD)
fpioa.set_function(12, FPIOA.UART2_RXD)

# 初始化UART2，波特率115200，8位数据位，无校验，1位停止位
uart = UART(UART.UART2, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

line = b''

#如果接收不到数据就一直尝试读取
while line == b'':
    # 读取数据
    line = uart.read()  # 尝试读取数据

#通过CanMV IDE K230中的串行终端控制台打印出来
print("Received:", line)

#通过串口2发送接收到的数据
uart.write("UART2 Received:{}\n".format(line))

# 释放UART资源
uart.deinit()
```

#### 3.2.3 使用readinto方法

```python
from machine import UART
from machine import FPIOA

# 配置引脚
fpioa = FPIOA()
fpioa.set_function(11, FPIOA.UART2_TXD)
fpioa.set_function(12, FPIOA.UART2_RXD)

# 初始化UART2，波特率115200，8位数据位，无校验，1位停止位
uart = UART(UART.UART2, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

# 创建一个空的缓冲区，大小为10字节（根据需要调整大小）
buffer = bytearray(10)

# 进入循环，如果接收不到数据就一直尝试读取
bytes_received = 0  # 记录实际读取到的字节数
while bytes_received == 0:
    # 使用readinto将数据读取到缓冲区
    bytes_received = uart.readinto(buffer)

#通过CanMV IDE K230中的串行终端控制台打印出来
print("Received:", buffer[:bytes_received])  # 仅打印接收到的字节数内容

# 将接收到的数据通过串口2发送回去
uart.write("UART2 Received:{}\n".format(buffer[:bytes_received].decode()))

# 释放UART资源
uart.deinit()
```

#### 3.2.4 连续接收数据

```python
import time
from machine import UART
from machine import FPIOA

# 配置引脚
fpioa = FPIOA()
fpioa.set_function(11, FPIOA.UART2_TXD)
fpioa.set_function(12, FPIOA.UART2_RXD)

# 初始化UART2，波特率115200，8位数据位，无校验，1位停止位
uart = UART(UART.UART2, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

data = b''

while True:
    data = uart.read()

    if data:
        #通过CanMV IDE K230中的串行终端控制台打印出来
        print("Received:", data)

        #通过串口2发送接收到的数据
        uart.write("UART2 Received:{}\n".format(data))
    time.sleep(0.1)  # 延时避免占用过多CPU资源

# 释放UART资源
uart.deinit()
```

### 3.3 串口接发测试

串口回环测试是验证串口发送和接收功能的有效方法。通过将 UART 的发送端（TXD）和接收端（RXD）连接在一起，可以实现自发自收，检测 UART 模块的工作情况。

```python
from machine import FPIOA, UART
import time

# 设置 UART 引脚
k230 = FPIOA()
k230.set_function(11, FPIOA.UART2_TXD)
k230.set_function(12, FPIOA.UART2_RXD)

# 初始化 UART2，波特率115200，8位数据位，无效校验位，1位停止位
uart = UART(UART.UART2, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)


def uart_echo():
    uart.write("UART Echo Test Started. Waiting for data from PC...\n")

    while True:
        # 读取 UART 数据（最大 64 字节），返回一个字节串
        re_data = uart.read(64)
        if re_data:  # 如果读取到数据
            uart.write(re_data)  # 将数据回传
        time.sleep(0.1)  # 延时，防止 CPU 占用过高


try:
    uart_echo()
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    uart.deinit()  # 释放 UART 资源
```
