from machine import Pin
from time import sleep as delay
import dht 
import network
import urequests as requests

firebase_url = 'https://upy-uas-default-rtdb.asia-southeast1.firebasedatabase.app/'
firebase_secret = 'amDEG02GQmM7rPADR0SZd5OprvFCYsyCtObLF834'

def initWifi(ssid="Anak kos",password="22445588") -> None:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        pass
    

def initDHT() -> dht.DHT22:
    #Inisialisasi pin pak gung
    sensor = dht.DHT22(Pin(14))
    
    #Inisialisasi wifi pak gung
    ssid = "Anak kos"
    password = "22445588"
    
    
    return sensor



def sendData(temp,hum) -> None:
    url = f"{firebase_url}/sensor_data.json?auth={firebase_secret}"
    data = {
        "temperature": temp,
        "humidity": hum
    }
    try:
        response = requests.put(url, json=data)
        if response.status_code == 200:
            print('Nyuukseesss')
        else:
            print('Gak dulu, response.text')
            
    except Exception as e:
        print('Waduh gagal nok ',str(e))
        
    finally:
        response.close()
    

def main() -> None:
    sensor = initDHT()
    initWifi()
    
    
    while True:
        try:
            delay(5)
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()

            print('Temperature: %3.1f C' %temp)
            print('Humidity: %3.1f %%' %hum)
            
            sendData(temp, hum)
       
        except OSError as e:
            print('Failed to read sensor.')
        except Exception as e:
            print('Failed to send data to Firebase.', str(e))
        
main()