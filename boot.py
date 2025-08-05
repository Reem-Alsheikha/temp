import time
from simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'Rechnernetze'
password = 'rnFIW625'
mqtt_server = 'broker.f4.htw-berlin.de'
mqtt_user = 'REPLACE_WITH_YOUR_MQTT_USERNAME'
mqtt_pass = 'REPLACE_WITH_YOUR_MQTT_PASSWORD'

#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'bis2025/notification'
topic_pub = b'bis2025/gruppe5/temperature'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
