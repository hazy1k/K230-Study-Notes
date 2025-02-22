from media.sensor import *
from media.display import *
from media.media import *
import time, math, os, gc, sys

picture_width = 800
picture_height = 480

sensor_id = 2
sensor = None

# 显示模式选择：可以是 "VIRT"、"LCD" 或 "HDMI"
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

# 注意！与find_qrcodes不同，find_apriltags方法无需对图像进行镜像校正。
# apriltag代码支持最多6个标签族，可以同时处理多个标签。
# 返回的标签对象将包含标签族和标签族内的标签ID。

tag_families = 0
#tag_families |= image.TAG16H5 # comment out to disable this family
#tag_families |= image.TAG25H7 # comment out to disable this family
#tag_families |= image.TAG25H9 # comment out to disable this family
#tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
#tag_families |= image.ARTOOLKIT # comment out to disable this family

# 标签族之间有什么区别？例如，TAG16H5标签族是一个4x4的正方形标签，
# 这意味着它可以在较远的距离检测到，而TAG36H11标签族是6x6的正方形标签。
# 然而，较低的H值（H5相比H11）意味着4x4标签的误识别率要比6x6标签高得多。
# 所以，除非有特定需要，否则使用默认的TAG36H11标签族。

def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"


try:
    sensor = Sensor(id=sensor_id)
    sensor.reset()

    # 设置通道0的输出尺寸
    sensor.set_framesize(width=picture_width, height=picture_height, chn=CAM_CHN_ID_0)
    # 设置通道0的输出像素格式为GRAYSCALE(灰度)
    sensor.set_pixformat(Sensor.GRAYSCALE, chn=CAM_CHN_ID_0)
    #sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

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
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        # 查找并处理AprilTag标签
        for tag in img.find_apriltags(families=tag_families):
            # 在图像中绘制标签的矩形框
            img.draw_rectangle([v for v in tag.rect()], color=(255, 0, 0))
            # 在标签中心绘制十字
            img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
            # 显示标签ID
            img.draw_string_advanced(tag.cx(), tag.cy(), 32, str(tag.id()))
            print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
            print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)

        # 显示捕获的图像，中心对齐，居中显示
        Display.show_image(img, x=int((DISPLAY_WIDTH - picture_width) / 2), y=int((DISPLAY_HEIGHT - picture_height) / 2))

        gc.collect()

        print(fps.fps())


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
