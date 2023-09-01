import ubluetooth

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_COMPLETE = const(6)

class ESP32ble():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
  
    def ble_irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
        # The result of a scan
            addr_type, addr, connectable, rssi, adv_data = data           
            try:
                if bytes(adv_data[5:]).decode('utf-8') == 'BLE_TEST_ESP32':
                                        
                    self._addr_type = addr_type
        
                    self._addr = bytes(
                        addr
                    )
                    
                    print("addr_type: {} adv_type: {}".format(addr_type, connectable))
                    print("addr: {}".format(bytes(addr)))
                    print("adv_data: {}".format(bytes(adv_data)))
                    
                    self._name = bytes(adv_data[5:]).decode('utf-8') or "?"
                    self.ble.gap_scan(None)
                    print("Found peripheral",self._name)

            except:
                pass
        elif event == _IRQ_SCAN_COMPLETE:
              print("Done") 
    
    def scan(self):
        self._addr_type = None
        self._addr = None
        self.ble.gap_scan(2000, 30000, 30000)
        sleep_ms(100)
    
if __name__ == "__main__":
    ble = ESP32ble("BLE_TEST_ESP")
    sleep_ms(100)
    print("Start")
    ble.scan()
    sleep_ms(100)