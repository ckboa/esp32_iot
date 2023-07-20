from machine import Pin
from umqtt.simple2 import MQTTClient
from machine import Timer
import time
import esp32
import dht
import gc
import json
gc.collect() 

sensor = dht.DHT22(Pin(16))

relay_1 = Pin(15, Pin.OUT)
relay_2 = Pin(13, Pin.OUT)
relay_3 = Pin(12, Pin.OUT)
relay_4 = Pin(14, Pin.OUT)
relay_list = [relay_1, relay_2, relay_3, relay_4]

for i in relay_list:
    i.value(0) 

mqtt_broker = "192.168.0.53"
mqtt_client_id = "esp32-sensor"
sensor_topic = "sensor_data"
relay_topic = b"relay_controller"

def on_message(topic, msg, retain, dup):
    if topic == relay_topic:
        print("Received message: topic: {} message: {}".format(
            topic.decode(), msg.decode()))
        relay_control(msg.decode())

def disconnect_mqtt():
    client.disconnect()

def relay_control(msg):
    data = json.loads(msg)
    relayNumber = int(data['relayNumber'])
    print(relayNumber)
    relay = relay_list[relayNumber - 1]
    
    if data['state'] == 'OFF':
        print("Relay: " + str(relayNumber) + ", State: OFF")
        relay.value(0)
    else:
        print("Relay: " + str(relayNumber) + ", State: ON")
        relay.value(1)

def reading_sensor():
    try: 
      sensor.measure()
      temperature_dht = sensor.temperature()
      humidity_dht = sensor.humidity()
      #fahrenheit to celsius of temperature_esp32
      fahrenheit = esp32.raw_temperature()
      temperature_esp32 = (fahrenheit - 32.0)/1.8

      print("Temperature (DHT): {}C, Humidity (DHT): {}%, Temperature (ESP32): {:.2f}C".
             format(temperature_dht, humidity_dht, temperature_esp32))
      payload = {
        'temperature': temperature_dht,
        'humidity': humidity_dht,
        'esp32Temperature': temperature_esp32
      }
      client.publish(sensor_topic, json.dumps(payload))
    except OSError:
        print("Please Check sensor")
        disconnect_mqtt() 


    

client = MQTTClient(mqtt_client_id, mqtt_broker, port=1883,
                       user=None, password=None,
                       keepalive=300, ssl=False, ssl_params={})

client.connect(clean_session=False)
client.set_last_will("esp32-sensor", "Disconnected")
client.set_callback(on_message)
client.subscribe(relay_topic)
print("Connected to MQTT broker")

while True:
    try:
        client.check_msg()
        time.sleep(1)
        reading_sensor()
    except KeyboardInterrupt:
        disconnect_mqtt() 
        print("Disconnected Broker")