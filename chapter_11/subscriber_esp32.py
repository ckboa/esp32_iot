import time
from umqtt.simple2 import MQTTClient


# Received messages from subscriptions will be delivered to this callback
def sub_callback(topic, msg, retain, dup):
    print("t:{} m:{}".format(topic, msg))


client = MQTTClient("esp32_sub", "192.168.0.52", port=1883,
                    user=None, password=None, keepalive=30,
                    ssl=False, ssl_params={})
                    
client.set_callback(sub_callback)                   
client.connect()
client.subscribe(b"#")
count = 0
for count in range(10): 
    client.check_msg()
    time.sleep(3)
client.disconnect()
