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
