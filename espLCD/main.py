from machine import Pin, I2C
from time import sleep as delay
from i2c_lcd import I2cLcd

import urequests
import network

# Konfigurasi I2C untuk LCD
I2C_ADDR = 0x27  # Alamat I2C dari LCD Anda
I2C_SDA_PIN = 21  # Pin SDA ESP32
I2C_SCL_PIN = 22  # Pin SCL ESP32

# Inisialisasi I2C untuk LCD
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)  # (i2c, address, row, column)

firebase_url = 'https://upy-uas-default-rtdb.asia-southeast1.firebasedatabase.app/'
firebase_secret = 'amDEG02GQmM7rPADR0SZd5OprvFCYsyCtObLF834'

def initWifi(ssid, password) -> None:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        pass

def setup() -> None:
    # Inisialisasi wifi
    ssid = "Anak kos"
    password = "22445588"
    initWifi(ssid, password)

def getDataFromFirebase():
    url = f"{firebase_url}/sensor_data.json?auth={firebase_secret}"
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("temperature"), data.get("humidity")
        else:
            print('Failed to get data from Firebase', response.text)
            return None, None
    except Exception as e:
        print('Exception: ', str(e))
        return None, None

def displayDataOnLCD(temp, hum):
    lcd.clear()
    lcd.putstr(f"Temp: {temp}C")
    lcd.move_to(0, 1)
    lcd.putstr(f"Humidity: {hum}%")

def main() -> None:
    setup()
    
    while True:
        temp, hum = getDataFromFirebase()
        if temp is not None and hum is not None:
            displayDataOnLCD(temp, hum)
        delay(10)

main()
