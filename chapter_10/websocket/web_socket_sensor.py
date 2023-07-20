import network
import time
from machine import ADC, Pin, Timer
import dht
from microWebSrv import MicroWebSrv

sensor = dht.DHT22(Pin(25))
adc34 = ADC(Pin(34))        
adc34.width(ADC.WIDTH_12BIT)

relay_1 = Pin(15,Pin.OUT)
relay_2 = Pin(13,Pin.OUT)
relay_3 = Pin(12,Pin.OUT)
relay_4 = Pin(14,Pin.OUT)
relay_list = [relay_1, relay_2, relay_3, relay_4]

for i in relay_list:
    i.value(0) 

tm = Timer(0)

def relay_number(msg):
    relay_status = msg[8:11]
    if(relay_status == 'OFF'):
        relay_list[int(msg[6:7]) -1].value(0)
    else:
        relay_list[int(msg[6:7]) -1].value(1)

def receiveData(webSocket, msg):
    print(msg)
    if msg[0:5] == 'Relay': 
      relay_number(msg)
      webSocket.SendText("%s" %msg)
    else:
      print('%s' %msg) 
      webSocket.SendText("%s" %msg)

def closed(webSocket):
    tm.deinit()
    print("(server)Close.., Stop Timer")
    
def reading_sensor_timer(timer, websocket):   
    sensor.measure()
    t,h,s = sensor.temperature(), sensor.humidity(), adc34.read()
    
    print("data,%5.2f,%5.2f,%5d" %(t,h,s))
    websocket.SendText("data,%5.2f,%5.2f,%5d" %(t,h,s)) 
    
def _acceptWebSocketCallback(webSocket, httpClient):
    webSocket.RecvTextCallback = receiveData
    webSocket.ClosedCallback = closed
    cb = lambda timer: reading_sensor_timer(timer, webSocket)  
    tm.init(period=3000, callback=cb)  
    print("(server)Connect..")


# start server
mws=MicroWebSrv(webPath='www/')
print("server started")
mws.MaxWebSocketRecvLen     = 256
mws.WebSocketThreaded       = True
mws.AcceptWebSocketCallback = _acceptWebSocketCallback
mws.Start(threaded=False)