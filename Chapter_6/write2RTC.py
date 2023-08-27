import machine
rtc = machine.RTC()
rtc_data = b'rtc_memory_save'
rtc.memory(rtc_data)
machine.deepsleep(5000)
