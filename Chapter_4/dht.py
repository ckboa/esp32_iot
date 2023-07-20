from machine import Pin
import dht
import utime
# setting GPIO Pin 
sensor = dht.DHT22(Pin(25))  # GPIO25 

def reading_sensor():
    sensor.measure()
    temp_str = "Temp: {0:3.1f}".format(sensor.temperature())
    humi_str = "Humi: {0:3.1f}".format(sensor.humidity())
    # set text display
    print(temp_str)
    print(humi_str)
    
while(1):
    reading_sensor()
    utime.sleep(5)

