from media.player import *
import os

start_play = False # 播放结束flag


def player_event(event, data):
    global start_play
    if event == K_PLAYER_EVENT_EOF: # 播放结束标识
        start_play = False # 设置播放结束标识


def play_mp4_test(filename):
    global start_play
    player=Player() # 创建播放器对象
    player.load(filename) # 加载mp4文件
    player.set_event_callback(player_event) # 设置播放器事件回调
    player.start() # 开始播放
    start_play = True

    # 等待播放结束
    try:
        while start_play:
            time.sleep(0.1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        sys.print_exception(e)

    player.stop() # 停止播放
    print("play over")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    play_mp4_test("/data/test.mp4") # 播放mp4文件
