
import network
import socket
import time

from machine import Pin, SoftI2C
import ssd1306
from time import sleep

import ujson
import socket

SSID = "yourSSID"
PASSWORD = "password"
port = 10000
wlan = None
listenSocket = None

#Initial
i2c = SoftI2C(scl=Pin(16), sda=Pin(17))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

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
    ip_address = wlan.ifconfig()[0]  
    print('Server IP address:', ip_address)  
    listenSocket = socket.socket()  
    listenSocket.bind((ip_address, port))  
    listenSocket.listen(1)  
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    print('TCP server waiting for connections...')

    while True:
        oled.fill(0)
        oled.text('Waiting for', 20, 20)
        oled.text('connections...', 10, 30)
        oled.show()
        print('Accepting connections...')
        conn, addr = listenSocket.accept()  
        print(addr, 'connected')
        
        while True:
            data = conn.recv(1024)  
            if len(data) == 0:
                print('Close socket')
                conn.close()  # if there is no data, close
                break
            else:
                # Deserialize received data
                received_data = ujson.loads(data)
  
                print("Received data: ", received_data)
                # Access the individual values in the received data
                temperature = received_data[0]
                humidity = received_data[1]
                
                # Display received data on OLED
                oled.fill(0)
                oled.text("Temperature:{}".format(temperature), 0, 20)
                oled.text("Humidity:{}".format(humidity), 0, 30)
                oled.show()
                
                #sent back received_data
                serialized_data = ujson.dumps(received_data)                          
                ret = conn.send(serialized_data)

except:
    if listenSocket:
        listenSocket.close()
    wlan.disconnect()
    wlan.active(False)




