# Homelab Dashboard V4 Ultimate Edition 🚀

[![Docker Pulls](https://img.shields.io/docker/pulls/YOUR_USERNAME/homelab-dashboard)](https://hub.docker.com/r/YOUR_USERNAME/homelab-dashboard)
[![Docker Image Size](https://img.shields.io/docker/image-size/YOUR_USERNAME/homelab-dashboard/latest)](https://hub.docker.com/r/YOUR_USERNAME/homelab-dashboard)
[![GitHub](https://img.shields.io/github/license/YOUR_USERNAME/homelab-dashboard)](https://github.com/YOUR_USERNAME/homelab-dashboard)

**Production-Ready Dashboard für dein Homelab mit Email-Notifications, HTTP Health Checks, SSL-Monitoring, Webhooks und automatischen Backups!**

---

## 🎯 Features

### 🔒 **Security**
- ✅ API Rate Limiting (Brute-Force-Schutz)
- ✅ Session Management (Auto-Logout)
- ✅ Passwort-Reset via Email
- ✅ Account-Lock nach Fehlversuchen

### 📧 **Email-System**
- ✅ SMTP-Integration (Gmail/Outlook/Custom)
- ✅ Service-Down-Notifications
- ✅ SSL-Ablauf-Warnungen
- ✅ Email-Queue mit Auto-Retry

### 🔍 **Monitoring**
- ✅ Echte HTTP/HTTPS Health Checks
- ✅ SSL-Zertifikat-Überwachung
- ✅ Response-Time-Messung
- ✅ Uptime-Statistiken (24h/7d/30d)

### 🔧 **System**
- ✅ Globale Suche
- ✅ Webhook-System (Discord/Slack)
- ✅ Alert-Rules mit Cooldown
- ✅ Automatische Backups
- ✅ Multi-User mit Rollen & Permissions

---

## 🚀 Quick Start

### Docker Run

```bash
docker run -d \
  --name homelab-dashboard \
  -p 5000:5000 \
  -v $(pwd)/data:/app \
  -e SMTP_USER=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  YOUR_USERNAME/homelab-dashboard:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  homelab-dashboard:
    image: YOUR_USERNAME/homelab-dashboard:latest
    container_name: homelab-dashboard
    ports:
      - "5000:5000"
    environment:
      - SMTP_USER=your-email@gmail.com
      - SMTP_PASSWORD=your-app-password
      - SMTP_FROM=your-email@gmail.com
      - AUTO_BACKUP_ENABLED=true
      - AUTO_BACKUP_TIME=02:00
    volumes:
      - ./data/homelab.db:/app/homelab.db
      - ./data/backups:/app/backups
      - ./data/screenshots:/app/screenshots
    restart: unless-stopped
```

### Unraid

1. **Community Applications** → Suche "Homelab Dashboard"
2. **Template installieren**
3. **SMTP konfigurieren** (optional)
4. **Apply**

---

## ⚙️ Umgebungsvariablen

### Email (SMTP)

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `SMTP_HOST` | `smtp.gmail.com` | SMTP Server |
| `SMTP_PORT` | `587` | SMTP Port (TLS) |
| `SMTP_USER` | - | Email-Adresse |
| `SMTP_PASSWORD` | - | App-Passwort |
| `SMTP_FROM` | `$SMTP_USER` | Absender |

### Health Checks

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `HEALTH_CHECK_INTERVAL` | `300` | Intervall in Sekunden |
| `HEALTH_CHECK_TIMEOUT` | `10` | Timeout in Sekunden |

### Backups

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `AUTO_BACKUP_ENABLED` | `true` | Automatische Backups |
| `AUTO_BACKUP_TIME` | `02:00` | Uhrzeit (HH:MM) |
| `AUTO_BACKUP_RETENTION` | `7` | Anzahl Backups |

### Sonstiges

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `TZ` | `Europe/Berlin` | Zeitzone |
| `PUID` | `1000` | User ID |
| `PGID` | `1000` | Group ID |

---

## 📦 Volumes

| Container-Path | Beschreibung |
|----------------|--------------|
| `/app/homelab.db` | Datenbank (SQLite) |
| `/app/backups` | Backup-Verzeichnis |
| `/app/screenshots` | Service-Screenshots |
| `/app/logs` | Logs (optional) |

---

## 🔐 Standard-Login

```
Username: admin
Passwort: homelab2025
```

**⚠️ WICHTIG:** Passwort nach erstem Login ändern!

---

## 🌐 Zugriff

Nach dem Start:
- **Dashboard:** http://localhost:5000
- **Login:** http://localhost:5000/login.html
- **API:** http://localhost:5000/api/*

---

## 📧 Gmail App-Passwort erstellen

1. Google Account → **Sicherheit**
2. **2-Faktor-Authentifizierung** aktivieren
3. **App-Passwörter** → Neue App → "Homelab Dashboard"
4. Passwort kopieren und als `SMTP_PASSWORD` verwenden

---

## 🔍 API-Beispiele

### Service-Status abrufen

```bash
curl http://localhost:5000/api/services
```

### Globale Suche

```bash
curl "http://localhost:5000/api/search?q=docker&type=all"
```

### System-Status

```bash
curl http://localhost:5000/api/system/status
```

---

## 🏗️ Architektur

- **Backend:** Python 3.11, Flask 3.0
- **Datenbank:** SQLite3 (26 Tabellen)
- **Frontend:** HTML5, CSS3, JavaScript
- **Scheduler:** Python schedule
- **Health Checks:** requests library
- **Email:** Python smtplib

---

## 🐳 Multi-Platform Support

Unterstützte Architekturen:
- ✅ `linux/amd64` (x86_64)
- ✅ `linux/arm64` (ARM 64-bit, z.B. Raspberry Pi 4)
- ✅ `linux/arm/v7` (ARM 32-bit, z.B. Raspberry Pi 3)

---

## 📊 Image-Tags

| Tag | Beschreibung |
|-----|--------------|
| `latest` | Neueste stabile Version |
| `v4` | V4 Ultimate Edition |
| `v4-ultimate` | V4 Ultimate Edition |
| `v4.0.0` | Spezifische Version |

---

## 🔧 Troubleshooting

### Emails werden nicht gesendet

```bash
# Logs prüfen
docker logs homelab-dashboard

# SMTP testen
docker exec homelab-dashboard env | grep SMTP
```

### Health Checks schlagen fehl

```bash
# Netzwerk-Modus auf host ändern
docker run --network host ...
```

### Backup funktioniert nicht

```bash
# Permissions prüfen
docker exec homelab-dashboard ls -la /app/backups
```

---

## 📚 Dokumentation

- **Vollständige Anleitung:** [ANLEITUNG-V4.md](https://github.com/YOUR_USERNAME/homelab-dashboard/blob/main/homelab-dashboard/ANLEITUNG-V4.md)
- **Changelog:** [CHANGELOG.md](https://github.com/YOUR_USERNAME/homelab-dashboard/blob/main/homelab-dashboard/CHANGELOG.md)
- **Installation:** [INSTALLATION.md](https://github.com/YOUR_USERNAME/homelab-dashboard/blob/main/homelab-dashboard/INSTALLATION.md)

---

## 🤝 Support

- **GitHub:** https://github.com/YOUR_USERNAME/homelab-dashboard
- **Issues:** https://github.com/YOUR_USERNAME/homelab-dashboard/issues
- **Discussions:** https://github.com/YOUR_USERNAME/homelab-dashboard/discussions

---

## 📜 Lizenz

MIT License - siehe [LICENSE](https://github.com/YOUR_USERNAME/homelab-dashboard/blob/main/LICENSE)

---

## ⭐ Features im Detail

### Webhook-Integration

```bash
# Discord Webhook
POST /api/webhooks
{
  "name": "Discord",
  "url": "https://discord.com/api/webhooks/...",
  "events": ["service_down", "ssl_expiring_soon"]
}
```

### Alert-Rules

```bash
# Email bei Service-Down
POST /api/alert-rules
{
  "name": "Critical Services",
  "condition_type": "service_down",
  "notification_channels": ["email", "webhook"],
  "cooldown_minutes": 60
}
```

### Passwort-Reset

```bash
# Reset anfordern
POST /api/auth/forgot-password
{
  "email": "admin@homelab.local"
}
```

---

**Gebaut mit ❤️ für die Homelab-Community**

🌟 **Star us on GitHub!** → https://github.com/YOUR_USERNAME/homelab-dashboard
