from machine import Timer
from time import sleep_ms
from micropython import const
import random
import ubluetooth

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

msg = ""

class ESP32_BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
        self.is_connected = False

    def connected(self):
        self.is_connected = True
        
    def disconnected(self):        
        self.is_connected = False

    def ble_irq(self, event, data):
        global msg
        if event == _IRQ_CENTRAL_CONNECT: 
            self.connected()

        elif event == _IRQ_CENTRAL_DISCONNECT: 
            self.advertiser()
            self.disconnected()
        
        elif event == _IRQ_GATTS_WRITE:
            buffer = self.ble.gatts_read(self.write)
            msg = buffer.decode('UTF-8').strip()
            print(msg)
           
            
    def register(self):        
        Test_UUID = ubluetooth.UUID("00002A6A-0000-1000-8000-00805F9B34FB")
        _write = (ubluetooth.UUID("00002A6E-0000-1000-8000-00805F9B34FB"), ubluetooth.FLAG_WRITE)
        _notify = (ubluetooth.UUID("00002A6F-0000-1000-8000-00805F9B34FB"), ubluetooth.FLAG_NOTIFY)
        
        BLE_Sensor = (Test_UUID, (_write, _notify,))
        SERVICES = (BLE_Sensor, )
        ((self.write, self.notify,), ) = self.ble.gatts_register_services(SERVICES)
        
    def send(self, data):
        self.ble.gatts_notify(0, self.notify, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray(b'\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(", ".join(hex(ad) for ad in adv_data))
        print("\r\n")

ble = ESP32_BLE("BLE_TEST_ESP32")

while True:
    if ble.is_connected:
        ble.send('%s' %random.randint(25,75))
    sleep_ms(1000)