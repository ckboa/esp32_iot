import network
from microWebSrv import MicroWebSrv
from machine import Pin, SoftI2C
from time import sleep_ms
import ssd1306
import gc 

gc.collect() 
#Connect WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('cknet', 'Teelek88')

while not wlan.isconnected():
    sleep_ms(100)
    
print('Network config:', wlan.ifconfig())
sleep_ms(2000)
#OLED Set
i2c = SoftI2C(scl=Pin(17), sda=Pin(16))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)




oled.text('Welcome to MPY ', 10, 0)
oled.text('IP:{}'.format(wlan.ifconfig()[0]), 0, 30) 
oled.show()

def _httpHandlerTestPost(httpClient, httpResponse):
    formData  = httpClient.ReadRequestPostedFormData()
    username = formData['username']
    oled.text('Login by:', 0, 40) 
    oled.text('{}'.format(username), 10, 50)
    oled.show()
    httpResponse.WriteResponseFile(
        "www/hello_micropython.html",
        contentType = 'text/html',
    )
    
# start server 
print("Server Started ")

routeHandlers = [
    ( "/test", "POST", _httpHandlerTestPost )
]
#srv = MicroWebSrv(routeHandlers = routeHandlers)
srv = MicroWebSrv(routeHandlers = routeHandlers, webPath='www/')
srv.Start(threaded = False)