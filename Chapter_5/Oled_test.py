from machine import Pin, SoftI2C
import ssd1306


i2c = SoftI2C(scl=Pin(21), sda=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)



oled.text('Hello World 6', 0, 0)
oled.show()