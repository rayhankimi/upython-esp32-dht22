from machine import Pin, I2C
import time
from i2c_lcd import I2cLcd

# Konfigurasi I2C
I2C_ADDR = 0x27  # Alamat I2C dari LCD Anda
I2C_SDA_PIN = 21  # Pin SDA ESP32
I2C_SCL_PIN = 22  # Pin SCL ESP32

# Inisialisasi I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

# Inisialisasi LCD
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)  # (i2c, address, row, column)

def main():
    lcd.putstr("Hello, World!")
    time.sleep(2)
    
    lcd.clear()
    lcd.putstr("ESP32 with LCD")

    while True:
        for i in range(10):
            lcd.move_to(0, 1)
            lcd.putstr(f"Count: {i}")
            time.sleep(1)

main()
