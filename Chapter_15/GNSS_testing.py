#micropyGPS from https://github.com/inmcm/micropyGPS
from micropyGPS import MicropyGPS
from machine import UART, Pin
import time
 
pin_set = Pin(25, Pin.OUT)
pin_reset = Pin(26, Pin.OUT)
        
pin_set.on
pin_reset.off()
 
uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=500)
gps = MicropyGPS(7)

def get_gps_data():
    buf = uart.readline()
    
    for char in buf:
       gps.update(chr(char))  
    
    print("Date: {} Time: {}:{}:{}".format(gps.date_string("long"), *gps.timestamp))
    print("Latitude:", gps.latitude)
    print("Longitude:", gps.longitude)

while True:
    print("Satellites in use: {}".format(gps.satellites_in_use))
    get_gps_data()      
    time.sleep(5) 

