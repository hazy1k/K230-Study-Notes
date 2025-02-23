import network, time

SSID = "iqoo"
PASSWORD = "12345678"

def sta_test():
    sta = network.WLAN(network.STA_IF) # 初始化STA模式
    if not sta.active():
        sta.active(True) # 使能STA模式
    print("WIFI模块激活状态:", sta.active())

    print("连接状态:", sta.status())

    # 扫描周围WiFi
    wifi_list = sta.scan()
    for wifi in wifi_list:
        ssid = wifi.ssid
        rssi = wifi.rssi
        print(f"SSID: {ssid}, 信号强度: {rssi}dBm")

    print(f"正在连接到 {SSID}....")
    sta.connect(SSID, PASSWORD) # 连接到指定的WiFi

    max_wait = 5
    while max_wait > 5:
        if sta.isconnected():
            break
        max_wait -= 1
        time.sleep(1)
        sta.connect(SSID, PASSWORD) # 连接到指定的WiFi
        print("剩余等待次数：", max_wait, "次")

    while sta.ifconfig()[0] == '0.0.0.0':
        pass

    if sta.isconnected():
        print("WIFI连接成功！")
        # 打印信息
        ip_info = sta.ifconfig()
        print(f"IP地址: {ip_info[0]}")
        print(f"子网掩码: {ip_info[1]}")
        print(f"网关: {ip_info[2]}")
        print(f"DNS: {ip_info[3]}")
    else:
        print("WIFI连接失败！")

sta_test()

while True:
    time.sleep(0.5)
