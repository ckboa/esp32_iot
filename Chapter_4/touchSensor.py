from machine import TouchPad, Pin
import time
pinlist= [    33] 

pin = TouchPad(Pin(33, Pin.IN))
for i in range(10):
    value = pin.read()
    print('Pin {}: Value = {}'.format(i, value))
    time.sleep_ms(500)