import time
from machine import ADC, Pin

adc35 = ADC(Pin(35))

adc35.width(ADC.WIDTH_12BIT)   

i = 0
for i in range(5):
  print(adc35.read())
  time.sleep(1)