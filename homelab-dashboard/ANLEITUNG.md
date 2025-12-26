# 🏠 Homelab Dashboard - Anleitung

Willkommen zu deinem persönlichen Homelab Dashboard! Diese Anleitung zeigt dir, wie du das Dashboard einrichtest, verwendest und anpasst.

---

## 📋 Inhaltsverzeichnis

1. [Installation](#installation)
2. [Erste Schritte](#erste-schritte)
3. [Services hinzufügen](#services-hinzufügen)
4. [Services bearbeiten und löschen](#services-bearbeiten-und-löschen)
5. [Kategorien und Filter](#kategorien-und-filter)
6. [Suche verwenden](#suche-verwenden)
7. [Dark Mode](#dark-mode)
8. [Konfiguration exportieren/importieren](#konfiguration-exportierenimportieren)
9. [Anpassung und Styling](#anpassung-und-styling)
10. [Tipps und Tricks](#tipps-und-tricks)
11. [Fehlerbehebung](#fehlerbehebung)

---

## 🚀 Installation

### Methode 1: Lokaler Webserver (Empfohlen)

**Mit Python:**
```bash
cd homelab-dashboard
python3 -m http.server 8000
```

Dann öffne im Browser: `http://localhost:8000`

**Mit Node.js (http-server):**
```bash
npm install -g http-server
cd homelab-dashboard
http-server -p 8000
```

**Mit PHP:**
```bash
cd homelab-dashboard
php -S localhost:8000
```

### Methode 2: Nginx/Apache

Kopiere den `homelab-dashboard` Ordner in dein Webserver-Verzeichnis:

**Nginx:**
```bash
sudo cp -r homelab-dashboard /var/www/html/
```

**Apache:**
```bash
sudo cp -r homelab-dashboard /var/www/html/
```

Dann öffne: `http://deine-server-ip/homelab-dashboard`

### Methode 3: Docker

Erstelle eine `Dockerfile`:
```dockerfile
FROM nginx:alpine
COPY homelab-dashboard/ /usr/share/nginx/html/
EXPOSE 80
```

Bauen und starten:
```bash
docker build -t homelab-dashboard .
docker run -d -p 8080:80 homelab-dashboard
```

---

## 🎯 Erste Schritte

### 1. Dashboard öffnen

Nach der Installation öffnest du das Dashboard in deinem Browser. Du siehst:

- **Header**: Titel und Untertitel
- **Quick Stats**: Services Online, Aktuelle Zeit, Session Uptime
- **Suchleiste**: Zum Durchsuchen deiner Services
- **Kategorie-Filter**: Zum Filtern nach Kategorien
- **Services Grid**: Deine Service-Karten
- **+ Button**: Zum Hinzufügen neuer Services (unten rechts)

### 2. Beispiel-Service

Beim ersten Start siehst du einen Beispiel-Service. Dieser zeigt dir, wie Service-Karten aussehen.

### 3. Erste Konfiguration

Klicke auf das **Bearbeiten-Symbol** (Stift) beim Beispiel-Service, um ihn an deine Bedürfnisse anzupassen.

---

## ➕ Services hinzufügen

### Schritt-für-Schritt Anleitung:

1. **Klicke auf den + Button** (unten rechts)
2. **Fülle das Formular aus:**

   **Name*** (Pflichtfeld)
   - Der Name deines Services
   - Beispiel: "Plex", "Nextcloud", "Pi-hole"

   **Beschreibung**
   - Kurze Beschreibung was der Service macht
   - Beispiel: "Media Server", "Cloud Storage"

   **URL*** (Pflichtfeld)
   - Die vollständige URL zu deinem Service
   - Format: `http://` oder `https://`
   - Beispiel: `http://192.168.1.100:32400`

   **Icon**
   - Font Awesome Icon-Name (ohne "fa-")
   - Beispiel: `play`, `cloud`, `home`, `server`
   - Komplette Liste: https://fontawesome.com/icons

   **Kategorie*** (Pflichtfeld)
   - Wähle aus: Media, Automation, Netzwerk, Monitoring, Storage, Sonstiges

   **Farbe**
   - Wähle eine Farbe für die Service-Karte
   - Verfügbar: Blau, Grün, Lila, Orange, Rot, Türkis

3. **Klicke auf "Speichern"**

### Beispiele für beliebte Services:

#### Plex Media Server
- **Name**: Plex
- **Beschreibung**: Streaming von Filmen und Serien
- **URL**: `http://192.168.1.100:32400`
- **Icon**: `fa-play`
- **Kategorie**: Media
- **Farbe**: Orange

#### Nextcloud
- **Name**: Nextcloud
- **Beschreibung**: Private Cloud Storage
- **URL**: `http://192.168.1.100:8080`
- **Icon**: `fa-cloud`
- **Kategorie**: Storage
- **Farbe**: Blau

#### Pi-hole
- **Name**: Pi-hole
- **Beschreibung**: Netzwerk-weiter Ad-Blocker
- **URL**: `http://192.168.1.100/admin`
- **Icon**: `fa-shield-alt`
- **Kategorie**: Netzwerk
- **Farbe**: Rot

#### Home Assistant
- **Name**: Home Assistant
- **Beschreibung**: Smart Home Steuerung
- **URL**: `http://192.168.1.100:8123`
- **Icon**: `fa-home`
- **Kategorie**: Automation
- **Farbe**: Lila

---

## ✏️ Services bearbeiten und löschen

### Service bearbeiten:

1. **Klicke auf das Stift-Symbol** auf der Service-Karte
2. **Bearbeite die Felder** nach Bedarf
3. **Klicke auf "Speichern"**

### Service löschen:

1. **Klicke auf das Stift-Symbol** auf der Service-Karte
2. **Klicke auf "Löschen"** (roter Button unten links)
3. **Bestätige die Löschung**

### Service öffnen:

**Klicke einfach irgendwo auf die Service-Karte** (außer auf den Stift), um den Service in einem neuen Tab zu öffnen.

---

## 🏷️ Kategorien und Filter

### Verfügbare Kategorien:

- **Alle**: Zeigt alle Services
- **Media**: Plex, Jellyfin, Sonarr, Radarr, etc.
- **Automation**: Home Assistant, Node-RED, etc.
- **Netzwerk**: Pi-hole, Unifi, Nginx Proxy Manager, etc.
- **Monitoring**: Grafana, Prometheus, Uptime Kuma, etc.
- **Storage**: Nextcloud, Synology, TrueNAS, etc.
- **Sonstiges**: Alle anderen Services

### Filter verwenden:

Klicke einfach auf einen der **Kategorie-Buttons** oberhalb der Service-Karten. Der aktive Filter wird blau hervorgehoben.

---

## 🔍 Suche verwenden

### So funktioniert die Suche:

1. **Klicke in die Suchleiste** oder drücke `Strg + K` (bzw. `Cmd + K` auf Mac)
2. **Tippe einen Suchbegriff** ein
3. Die Services werden **sofort gefiltert**

Die Suche durchsucht:
- Service-Namen
- Beschreibungen

### Beispiele:

- Suche nach "media" → Zeigt alle Media-Services
- Suche nach "192.168.1.100" → Zeigt alle Services auf dieser IP
- Suche nach "cloud" → Findet Nextcloud, etc.

---

## 🌙 Dark Mode

### Dark Mode aktivieren/deaktivieren:

**Klicke auf den Mond/Sonne Button** oben rechts

- 🌙 **Mond-Symbol**: Aktiviert Dark Mode
- ☀️ **Sonnen-Symbol**: Aktiviert Light Mode

Deine Einstellung wird **automatisch gespeichert** und beim nächsten Besuch wiederhergestellt.

---

## 💾 Konfiguration exportieren/importieren

### Warum exportieren/importieren?

- **Backup**: Sichere deine Service-Konfiguration
- **Migration**: Übertrage deine Services auf ein anderes Gerät
- **Teilen**: Teile deine Konfiguration mit anderen

### Konfiguration exportieren:

1. **Scrolle nach unten** zum Footer
2. **Klicke auf "Konfiguration exportieren"**
3. Eine JSON-Datei wird **automatisch heruntergeladen**
4. Dateiname: `homelab-config-[timestamp].json`

### Konfiguration importieren:

1. **Scrolle nach unten** zum Footer
2. **Klicke auf "Konfiguration importieren"**
3. **Wähle eine JSON-Datei** aus
4. **Bestätige** dass du die aktuellen Services ersetzen möchtest
5. Deine Services werden **sofort aktualisiert**

### Beispiel-Konfiguration verwenden:

Eine Beispiel-Konfiguration mit vielen beliebten Homelab-Services findest du in `example-config.json`.

So importierst du sie:
1. Klicke auf "Konfiguration importieren"
2. Wähle `example-config.json`
3. Bestätige
4. Passe die URLs an deine IP-Adressen an

---

## 🎨 Anpassung und Styling

### Dashboard-Titel ändern:

Bearbeite `index.html`:
```html
<h1><i class="fas fa-server"></i> Dein Custom Titel</h1>
<p class="subtitle">Dein Custom Untertitel</p>
```

### Farben anpassen:

Bearbeite `styles.css` - Abschnitt "CSS Variables":

```css
:root {
    --color-blue: #3498db;     /* Deine Farbe */
    --color-green: #2ecc71;    /* Deine Farbe */
    /* ... etc ... */
}
```

### Neue Kategorie hinzufügen:

1. **In `index.html`** - Füge neuen Filter-Button hinzu:
```html
<button class="filter-btn" data-category="neuekategorie">
    <i class="fas fa-icon"></i> Neue Kategorie
</button>
```

2. **In `app.js`** - Füge Kategorie-Namen hinzu:
```javascript
getCategoryName(category) {
    const names = {
        // ... bestehende ...
        neuekategorie: 'Neue Kategorie'
    };
    return names[category] || category;
}
```

3. **In beiden Modals** (`index.html`) - Füge Option hinzu:
```html
<option value="neuekategorie">Neue Kategorie</option>
```

---

## 💡 Tipps und Tricks

### 🎯 Tastatur-Shortcuts

- **`Strg/Cmd + K`**: Fokussiert die Suchleiste
- **`Escape`**: Schließt geöffnete Modals

### 🔗 Service-URLs

**Lokale IPs:**
- Format: `http://192.168.1.100:8080`
- Kein Trailing Slash nötig

**Hostnamen:**
- Format: `http://server.local:8080`
- Funktioniert wenn DNS/Hosts-Datei konfiguriert

**HTTPS:**
- Auch möglich: `https://domain.com`

### 🎨 Icons finden

Besuche https://fontawesome.com/icons und suche nach Icons.

**Beispiele:**
- Server: `fa-server`
- Cloud: `fa-cloud`
- Home: `fa-home`
- Shield: `fa-shield-alt`
- Chart: `fa-chart-line`
- Docker: `fa-docker`

**Tipp**: Verwende nur den Teil **nach** "fa-"

### 📱 Mobile Nutzung

Das Dashboard ist **voll responsive**:
- Automatische Anpassung auf Tablets und Smartphones
- Touch-freundliche Buttons
- Scrollbare Filter

### 🔄 Automatisches Speichern

Alle Änderungen werden **automatisch im Browser gespeichert** (LocalStorage).

**Wichtig:**
- Daten sind **pro Browser** gespeichert
- Bei Browser-Cache-Löschung gehen Daten verloren
- **Regelmäßig exportieren** für Backups!

---

## 🔧 Fehlerbehebung

### Services werden nicht angezeigt

**Ursache**: LocalStorage könnte leer sein
**Lösung**:
1. Importiere die `example-config.json`
2. Oder füge manuell Services hinzu

### Icons werden nicht angezeigt

**Ursache**: Font Awesome CDN nicht erreichbar
**Lösung**:
1. Prüfe Internet-Verbindung
2. Oder lade Font Awesome lokal herunter

### Dark Mode funktioniert nicht

**Ursache**: JavaScript-Fehler oder LocalStorage-Problem
**Lösung**:
1. Öffne Browser-Konsole (F12)
2. Lösche LocalStorage: `localStorage.clear()`
3. Lade Seite neu

### Service öffnet nicht beim Klick

**Ursache**: URL falsch formatiert
**Lösung**:
1. URL muss mit `http://` oder `https://` beginnen
2. Beispiel: `http://192.168.1.100:8080`

### Konfiguration-Import schlägt fehl

**Ursache**: Ungültige JSON-Datei
**Lösung**:
1. Prüfe JSON-Syntax
2. Vergleiche mit `example-config.json`
3. Nutze JSON-Validator online

### Änderungen gehen verloren

**Ursache**: Browser-Cache wurde gelöscht
**Lösung**:
- **Wichtig**: Exportiere regelmäßig deine Konfiguration!
- Erstelle Backups der JSON-Dateien

---

## 📦 Datei-Struktur

```
homelab-dashboard/
├── index.html           # Haupt-HTML-Datei
├── styles.css           # Alle Styles (Light & Dark Mode)
├── app.js              # JavaScript-Logik
├── example-config.json # Beispiel-Konfiguration
└── ANLEITUNG.md        # Diese Anleitung
```

---

## 🌐 Browser-Kompatibilität

✅ **Getestet und funktioniert in:**
- Chrome/Chromium (Version 90+)
- Firefox (Version 88+)
- Safari (Version 14+)
- Edge (Version 90+)

---

## 🚀 Erweiterte Nutzung

### Als Standard-Tab im Browser setzen

**Chrome/Edge:**
1. Einstellungen → Beim Start
2. "Bestimmte Seite oder Seiten öffnen"
3. Füge URL hinzu: `http://localhost:8000`

**Firefox:**
1. Einstellungen → Startseite
2. Benutzerdefinierte Adressen
3. Füge URL hinzu

### Als App auf Android/iOS

**Android (Chrome):**
1. Öffne Dashboard
2. Menü → "Zum Startbildschirm hinzufügen"
3. Benenne die App
4. Bestätige

**iOS (Safari):**
1. Öffne Dashboard
2. Teilen-Button → "Zum Home-Bildschirm"
3. Benenne die App
4. Fertig

### Reverse Proxy Setup

**Nginx Beispiel:**
```nginx
server {
    listen 80;
    server_name homelab.local;

    root /var/www/html/homelab-dashboard;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## 📞 Support & Fragen

### Logs prüfen

Öffne Browser-Konsole (F12) um Fehler zu sehen.

### Konfiguration zurücksetzen

```javascript
// In Browser-Konsole (F12):
localStorage.clear();
location.reload();
```

---

## 🎉 Viel Spaß mit deinem Homelab Dashboard!

Dieses Dashboard wurde entwickelt um dir einen **schnellen und schönen Überblick** über alle deine Homelab-Services zu geben.

**Feedback und Verbesserungsvorschläge sind willkommen!**

---

**Version**: 1.0
**Letzte Aktualisierung**: 2025-12-26
