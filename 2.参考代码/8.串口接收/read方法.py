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
