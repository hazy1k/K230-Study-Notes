import time, os, urandom, sys
from media.display import *
from media.media import *

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


# 显示测试函数
def display_test():
    print(f"当前模式为{display_mode}")
    img = image.Image(display_width, display_height, image.ARGB8888)
    if display_mode == "VIRT":
        Display.init(Display.VIRT, width=display_width, height=display_height, fps=60)
    elif display_mode == "LCD":
        Display.init(Display.ST7701, width=display_width, height=display_height, to_ide=True)
    elif display_mode == "HDMI":
        Display.init(Display.LT9611, width=display_width, height=display_height, to_ide=True)
    MediaManager.init()  # 初始化媒体管理器

    try:
        while True:
            img.clear()  # 清除
            for i in range(10):
                # 随机生成字符串位置、颜色、大小
                x = (urandom.getrandbits(11) % img.width())  # 随机X坐标
                y = (urandom.getrandbits(11) % img.height())  # 随机Y坐标
                r = urandom.getrandbits(8)
                g = urandom.getrandbits(8)
                b = urandom.getrandbits(8)
                size = (urandom.getrandbits(30) % 64) + 32  # 字体大小32到96之间
                # 绘制字符串
                img.draw_string_advanced(x, y, size, "Hello, K230, 显示图画测试", color=(r, g, b))
                Display.show_image(img)
                time.sleep(1)

    except KeyboardInterrupt as e:
        print("用户终止：", e)  # 捕获键盘中断异常
    except BaseException as e:
        print(f"异常：{e}")  # 捕获其他异常
    finally:
        # 清理资源
        Display.deinit()
        os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)  # 启用睡眠模式的退出点
        time.sleep_ms(100)
        MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)  # 启用退出点
    display_test()  # 调用显示测试函数
