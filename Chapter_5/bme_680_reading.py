from machine import Pin, SoftI2C, UART
from time import sleep
from bme680 import *


uart = UART(2, baudrate=115200, bits=8, parity=None, stop=1, timeout=5000)
i2c = SoftI2C(scl=Pin(21), sda=Pin(22))
bme = BME680_I2C(i2c=i2c)

while True:
    temperature = bme.temperature
    humidity = bme.humidity
    pressure = bme.pressure
    gas = bme.gas/1000 
      
    uart.write("{0:.2f},{1:.2f},{2:.2f},{3:.2f}\r\n"
               .format(temperature, humidity, pressure, gas))
    
    print("ESP32 Temperature:{:.2f}".format(temperature))
    print("ESP32 Humidity:{:.2f}".format(humidity))
    print("ESP32 Pressure:{:.2f}".format(pressure))
    print('ESP32 Gas:{:.2f}'.format(gas))
 
    sleep(5)