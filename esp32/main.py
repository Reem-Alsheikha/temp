import time
import json
from simple import MQTTClient
import machine
import dht
from machine import Pin, ADC


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

# Temperatur messen und senden
def send_temperature(client):
    sensor.measure()
    temperature = sensor.temperature()
    payload = json.dumps({
        "temperature": temperature,
        "timestamp": time.time()
    })
    client.publish(topic_pub, payload)
    print("Gesendet an temperature:", payload)
# Bodenfeuchtigkeit messen und senden
def send_soil_moisture(client):
    soil_raw = soil_sensor.read()
    soil_percent = round((1 - (soil_raw / 4095)) * 100, 1 )
    soil_payload = json.dumps({
        "soil-moisture": soil_percent,
        "timestamp": time.time()
    })
    client.publish(topic_pub_soil, soil_payload)
    print("Gesendet an soilmoisture:", soil_payload)
# Verbindung zu MQTT aufbauen
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

# Hauptschleife für Messung, Formatierung und Senden
while True:
    try:
        client.check_msg()  # Auf eingehende MQTT-Nachrichten prüfen
        if (time.time() - last_message) > message_interval:
            # Aufgerufene Funktionen
            send_temperature(client)
            send_soil_moisture(client)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()