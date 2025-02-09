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
R = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
G = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
B = Pin(63, Pin.OUT, pull=Pin.PULL_NONE, drive=15)


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
