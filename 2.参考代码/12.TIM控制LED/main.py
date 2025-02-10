from machine import FPIOA, Pin, Timer
import time

RGB = FPIOA()
RGB.set_function(62, FPIOA.GPIO62)
RGB.set_function(20, FPIOA.GPIO20)
RGB.set_function(63, FPIOA.GPIO63)
R = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
G = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
B = Pin(63, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
R.high()
G.high()
B.high()
# 颜色状态
color_state = 0  # 0红1绿2蓝


# 中断回调函数
def led_toggle(timer):
    global color_state
    R.high()
    G.high()
    B.high()
    if color_state == 0:
        R.low()
    elif color_state == 1:
        G.low()
    elif color_state == 2:
        B.low()

    color_state = (color_state + 1) % 3  # 切换颜色


# 创建软件定时器-1
tim = Timer(-1)
# 初始化定时器，每隔500ms调用一次回调函数
tim.init(period=500, mode=Timer.PERIODIC, callback=led_toggle)

while True:
    time.sleep(1)
