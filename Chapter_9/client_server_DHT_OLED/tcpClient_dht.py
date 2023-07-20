import network
import socket
import time
from machine import Pin
import dht

import ujson
import socket

SSID = "yourSSID"
PASSWORD = "password"
host = "serverIP"
port = 10000
wlan = None
s = None
# DHT sensor
sensor = dht.DHT22(Pin(16))

def connectWifi(ssid, passwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)                    
    wlan.active(True)                                    
    wlan.disconnect()                                    
    wlan.connect(ssid, passwd)                           
    while(wlan.ifconfig()[0] == '0.0.0.0'):
        time.sleep(1)
    return True

# Catch exceptions, stop program if interrupted accidentally in the 'try'
try:
    connectWifi(SSID, PASSWORD)
    ip = wlan.ifconfig()[0]                              
    s = socket.socket()                                  
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))	

    while True:                                          
        sensor.measure()
        temp = sensor.temperature()
        humi = sensor.humidity()
        measData = [temp, humi]
        serialized_data = ujson.dumps(measData)
         # send data
        s.send(serialized_data)                           
         # Receive 1024 byte of data from the socket
        data = s.recv(1024)                               
        
        sent_data = ujson.loads(data)
        print("temperature: %3.1f" % sent_data[0])
        print("Humidity: %3.1f" % sent_data[1])
        time.sleep(2)

except:
    if (s):
        s.close()
    wlan.disconnect()
    wlan.active(False)

