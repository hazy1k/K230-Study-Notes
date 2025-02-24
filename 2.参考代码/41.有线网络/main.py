import network

def nic_config():
    nic = network.WLAN() # 创建网络接口
    nic.ifconfig('dhcp') # 设置DHCP模式

    if nic.isconnected(): # 检查是否连接成功
        print("网络配置成功")
        print("自动获取的配置：", nic.ifconfig())
    else:
        print("网络连接失败")

nic_config()
