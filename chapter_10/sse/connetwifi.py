from time import sleep_ms
import network
import gc 


gc.collect() 

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("cknet", "Teelek88")
while not wlan.isconnected():
    sleep_ms(100)
print('Network config:', wlan.ifconfig())
sleep_ms(2000)