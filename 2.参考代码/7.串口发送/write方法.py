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
    