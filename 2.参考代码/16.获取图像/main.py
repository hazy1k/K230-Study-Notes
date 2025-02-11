import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

# 设备id
sensor_id = 2
sensor = None

try:
    sensor = Sensor(id=sensor_id)  # 创建一个摄像头对象，使用摄像头2
    sensor.reset()  # 先复位
    # 设置通道0的输出尺寸为1920x1080
    sensor.set_framesize(sensor.FHD, chn=CAM_CHN_ID_0)
    # 设置像素格式为RGB888
    sensor.set_pixformat(sensor.RGB888, chn=CAM_CHN_ID_0)
    # 使用K230的IDE帧缓冲区作为显示输出
    Display.init(Display.VIRT, width=1920, height=1080, to_ide=True)
    MediaManager.init()  # 初始化媒体管理器
    sensor.run()  # 启动摄像头

    while True:
        # 捕获通道0的图像
        img = sensor.snapshot(chn=CAM_CHN_ID_0)
        Display.show_image(img)  # 显示图像

except KeyboardInterrupt as e:
    print('Interrupted')
except BaseException as e:
    print(f'Error: {str(e)}')
finally:
    # 停止传感器运行
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 反初始化
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)  # 进入低功耗模式
    time.sleep_ms(100)
    MediaManager.deinit()
