from machine import FPIOA, Pin, WDT
import time

gpio = FPIOA()
gpio.set_function(62, FPIOA.GPIO62)
gpio.set_function(20, FPIOA.GPIO20)
gpio.set_function(63, FPIOA.GPIO63)
gpio.set_function(53, FPIOA.GPIO53)
R = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
G = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
B = Pin(63, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
key = Pin(53, Pin.IN, Pin.PULL_DOWN)
R.high()
G.high()
B.high()
color_state = 0 # 颜色状态
# 初始化看门狗，通道1，喂狗时间10s
wwdg = WDT(1, 10)
wwdg.feed() # 先喂狗
while True:
    R.high()
    G.high()
    B.high()
    if color_state == 0:
        R.low()
    elif color_state == 1:
        G.low()
    elif color_state == 2:
        B.low()

    color_state = (color_state + 1) % 3

    if key.value() == 1:
        wwdg.feed() # 进行喂狗
        print("已经成功喂狗啦")
        time.sleep(0.2)

    time.sleep(1)
