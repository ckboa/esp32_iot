import microcoapy
from time import sleep_ms

_SERVER_IP="192.168.0.58"
_SERVER_PORT=5683

def sendGetRequest(client):

    messageId = client.get(_SERVER_IP, _SERVER_PORT, "temp")
    print("[GET] Message Id: ", messageId)
    client.poll(5000)

def sendPostRequest(client):
    i = 0 
    for i in range(4):
      messageId = client.post(_SERVER_IP, _SERVER_PORT, "relay/on", "{}".format(i) ,
                                   None, microcoapy.COAP_CONTENT_FORMAT.COAP_TEXT_PLAIN)
      print("[POST] Message Id: ", messageId)
      client.poll(5000)


def sendPutRequest(client):
    i = 0 
    for i in range(4):
      messageId = client.put(_SERVER_IP, _SERVER_PORT, "relay/off",  "{}".format(i),
                                   None,
                                   microcoapy.COAP_CONTENT_FORMAT.COAP_TEXT_PLAIN)
      print("[PUT] Message Id: ", messageId)
      client.poll(5000)



def receivedMessageCallback(packet, sender):
    print('Message received:', packet.toString(), ', from: ', sender)


client = microcoapy.Coap()
# setup callback for incoming response to a request
client.responseCallback = receivedMessageCallback


client.start()
print("client Started")
sendGetRequest(client)
sendPostRequest(client)
sendPutRequest(client)

# stop CoAP
client.stop()
