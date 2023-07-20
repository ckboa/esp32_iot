import network, ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan_mac = wlan.config('mac')
print('MAC Address: {} or {}'.format(wlan_mac, ubinascii.hexlify(wlan_mac).decode().upper()))