import network
from time import sleep_ms
import gc
gc.collect()

ssid = "myAP"
password = "mypassword"

ipassigned = ('192.168.8.1', '255.255.255.0', '192.168.1.1', '8.8.8.8')
ap =network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password = password)
ap.ifconfig(ipassigned) 


while ap.active() == False:
   pass


print("Acess point ready!")
print(ap.ifconfig())
  
  
