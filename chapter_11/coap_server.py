import microcoapy
import utime as time
import esp32
from machine import Pin
# read temp 
temp = (esp32.raw_temperature()-32.0)/1.8
# assign relay connection PIN
relay_1 = Pin(15,Pin.OUT)
relay_2 = Pin(13,Pin.OUT)
relay_3 = Pin(12,Pin.OUT)
relay_4 = Pin(14,Pin.OUT)
relay_list = [relay_1, relay_2, relay_3, relay_4]

client = microcoapy.Coap()

def measureCurrent(packet, senderIp, senderPort):
    print('request received: ', packet.toString(),
          ', from: ', senderIp, ":", senderPort)
    client.sendResponse(senderIp, senderPort, packet.messageid,
          'raw temp = {}'.format(temp), microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT,
          microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
 
def relayOn(packet, senderIp, senderPort):
    print('request received: ', packet.toString(),
          ', from: ', senderIp, ":", senderPort)
    if packet.payload != None:
        data=packet.payload.decode("utf-8")
        relay_list[int(data) - 1].value(1) 
        client.sendResponse(senderIp, senderPort, packet.messageid,
              'relay {} ON'.format(data),
                microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT,
               microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
        

def relayOff(packet, senderIp, senderPort):
    if packet.payload != None:
        data=packet.payload.decode("utf-8")
        relay_list[int(data) - 1].value(0) 
        client.sendResponse(senderIp, senderPort, packet.messageid,
              'relay {} OFF'.format(data),
                microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT,
               microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)

client.addIncomingRequestCallback('temp', measureCurrent)
client.addIncomingRequestCallback('relay/on', relayOn)
client.addIncomingRequestCallback('relay/off', relayOff)

client.start()
print("Server Started") 
# wait for incoming request for 60 seconds = 60000
timeoutMs = 120000
start_time = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start_time) < timeoutMs:
    client.poll(60000)

client.stop()
