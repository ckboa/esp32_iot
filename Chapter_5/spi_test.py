"""ILI9341 demo (shapes)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI
import random 

spi = SPI(2,baudrate=40000000, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
display = Display(spi,cs=Pin(5), dc=Pin(21), rst=Pin(22))
display.clear()
while True:
    circuit_count = 0
    for circuit_count in range(10):
        x = random.randint(50,180)
        y = random.randint(50,205)
        r = random.randint(1,50)
        display.fill_circle(x, y, r, color565(x, y, r))
        sleep(2)
    display.clear(color565(x, y, r))
    sleep(5)
    
