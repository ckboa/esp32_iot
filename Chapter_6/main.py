import machine
rtc = machine.RTC()
rtc_data = rtc.memory() 
print(rtc_data)