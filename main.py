import time
import json
from simple import MQTTClient
import machine
import dht
from machine import Pin, ADC

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'bis2025/notification'
topic_pub = b'bis2025/gruppe5/temperature' # Passendes Topic zum Senden
topic_pub_soil = b'bis2025/gruppe5/soilmoisture'


# Empfang von MQTT-Nachrichten ermöglichen (Callback)
def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

# Verbindung zum MQTT-Broker herstellen
def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client
# Bei Verbindungsfehler: Neustart
def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

# Sensor initalisieren (DHT22 an Pin D4)
DHT_PIN = 4
sensor = dht.DHT22(Pin(DHT_PIN))

# Bodenfeuchtesensor an GPIO32
SOIL_PIN = 32
soil_sensor = ADC(Pin(SOIL_PIN))
soil_sensor.atten(ADC.ATTN_11DB)

# Verbindung zu MQTT aufbauen
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
# Hauptschleife für Messung, Formatierung und senden
while True:
    try:
        client.check_msg() # Auf eingehende MQTT-Nachrichten prüfen
        if (time.time() - last_message) > message_interval:
            sensor.measure()
            temperature = sensor.temperature()
            # Daten in JSON-Format mit Zeitstampel umwandeln
            payload = json.dumps({  
                "temperature": temperature,
                "timestamp": time.time()
            })
            #Daten an MQTT-Topic senden
            client.publish(topic_pub, payload)
            #Debug Ausgabe
            print("Gesendet an temperature:", payload)
            
            soil_value = soil_sensor.read()
            soil_payload = json.dumps({
                "soil-moisture": soil_value,
                "timestamp": time.time()
                })
            client.publish(topic_pub_soil, soil_payload)
            #Debug Ausgabe
            print("Gesendet an soilmoisture:", soil_payload)
            
            
            
            
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()