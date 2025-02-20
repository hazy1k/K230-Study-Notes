import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

sensor_id = 2
sensor = None
# 处理尺寸
picture_width = 400
picture_height = 240

DISPLAY_MODE = "LCD"

# 根据模式设置显示宽高
if DISPLAY_MODE == "VIRT":
    # 虚拟显示器模式
    DISPLAY_WIDTH = ALIGN_UP(1920, 16)
    DISPLAY_HEIGHT = 1080
elif DISPLAY_MODE == "LCD":
    # 3.1寸屏幕模式
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 480
elif DISPLAY_MODE == "HDMI":
    # HDMI扩展板模式
    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080
else:
    raise ValueError("未知的 DISPLAY_MODE，请选择 'VIRT', 'LCD' 或 'HDMI'")

try:
    sensor = Sensor(id=sensor_id,width=1920, height=1080)
    sensor.reset()

    sensor.set_framesize(width=picture_width, height=picture_height, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

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
        # 查找线段（LSD算法）
        lines = img.find_line_segments(merge_distance=5, max_theta_diff=10)
        count = 0
        print("----------线段统计开始----------")
        for line in lines:
            img.draw_line(line.line(), color=(1, 147, 230), thickness=3) # 画线
            print(f"Line {count}: {line}")
            count += 1
        print("----------线段统计结束----------")

        Display.show_image(img, x=int((DISPLAY_WIDTH-picture_width)/2),y=int((DISPLAY_HEIGHT-picture_height)/2))

except KeyboardInterrupt as e:
    print("用户停止: ", e)
except BaseException as e:
    print(f"异常: {e}")
finally:
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 反初始化显示模块
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()
