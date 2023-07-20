import esp32
fahrenheit  = esp32.raw_temperature()
celsius = (fahrenheit -32.0)/1.8
print("Temp %d F = %5.2f C" %(fahrenheit, celsius))
