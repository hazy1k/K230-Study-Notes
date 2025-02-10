from machine import FPIOA, Pin, RTC
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
LED = B  # 选择蓝灯
rtc = RTC()
# 初始化时间(年，月，日，星期，时，分，秒，微秒)
rtc.init((2025, 2, 10, 1, 10, 10, 10, 0))  # 2025年2月10日星期一，时间10:10:10
print("RTC初始化时间为:", rtc.datetime())
# 定义目标时间，也就是触发时间
target_hour = 10
target_minute = 11


def check_event():
    Temp = rtc.datetime()  # 读取当前时间
    print("当前时间为:", Temp)
    Temp_hour = Temp[4]  # 提前当前时间的小时
    Temp_minute = Temp[5]  # 提前当前时间的分钟
    # 判断是否到规定的触发时间
    if Temp_hour == target_hour and Temp_minute == target_minute:
        target_event()


def target_event():
    LED.low()  # 点亮蓝灯
    print("规定时间到了")


while True:
    check_event()
    time.sleep(1)
