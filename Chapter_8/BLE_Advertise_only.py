
import ubluetooth

class ESP32_BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.register()
        self.advertiser()

    def register(self):        
        Test_UUID = ubluetooth.UUID("00002A6A-0000-1000-8000-00805F9B34FB")
        _write = (ubluetooth.UUID("00002A6E-0000-1000-8000-00805F9B34FB"), ubluetooth.FLAG_WRITE)
        _notify = (ubluetooth.UUID("00002A6F-0000-1000-8000-00805F9B34FB"), ubluetooth.FLAG_NOTIFY)
        BLE_Sensor = (Test_UUID, (_write, _notify,))
        SERVICES = (BLE_Sensor, )

        ((self.write, self.notify,), ) = self.ble.gatts_register_services(SERVICES)

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(", ".join(hex(ad) for ad in adv_data))
        print("\r\n")


ble = ESP32_BLE("BLE_TEST_ESP32")


