# 第二章 GPIO与FPIOA

## 1. 导入

1. GPIO就是我们常说的IO引脚，它直接从芯片上引出，可以被设置为输入或输出信号。没有额外功能的GPIO主要用来控制简单的设备，比如点亮LED灯或者读取按键的状态。
2. FPIOA是一种灵活的输入输出阵列，允许芯片对IO功能进行重新配置，类似用STM32上的复用引脚，也就是说不同的引脚可以根据需求重新定义。
3. iomux就是引脚复用了，主要是配置物理PAD(管脚)的功能，由于soc功能多管脚(pads)少，多个功能共享同一个I/O管脚(pads),但是一个pads同一时间只能使用其中一个功能,所以需要IOMUX进行功能选择。IOMUX也叫FPIOA，Pin multiplexing，管脚功能选择等，在K230中，FPIOA就是iomux。
4. 我们使用 MicroPython 语法来控制K230的引脚，`machine.Pin` 模块用于控制微控制器的 GPIO 引脚。`Pin` 类提供了访问和控制硬件引脚的功能，主要包括配置引脚模式，读写引脚状态等

## 2. 各引脚的复用功能

```python
from machine import FPIOA
IO = FPIOA()
IO.help()
```

![屏幕截图 2025-02-06 155609.png](https://raw.githubusercontent.com/hazy1k/My-drawing-bed/main/2025/02/06-15-57-52-屏幕截图%202025-02-06%20155609.png)

| pin | cur func   | can be func                                   |
| --- | ---------- | --------------------------------------------- |
| 0   | GPIO0      | GPIO0/BOOT0/RESV/                             |
| 1   | GPIO1      | GPIO1/BOOT1/RESV/                             |
| 2   | JTAG_TCK   | GPIO2/JTAG_TCK/PULSE_CNTR0/RESV/              |
| 3   | JTAG_TDI   | GPIO3/JTAG_TDI/PULSE_CNTR1/UART1_TXD/RESV/    |
| 4   | JTAG_TDO   | GPIO4/JTAG_TDO/PULSE_CNTR2/UART1_RXD/RESV/    |
| 5   | UART2_TXD  | GPIO5/JTAG_TMS/PULSE_CNTR3/UART2_TXD/RESV/    |
| 6   | UART2_RXD  | GPIO6/JTAG_RST/PULSE_CNTR4/UART2_RXD/RESV/    |
| 7   | PWM2       | GPIO7/PWM2/IIC4_SCL/RESV/RESV/                |
| 8   | PWM3       | GPIO8/PWM3/IIC4_SDA/RESV/RESV/                |
| 9   | PWM4       | GPIO9/PWM4/UART1_TXD/IIC1_SCL/RESV/           |
| 10  | CTRL_IN_3D | GPIO10/CTRL_IN_3D/UART1_RXD/IIC1_SDA/RESV/    |
| 11  | CTRL_O1_3D | GPIO11/CTRL_O1_3D/UART2_TXD/IIC2_SCL/RESV/    |
| 12  | CTRL_O2_3D | GPIO12/CTRL_O2_3D/UART2_RXD/IIC2_SDA/RESV/    |
| 13  | M_CLK1     | GPIO13/M_CLK1/RESV/                           |
| 14  | OSPI_CS    | GPIO14/OSPI_CS/RESV/QSPI0_CS0/RESV/           |
| 15  | OSPI_CLK   | GPIO15/OSPI_CLK/RESV/QSPI0_CLK/RESV/          |
| 16  | OSPI_D0    | GPIO16/OSPI_D0/QSPI1_CS4/QSPI0_D0/RESV/       |
| 17  | OSPI_D1    | GPIO17/OSPI_D1/QSPI1_CS3/QSPI0_D1/RESV/       |
| 18  | OSPI_D2    | GPIO18/OSPI_D2/QSPI1_CS2/QSPI0_D2/RESV/       |
| 19  | OSPI_D3    | GPIO19/OSPI_D3/QSPI1_CS1/QSPI0_D3/RESV/       |
| 20  | GPIO20     | GPIO20/OSPI_D4/QSPI1_CS0/PULSE_CNTR0/RESV/    |
| 21  | OSPI_D5    | GPIO21/OSPI_D5/QSPI1_CLK/PULSE_CNTR1/RESV/    |
| 22  | OSPI_D6    | GPIO22/OSPI_D6/QSPI1_D0/PULSE_CNTR2/RESV/     |
| 23  | GPIO23     | GPIO23/OSPI_D7/QSPI1_D1/PULSE_CNTR3/RESV/     |
| 24  | GPIO24     | GPIO24/OSPI_DQS/QSPI1_D2/PULSE_CNTR4/RESV/    |
| 25  | GPIO25     | GPIO25/PWM5/QSPI1_D3/PULSE_CNTR5/RESV/        |
| 26  | PDM_CLK    | GPIO26/MMC1_CLK/RESV/PDM_CLK/                 |
| 27  | GPIO27     | GPIO27/MMC1_CMD/PULSE_CNTR5/PDM_IN0/RESV/     |
| 28  | GPIO28     | GPIO28/MMC1_D0/UART3_TXD/PDM_IN1/RESV/        |
| 29  | GPIO29     | GPIO29/MMC1_D1/UART3_RXD/CTRL_IN_3D/RESV/     |
| 30  | GPIO30     | GPIO30/MMC1_D2/UART3_RTS/CTRL_O1_3D/RESV/     |
| 31  | GPIO31     | GPIO31/MMC1_D3/UART3_CTS/CTRL_O2_3D/RESV/     |
| 32  | IIS_CLK    | GPIO32/IIC0_SCL/IIS_CLK/UART3_TXD/RESV/       |
| 33  | IIS_WS     | GPIO33/IIC0_SDA/IIS_WS/UART3_RXD/RESV/        |
| 34  | IIS_D_IN0  | GPIO34/IIC1_SCL/IIS_D_IN0/PDM_IN3/UART3_RTS/  |
| 35  | IIS_D_OUT0 | GPIO35/IIC1_SDA/IIS_D_OUT0/PDM_IN1/UART3_CTS/ |
| 36  | GPIO36     | GPIO36/IIC3_SCL/IIS_D_IN1/PDM_IN2/UART4_TXD/  |
| 37  | GPIO37     | GPIO37/IIC3_SDA/IIS_D_OUT1/PDM_IN0/UART4_RXD/ |
| 38  | UART0_TXD  | GPIO38/UART0_TXD/RESV/QSPI1_CS0/HSYNC0/       |
| 39  | UART0_RXD  | GPIO39/UART0_RXD/RESV/QSPI1_CLK/VSYNC0/       |
| 40  | IIC1_SCL   | GPIO40/UART1_TXD/IIC1_SCL/QSPI1_D0/RESV/      |
| 41  | IIC1_SDA   | GPIO41/UART1_RXD/IIC1_SDA/QSPI1_D1/RESV/      |
| 42  | GPIO42     | GPIO42/UART1_RTS/PWM0/QSPI1_D2/RESV/          |
| 43  | GPIO43     | GPIO43/UART1_CTS/PWM1/QSPI1_D3/RESV/          |
| 44  | IIC3_SCL   | GPIO44/UART2_TXD/IIC3_SCL/RESV/SPI2AXI_CK/    |
| 45  | IIC3_SDA   | GPIO45/UART2_RXD/IIC3_SDA/RESV/SPI2AXI_CS/    |
| 46  | IIC4_SCL   | GPIO46/UART2_RTS/PWM2/IIC4_SCL/RESV/          |
| 47  | IIC4_SDA   | GPIO47/UART2_CTS/PWM3/IIC4_SDA/RESV/          |
| 48  | IIC0_SCL   | GPIO48/UART4_TXD/RESV/IIC0_SCL/SPI2AXI_DI/    |
| 49  | IIC0_SDA   | GPIO49/UART4_RXD/RESV/IIC0_SDA/SPI2AXI_DO/    |
| 50  | UART3_TXD  | GPIO50/UART3_TXD/IIC2_SCL/QSPI0_CS4/RESV/     |
| 51  | UART3_RXD  | GPIO51/UART3_RXD/IIC2_SDA/QSPI0_CS3/RESV/     |
| 52  | GPIO52     | GPIO52/UART3_RTS/PWM4/IIC3_SCL/RESV/          |
| 53  | GPIO53     | GPIO53/UART3_CTS/PWM5/IIC3_SDA/               |
| 54  | MMC1_CMD   | GPIO54/QSPI0_CS0/MMC1_CMD/PWM0/RESV/          |
| 55  | MMC1_CLK   | GPIO55/QSPI0_CLK/MMC1_CLK/PWM1/RESV/          |
| 56  | MMC1_D0    | GPIO56/QSPI0_D0/MMC1_D0/PWM2/RESV/            |
| 57  | MMC1_D1    | GPIO57/QSPI0_D1/MMC1_D1/PWM3/RESV/            |
| 58  | MMC1_D2    | GPIO58/QSPI0_D2/MMC1_D2/PWM4/RESV/            |
| 59  | MMC1_D3    | GPIO59/QSPI0_D3/MMC1_D3/PWM5/                 |
| 60  | GPIO60     | GPIO60/PWM0/IIC0_SCL/QSPI0_CS2/HSYNC1/        |
| 61  | GPIO61     | GPIO61/PWM1/IIC0_SDA/QSPI0_CS1/VSYNC1/        |
| 62  | M_CLK2     | GPIO62/M_CLK2/UART3_DE/RESV/                  |
| 63  | M_CLK3     | GPIO63/M_CLK3/UART3_RE/RESV/                  |

## 3. GPIO基础使用

### 3.1 使用FPIOA

**FPIOA**（灵活外设输入/输出阵列）是 K230 CanMV 系列微处理器提供的功能，允许用户灵活配置引脚来连接不同的外设。通过这个模块，我们可以轻松管理各种硬件接口。**FPIOA** 可以允许用户根据需要，将特定的引脚分配给不同的功能（比如 SPI、I2C、UART 等），每个引脚在同一时刻只能激活一种功能。使用 FPIOA，可以简化引脚管理，提升芯片的灵活性。

#### 3.1.1 构造函数

```python
from machine import FPIOA
test = FPIOA()
```

#### 3.1.2 设置引脚

```python
test.set_function(pin, func, ie=-1, oe=-1, pu=-1, pd=-1, st=-1, sl=-1, ds=-1)
```

##### 3.1.2.1 参数：

- `pin`: 要配置的引脚编号，范围：[0, 63]
- `func`: 要分配给引脚的功能代码
  - 普通GPIO：`FPIOA.GPIO0`，`FPIOA.GPIO1`，`FPIOA.GPIO2`等，范围[0，63]
  - 串口：`FPIOA.UART0_TXD`，`FPIOA.UART0_RXD`，`FPIOA.UART1_RXD`等。
  - IIC：`FPIOA.IIC0_SCL`，`FPIOA.IIC0_SDA`，`FPIOA.IIC1_SCL`，`FPIOA.IIC1_SDA`等。
  - PWM： `FPIOA.PWM0`， `FPIOA.PWM1`， `FPIOA.PWM2`等。

##### 3.1.2.2 更多可选参数：

- `ie`: 输入使能，**可选参数**(-1为默认值，0为不使能，1为使能)
- `oe`: 输出使能，**可选参数**(-1为默认值，0为不使能，1为使能)
- `pu`: 上拉使能，**可选参数**(-1为默认值，0为不使能，1为使能)
- `pd`: 下拉使能，**可选参数**(-1为默认值，0为不使能，1为使能)
- `st`: st 使能，**可选参数**(-1为默认值，0为不使能，1为使能)
  - 输入施密特触发器控制使能，使能后提高信号的干扰抵抗能力和改善信号的完整性，简单来说，施密特触发器是一种具有滞回特性的电子电路，其输出只在输入信号超过设定的正向或负向阈值时改变，提高了对噪声的抗干扰能力。
- `sl`: sl 使能，**可选参数**(-1为默认值，0为不使能，1为使能)
  - 目前已经不再使用，建议直接设置为-1.
- `ds`: 驱动电流能力，**可选参数**(-1为默认值)
  - 默认值为`7`，范围`0-15`，数值越大IO的驱动能力越强，除了boot 0 1其他引脚都可以设置最大15。

#### 3.1.3 读取引脚

```python
test.get_pin_func(pin)
test.get_pin_num(func) # 获取指定功能当前所在的引脚
```

##### 3.1.3.1 参数：

`pin`: 要配置的引脚编号，范围：[0, 63]。

##### 3.1.3.2 返回值：

返回引脚当前的功能号。

##### 3.1.3.3 示例

![屏幕截图 2025-02-06 161244.png](https://raw.githubusercontent.com/hazy1k/My-drawing-bed/main/2025/02/06-16-12-59-屏幕截图%202025-02-06%20161244.png)

其运行结果打印出来的数值为`64`，结合下方表格，可知`64`代表当前引脚的功能为 **BOOT0**

| 序号  | 功能名                |
| --- | ------------------ |
| 0   | GPIO0              |
| 1   | GPIO1              |
| 2   | GPIO2              |
| 3   | GPIO3              |
| 4   | GPIO4              |
| 5   | GPIO5              |
| 6   | GPIO6              |
| 7   | GPIO7              |
| 8   | GPIO8              |
| 9   | GPIO9              |
| 10  | GPIO10             |
| 11  | GPIO11             |
| 12  | GPIO12             |
| 13  | GPIO13             |
| 14  | GPIO14             |
| 15  | GPIO15             |
| 16  | GPIO16             |
| 17  | GPIO17             |
| 18  | GPIO18             |
| 19  | GPIO19             |
| 20  | GPIO20             |
| 21  | GPIO21             |
| 22  | GPIO22             |
| 23  | GPIO23             |
| 24  | GPIO24             |
| 25  | GPIO25             |
| 26  | GPIO26             |
| 27  | GPIO27             |
| 28  | GPIO28             |
| 29  | GPIO29             |
| 30  | GPIO30             |
| 31  | GPIO31             |
| 32  | GPIO32             |
| 33  | GPIO33             |
| 34  | GPIO34             |
| 35  | GPIO35             |
| 36  | GPIO36             |
| 37  | GPIO37             |
| 38  | GPIO38             |
| 39  | GPIO39             |
| 40  | GPIO40             |
| 41  | GPIO41             |
| 42  | GPIO42             |
| 43  | GPIO43             |
| 44  | GPIO44             |
| 45  | GPIO45             |
| 46  | GPIO46             |
| 47  | GPIO47             |
| 48  | GPIO48             |
| 49  | GPIO49             |
| 50  | GPIO50             |
| 51  | GPIO51             |
| 52  | GPIO52             |
| 53  | GPIO53             |
| 54  | GPIO54             |
| 55  | GPIO55             |
| 56  | GPIO56             |
| 57  | GPIO57             |
| 58  | GPIO58             |
| 59  | GPIO59             |
| 60  | GPIO60             |
| 61  | GPIO61             |
| 62  | GPIO62             |
| 63  | GPIO63             |
| 64  | BOOT0              |
| 65  | BOOT1              |
| 66  | CI0                |
| 67  | CI1                |
| 68  | CI2                |
| 69  | CI3                |
| 70  | CO0                |
| 71  | CO1                |
| 72  | CO2                |
| 73  | CO3                |
| 74  | DI0                |
| 75  | DI1                |
| 76  | DI2                |
| 77  | DI3                |
| 78  | DO0                |
| 79  | DO1                |
| 80  | DO2                |
| 81  | DO3                |
| 82  | HSYNC0             |
| 83  | HSYNC1             |
| 84  | IIC0_SCL           |
| 85  | IIC0_SDA           |
| 86  | IIC1_SCL           |
| 87  | IIC1_SDA           |
| 88  | IIC2_SCL           |
| 89  | IIC2_SDA           |
| 90  | IIC3_SCL           |
| 91  | IIC3_SDA           |
| 92  | IIC4_SCL           |
| 93  | IIC4_SDA           |
| 94  | IIS_CLK            |
| 95  | IIS_D_IN0_PDM_IN3  |
| 96  | IIS_D_IN1_PDM_IN2  |
| 97  | IIS_D_OUT0_PDM_IN1 |
| 98  | IIS_D_OUT1_PDM_IN0 |
| 99  | IIS_WS             |
| 100 | JTAG_RST           |
| 101 | JTAG_TCK           |
| 102 | JTAG_TDI           |
| 103 | JTAG_TDO           |
| 104 | JTAG_TMS           |
| 105 | M_CLK1             |
| 106 | M_CLK2             |
| 107 | M_CLK3             |
| 108 | MMC1_CLK           |
| 109 | MMC1_CMD           |
| 110 | MMC1_D0            |
| 111 | MMC1_D1            |
| 112 | MMC1_D2            |
| 113 | MMC1_D3            |
| 114 | OSPI_CLK           |
| 115 | OSPI_CS            |
| 116 | OSPI_D0            |
| 117 | OSPI_D1            |
| 118 | OSPI_D2            |
| 119 | OSPI_D3            |
| 120 | OSPI_D4            |
| 121 | OSPI_D5            |
| 122 | OSPI_D6            |
| 123 | OSPI_D7            |
| 124 | OSPI_DQS           |
| 125 | PDM_IN0            |
| 126 | PDM_IN1            |
| 127 | PDM_IN2            |
| 128 | PDM_IN3            |
| 129 | PULSE_CNTR0        |
| 130 | PULSE_CNTR1        |
| 131 | PULSE_CNTR2        |
| 132 | PULSE_CNTR3        |
| 133 | PULSE_CNTR4        |
| 134 | PULSE_CNTR5        |
| 135 | PWM0               |
| 136 | PWM1               |
| 137 | PWM2               |
| 138 | PWM3               |
| 139 | PWM4               |
| 140 | PWM5               |
| 141 | QSPI0_CLK          |
| 142 | QSPI0_CS0          |
| 143 | QSPI0_CS1          |
| 144 | QSPI0_CS2          |
| 145 | QSPI0_CS3          |
| 146 | QSPI0_CS4          |
| 147 | QSPI0_D0           |
| 148 | QSPI0_D1           |
| 149 | QSPI0_D2           |
| 150 | QSPI0_D3           |
| 151 | QSPI1_CLK          |
| 152 | QSPI1_CS0          |
| 153 | QSPI1_CS1          |
| 154 | QSPI1_CS2          |
| 155 | QSPI1_CS3          |
| 156 | QSPI1_CS4          |
| 157 | QSPI1_D0           |
| 158 | QSPI1_D1           |
| 159 | QSPI1_D2           |
| 160 | QSPI1_D3           |
| 161 | SPI2AXI_CK         |
| 162 | SPI2AXI_CS         |
| 163 | SPI2AXI_DI         |
| 164 | SPI2AXI_DO         |
| 165 | UART0_RXD          |
| 166 | UART0_TXD          |
| 167 | UART1_CTS          |
| 168 | UART1_RTS          |
| 169 | UART1_RXD          |
| 170 | UART1_TXD          |
| 171 | UART2_CTS          |
| 172 | UART2_RTS          |
| 173 | UART2_RXD          |
| 174 | UART2_TXD          |
| 175 | UART3_CTS          |
| 176 | UART3_DE           |
| 177 | UART3_RE           |
| 178 | UART3_RTS          |
| 179 | UART3_RXD          |
| 180 | UART3_TXD          |
| 181 | UART4_RXD          |
| 182 | UART4_TXD          |
| 183 | PDM_CLK            |
| 184 | VSYNC0             |
| 185 | VSYNC1             |
| 186 | CTRL_IN_3D         |
| 187 | CTRL_O1_3D         |
| 188 | CTRL_O2_3D         |
| 189 | TEST_PIN0          |
| 190 | TEST_PIN1          |
| 191 | TEST_PIN2          |
| 192 | TEST_PIN3          |
| 193 | TEST_PIN4          |
| 194 | TEST_PIN5          |
| 195 | TEST_PIN6          |
| 196 | TEST_PIN7          |
| 197 | TEST_PIN8          |
| 198 | TEST_PIN9          |
| 199 | TEST_PIN10         |
| 200 | TEST_PIN11         |
| 201 | TEST_PIN12         |
| 202 | TEST_PIN13         |
| 203 | TEST_PIN14         |
| 204 | TEST_PIN15         |
| 205 | TEST_PIN16         |
| 206 | TEST_PIN17         |
| 207 | TEST_PIN18         |
| 208 | TEST_PIN19         |
| 209 | TEST_PIN20         |
| 210 | TEST_PIN21         |
| 211 | TEST_PIN22         |
| 212 | TEST_PIN23         |
| 213 | TEST_PIN24         |
| 214 | TEST_PIN25         |
| 215 | TEST_PIN26         |
| 216 | TEST_PIN27         |
| 217 | TEST_PIN28         |
| 218 | TEST_PIN29         |
| 219 | TEST_PIN30         |
| 220 | TEST_PIN31         |
| 221 | FUNC_MAX           |

#### 3.1.4 获取引脚信息

```python
test.help([number, func=False])
```

打印引脚配置提示信息。

##### 3.1.4.1 参数

- `number`: 引脚号或功能号， 可选参数
- `func`: 是否启用功能号查询，默认为 `False`

##### 3.1.4.2 返回值

可能为以下三种：

1. 所有引脚的配置信息（未设置 `number`）
2. 指定引脚的详细配置信息（设置了 `number`，未设置 `func` 或设置为 `False`）
3. 指定功能的所有可配置引脚号（设置了 `number`，并将 `func` 设置为 `True`）

##### 3.1.4.3 示例

![屏幕截图 2025-02-06 163219.png](C:\Users\qiu\AppData\Roaming\marktext\images\4365004fd3368f925f7f2a4096b1453d0938db9b.png)

### 3.2 使用machine.Pin

`machine.Pin` 类是 MicroPython 中用于控制输入/输出引脚的核心模块。通过该模块，我们可以轻松地管理微控制器上的 GPIO 引脚，进行基础的输入输出操作。

#### 3.2.1 构造函数/初始化引脚

```python
pin = Pin(index, mode, pull=Pin.PULL_NONE, drive=7)
```

用于构造pin对象，可同时对引脚进行初始化。

##### 3.2.1.1 参数

- `index`: 引脚编号，范围为 [0, 63]。
- `mode`: 引脚的模式，支持输入模式或输出模式。
  - `Pin.OUT`
  - `Pin.IN`
- `pull`: 上下拉配置（**可选**），默认为 `Pin.PULL_NONE`。
  - `Pin.PULL_NONE`
  - `Pin.PULL_UP`
  - `Pin.PULL_DOWN`
- `drive`: 驱动能力配置（**可选**），默认值为 7。
  - 默认值为`7`，范围`0-15`，数值越大IO的驱动能力越强，除了boot 0 1其他引脚都可以设置最大15。

##### 3.2.1.2 示例

```python
from machine import Pin
pin = Pin(1, Pin.OUT, pill = Pin.PULL_NONE, drive = 15)
```

#### 3.2.2 控制Pin

##### 3.2.2.1 value方法

```python
pin.value(x)
```

获取引脚的输入电平值或设置引脚的输出电平。

参数：

- `value`: 输出值（可选），如果传递该参数则设置引脚输出为指定值。如果不传参则返回引脚的当前输入电平值。
  - 0：输出低电平。
  - 1：输出高电平。

示例：

```python
from machine import Pin
pin.value(1) # 设置输出高电平
pin.value(0) # 设置输出低电平
print(pin.value()) # 获取电平
```

##### 3.2.2.2 mode方法

```python
pin.mode(x)
```

主要用来获取或设置引脚的模式。

参数：

- `mode`: 引脚模式（输入或输出），如果不传参则返回当前引脚的模式。
  - `Pin.OUT`
  - `Pin.IN`

示例：

```python
from machine import Pin
pin.mode(Pin.IN) # 配置为输入模式
pin.mode(Pin.OUT) # 配置为输出模式
print(pin.mode())
```

##### 3.2.2.3 pull方法

```python
pin.pull(x)
```

获取或设置引脚的上下拉配置。

参数:

- `pull`: 上下拉配置（可选），如果不传参则返回当前上下拉配置。

示例：

```python
from machine import Pin
pin.pull(Pin.PULL_NONE)
pin.pull(Pin.PULL_UP)
pin.pull(Pin.PULL_DOWM)
print(pin.pull())
```

##### 3.2.2.4  drive方法

```python
pin.drive(x)
```

获取或设置引脚的驱动能力。

##### 3.2.2.5 on方法

```python
pin.on()
```

将引脚输出设置为高电平。

##### 3.2.2.6 off方法

```python
pin.off()
```

将引脚输出设置为低电平。

##### 3.2.2.7 high方法

```python
pin.high()
```

将引脚输出设置为高电平。

##### 3.2.2.8 low方法

```python
pin.low()
```

将引脚输出设置为低电平。

## 4. 点亮RGB灯

### 4.1 LED闪烁实验

```python
from machine import Pin
from machine import FPIOA
import time
# 创建对象
RGB = FPIOA()
# 初始化引脚，作为普通的IO
RGB.set_function(62, FPIOA.GPIO62)
RGB.set_function(20, FPIOA.GPIO20)
RGB.set_function(63, FPIOA.GPIO63)
# 配置IO输出
R = Pin(62, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
G = Pin(20, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
B = Pin(63, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
# 初始化全灭，开发板上的RGB低电平点亮
R.high()
G.high()
B.high()
# 选择RGB颜色绿色
LED = G
while True:
    LED.low()
    time.sleep(1)
    LED.high()
    time.sleep(1)
```

将对应LED灯的GPIO初始化为普通GPIO后实例化了这三个GPIO引脚，分别用于控制RGB灯的红、绿和蓝三种颜色的LED灯，都指定了对应的引脚号，输出模式，不使用上下拉，输出能力。

接下来初始化了LED灯的状态，通过让每个灯的控制引脚变为高电平来熄灭所有LED灯。

### 4.2 流水灯

```python
from machine import Pin
from machine import FPIOA
import time
# 创建对象
RGB = FPIOA()
# 初始化引脚，作为普通的IO
RGB.set_function(62, FPIOA.GPIO62)
RGB.set_function(20, FPIOA.GPIO20)
RGB.set_function(63, FPIOA.GPIO63)
# 配置IO输出
R = Pin(62, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
G = Pin(20, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
B = Pin(63, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
# 设置颜色函数
def set_color(r, g, b):
    if r == 0:
        R.low()
    else:
        R.high()

    if g == 0:
        G.low()
    else:
        G.high()

    if b == 0:
        B.low()
    else:
        B.high()

# LDE亮一会儿灭        
def delay_color(r, g, b, delay):
    set_color(r, g, b)
    time.sleep(delay)
    set_color(1, 1, 1)
    time.sleep(delay)

while True:
    # 红色
    delay_color(0, 1, 1, 0.5)
    # 绿色
    delay_color(1, 0, 1, 0.5)
    # 蓝色
    delay_color(1, 1, 0, 0.5)
    # 黄色（红+绿）
    delay_color(0, 0, 1, 0.5)
    # 紫色（红+蓝）
    delay_color(0, 1, 0, 0.5)
    # 青色（绿+蓝）
    delay_color(1, 0, 0, 0.5)
    # 白色（红+绿+蓝）
    delay_color(0, 0, 0, 0.5)
```

## 5. 按键控制

### 5.1 按键控制LED开关

```python
from machine import Pin
from machine import FPIOA
import time
# 创建FPIOA对象，初始化GPIO
LED = FPIOA()
LED.set_function(62, FPIOA.GPIO62)
LED.set_function(20, FPIOA.GPIO20)
LED.set_function(63, FPIOA.GPIO63)
LED.set_function(53, FPIOA.GPIO53)
# 配置三色灯
R = Pin(62, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
G = Pin(20, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
B = Pin(63, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
# 配置按键
button = Pin(53, Pin.IN, Pin.PULL_DOWN)
R.high()
G.high()
B.high()
# 选择颜色
RGB = B # 蓝
while True:
    if button.value() == 1: # 按键按下
        RGB.high()
    else:
        RGB.low()    
        
```

前半部分和我们在前面学习的点亮RGB灯是一样的，就是初始化灯对应的引脚。不同的是我们这里还对按键用到的GPIO（Pin53）进行了初始化，引脚62、20和63将用于控制LED灯，而引脚53将用于读取按钮的状态，将控制LED灯的引脚设置为了输出模式，将读取按钮的GPIO设置为了输入模式。

然后把按钮配置为了下拉输入模式，代表当按钮没有被按下是，输入信号为低电平（0），按下时为高电平（1）。

可以看到我们这里并没有进行按键消抖处理，这里按钮的作用是直接控制LED灯的熄灭，而不是在不同状态之间切换。当我们按下按钮时，LED灯熄灭；而当我们释放按钮时，LED灯将再次点亮。在上面的程序中，我们关注的是按钮是否被按下（按下就熄灭LED灯），而不是按钮有没有改变状态。如果我们需要判断按钮的改变状态来切换LED灯状态，就必须要进行消抖处理了，详情请看下面的程序。

### 5.2 按键控制LED状态

```python
from machine import Pin
from machine import FPIOA
import time
# 创建FPIOA对象，初始化GPIO
LED = FPIOA()
LED.set_function(62, FPIOA.GPIO62)
LED.set_function(20, FPIOA.GPIO20)
LED.set_function(63, FPIOA.GPIO63)
LED.set_function(53, FPIOA.GPIO53)
# 配置三色灯
R = Pin(62, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
G = Pin(20, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
B = Pin(63, Pin.OUT, pull = Pin.PULL_NONE, drive = 15)
# 配置按键
button = Pin(53, Pin.IN, Pin.PULL_DOWN)
R.high()
G.high()
B.high()
RGB = B
# 按键消抖
button_delay = 20 # 20ms
press_time = 0 # 记录按下的时间
led_flag = False # 记录LED状态，False表示灭
button_flag = 0 # 记录按键状态

while True:
    button_state = button.value() # 获取当前按键状态
    current_time = time.ticks_ms() # 获取当前时间
    # 按键 0->1 代表按下，也就是检测上升沿
    if button_state == 1 and button_flag == 0:
        # 检测消抖时间
        if current_time - press_time > button_delay:
            if led_flag:
                RGB.high()
            else:
                RGB.low()
                
            led_flag = not led_flag # 翻转LED状态
            press_time = current_time # 更新按键按下时间
    
    button_flag = button_state # 更新按键状态
    time.sleep_ms(10)
        
```

首先获取当前按钮状态和时间。如果按钮的状态从未按下（0，低电平）变为按下（1，高电平），且在消抖延迟后，程序将切换LED的状态（点亮或熄灭），然后更新LED当前状态和最后按键按下的时间。

这个程序最重要的改进就是进行了按键的消抖，确保每次按钮的状态变化都有效，避免由于机械抖动造成的错误信号。
