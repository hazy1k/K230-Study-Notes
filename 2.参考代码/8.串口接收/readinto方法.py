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
