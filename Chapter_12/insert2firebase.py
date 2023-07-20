import utime, machine
import random
from machine import RTC, I2C, Pin
import dht
import urequests as requests
import ujson
import random
import network

url_bkk = "http://worldtimeapi.org/api/timezone/Asia/Bangkok" 
url_firebase = "https://esp32micropython-c827d.firebaseio.com/.json"
# internal real time clock
rtc = RTC()
sensor = dht.DHT22(Pin(16))

# connect wifi
def connect():  
    ssid = "ssid"
    password =  "password"
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
      print("Already connected")
      return
    station.active(True)
    station.connect(ssid, password)

# get Bangkok time 
def get_bangkok_time():   
    response = requests.get(url_bkk)
       
    if response.status_code == 200: 
        parsed = response.json()
        datetime_str = str(parsed["datetime"])
        year = int(datetime_str[0:4])
        month = int(datetime_str[5:7])
        day = int(datetime_str[8:10])
        hour = int(datetime_str[11:13])
        minute = int(datetime_str[14:16])
        second = int(datetime_str[17:19])
        subsecond = int(round(int(datetime_str[20:26]) / 10000))                
        rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))

# get time 
def get_current_time():  
    current_time = "{0:4d}-{1:02d}-{2:02d}T{4:02d}:{5:02d}:{6:02d}".format(*rtc.datetime())
    return current_time

#insert temperature and humidity to database 
def insert_temp_humi(current_time, temperature, humidity):
    post_data = ujson.dumps({"time": current_time, "temperature": temperature, "humidity": humidity})    
    res = requests.post(url_firebase, headers = {'content-type': 'application/json'},  data = post_data)
    text = res.text
    return text

print("running")
connect()
get_bangkok_time()
while True: 
    print(get_current_time())
    sensor.measure()
    temp = sensor.temperature()
    humi = sensor.humidity()
    print("temperature: %3.1f" %temp)
    print("Huminity: %3.1f" %humi)
    insert_temp_humi(get_current_time(), temp, humi)
    utime.sleep(300)    