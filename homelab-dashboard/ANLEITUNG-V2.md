# 🏠 Homelab Dashboard V2 - Vollständige Anleitung

**Version 2.0** mit Backend, Authentifizierung und erweiterten Features!

---

## 🎉 Neue Features in Version 2.0

### ✨ Alle gewünschten Features sind jetzt implementiert:

✅ **Service-Status-Check (ping)** - Prüfe ob deine Services erreichbar sind
✅ **Drag & Drop zum Sortieren** - Ziehe Services per Drag & Drop um
✅ **Gruppen/Ordner für Services** - Organisiere Services in Gruppen
✅ **Custom Themes** - Erstelle eigene Farbthemes
✅ **Service-Notizen** - Füge Notizen zu Services hinzu
✅ **Favoriten/Sterne** - Markiere wichtige Services
✅ **Service-Tags** - Tagge Services für bessere Organisation

### 🔒 Sicherheit & Backend:

✅ **Login-System** - Passwortgeschützter Zugriff
✅ **Serverseitige Speicherung** - Daten in SQLite-Datenbank
✅ **Session-Management** - Bleibe 7 Tage eingeloggt
✅ **Passwort ändern** - Ändere dein Passwort im Dashboard

---

## 📋 Inhaltsverzeichnis

1. [Installation & Setup](#installation--setup)
2. [Erster Start](#erster-start)
3. [Login](#login)
4. [Dashboard-Übersicht](#dashboard-übersicht)
5. [Services verwalten](#services-verwalten)
6. [Status-Checks](#status-checks)
7. [Favoriten](#favoriten)
8. [Notizen](#notizen)
9. [Tags](#tags)
10. [Gruppen/Ordner](#gruppenordner)
11. [Drag & Drop Sortierung](#drag--drop-sortierung)
12. [Custom Themes](#custom-themes)
13. [Import/Export](#importexport)
14. [Passwort ändern](#passwort-ändern)
15. [Fehlerbehebung](#fehlerbehebung)

---

## 🚀 Installation & Setup

### Voraussetzungen

- **Python 3.7+** installiert
- **pip3** installiert

### Schritt 1: Dependencies installieren

```bash
cd homelab-dashboard
pip3 install -r requirements.txt
```

Falls Fehler auftreten:
```bash
sudo pip3 install -r requirements.txt
```

### Schritt 2: Backend starten

**Mit Start-Skript (empfohlen):**
```bash
./start.sh
```

**Manuell:**
```bash
python3 backend.py
```

### Schritt 3: Dashboard öffnen

Öffne im Browser:
```
http://localhost:5000
```

---

## 🔐 Erster Start

### Standard-Zugangsdaten

Beim ersten Start werden diese Zugangsdaten erstellt:

```
Benutzername: admin
Passwort: homelab2025
```

⚠️ **WICHTIG**: Ändere das Passwort sofort nach dem ersten Login!

### Was passiert beim ersten Start?

1. Datenbank wird erstellt (`homelab.db`)
2. Tabellen werden angelegt
3. Standard-User wird erstellt
4. Backend startet auf Port 5000

---

## 🔑 Login

### Login-Seite

1. Öffne `http://localhost:5000`
2. Du wirst zur Login-Seite umgeleitet
3. Gib Benutzername und Passwort ein
4. Optional: "Angemeldet bleiben" aktivieren (7 Tage)
5. Klicke auf "Anmelden"

### Session

- Session bleibt 7 Tage aktiv
- Bei Inaktivität automatischer Logout
- Logout über Button oben rechts

---

## 📊 Dashboard-Übersicht

### Header-Bereich

- **Dashboard-Titel** - Anpassbar in index.html
- **Theme-Toggle** - Wechsel zwischen Light/Dark Mode (oben rechts)
- **Logout-Button** - Abmelden (oben rechts)

### Quick Stats

Drei Informations-Karten zeigen:

1. **Services Online** - Anzahl konfigurierter Services
2. **Services Status** - Online/Gesamt (z.B. "8/10")
3. **Aktuelle Zeit** - Live-Uhr
4. **Session Uptime** - Wie lange läuft deine Session

### Suchleiste

- Echtzeitsuche durch Services
- Durchsucht Name und Beschreibung
- Tastatur-Shortcut: `Strg/Cmd + K`

### Filter-Buttons

**Kategorien:**
- Alle
- Media
- Automation
- Netzwerk
- Monitoring
- Storage
- Sonstiges
- **NEU: Favoriten** - Zeigt nur favorisierte Services

**NEU: Gruppen-Filter** (wenn Gruppen erstellt)
- Zeigt Services einer bestimmten Gruppe

### Services Grid

- Service-Karten in responsivem Grid
- **NEU: Status-Indikator** - Grün (online), Rot (offline), Grau (unbekannt)
- **NEU: Favoriten-Stern** - Gelber Stern für Favoriten
- **NEU: Drag & Drop** - Services können verschoben werden

### Floating Action Button (+)

Unten rechts - Öffnet Dialog zum Hinzufügen neuer Services

---

## 📝 Services verwalten

### Service hinzufügen

1. Klicke auf **+ Button** (unten rechts)
2. Fülle Formular aus:

   **Pflichtfelder:**
   - **Name*** - Service-Name (z.B. "Plex")
   - **URL*** - Vollständige URL (z.B. `http://192.168.1.100:32400`)
   - **Kategorie*** - Media, Automation, etc.

   **Optionale Felder:**
   - **Beschreibung** - Kurzbeschreibung
   - **Icon** - Font Awesome Icon-Name (z.B. `fa-play`)
   - **Farbe** - Blau, Grün, Lila, Orange, Rot, Türkis
   - **NEU: Notizen** - Persönliche Notizen zum Service
   - **NEU: Gruppe** - Ordne Service einer Gruppe zu

3. Klicke auf **"Speichern"**

### Service bearbeiten

1. Klicke auf **Stift-Symbol** auf der Service-Karte
2. Bearbeite Felder
3. Klicke auf **"Speichern"**

### Service löschen

1. Öffne Bearbeiten-Dialog
2. Klicke auf **"Löschen"** (roter Button unten links)
3. Bestätige Löschung

### Service öffnen

Klicke einfach auf die Service-Karte → Öffnet in neuem Tab

---

## 🔍 Status-Checks

### ⭐ NEUES FEATURE: Service-Status prüfen

Das Dashboard kann jetzt automatisch prüfen, ob deine Services erreichbar sind!

### Einzelnen Service prüfen

1. Klicke auf **Sync-Symbol** (🔄) auf der Service-Karte
2. Status wird geprüft
3. **Status-Indikator** wird aktualisiert:
   - 🟢 **Grün** = Online (zeigt Response-Zeit)
   - 🔴 **Rot** = Offline
   - ⚫ **Grau** = Unbekannt

### Alle Services prüfen

1. Klicke auf **"Alle Status prüfen"** Button (oben)
2. Alle Services werden nacheinander geprüft
3. Dauert ca. 1-3 Sekunden pro Service

### Automatische Status-Checks

- Status wird **alle 5 Minuten** automatisch geprüft
- Kann in `app-v2.js` angepasst werden

### Wie funktioniert der Status-Check?

- Verwendet Socket-Verbindung zum Host
- Prüft Port-Erreichbarkeit
- Misst Response-Zeit in Millisekunden
- Speichert Ergebnis in Datenbank

---

## ⭐ Favoriten

### ⭐ NEUES FEATURE: Services als Favoriten markieren

Markiere wichtige Services für schnellen Zugriff!

### Service zu Favoriten hinzufügen

1. Klicke auf **Stern-Symbol** (☆) auf der Service-Karte
2. Stern wird gelb gefüllt (★)
3. Service ist jetzt Favorit

### Service aus Favoriten entfernen

1. Klicke erneut auf **gelben Stern** (★)
2. Stern wird leer (☆)
3. Service ist kein Favorit mehr

### Nur Favoriten anzeigen

1. Klicke auf Filter-Button **"Favoriten"**
2. Nur favorisierte Services werden angezeigt

---

## 📝 Notizen

### ⭐ NEUES FEATURE: Notizen zu Services

Füge persönliche Notizen zu jedem Service hinzu!

### Notiz hinzufügen

1. **Beim Erstellen:** Fülle Feld "Notizen" aus
2. **Beim Bearbeiten:** Öffne Service → Feld "Notizen" → Speichern

### Notizen anzeigen

- Notizen werden unter der Beschreibung angezeigt
- Icon: 📝 (Sticky Note)
- Nur wenn Notiz vorhanden

### Verwendungsbeispiele

- **Zugangsdaten**: "Admin-Login: user123"
- **Wartung**: "Letzte Wartung: 2025-12-20"
- **Hinweise**: "Benötigt VPN-Verbindung"
- **Probleme**: "Port-Weiterleitung auf Router nötig"

---

## 🏷️ Tags

### ⭐ NEUES FEATURE: Service-Tags

Organisiere Services mit Tags!

### Tag erstellen

```javascript
// Aktuell über API oder Datenbank
// UI folgt in zukünftigem Update
```

### Tag zu Service hinzufügen

```javascript
// Über API:
POST /api/services/{service_id}/tags
{
  "tag_id": 1
}
```

### Tag-Beispiele

- `wichtig`
- `extern-erreichbar`
- `docker`
- `vm`
- `beta`
- `produktiv`

---

## 📁 Gruppen/Ordner

### ⭐ NEUES FEATURE: Organisiere Services in Gruppen

Erstelle Ordner für bessere Organisation!

### Gruppe erstellen

**Über API:**
```bash
curl -X POST http://localhost:5000/api/groups \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Media Server",
    "icon": "fa-film",
    "color": "purple"
  }'
```

**Oder über Python:**
```python
import requests
requests.post('http://localhost:5000/api/groups',
  json={"name": "Media Server", "icon": "fa-film", "color": "purple"})
```

### Service zu Gruppe zuweisen

1. Öffne Service bearbeiten
2. Wähle Gruppe im Dropdown "Gruppe"
3. Speichern

### Gruppen filtern

- Gruppen erscheinen als Filter-Buttons
- Klicke auf Gruppen-Button zum Filtern

### Gruppen-Beispiele

- **Media Server** (Plex, Jellyfin, Sonarr, Radarr)
- **Netzwerk** (Pi-hole, Unifi, Nginx)
- **Monitoring** (Grafana, Prometheus, Uptime Kuma)
- **Docker** (Portainer, Yacht, etc.)

---

## 🎯 Drag & Drop Sortierung

### ⭐ NEUES FEATURE: Services per Drag & Drop sortieren

Ordne Services nach deinen Wünschen an!

### Services sortieren

1. **Klicke und halte** eine Service-Karte
2. **Ziehe** die Karte an die gewünschte Position
3. **Loslassen** - Neue Reihenfolge wird gespeichert

### Tipps

- Funktioniert auf Desktop und Tablet
- Sortierung wird in Datenbank gespeichert
- Bleibt nach Reload erhalten
- Sortierung gilt pro Ansicht (Filter beachten)

---

## 🎨 Custom Themes

### ⭐ NEUES FEATURE: Erstelle eigene Farbthemes

Passe das Dashboard an deine Vorlieben an!

### Theme erstellen

**Über API:**
```bash
curl -X POST http://localhost:5000/api/themes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ocean Blue",
    "colors": {
      "primary": "#0077be",
      "secondary": "#00a8e8",
      "accent": "#00d4ff"
    }
  }'
```

### Theme aktivieren

```bash
curl -X POST http://localhost:5000/api/themes/1/activate
```

### Standard-Themes

- **Light Mode** - Heller, freundlicher Look
- **Dark Mode** - Dunkler, augenfreundlicher Look

### Theme-Variablen

Bearbeite `styles.css` um Farben anzupassen:

```css
:root {
    --color-blue: #3498db;
    --color-green: #2ecc71;
    /* ... weitere Farben ... */
}
```

---

## 💾 Import/Export

### Konfiguration exportieren

1. Footer → **"Konfiguration exportieren"**
2. JSON-Datei wird heruntergeladen
3. **NEU**: Enthält jetzt auch Gruppen und Tags

### Konfiguration importieren

1. Footer → **"Konfiguration importieren"**
2. JSON-Datei auswählen
3. Bestätigen
4. **Warnung**: Ersetzt alle aktuellen Daten!

### Export-Format V2.0

```json
{
  "version": "2.0",
  "exportDate": "2025-12-26T...",
  "services": [...],
  "groups": [...],
  "tags": [...]
}
```

---

## 🔐 Passwort ändern

### ⭐ NEUES FEATURE: Passwort sicher ändern

Ändere dein Passwort regelmäßig für mehr Sicherheit!

### Passwort ändern über API

```bash
curl -X POST http://localhost:5000/api/auth/change-password \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "homelab2025",
    "new_password": "mein-neues-passwort"
  }'
```

### Passwort-Richtlinien

✅ Mindestens 8 Zeichen empfohlen
✅ Kombination aus Buchstaben und Zahlen
✅ Sonderzeichen für höhere Sicherheit
✅ Nicht das Standard-Passwort verwenden!

---

## 🔧 Fehlerbehebung

### Backend startet nicht

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Lösung:**
```bash
pip3 install -r requirements.txt
# oder
sudo pip3 install -r requirements.txt
```

---

### Login funktioniert nicht

**Problem**: "Verbindung zum Server fehlgeschlagen"

**Lösung:**
1. Prüfe ob Backend läuft: `http://localhost:5000`
2. Prüfe Terminal-Ausgabe auf Fehler
3. Starte Backend neu: `./start.sh`

---

### Status-Check funktioniert nicht

**Problem**: Alle Services zeigen "Offline" obwohl online

**Lösung:**
1. Prüfe ob URLs korrekt sind
2. Prüfe Firewall-Einstellungen
3. Manche Services blockieren Status-Checks
4. Verwende lokale IP statt Hostname

---

### Drag & Drop funktioniert nicht

**Problem**: Services lassen sich nicht verschieben

**Lösung:**
1. Aktualisiere Browser (Chrome/Firefox empfohlen)
2. Deaktiviere Browser-Erweiterungen
3. Prüfe JavaScript-Konsole (F12) auf Fehler

---

### Services verschwinden nach Neustart

**Problem**: Services sind nach Neustart weg

**Lösung:**
1. **NICHT** mehr möglich - Daten sind in Datenbank!
2. Exportiere regelmäßig als Backup
3. Prüfe ob `homelab.db` existiert

---

## 📊 API-Referenz

### Authentifizierung

```bash
# Login
POST /api/auth/login
{
  "username": "admin",
  "password": "homelab2025"
}

# Logout
POST /api/auth/logout

# Status prüfen
GET /api/auth/check

# Passwort ändern
POST /api/auth/change-password
{
  "old_password": "...",
  "new_password": "..."
}
```

### Services

```bash
# Alle Services
GET /api/services

# Service hinzufügen
POST /api/services
{
  "id": "...",
  "name": "Plex",
  "url": "http://...",
  ...
}

# Service aktualisieren
PUT /api/services/{id}
{
  "name": "Plex Media Server",
  ...
}

# Service löschen
DELETE /api/services/{id}

# Favorit umschalten
POST /api/services/{id}/favorite
{
  "is_favorite": 1
}

# Status prüfen
POST /api/services/{id}/check-status

# Alle Status prüfen
POST /api/services/check-all-status

# Services neu sortieren
POST /api/services/reorder
{
  "order": ["id1", "id2", "id3"]
}
```

### Gruppen

```bash
# Alle Gruppen
GET /api/groups

# Gruppe hinzufügen
POST /api/groups
{
  "name": "Media Server",
  "icon": "fa-film",
  "color": "purple"
}

# Gruppe aktualisieren
PUT /api/groups/{id}

# Gruppe löschen
DELETE /api/groups/{id}
```

### Tags

```bash
# Alle Tags
GET /api/tags

# Tag hinzufügen
POST /api/tags
{
  "name": "wichtig",
  "color": "red"
}

# Tag zu Service hinzufügen
POST /api/services/{service_id}/tags
{
  "tag_id": 1
}

# Tag von Service entfernen
DELETE /api/services/{service_id}/tags/{tag_id}
```

---

## 🚀 Produktiv-Deployment

### Mit Nginx (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name homelab.local;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Mit systemd (Auto-Start)

Erstelle `/etc/systemd/system/homelab-dashboard.service`:

```ini
[Unit]
Description=Homelab Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/homelab-dashboard
ExecStart=/usr/bin/python3 backend.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Aktivieren:
```bash
sudo systemctl enable homelab-dashboard
sudo systemctl start homelab-dashboard
```

---

## 📝 Changelog V2.0

### ✨ Neue Features

- ✅ Backend mit Flask und SQLite
- ✅ Login-System mit Session-Management
- ✅ Service-Status-Checks
- ✅ Drag & Drop Sortierung
- ✅ Gruppen/Ordner für Services
- ✅ Service-Notizen
- ✅ Favoriten-System
- ✅ Service-Tags
- ✅ Custom Themes (API)
- ✅ Verbesserte Import/Export-Funktion

### 🔧 Verbesserungen

- Serverseitige Datenspeicherung
- Schnellere Ladezeiten
- Bessere Fehlerbehandlung
- API-First Design
- Session-basierte Authentifizierung

---

## 📞 Support

### Logs prüfen

**Backend-Logs:**
```bash
# Im Terminal wo backend.py läuft
# Alle Requests und Fehler werden angezeigt
```

**Browser-Konsole:**
```
F12 → Console
# JavaScript-Fehler werden hier angezeigt
```

### Datenbank zurücksetzen

```bash
# Vorsicht: Löscht ALLE Daten!
rm homelab.db
python3 backend.py
# Neue DB wird mit Standard-Zugangsdaten erstellt
```

---

## 🎉 Viel Erfolg mit Version 2.0!

Alle gewünschten Features sind jetzt implementiert:

✅ Service-Status-Check (ping)
✅ Drag & Drop zum Sortieren
✅ Gruppen/Ordner für Services
✅ Custom Themes
✅ Service-Notizen
✅ Favoriten/Sterne
✅ Service-Tags

Plus:
✅ Backend mit Datenbank
✅ Login-System
✅ Serverseitige Speicherung

**Viel Spaß mit deinem erweiterten Homelab Dashboard! 🚀**
