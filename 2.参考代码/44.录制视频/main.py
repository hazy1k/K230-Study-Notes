from media.mp4format import *
import os

width = 800
height = 480

file_name = "/data/test.mp4"

MAX_RECORD_TIME = 30 # 设置默认录制时间（单位：秒）

def mp4_muxer_test():
    print("mp4_muxer_test start")

    mp4_muxer = Mp4Container() # 实例化mp4 container
    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)
    mp4_muxer.Create(mp4_cfg) # 创建mp4 muxer
    mp4_muxer.Start() # 启动mp4 muxer
    start_time_ms = time.ticks_ms()  # 记录开始时间
    elapsed_time = 0
    frame_count = 0

    try:
        while True:
            os.exitpoint()
            # 处理音视频数据，按MP4格式写入文件
            mp4_muxer.Process()
            frame_count += 1
            print("frame_count = ", frame_count)
            # 检查当前时间与开始时间的差值是否超过最大录制时间
            elapsed_time = time.ticks_ms() - start_time_ms
            if elapsed_time >= MAX_RECORD_TIME*1000:
                print("录制已超过最大时长，停止录制,请等待视频保存")
                break

    except BaseException as e:
        print(e)
    # 停止mp4 muxer
    mp4_muxer.Stop()
    # 销毁mp4 muxer
    mp4_muxer.Destroy()
    print("mp4_muxer_test stop,video saved!")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    mp4_muxer_test()
