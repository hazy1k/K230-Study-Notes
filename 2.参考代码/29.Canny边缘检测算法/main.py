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
    sensor.set_hmirror(False)
    sensor.set_vflip(False)
    sensor.set_framesize(width=picture_width, height=picture_height, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.GRAYSCALE, chn=CAM_CHN_ID_0)

    # 根据模式初始化显示器
    if DISPLAY_MODE == "VIRT":
        Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)
    elif DISPLAY_MODE == "LCD":
        Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    elif DISPLAY_MODE == "HDMI":
        Display.init(Display.LT9611, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

    MediaManager.init()
    sensor.run()
    fps = time.clock()

    while True:
        fps.tick()
        os.exitpoint()
        # 捕获通道0的图像
        src_img = sensor.snapshot(chn=CAM_CHN_ID_0)
        # 在屏幕左上角显示原始图像
        Display.show_image(src_img,x=0,y=0,layer = Display.LAYER_OSD0)
        # 图像处理
        src_img.find_edges(image.EDGE_SIMPLE, threshold=(50, 255))
        # 在屏幕右上角显示处理后的图像
        Display.show_image(src_img,x=DISPLAY_WIDTH-picture_width,y=0,layer = Display.LAYER_OSD1)

        print(fps.fps())

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
