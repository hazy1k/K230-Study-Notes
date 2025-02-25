import time
from machine import TOUCH

tp = TOUCH(0)

while True:
    # 获取最多 5 个触摸点数据，默认为1.
    p = tp.read(5)

    # 如果返回的 p 为空元组，表示没有触摸
    if p != ():
        print("触摸数据：")
        for idx, point in enumerate(p, start=1):  # 对触摸点进行编号，从 1 开始
            print(f"触摸点 {idx}: X = {point.x}, Y = {point.y}")

    time.sleep(0.01)
