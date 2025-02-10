from machine import ADC
import time
# 初始化ADC通道0
adc = ADC(0)
while True:
    # 获取ADC通道0的采样值
    adc_value = adc.read_u16()
    # 获取ADX通道0的电压值
    adc_voltage = adc.read_uv()
    # ADC转换
    adc_v = adc_voltage/(1000*1000) # 转换成电压V
    print("ADC Value: %d, Voltage: %d uV, %.6f V" % (adc_value, adc_voltage, adc_v)) # 采集值，转换微伏，计算伏
    time.sleep_ms(100)
    