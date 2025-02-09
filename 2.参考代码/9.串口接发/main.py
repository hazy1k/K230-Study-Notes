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
