# Internetgeschwindigkeits-Rechner

Ein benutzerfreundlicher Python-Rechner zur Umrechnung von Internetgeschwindigkeiten und zur Berechnung von Download-Zeiten.

## Features

✨ **Geschwindigkeitsumrechnung**
- Konvertierung zwischen allen gängigen Einheiten
- Bit-basiert: bit/s, Kbit/s, Mbit/s, Gbit/s
- Byte-basiert: Byte/s, KB/s, MB/s, GB/s

⏱️ **Download-Zeit-Berechnung**
- Berechnet die Zeit für Downloads bei verschiedenen Geschwindigkeiten
- Unterstützt Dateigrößen von Bytes bis Terabytes
- Zeigt Ergebnisse in Tagen, Stunden, Minuten und Sekunden

📊 **Schnellreferenz**
- Übersicht über gängige Internetgeschwindigkeiten
- Beispielberechnungen für 1 GB Downloads

## Installation

Keine zusätzlichen Abhängigkeiten erforderlich! Benötigt nur Python 3.6+

```bash
# Repository klonen
git clone <repository-url>
cd Claude-main

# Ausführbar machen (Linux/Mac)
chmod +x internet_speed_calculator.py
```

## Verwendung

### Interaktiver Modus

```bash
python3 internet_speed_calculator.py
```

Das Programm bietet ein interaktives Menü mit folgenden Optionen:

1. **Geschwindigkeit umrechnen** - Konvertiert einen Wert in alle verfügbaren Einheiten
2. **Download-Zeit berechnen** - Berechnet die Zeit für einen Download
3. **Schnellreferenz** - Zeigt gängige Geschwindigkeiten und Beispiele
4. **Beenden** - Programm verlassen

### Beispiele

#### Geschwindigkeit umrechnen
```
Geschwindigkeit eingeben: 100
Von welcher Einheit? Mbit/s

100 Mbit/s entspricht:
- 100.000.000 bit/s
- 100.000 Kbit/s
- 100 Mbit/s
- 0,1 Gbit/s
- 12.500.000 Byte/s
- 12.500 KB/s
- 12,5 MB/s
- 0,0125 GB/s
```

#### Download-Zeit berechnen
```
Dateigröße eingeben: 5
Einheit? GB

Internetgeschwindigkeit eingeben: 50
Einheit? Mbit/s

Download von 5 GB bei 50 Mbit/s
Geschätzte Download-Zeit: 13 Minuten 20 Sekunden
```

## Programmstruktur

```
Claude-main/
├── internet_speed_calculator.py  # Hauptprogramm
├── README.md                      # Diese Datei
├── example_usage.py              # Beispiele für programmgesteuerte Nutzung
└── CLAUDE.md                     # Entwicklerdokumentation
```

## Klassen und Methoden

### `InternetSpeedCalculator`

**Methoden:**

- `convert_speed(value, from_unit, to_unit)` - Konvertiert zwischen zwei Einheiten
- `convert_all_units(value, from_unit)` - Konvertiert in alle verfügbaren Einheiten
- `calculate_download_time(file_size, size_unit, speed, speed_unit)` - Berechnet Download-Zeit

### Beispiel für programmgesteuerte Nutzung

```python
from internet_speed_calculator import InternetSpeedCalculator, SpeedUnit, SizeUnit

calculator = InternetSpeedCalculator()

# Geschwindigkeit umrechnen
speed_mb = calculator.convert_speed(100, SpeedUnit.MBIT_S, SpeedUnit.MB_S)
print(f"100 Mbit/s = {speed_mb} MB/s")  # 12.5 MB/s

# Download-Zeit berechnen
days, hours, minutes, seconds = calculator.calculate_download_time(
    10, SizeUnit.GB,
    50, SpeedUnit.MBIT_S
)
print(f"Download-Zeit: {hours}h {minutes}m {seconds}s")
```

## Gängige Umrechnungen

| Mbit/s | MB/s | Beschreibung |
|--------|------|--------------|
| 16 | 2 | DSL 16.000 |
| 50 | 6,25 | Kabel 50 |
| 100 | 12,5 | Glasfaser 100 |
| 250 | 31,25 | Glasfaser 250 |
| 500 | 62,5 | Glasfaser 500 |
| 1000 | 125 | Gigabit |

**Wichtig**:
- 1 Byte = 8 Bits
- Internetanbieter geben Geschwindigkeit meist in Mbit/s an
- Download-Geschwindigkeit wird oft in MB/s angezeigt

## Tipps

💡 **Realistische Geschwindigkeiten**
Die berechneten Zeiten sind theoretische Werte. In der Praxis können Downloads langsamer sein durch:
- Netzwerkauslastung
- Server-Geschwindigkeit
- Overhead (Protokolle, Fehlerkorrektur)
- WLAN statt LAN-Verbindung

💡 **Bit vs. Byte**
- Internetgeschwindigkeit: meist in **Bit** pro Sekunde (Mbit/s)
- Dateigrößen: meist in **Byte** (MB, GB)
- 1 Byte = 8 Bits

## Lizenz

Dieses Projekt steht zur freien Verfügung.

## Beiträge

Verbesserungsvorschläge und Beiträge sind willkommen! Siehe [CLAUDE.md](CLAUDE.md) für Entwicklungsrichtlinien.
