import time, os, urandom, sys, gc
from media.display import *
from media.media import *

try:
    # 显示模式选择
    display_mode = "VIRT" # VIRT:IDE LCD:LCD屏幕 HDMI:通过HDMI连接
    # 根据显示模式调整显示宽高
    if display_mode == "VIRT":
        display_width = ALIGN_UP(1920, 16)  # 如果没有定义，改为math.ceil
        display_height = 1080
    elif display_mode == "LCD":
        display_width = 800
        display_height = 480
    elif display_mode == "HDMI":
        display_width = 1920
        display_height = 1080
    else:
        raise Exception("Invalid display mode")

    if display_mode == "VIRT":
        Display.init(Display.VIRT, width=display_width, height=display_height, fps=60)
    elif display_mode == "LCD":
        Display.init(Display.ST7701, width=display_width, height=display_height, to_ide=True)
    elif display_mode == "HDMI":
        Display.init(Display.LT9611, width=display_width, height=display_height, to_ide=True)

    width = display_width
    height = display_height
    MediaManager.init()  # 初始化媒体管理器
    fps = time.clock()
    img = image.Image(width, height, image.ARGB8888)
    # 随机颜色生成
    def random_color():
        return (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))
    # 随机尺寸生成
    def random_size():
        return urandom.getrandbits(10) & max_size

    while True:
        fps.tick()
        os.exitpoint()
        img.clear()
        # 绘制红色线
        img.draw_line(10,10,100,100,color=(255,0,0))
        # 绘制绿色矩形
        img.draw_rectangle(20, 20, 50, 30, color=(0, 255, 0), thickness=2)
        # 绘制蓝色圆
        img.draw_circle(30, 30, 30, color=(0, 0, 255), thickness=3)
        # 绘制黄色交叉
        img.draw_cross(40, 40, color=(255, 255, 0), size=10, thickness=2)
        # 绘制红色字符串
        img.draw_string_advanced(50, 50, 32, "你好K230", color=(255, 0, 0))
        # 绘制白色字符串
        img.draw_string_advanced(50, 100, 32, "Hello CanMV", color=(255, 255, 255), scale=2)
        # 绘制红色箭头
        img.draw_arrow(60, 60, 100, 100, color=(255, 0, 0), thickness=2)
        # 绘制蓝色椭圆
        radius_x = urandom.getrandbits(30) % (max(img.height(), img.width())//2)
        radius_y = urandom.getrandbits(30) % (max(img.height(), img.width())//2)
        rot = urandom.getrandbits(30)
        img.draw_ellipse(70, 70, radius_x, radius_y, rot, color = (0, 0, 255), thickness = 2, fill = False)
        # 绘制黄色关键点
        keypoints = [(30, 30), (50, 50), (70, 70)]
        img.draw_keypoints([(30, 40, rot)], color = (255, 255, 0), size = 20, thickness = 2, fill = False)
        # 动态线条绘制
        for _ in range(2):
           x0, y0 = urandom.getrandbits(10) % width, urandom.getrandbits(10) % height
           x1, y1 = urandom.getrandbits(10) % width, urandom.getrandbits(10) % height
           img.draw_line(x0, y0, x1, y1, color=random_color(),thickness=2)
        # 椭圆动态变化
        for _ in range(5):
            x, y = urandom.getrandbits(10) % width, urandom.getrandbits(10) % height
            img.draw_cross(x, y, color=random_color(), size=10, thickness=1)
        # 动态箭头
        for _ in range(3):
            x0, y0 = urandom.getrandbits(10) % width, urandom.getrandbits(10) % height
            x1, y1 = urandom.getrandbits(10) % width, urandom.getrandbits(10) % height
            img.draw_arrow(x0, y0, x1, y1, color=random_color(), thickness=5)
        # 动态洪水填充
        fx, fy = urandom.getrandbits(10) % width, urandom.getrandbits(10) % height
        img.flood_fill(fx, fy, color=random_color(), threshold=30)
        # 显示绘制结果
        Display.show_image(img)
        print(fps.fps())
        time.sleep_ms(10)
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()
