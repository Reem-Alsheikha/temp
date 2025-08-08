# IoT-Projekt – Temperatur- und Bodenfeuchtemessung mit ESP32
Im Rahmen des Hackathons **"Building IoT Solutions with OSS"** an der HTW Berlin haben wir eine IoT-Lösung mit dem ESP32-Mikrocontroller umgesetzt.

### Basisfunktion
Im ersten Teil des Projekts wurde die **Raumtemperatur** mithilfe eines **DHT22-Sensors** gemessen, welches am **ESP32** gebunden ist. Dieser **ESP32** ist über WLAN mit dem **MQTT-Broker** verbunden und sendet alle 5 Sekunden die Messwerte als MQTT-Nachrichten auf ein vordefiniertes Topic. Dieses Topic wird von **NodeRed** abonniert. Dort wird die Datenverarbeitung visuell programmiert. Diese DAten empfängt **InfluxDB** über HTTP Requests. Nachdem die InfluxDB die Daten speichert, fragt **Grafana** über HTTP Querys die Daten ab. Dort können sie letzendlich in Grafana z.B. als Diagramm visualisiert werden.

### Erweiterung: Bodenfeuchtesensor & Telegram-Alarm

Im zweiten Teil haben wir die Lösung um einen **kapazitiven Bodenfeuchtesensor** erweitert. Der ESP32 misst die Bodenfeuchtigkeit regelmäßig und berechnet daraus einen **Prozentwert**, basierend auf empirisch bestimmten Minimal- und Maximalwerten.

Sobald die Bodenfeuchtigkeit unter einen definierten Schwellwert fällt (z. B. 30 %), wird automatisch eine **Benachrichtigung über Telegram** ausgelöst. Die Logik zur Schwellenwertprüfung und Benachrichtigung wurde dabei vollständig in **Node-RED** umgesetzt. 


Dadurch wird der Nutzer aktiv informiert, wenn die Pflanze gegossen werden muss
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
- **Raspberry pi** (Node-RED)
  
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
- Das Dashboard zeigt:
      - Live-Anzeige der aktuellen Temperatur
      - Zeitverlauf
- Grafana öffnen: [`http://bis.f4.htw-berlin.de:3000`]
-  Data Source: **Team5**
