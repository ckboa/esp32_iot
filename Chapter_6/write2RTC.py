import machine
from esp32 import ULP
import esp32
esp32.wake_on_ulp(True)
ulp = ULP()
ulp.set_wakeup_period(0, 5000)  # use timer0, wakeup after 50.000 cycles
rtc = machine.RTC()
rtc_data = 'rtc_memory_save'
rtc.memory(rtc_data)
machine.lightsleep() 
