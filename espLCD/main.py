from machine import Pin, I2C, PWM
from time import sleep as delay
from i2c_lcd import I2cLcd
import urequests
import network


I2C_ADDR = 0x27  
I2C_SDA_PIN = 21  
I2C_SCL_PIN = 22


buzzer_pin = Pin(15, Pin.OUT)
buzzer = PWM(buzzer_pin)
buzzer.duty(0) 


led_pin= Pin(4, Pin.OUT)


i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)  


firebase_url = 'firebase-url'
firebase_secret = 'firebase-secret'


def initWifi(ssid, password) -> None:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        pass


def setup() -> None:
    ssid = "ssid wifi"
    password = "passwordwifi"
    initWifi(ssid, password)


def getDataFromFirebase() -> float:
    url = f"{firebase_url}/sensor_data.json?auth={firebase_secret}"
    
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            response.close()  # cek komen bawah pak
            return data.get("temperature"), data.get("humidity")
        
        else:
            print('Failed to get data from Firebase', response.text)
            response.close()  # Tutup koneksi biar egk error niki pak
            return None, None
        
    except Exception as e:
        print('Exception: ', str(e))
        return None, None


def displayDataOnLCD(temp, hum) -> None:
    lcd.clear()
    lcd.putstr(f"Suhu: {temp}C")
    lcd.move_to(0, 1)
    lcd.putstr(f"Kelb: {hum}%")


def play_tone(frequency, duration) -> None:
    buzzer.freq(frequency)
    buzzer.duty(512)  # Duty cycle 50% nggih pak dari 1024
    delay(duration / 1000)  
    buzzer.duty(0)  # Biar gak biiiiiiip gitu pak


def main() -> None:
    
    setup()
    
    while True:
        try:
            temp, hum = getDataFromFirebase()
            
            if temp is not None and hum is not None:
                displayDataOnLCD(temp, hum)
                
                if temp >= 35:
                    led_pin.on()
                    play_tone(1535, 1000)
                    
                elif temp < 35:
                    led_pin.off()
                    
        except Exception as e:
            print('Exception: ', str(e))
        
        delay(2)

main()
