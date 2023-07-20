from umqtt.simple2 import MQTTClient

client = MQTTClient("esp32", "192.168.0.51", port=1883,
                    user=None, password=None, keepalive=30,
                    ssl=False, ssl_params={})
client.connect()
client.publish(b"computer/hardware/CPU/speed",
               b"Hello from ESP32")
client.disconnect()
