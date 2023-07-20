from machine import UART, Pin
from binascii import hexlify
import time
import dht
import ujson

sensor = dht.DHT22(Pin(25))
data = "temp= {:5.2f}, humi= {:5.2f}"
uart = UART(2, baudrate=115200, bits=8, parity=None, stop=1, timeout=1000)

def sensorget():
    sensor.measure()
    temp = sensor.temperature()
    humi = sensor.humidity()
    print("temperature: %3.1f°C" % temp)
    print("humidity: %3.1f%%" % humi)
    date_json = ujson.dumps({"temp": temp, "humi": humi})
    return date_json

def read():
    uart_read = uart.read()
    if uart_read != None:
        print('-----UART READ-----')
        print(uart_read)
        print('-----****-****-----')


while True:
    date_sensor = sensorget()
    date_sensor = ujson.loads(date_sensor)
    lora_data = data.format(float(date_sensor["temp"]), float(date_sensor["humi"]))
    print(lora_data)
    hexa_data = hexlify(lora_data.encode("utf-8")).decode("utf-8")  # แปลงเป็นสตริงและเข้ารหัสเป็นฐานสิบหก
    uart.write("mac tx ucnf 2 {}".format(hexa_data))
    read()
    time.sleep(10)
