from machine import Pin
from time import sleep
from machine import UART
import network
import time
import json
from robust import MQTTClient

uart = UART(2, tx=17, rx=16)
uart.init(115200, bits=8, parity=None, stop=1)

led = Pin(2, Pin.OUT)

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('Mindi', 'huantuyendieuminhanh')

ssid = 'Watermelon_Fox'
password = 'aio_jcvR41arNGAb1nKmIBuswsmpZjZU'
mqttHost = 'io.adafruit.com'

while nic.isconnected() == False:
    print("Not connected")
    sleep(1)

print('Connected')

client = MQTTClient('pga', mqttHost, user=ssid, password=password)
client.connect()

uart.write('Invalid\n')
lastTime = 0
while True:
    data = uart.readline()
    if data is None:
        continue
    a = data.decode('utf-16')
    a = ''.join(a.split())
    if '-' in a:
        if time.time() - lastTime > 3:
            feeds = a.split('-')
            compass = int(feeds[0])
            step = int(feeds[1])
            jsonData = {
              "compass": compass,
              "step": step
            }
            print("SENDING ON")
            client.publish(topic='Watermelon_Fox/feeds/testing', msg=json.dumps(jsonData))
            print(a)
            lastTime = time.time()

        uart.write('OK\n')
        continue
    else:

        uart.write('Invalid\n')
