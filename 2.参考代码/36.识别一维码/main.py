import time, math, os, gc, sys
from media.sensor import *
from media.display import *
from media.media import *

sensor_id = 2
sensor = None
# 处理尺寸
picture_width = 640
picture_height = 480

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

# 一维码识别
def barcode_reader(code):
    if(code.type() == image.EAN2):
        return "EAN2"
    if(code.type() == image.EAN5):
        return "EAN5"
    if(code.type() == image.EAN8):
        return "EAN8"
    if(code.type() == image.UPCE):
        return "UPCE"
    if (code.type() == image.ISBN10):
        return "ISBN10"
    if (code.type() == image.UPCA):
        return "UPCA"
    if (code.type() == image.EAN13):
        return "EAN13"
    if (code.type() == image.ISBN13):
        return "ISBN13"
    if (code.type() == image.I25):
        return "I25"
    if (code.type() == image.DATABAR):
        return "DATABAR"
    if (code.type() == image.DATABAR_EXP):
        return "DATABAR_EXP"
    if (code.type() == image.CODABAR):
        return "CODABAR"
    if (code.type() == image.CODE39):
        return "CODE39"
    if (code.type() == image.PDF417):
        return "PDF417"
    if (code.type() == image.CODE93):
        return "CODE93"
    if (code.type() == image.CODE128):
        return "CODE128"

try:
    sensor = Sensor(id=sensor_id)
    sensor.reset()
    sensor.set_framesize(width=picture_width, height=picture_height, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.GRAYSCALE, chn=CAM_CHN_ID_0)
    # sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

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
        os.exitpoint()
        fps.tick()
        # 捕获通道0的图像
        img = sensor.snapshot(chn=CAM_CHN_ID_0)
        # 寻找条形码
        for code in img.find_barcodes():
            img.draw_rectangle([v for v in code.rect()], color=(255, 0, 0), thickness=5)
            # 打印条形码信息
            print_args = (f"条形码: {barcode_reader(code)}", code.payload(), (180*code.payload()/math.pi, code.quality(), fps.fps()))
            print("Barcode %s, Payload \"%s\", rotation %f (degrees), quality %d, FPS %f" % print_args)

        # 显示捕获到的图像
        Display.show_image(img, x=int((DISPLAY_WIDTH - picture_width) / 2), y=int((DISPLAY_HEIGHT - picture_height) / 2))


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
