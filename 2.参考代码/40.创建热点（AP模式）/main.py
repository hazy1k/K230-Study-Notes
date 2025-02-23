import network, time

AP_SSID = "K230_AP"
AP_KEY = "12345678"

def ap_test():
    ap = network.WLAN(network.AP_IF)
    if not ap.active():
        ap.active(True)
    print("AP模块激活状态:", ap.active())

    ap.config(ssid=AP_SSID, key=AP_KEY)
    print("\n热点已经创建:")
    print(f"SSID: {AP_SSID}")
    print(f"Channel: {AP_KEY}")
    time.sleep(3)

    ip_info = ap.ifconfig()
    print(f"IP地址: {ip_info[0]}")
    print(f"子网掩码: {ip_info[1]}")
    print(f"网关: {ip_info[2]}")
    print(f"DNS: {ip_info[3]}")

    while True:
        # 获取当前连接的客户端数量
        clients = ap.status('stations')
        print(f"\n当前连接的客户端数量: {len(clients)}")
        time.sleep(0.5)

ap_test()
