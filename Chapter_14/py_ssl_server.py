import socket
import ssl

IP_Addr = '192.168.0.52'
Port = 8443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('cert.pem', 'key.pem')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind((IP_Addr, Port))
sock.listen(5)

ssock = context.wrap_socket(sock, server_side=True)
conn, addr = ssock.accept()

while True:
    data = conn.recv(1024)
    if(len(data) == 0):    
      print("close socket")
      conn.close()
      break
    print(f"Received: {data.decode('utf-8')}")
    ret = conn.send(b'OK, I am a server\r\n')
 