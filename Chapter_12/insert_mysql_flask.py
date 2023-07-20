from machine import Pin
import urequests as requests
import random, ujson, utime
import dht
import gc

url = "https://192.168.0.76:5000/sensor_dht"
sensor = dht.DHT22(Pin(25))

while True:
    sensor.measure()
    temp = sensor.temperature()
    humi = sensor.humidity()
    print("temperature: %3.1f°C" % temp)
    print("humidity: %3.1f%%" % humi)
    post = ujson.dumps({"temp": temp, "humi": humi})
    try:
        res = requests.post(url, headers = {'content-type': 'application/json'}, data=post)
        res.close() # ปิดการเชื่อมต่อ
        if res.status_code == 200:
            print("Request successful!")
        else:
            print("Request failed with status code {}".format(res.status_code))
    except:
        print("Error: Could not establish connection.")
    gc.collect()
    utime.sleep(10)