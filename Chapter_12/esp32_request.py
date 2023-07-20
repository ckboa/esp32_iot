from machine import Pin
import urequests as requests
import random, ujson, utime
import dht
import gc

sensor = dht.DHT22(Pin(16))

url_request = "https://192.168.0.53:5000/sensor_dth"
    
while True:
    sensor.measure()
    temperature_dht = sensor.temperature()
    humidity_dht = sensor.humidity()

    print("Temperature (DHT): {}C, Humidity (DHT): {}%".format(temperature_dht, humidity_dht))
    
    post = ujson.dumps({'temperature': temperature_dht,
                        'humidity': humidity_dht})
    try:
        res = requests.post(url_request, headers = {'content-type': 'application/json'}, data=post)
        res.close()
        if res.status_code == 200:
            print("Request successful!")
        else:
            print("Request failed with status code {}".format(res.status_code))

    except:
        print("Error: Could not establish connection.")
        
    gc.collect()
    utime.sleep(5)