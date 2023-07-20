import network, espnow
from time import sleep_ms

sta = network.WLAN(network.STA_IF)
sta.active(True)

# Set up Esp_Now
sender = espnow.ESPNow()
sender.active(True)

# Set MAC Address
mypeer = b'\xac\x0b\xfb)\xce\xbc'

# add_peer()
sender.add_peer(mypeer)

# Start sending
for i in range(10):
    sleep_ms(100)
    sender.send(mypeer,'Hello', True)
sender.send(mypeer, b'bye')
sleep_ms(100)

# Show sending Stat
print('Send:{}, Response:{}, Failures: {}'.format(sender.stats()[0], sender.stats()[1], sender.stats()[2]) ) 
