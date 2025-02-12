import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

sensor_id = 2
sensor = None


DISPLAY_MODE = "VIRT"
# 根据模式设置显示宽高
if DISPLAY_MODE == "VIRT":
    DISPLAY_WIDTH = ALIGN_UP(1920, 16)
    DISPLAY_HEIGHT = 1080
elif DISPLAY_MODE == "LCD":
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 480
elif DISPLAY_MODE == "HDMI":
    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080
else:
    raise ValueError("未知的 DISPLAY_MODE，请选择 'VIRT', 'LCD' 或 'HDMI'")

try:
    sensor = Sensor(id=sensor_id)
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB888, chn=CAM_CHN_ID_0)
    # 根据模式初始化显示器
    if DISPLAY_MODE == "VIRT":
        Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)
    elif DISPLAY_MODE == "LCD":
        Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    elif DISPLAY_MODE == "HDMI":
        Display.init(Display.LT9611, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()
    sensor.run()

    while True:
        os.exitpoint()
        # 捕获通道0的图像
        img = sensor.snapshot(chn=CAM_CHN_ID_0)
        # 绘制内容
        # 1. 绘制绿色矩形
        img.draw_rectangle(20, 20, 100, 50, color=(0, 255, 0), thickness=5)
        # 2. 绘制红色圆形
        img.draw_circle(200, 150, 50, color=(255, 0, 0), thickness=3)
        # 3. 绘制蓝色线条
        img.draw_line(300, 50, 400, 200, color=(0, 0, 255), thickness=2)
        # 4. 绘制黄色字符串
        img.draw_string_advanced(50, 100, 32,"你好, 立创·庐山派K230-CanMV开发板!", color=(255, 255, 0), scale=2)
        # 5. 绘制十字交叉点
        img.draw_cross(400, 240, color=(255, 255, 255), size=20, thickness=2)
        # 显示捕获的图像
        Display.show_image(img)

except KeyboardInterrupt as e:
    print("用户停止: ", e)
except BaseException as e:
    print(f"异常: {e}")
finally:
    # 停止传感器运行
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 反初始化显示模块
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()
