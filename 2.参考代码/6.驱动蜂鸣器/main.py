from machine import PWM, FPIOA
import time

beep = FPIOA()
beep.set_function(43, FPIOA.PWM1)
beep_pwm = PWM(1, 4000, 50, enable = False) # PWM1,4000KHz,50%,禁止立即输出使能
beep_pwm.enable(1) # 使能PWM输出
time.sleep_ms(50)
beep_pwm.enable(0) # 关闭PWM
beep_pwm.deinit() # 释放PWM
