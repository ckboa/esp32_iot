import network, espnow


sta = network.WLAN(network.STA_IF)
sta.active(True)

# Set up Esp_Now
receiver = espnow.ESPNow()
receiver.active(True)

# Waiting to receive data 
while True:
    host, msg = receiver.recv()
    print('{} from {}'.format(msg, host))
    if msg == b'bye':
       print("END") 
       break 

# Show reciving Stat
print('Receive:{}, Drop:{}'.format(receiver.stats()[3], receiver.stats()[4])) 
