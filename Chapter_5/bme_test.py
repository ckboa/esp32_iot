from machine import Pin, SoftI2C
import bme280_float as bme280

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
bme = bme280.BME280(i2c=i2c)

print(bme.values)