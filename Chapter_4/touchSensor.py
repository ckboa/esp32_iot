from machine import TouchPad, Pin
import time
pinlist= [4, 0, 15, 13, 12, 14, 27, 33, 32]
for i in pinlist:
    pin = TouchPad(Pin(i, Pin.IN))
    value = pin.read()
    print('Pin {}: Value = {}'.format(i, value))
    time.sleep_ms(500)
