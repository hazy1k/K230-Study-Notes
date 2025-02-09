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
R = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
G = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
B = Pin(63, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
# 配置按键
button = Pin(53, Pin.IN, Pin.PULL_DOWN)
R.high()
G.high()
B.high()
# 选择颜色
RGB = B  # 蓝
while True:
    if button.value() == 1:  # 按键按下
        RGB.high()
    else:
        RGB.low()
