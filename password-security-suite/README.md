# 🔐 Password Security Suite

Eine umfassende Web-Anwendung zum Generieren sicherer Passwörter und zur Überprüfung ihrer Sicherheit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎲 Password Generator
- **Anpassbare Länge**: 4-64 Zeichen
- **Zeichentypen**: Groß-/Kleinbuchstaben, Zahlen, Sonderzeichen
- **Filteroptionen**: Mehrdeutige Zeichen ausschließen
- **Eigene Zeichensätze**: Definiere deinen eigenen Zeichenpool
- **Echtzeit-Stärkeanalyse**: Sofortige Bewertung der generierten Passwörter

### 📊 Password Strength Checker
- **Umfassende Analyse**: Score von 0-100
- **Detaillierte Metriken**:
  - Passwortlänge
  - Entropie-Berechnung (in Bits)
  - Crack-Zeit-Schätzung
  - Zeichenvielfalt-Analyse
- **Intelligente Erkennung**:
  - Häufig verwendete Passwörter
  - Sequenzielle Zeichen (123, abc)
  - Wiederholte Zeichen
  - Gängige Wörter
- **Visuelles Feedback**: Farbcodierte Stärkeanzeige
- **Konstruktive Verbesserungsvorschläge**

### 🔤 Passphrase Generator
- **Merkbare Passwörter**: Zufällige Wörter statt zufällige Zeichen
- **Anpassbar**:
  - 2-8 Wörter
  - Verschiedene Trennzeichen (-, _, ., Leerzeichen)
  - Großschreibung optional
  - Zahlen am Ende optional
- **Hohe Sicherheit**: Trotz Lesbarkeit sehr sicher durch Länge
- **Beispiel**: `Quantum-Dragon-Harbor-Sunset-7482`

### ⚠️ Data Breach Check
- **Have I Been Pwned Integration**: Prüft gegen Millionen geleakter Passwörter
- **100% Datenschutz**: k-Anonymität schützt dein Passwort
  - Nur die ersten 5 Zeichen des Hash werden übertragen
  - Dein echtes Passwort verlässt niemals deinen Browser
- **Echtzeit-Prüfung**: Sofortige Ergebnisse
- **Transparenz**: Zeigt Anzahl der Leaks an

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritt 1: Repository klonen
```bash
git clone <repository-url>
cd password-security-suite
```

### Schritt 2: Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### Schritt 3: Server starten
```bash
python backend.py
```

### Schritt 4: Im Browser öffnen
```
http://localhost:5000
```

Die Anwendung läuft nun lokal auf deinem Computer! 🎉

## 📖 Verwendung

### Password Generator

1. **Wähle deine Einstellungen**:
   - Schiebe den Längen-Slider (4-64 Zeichen)
   - Aktiviere/Deaktiviere Zeichentypen
   - Optional: Mehrdeutige Zeichen ausschließen
   - Optional: Eigene Zeichen definieren

2. **Generiere Passwort**:
   - Klicke auf "🎲 Generieren"
   - Oder nutze den 🔄 Button zum schnellen Neugenerieren

3. **Passwort kopieren**:
   - Klicke auf das 📋 Symbol
   - Passwort ist in der Zwischenablage!

### Password Checker

1. **Passwort eingeben**:
   - Tippe dein Passwort in das Eingabefeld
   - Nutze 👁️ zum Ein-/Ausblenden

2. **Analyse starten**:
   - Klicke auf "📊 Stärke prüfen"
   - Oder drücke Enter

3. **Ergebnisse ansehen**:
   - **Stärke-Score**: 0-100 Punkte
   - **Kategorien**: Very Weak → Very Strong
   - **Details**: Länge, Entropie, Crack-Zeit
   - **Feedback**: Konkrete Verbesserungsvorschläge

### Passphrase Generator

1. **Einstellungen anpassen**:
   - Wähle Anzahl der Wörter (2-8)
   - Wähle Trennzeichen
   - Großschreibung aktivieren?
   - Zahl am Ende hinzufügen?

2. **Generieren & Kopieren**:
   - Klicke auf "🔤 Passphrase generieren"
   - Kopiere mit dem 📋 Button

### Breach Check

1. **Passwort eingeben**:
   - Tippe dein Passwort ein
   - Nutze 👁️ zum Anzeigen

2. **Prüfung starten**:
   - Klicke auf "🔍 Auf Leaks prüfen"
   - Warte auf Ergebnis (ca. 1-2 Sekunden)

3. **Ergebnis interpretieren**:
   - ✓ **Grün**: Passwort nicht in Leaks gefunden
   - ⚠️ **Rot**: Passwort wurde geleakt → SOFORT ÄNDERN!

## 🔒 Sicherheit & Datenschutz

### Lokale Verarbeitung
- Alle Passwörter werden **lokal auf deinem Computer** generiert und analysiert
- **Keine Speicherung**: Passwörter werden niemals auf einem Server gespeichert
- **Kein Tracking**: Keine Analytik, keine Cookies, kein Tracking

### Breach Check Datenschutz
Die Anwendung nutzt die [Have I Been Pwned API](https://haveibeenpwned.com/) mit **k-Anonymität**:

1. Dein Passwort wird lokal mit SHA-1 gehasht
2. Nur die **ersten 5 Zeichen** des Hash werden an die API gesendet
3. Die API sendet alle Hashes zurück, die mit diesen 5 Zeichen beginnen
4. Der Abgleich findet **lokal auf deinem Computer** statt

**Beispiel**:
```
Passwort: "MyPassword123"
SHA-1 Hash: "A1B2C3D4E5F6G7H8..."
Gesendet: "A1B2C" (nur erste 5 Zeichen)
Empfangen: Liste aller Hashes die mit A1B2C beginnen
Prüfung: Lokal, ob vollständiger Hash in Liste
```

→ **Dein echtes Passwort kann niemals rekonstruiert werden!**

## 🧮 Technische Details

### Passwort-Stärke-Bewertung

Die Stärke basiert auf mehreren Faktoren:

#### Länge (max. 30 Punkte)
- < 8 Zeichen: 0 Punkte (Warnung)
- 8-11 Zeichen: 10 Punkte
- 12-15 Zeichen: 20 Punkte
- 16+ Zeichen: 30 Punkte
- 20+ Zeichen: +5 Bonus

#### Zeichenvielfalt (max. 30 Punkte)
- 1 Typ (nur Kleinbuchstaben): 0 Punkte
- 2 Typen: 10 Punkte
- 3 Typen: 20 Punkte
- 4 Typen (alle): 30 Punkte

#### Entropie (max. 25 Punkte)
- < 28 bits: 0 Punkte (kritisch)
- 28-35 bits: 5 Punkte
- 36-59 bits: 15 Punkte
- 60+ bits: 25 Punkte

#### Einzigartigkeit (max. 10 Punkte)
- > 80% einzigartige Zeichen: +10 Punkte
- < 50% einzigartige Zeichen: -5 Punkte

#### Abzüge
- Häufiges Passwort: -30 Punkte
- Sequenzielle Zeichen: -10 Punkte
- Wiederholte Zeichen: -10 Punkte
- Gängige Wörter: -15 Punkte

### Entropie-Berechnung

```
Entropie = Länge × log₂(Zeichensatz-Größe)
```

**Zeichensatz-Größen**:
- Kleinbuchstaben: 26
- Großbuchstaben: 26
- Zahlen: 10
- Sonderzeichen: 32

**Beispiel**:
```
Passwort: "Abc123!@#" (9 Zeichen)
Zeichensatz: 26 + 26 + 10 + 32 = 94
Entropie: 9 × log₂(94) = 9 × 6.55 ≈ 59 bits
```

### Crack-Zeit-Schätzung

Annahme: **10 Milliarden Versuche/Sekunde** (moderne GPU)

```
Kombinationen = 2^Entropie
Zeit = Kombinationen / (2 × 10^10)  # Average case
```

**Beispiele**:

| Entropie | Kombinationen | Crack-Zeit |
|----------|---------------|------------|
| 28 bits | 268 Millionen | Sekunden |
| 36 bits | 69 Milliarden | Minuten |
| 60 bits | 1,15 Quintillion | Jahrtausende |
| 80 bits | 1,2 Septillion | Ewigkeit |

## 🎨 Technologie-Stack

### Backend
- **Flask**: Leichtgewichtiges Python Web-Framework
- **Python 3.8+**: Moderne Python-Features
- **requests**: HTTP-Library für Breach-Check
- **hashlib**: Kryptografische Hash-Funktionen (SHA-1)

### Frontend
- **Vanilla JavaScript**: Kein Framework-Overhead, pure Performance
- **CSS3**: Modernes Design mit Gradients & Animationen
- **Responsive Design**: Funktioniert auf allen Geräten
- **Dark Theme**: Angenehm für die Augen

### APIs
- **Have I Been Pwned API**: Passwort-Leak-Datenbank
- **RESTful API**: Eigene Backend-Endpunkte

## 📁 Projektstruktur

```
password-security-suite/
├── backend.py              # Flask Backend-Server
├── index.html              # Haupt-HTML-Datei
├── styles.css              # CSS-Styling
├── app.js                  # Frontend-Logik
├── requirements.txt        # Python-Abhängigkeiten
└── README.md              # Diese Datei
```

## 🔧 API-Endpunkte

### POST `/api/generate/password`
Generiert ein zufälliges Passwort.

**Request**:
```json
{
  "length": 16,
  "use_uppercase": true,
  "use_lowercase": true,
  "use_digits": true,
  "use_symbols": true,
  "exclude_ambiguous": false,
  "custom_chars": ""
}
```

**Response**:
```json
{
  "password": "Xy7!mK9@pLq3#Zw8",
  "strength": {
    "score": 85,
    "strength": "Very Strong",
    "feedback": ["Excellent password!"],
    "details": { ... }
  }
}
```

### POST `/api/generate/passphrase`
Generiert eine merkbare Passphrase.

**Request**:
```json
{
  "num_words": 4,
  "separator": "-",
  "capitalize": true,
  "add_number": true
}
```

**Response**:
```json
{
  "passphrase": "Dragon-Galaxy-Thunder-Nebula-5829",
  "strength": { ... }
}
```

### POST `/api/check/strength`
Analysiert Passwort-Stärke.

**Request**:
```json
{
  "password": "MyPassword123"
}
```

**Response**:
```json
{
  "score": 45,
  "strength": "Fair",
  "feedback": [
    "Consider using at least 12 characters",
    "Add symbols for better security"
  ],
  "details": {
    "length": 13,
    "entropy": 65.2,
    "crack_time": "52 years",
    "has_lowercase": true,
    "has_uppercase": true,
    "has_digits": true,
    "has_symbols": false,
    ...
  }
}
```

### POST `/api/check/breach`
Prüft Passwort gegen Leak-Datenbank.

**Request**:
```json
{
  "password": "password123"
}
```

**Response**:
```json
{
  "breached": true,
  "count": 2458631,
  "message": "⚠️ This password has been exposed 2458631 times in data breaches!"
}
```

## 💡 Tipps für sichere Passwörter

### ✅ DO
- **Mindestens 12 Zeichen** (besser 16+)
- **Alle Zeichentypen** nutzen (A-Z, a-z, 0-9, !@#$)
- **Einzigartig** für jeden Dienst
- **Passphrasen** für leicht merkbare Passwörter
- **Password Manager** verwenden
- **2FA aktivieren** wo möglich

### ❌ DON'T
- Keine persönlichen Infos (Name, Geburtstag)
- Keine Wörter aus dem Wörterbuch
- Keine einfachen Muster (qwerty, 123456)
- Passwörter nicht wiederverwenden
- Passwörter nicht teilen
- Passwörter nicht in Klartext speichern

### 🎯 Passphrase vs. Passwort

**Passwort**: `Xy7!mK9@pLq3`
- ✅ Sehr sicher
- ❌ Schwer zu merken
- ❌ Tippfehler-anfällig

**Passphrase**: `Correct-Horse-Battery-Staple-4892`
- ✅ Sehr sicher (Länge!)
- ✅ Leicht zu merken
- ✅ Weniger Tippfehler

→ **Für Login-Passwörter: Passphrasen bevorzugen!**

## 🐛 Troubleshooting

### Server startet nicht
```bash
# Prüfe ob Port 5000 bereits belegt ist
lsof -i :5000

# Oder starte auf anderem Port
export FLASK_RUN_PORT=8080
python backend.py
```

### "Module not found" Fehler
```bash
# Installiere Abhängigkeiten erneut
pip install -r requirements.txt

# Oder mit explizitem Python3
python3 -m pip install -r requirements.txt
```

### Breach Check funktioniert nicht
- **Internetverbindung prüfen**: API erfordert Online-Zugang
- **Firewall**: Stelle sicher, dass `api.pwnedpasswords.com` erreichbar ist
- **Timeout erhöhen**: Bei langsamer Verbindung

## 🚀 Erweiterungen & Ideen

Mögliche zukünftige Features:

- [ ] **Passwort-Manager**: Verschlüsselte Speicherung von Passwörtern
- [ ] **Passwort-Historie**: Verlauf generierter Passwörter (lokal)
- [ ] **QR-Code**: Passwörter als QR-Code für Mobile
- [ ] **Bulk-Generierung**: Mehrere Passwörter auf einmal
- [ ] **Export-Funktion**: Als CSV/JSON exportieren
- [ ] **Sprach-Optionen**: Englisch, Französisch, Spanisch
- [ ] **Themes**: Light Mode, Custom Colors
- [ ] **Offline-Modus**: Progressive Web App (PWA)
- [ ] **Browser-Extension**: Als Chrome/Firefox Extension
- [ ] **CLI-Version**: Terminal-Interface

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe LICENSE-Datei für Details.

## 🙏 Credits

- **Have I Been Pwned API**: Troy Hunt ([@troyhunt](https://twitter.com/troyhunt))
- **Wordlist**: Kuratierte Liste häufiger englischer Wörter
- **Icons**: Unicode Emojis

## 📞 Support

Bei Fragen oder Problemen:
- 📧 Email: [deine-email@example.com]
- 🐛 Issues: [GitHub Issues](link-to-issues)
- 💬 Diskussionen: [GitHub Discussions](link-to-discussions)

---

**Made with ❤️ for Security**

*Deine Passwörter bleiben privat und sicher. Immer.*
