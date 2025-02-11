import time, os, sys
import image
from machine import Pin, FPIOA
from media.sensor import Sensor, CAM_CHN_ID_0  # 注意修改这里
from media.display import Display
from media.media import MediaManager

sensor_id = 2

gpio = FPIOA()
gpio.set_function(62, FPIOA.GPIO62)
gpio.set_function(20, FPIOA.GPIO20)
gpio.set_function(63, FPIOA.GPIO63)
gpio.set_function(53, FPIOA.GPIO53)

# LED模块配置
R = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
G = Pin(20, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
B = Pin(63, Pin.OUT, pull=Pin.PULL_NONE, drive=15)
R.high()
G.high()
B.high()
led_color = B

# 按键模块配置
button = Pin(53, Pin.IN, Pin.PULL_DOWN)
button_delay = 200  # 消抖时间
last_press_time = 0
button_last_state = 0

# 显示模式配置
Sensor_Mode = "LCD"
if Sensor_Mode == "VIRT":
    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080
    FPS = 30
elif Sensor_Mode == "LCD":
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 480
    FPS = 60
elif Sensor_Mode == "HDMI":
    DISPLAY_WIDTH = 1920
    DISPLAY_HEIGHT = 1080
    FPS = 30
else:
    raise Exception("Invalid Sensor Mode")


# 压缩并保存图像文件
def save_ipg(img, filename, quality=95):
    compressed = img.compress(quality=quality)
    with open(filename, 'wb') as f:
        f.write(compressed)
    print(f"[INFO] 使用save_ipg() 保存：{filename}")


# 创建图片文件夹，计算图片数量
image_folder = "/sdcard/images"
try:
    os.stat(image_folder)  # 先获取图像文件夹
except OSError:
    os.mkdir(image_folder)  # 创建文件夹

image_count = 0
existing_images = [fname for fname in os.listdir(image_folder)
                   if fname.startswith("lckfb_") and fname.endswith(".jpg")]

if existing_images:
    numbers = []
    for fname in existing_images:
        try:
            num_part = fname[6:11]
            numbers.append(int(num_part))
        except:
            pass
    if numbers:
        image_count = max(numbers)


# 摄像头配置
try:
    print("[INFO] 初始化摄像头")
    sensor = Sensor(id=sensor_id)
    sensor.reset()
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)  # 修改为 CAM_CHN_ID_0

    if Sensor_Mode == "VIRT":
        Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=FPS)
    elif Sensor_Mode == "LCD":
        Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    elif Sensor_Mode == "HDMI":
        Display.init(Display.LT9611, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)

    MediaManager.init()
    sensor.run()
    print("[INFO] 摄像头已启动")

    fps = time.ticks_ms()  # 使用 ticks_ms()

    while True:
        current_time = time.ticks_ms()
        img = sensor.snapshot(chn=CAM_CHN_ID_0)
        button_state = button.value()

        # 判断按键是否按下
        if button_state == 1 and button_last_state == 0:
            if current_time - last_press_time > button_delay:
                led_color.low()
                time.sleep_ms(20)
                led_color.high()
                # 拍照并保存
                image_count += 1
                filename = f"{image_folder}/lckfb_{image_count:05d}_{img.width()}x{img.height()}.jpg"
                print(f"[INFO] 照片保存在 -> {filename}")
                save_ipg(img, filename, quality=95)
                last_press_time = current_time

        button_last_state = button_state

        # 绘制图片信息
        img.draw_string_advanced(0, 0, 32, str(image_count), color=(255, 0, 0))  # 使用 str(image_count)
        img.draw_string_advanced(0, DISPLAY_HEIGHT - 32, 32, str(fps), color=(255, 0, 0))

        Display.show_image(img)

except KeyboardInterrupt:
    print("[INFO] 用户停止")
except BaseException as e:
    print(f"[ERROR] 出现异常: {e}")
finally:
    if 'sensor' in locals() and isinstance(sensor, Sensor):
        sensor.stop()
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()
