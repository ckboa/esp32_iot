try:
    import usocket as _socket
except:
    import _socket
try:
    import ussl as ssl
except:
    import ssl


import network
from time import sleep 

IP_Addr = '192.168.0.52'
Port = 8443

def main():
    soc = _socket.socket()
    soc_info = _socket.getaddrinfo(IP_Addr, Port)
    print("Address infos:", soc_info)
    addr = soc_info[0][-1]
    print("Connect address:", addr)
    soc.connect(addr)
    soc = ssl.wrap_socket(soc)
    #MicroPython SSLSocket objects support read() and write() methods.
    soc.write(b"Sending to server")       
    print(soc.readline().decode())
    soc.close()

main()
