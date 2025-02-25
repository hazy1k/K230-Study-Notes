import time, os, gc, sys, urandom

from media.display import *
from media.media import *
from machine import TOUCH

try:
    DISPLAY_MODE = "LCD"
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

    # 根据模式初始化显示器
    if DISPLAY_MODE == "VIRT":
        Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)
    elif DISPLAY_MODE == "LCD":
        Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    elif DISPLAY_MODE == "HDMI":
        Display.init(Display.LT9611, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

    width = DISPLAY_WIDTH
    height = DISPLAY_HEIGHT

    MediaManager.init()

    fps = time.clock()
    img = image.Image(width, height, image.RGB565)
    img.clear()

    # 设置默认画笔颜色和大小
    current_color = (0, 255, 0)  # 默认绿色
    brush_size = 10  # 默认画笔大小

    # 定义画布中的按钮区域
    clear_button_area = (width - 100, 0, 100, 50)  # 清除按钮区域（右上角）
    color_button_area = (0, 0, 130, 50)  # 颜色选择按钮区域（左上角）

    tp = TOUCH(0)

    last_point = None  # 记录上一个触摸点

    def draw_clear_button():
        # 绘制清除按钮
        img.draw_rectangle(clear_button_area[0], clear_button_area[1], clear_button_area[2], clear_button_area[3], color=(255, 0, 0),fill=True)
        img.draw_string_advanced (clear_button_area[0] + 10, clear_button_area[1] + 10,30, "清除", color=(255, 255, 255), scale=2)

    def draw_color_buttons():
        # 绘制颜色选择按钮
        img.draw_rectangle(color_button_area[0], color_button_area[1], color_button_area[2], color_button_area[3], color=(255, 255, 0),fill=True)
        img.draw_string_advanced (color_button_area[0] + 10, color_button_area[1] + 10,30, "随机颜色", color=(0, 0, 0), scale=2)

    def select_color(x, y):
        global current_color
        # 如果点击了颜色选择区域，则随机更改颜色
        if color_button_area[0] <= x <= color_button_area[0]+color_button_area[2] and color_button_area[1] <= y <= color_button_area[1]+color_button_area[3]:
            current_color = (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))
            print(f"select_color to {current_color}")
            # 更新触点颜色
            img.draw_circle(color_button_area[0]+200,25,25,color=current_color, thickness=3,fill=True)


    def check_clear_button(x, y):
        # 检查是否点击了清除按钮
        if clear_button_area[0] <= x <= clear_button_area[0]+clear_button_area[2] and clear_button_area[1] <= y <= clear_button_area[1]+clear_button_area[3]:
            img.clear()  # 清除画布

    def draw_line_between_points(last_point, current_point):
        """在两个触摸点之间绘制连线，插入中间点以平滑移动"""
        if last_point is not None:

            # 计算两点之间的距离
            dx = current_point.x - last_point.x
            dy = current_point.y - last_point.y
            distance = (dx**2 + dy**2) ** 0.5

            # 如果距离大于30，则不进行绘制
            if distance > 30:
                return

            # 设定最小距离，如果两个点之间的距离大于该值，则进行插值
            min_distance = 10  # 可以调整此值来改变插值的密度
            if distance > min_distance:
                steps = int(distance // min_distance)  # 计算插值的步数
                for i in range(1, steps + 1):
                    # 插值计算中间点
                    new_x = last_point.x + i * dx / (steps + 1)
                    new_y = last_point.y + i * dy / (steps + 1)
                    # 绘制圆点
                    img.draw_circle(int(new_x), int(new_y), brush_size, color=current_color, thickness=3, fill=True)

        # 最后绘制当前点
        img.draw_circle(current_point.x, current_point.y, brush_size, color=current_color, thickness=3, fill=True)


    while True:
        fps.tick()
        # 检查是否在退出点
        os.exitpoint()

        # 只读取 1 个触摸点数据
        p = tp.read(1)

        # 如果返回的 p 为空元组，表示没有触摸
        if p != ():
            for idx, point in enumerate(p, start=1):  # 对触摸点进行编号，从 1 开始
                # 如果触摸区域为颜色选择按钮，则随机选择颜色
                select_color(point.x, point.y)
                # 如果触摸区域为清除按钮，则清除画布
                check_clear_button(point.x, point.y)
                # 绘制当前点与上一个点之间的线段
                draw_line_between_points(last_point, point)
                # 更新上一个触摸点和上次触摸的时间
                last_point = point

        # 绘制按钮和其他元素
        draw_clear_button()
        draw_color_buttons()
        # 显示绘制结果
        Display.show_image(img)
        time.sleep_ms(1)
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()
