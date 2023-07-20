from machine import UART
import time

uart = UART(2, baudrate=115200, bits=8, parity=None, stop=1, timeout=5000)
i = 0
for i in range(3):
   uart.write("\r\n time {}: input value {}:"
              .format(time.ticks_ms(),i+1) )
   readfromcome = uart.readline()
   print("time {}: value: {} \r\n"
              .format(time.ticks_ms(), readfromcome))
         