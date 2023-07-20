import esp32
esp32.hall_sensor()
i = 0
for i in range(5):
   print("Value = %d" %esp32.hall_sensor())