from machine import Pin, SoftI2C
import ssd1306
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.text('Hello World ', 0, 0)

for i in range(10, 60, 10):
    display.text("line {}".format(i), i, i)
display.show() 