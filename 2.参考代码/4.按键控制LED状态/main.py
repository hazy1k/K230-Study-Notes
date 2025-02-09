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

