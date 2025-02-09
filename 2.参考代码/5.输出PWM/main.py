from machine import PWM, FPIOA
# 配置PWM输出引脚
pwm = FPIOA()
pwm.set_function(47, FPIOA.PWM3)
# 初始化PWM
pwm_start = PWM(3, 2000, 50, enable = True) # 通道3,频率2KHz,占空比50%,立即使能
