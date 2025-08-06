# Temperaturüberwachung mit ESP32, DHT22 und MQTT

## Projektbeschreibung
In diesem Projekt messen wir die Raumtemperatur mit einem **DHT22-Sensor** auf einem **ESP32**-Mikrocontroller. Die Daten werden per **MQTT** an einen Broker gesendet, mit **Node-RED** verarbeitet, in **InfluxDB** gespeichert und schließlich in **Grafana** visualisiert.
Das Projekt ist Teil des Hackathons „Building IoT Solutions with OSS" an der HTW Berlin.
---
## Verwendete Software Komponente
- **ESP32** (MicroPython)
- **DHT22** (Temperatursensor)
- **Thonny** (Entwicklungsumgebung)
- **MicroPython** (Laufzeitumgebung auf ESP32)
- **MQTT** (über `broker.f4.htw-berlin.de`)
- **Node-RED** (MQTT→InfluxDB)
- **InfluxDB** (Zeitspeicher für Messdaten)
- **Grafana** (Live-Dashboard)

## Verwendete Hardware Komponente
- **ESP32** (Mikrokontroller, liest Daten)
- **DHT22** (Temperatursensor)
- **Raspberry pi** (Hostet MQTT Broker, Node-RED, InfluxDB, Grafana)
  
---

## Setup-Anleitung

### 1. ESP32 starten
- MicroPython für ESP32   
- MicroPython-Skript auf dem ESP32 ausführen :
  - `boot.py`: stellt WLAN und MQTT verbindung her 
  - `main.py` : Misst Temperatur und sendet Daten per MQTT
- MQTT-Topic: `bis2025/gruppe5/temperature`

### 2. Node-RED Flow importieren
- Node-RED öffnen: [`http://bis.f4.htw-berlin.de:1880`]
- Flow importieren oder erstellen:
  - MQTT IN → function : → InfluxDB OUT → Debug
                   
- MQTT Topic abonnieren: `bis2025/gruppe5/temperature`

### 3. InfluxDB
- Bucket (`Team5`) anlegen
- Daten kommen automatisch über Node-RED rein
  
### 4. Grafana Dashboard erstellen
- Grafana öffnen: [`http://bis.f4.htw-berlin.de:3000`]
- Neue Data Source: **Team5**
