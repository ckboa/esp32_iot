import machine
import esp32
from time import *
from machine import TouchPad, Pin

touch = TouchPad(Pin(33))
print("Pin 33 touch value: {}".format(touch.read())) 
touch.config(250)
esp32.wake_on_touch(True)
touch_count = 0
timer_count = 0
cur_time = ticks_ms()
while True:
   
    sleep(0.1)
    machine.lightsleep(3000)    
    wake_from = machine.wake_reason()
    if wake_from == machine.TOUCHPAD_WAKE:
        touch_count = touch_count + 1
        cur_time = ticks_ms()
        print("Touch value : {}".format(touch.read()))
    else:
        new_time = ticks_ms() 
        time_diff = ticks_diff(new_time,cur_time)
        cur_time = new_time
        print("Time diff : {}".format(time_diff)) 
        timer_count = timer_count + 1
        
    print("--Light sleep wake time: {}".format(touch_count+timer_count))
    sleep(0.1)
    if touch_count + timer_count == 5:
        print("Wake from touch {0} and timer {1}".format(touch_count, timer_count))   
        break 