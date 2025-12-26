# 🏠 Homelab Dashboard

Ein modernes, interaktives Dashboard zur Verwaltung und zum schnellen Zugriff auf alle deine Homelab-Services.

![Dashboard Preview](https://img.shields.io/badge/Status-Ready-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

---

## ✨ Features

### 🎨 Modernes Design
- **Responsive Layout** - Funktioniert auf Desktop, Tablet und Smartphone
- **Dark/Light Mode** - Automatisch gespeicherte Theme-Präferenz
- **Animationen** - Flüssige Übergänge und Hover-Effekte
- **Farbcodierung** - 6 verschiedene Farben zur Kategorisierung

### 🚀 Funktionalität
- **Service-Verwaltung** - Einfaches Hinzufügen, Bearbeiten und Löschen
- **Kategorien** - 6 vordefinierte Kategorien (Media, Automation, Netzwerk, etc.)
- **Suche** - Echtzeit-Suche durch Services
- **Filter** - Schnelles Filtern nach Kategorien
- **Icons** - Font Awesome Integration für über 7000 Icons

### 💾 Datenverwaltung
- **LocalStorage** - Alle Daten werden lokal im Browser gespeichert
- **Export/Import** - JSON-basierte Konfiguration zum Backup und Teilen
- **Keine Datenbank nötig** - 100% clientseitig

### 📊 Dashboard-Stats
- **Services Online** - Anzahl der konfigurierten Services
- **Aktuelle Zeit** - Live-Uhr
- **Session Uptime** - Laufzeit seit Dashboard-Start

---

## 🚀 Schnellstart

### 1. Installation

**Mit Python (empfohlen für lokale Nutzung):**
```bash
cd homelab-dashboard
python3 -m http.server 8000
```

Dann öffne: `http://localhost:8000`

### 2. Ersten Service hinzufügen

1. Klicke auf den **+ Button** (unten rechts)
2. Fülle das Formular aus
3. Klicke auf **Speichern**

### 3. Beispiel-Konfiguration laden

Klicke im Footer auf **"Konfiguration importieren"** und wähle `example-config.json` aus.

---

## 📁 Dateien

```
homelab-dashboard/
├── index.html           # Haupt-HTML (Dashboard-Struktur)
├── styles.css           # Komplettes Styling (Light & Dark Mode)
├── app.js              # Gesamte Logik und Interaktivität
├── example-config.json # Beispiel-Konfiguration mit 12 Services
├── ANLEITUNG.md        # Ausführliche deutsche Anleitung
└── README.md           # Diese Datei
```

---

## 🎯 Verwendung

### Service hinzufügen

**Erforderliche Felder:**
- **Name**: Der Anzeigename (z.B. "Plex")
- **URL**: Vollständige URL (z.B. `http://192.168.1.100:32400`)
- **Kategorie**: Media, Automation, Netzwerk, Monitoring, Storage, Sonstiges

**Optionale Felder:**
- **Beschreibung**: Kurzbeschreibung des Services
- **Icon**: Font Awesome Icon-Name (z.B. `fa-play`)
- **Farbe**: Blau, Grün, Lila, Orange, Rot, Türkis

### Service öffnen

Klicke einfach auf eine Service-Karte → Öffnet in neuem Tab

### Service bearbeiten

Klicke auf das **Stift-Symbol** auf der Karte

### Service löschen

Öffne Bearbeiten-Dialog → Klicke auf **Löschen**

---

## 🎨 Kategorien

| Kategorie | Icon | Verwendung |
|-----------|------|------------|
| **Media** | 📺 | Plex, Jellyfin, Sonarr, Radarr |
| **Automation** | 🤖 | Home Assistant, Node-RED |
| **Netzwerk** | 🌐 | Pi-hole, Unifi, Nginx Proxy Manager |
| **Monitoring** | 📊 | Grafana, Prometheus, Uptime Kuma |
| **Storage** | 💾 | Nextcloud, TrueNAS, Synology |
| **Sonstiges** | ⚙️ | Portainer, Heimdall, etc. |

---

## 🌙 Dark Mode

- **Toggle**: Mond/Sonne Button (oben rechts)
- **Auto-Save**: Theme-Präferenz wird gespeichert
- **Farbanpassung**: Beide Themes komplett angepasst

---

## 💾 Backup & Restore

### Konfiguration exportieren

Footer → **"Konfiguration exportieren"** → JSON-Datei wird heruntergeladen

### Konfiguration importieren

Footer → **"Konfiguration importieren"** → JSON-Datei auswählen

**Beispiel-Format:**
```json
{
  "version": "1.0",
  "exportDate": "2025-12-26T00:00:00.000Z",
  "services": [
    {
      "id": "unique-id",
      "name": "Plex",
      "description": "Media Server",
      "url": "http://192.168.1.100:32400",
      "icon": "fa-play",
      "category": "media",
      "color": "orange"
    }
  ]
}
```

---

## 🔧 Installation auf verschiedenen Plattformen

### Docker

```dockerfile
FROM nginx:alpine
COPY homelab-dashboard/ /usr/share/nginx/html/
EXPOSE 80
```

```bash
docker build -t homelab-dashboard .
docker run -d -p 8080:80 homelab-dashboard
```

### Nginx

```nginx
server {
    listen 80;
    server_name homelab.local;
    root /var/www/html/homelab-dashboard;
    index index.html;
}
```

### Apache

```apache
<VirtualHost *:80>
    ServerName homelab.local
    DocumentRoot /var/www/html/homelab-dashboard
    <Directory /var/www/html/homelab-dashboard>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

---

## ⌨️ Tastatur-Shortcuts

| Shortcut | Aktion |
|----------|--------|
| `Strg/Cmd + K` | Suchleiste fokussieren |
| `Escape` | Modals schließen |

---

## 🎨 Anpassung

### Titel ändern

**`index.html` (Zeile ~30):**
```html
<h1><i class="fas fa-server"></i> Dein Titel</h1>
<p class="subtitle">Dein Untertitel</p>
```

### Farben ändern

**`styles.css` (Zeile ~6):**
```css
:root {
    --color-blue: #3498db;
    --color-green: #2ecc71;
    /* ... weitere Farben ... */
}
```

### Neue Kategorie hinzufügen

1. Filter-Button in `index.html` hinzufügen
2. Kategorie-Name in `app.js` → `getCategoryName()` hinzufügen
3. Option in beiden Modals hinzufügen

Siehe **ANLEITUNG.md** für Details.

---

## 📱 Mobile Nutzung

### Als App hinzufügen

**Android (Chrome):**
Menü → "Zum Startbildschirm hinzufügen"

**iOS (Safari):**
Teilen → "Zum Home-Bildschirm"

---

## 🌐 Browser-Kompatibilität

✅ Chrome/Chromium 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+

---

## 📖 Dokumentation

Siehe **[ANLEITUNG.md](ANLEITUNG.md)** für:
- Ausführliche Schritt-für-Schritt-Anleitungen
- Tipps und Tricks
- Fehlerbehebung
- Erweiterte Konfiguration

---

## 🛠️ Technologie-Stack

- **HTML5** - Semantische Struktur
- **CSS3** - Modernes Styling mit CSS Variables
- **Vanilla JavaScript** - Keine Frameworks, keine Dependencies
- **Font Awesome** - Icons (CDN)
- **LocalStorage API** - Datenpersistenz

---

## 🎯 Beliebte Homelab-Services

Das Dashboard funktioniert perfekt mit:

### Media
- Plex, Jellyfin, Emby
- Sonarr, Radarr, Lidarr
- Tautulli, Overseerr

### Automation
- Home Assistant
- Node-RED
- Homebridge

### Netzwerk
- Pi-hole, AdGuard Home
- Unifi Controller
- Nginx Proxy Manager
- pfSense, OPNsense

### Monitoring
- Grafana
- Prometheus
- Uptime Kuma
- Netdata

### Storage
- Nextcloud
- TrueNAS, Synology
- Filerun

### Container Management
- Portainer
- Yacht
- Cockpit

---

## 🔒 Sicherheit

### Empfehlungen:

1. **Kein öffentliches Internet**: Nur im lokalen Netzwerk verwenden
2. **HTTPS verwenden**: Bei externem Zugriff immer HTTPS
3. **Reverse Proxy**: Nutze Nginx Proxy Manager o.ä.
4. **VPN**: Für externen Zugriff VPN empfohlen (WireGuard, OpenVPN)

### Was das Dashboard NICHT speichert:

- ❌ Keine Passwörter
- ❌ Keine Login-Daten
- ❌ Keine persönlichen Informationen
- ✅ Nur Namen, URLs und Konfiguration

---

## 📊 Features im Detail

### Suche
- Echtzeit-Filterung
- Durchsucht Namen und Beschreibungen
- Case-insensitive

### Filter
- 7 Filter-Buttons (inkl. "Alle")
- Kombinierbar mit Suche
- Visuelles Feedback (blauer Button)

### Service-Karten
- Hover-Effekte
- Farbcodierung am oberen Rand
- Icon-Anzeige
- Kategorie-Badge
- URL-Anzeige

### Statistiken
- Live-Uhr (Sekunden-genau)
- Service-Zähler
- Session-Uptime

---

## 🐛 Fehlerbehebung

### Services verschwinden nach Browser-Neustart

**Ursache**: Browser löscht LocalStorage
**Lösung**: Regelmäßig Konfiguration exportieren!

### Icons werden nicht angezeigt

**Ursache**: Font Awesome CDN nicht erreichbar
**Lösung**:
1. Internet-Verbindung prüfen
2. Oder Font Awesome lokal hosten

### URL öffnet nicht

**Ursache**: Falsche URL-Formatierung
**Lösung**: URL muss mit `http://` oder `https://` beginnen

Siehe **ANLEITUNG.md** für mehr Lösungen.

---

## 🤝 Beiträge

Verbesserungen und Vorschläge sind willkommen!

### Ideen für zukünftige Features:

- [ ] Service-Status-Check (ping)
- [ ] Drag & Drop zum Sortieren
- [ ] Gruppen/Ordner für Services
- [ ] Custom Themes
- [ ] Service-Notizen
- [ ] Favoriten/Sterne
- [ ] Service-Tags

---

## 📜 Lizenz

MIT License - Frei verwendbar für persönliche und kommerzielle Projekte.

---

## 🙏 Credits

- **Icons**: [Font Awesome](https://fontawesome.com)
- **Design**: Inspiriert von modernen Dashboard-Designs
- **Entwickelt mit**: ❤️ für die Homelab-Community

---

## 📞 Support

Bei Fragen oder Problemen:
1. Lies die **ANLEITUNG.md**
2. Prüfe Browser-Konsole (F12) auf Fehler
3. Teste mit `example-config.json`

---

**Viel Spaß mit deinem Homelab Dashboard! 🚀**

Made with ❤️ for Homelabbers
