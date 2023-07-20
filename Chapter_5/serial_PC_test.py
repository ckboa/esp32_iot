import serial
ser = serial.Serial('COM4')
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS 
ser.parity = serial.PARITY_NONE 
ser.stopbits = serial.STOPBITS_ONE              
ser.xonxoff = False    
ser.rtscts = False    
ser.dsrdtr = False
ser.timeout = 10
ser.flushInput()

while True:
   ser_data = ser.readline()
   ser_decode = ser_data.decode("utf-8")
   data = ser_decode.split(',')
        
   print("PC Temperature:{}".format(data[0]))
   print("PC Humidity:{}".format(data[1]))
   print("PC Pressure:{}".format(data[2]))
   print("PC Gas:{}".format(data[3]))
  
   