# 🚀 Homelab Dashboard V4 ULTIMATE EDITION - Anleitung

**Version:** 4.0 Ultimate
**Datum:** 2025-12-26
**Status:** Production Ready

---

## 📋 Inhaltsverzeichnis

1. [Was ist neu in V4?](#was-ist-neu-in-v4)
2. [Schnellstart](#schnellstart)
3. [Installation](#installation)
4. [Konfiguration](#konfiguration)
5. [Neue Features im Detail](#neue-features-im-detail)
6. [API-Dokumentation](#api-dokumentation)
7. [Troubleshooting](#troubleshooting)
8. [Migration von V3](#migration-von-v3)
9. [Best Practices](#best-practices)
10. [FAQ](#faq)

---

## 🎉 Was ist neu in V4?

V4 ULTIMATE EDITION bringt **10 kritische Must-Have-Features**:

### 🔒 **Security & Authentifizierung**

#### ✅ **1. API Rate Limiting**
- **Schutz vor Brute-Force-Attacken**
- Max. 5 Login-Versuche pro Minute
- Automatische IP-basierte Sperrung
- Account-Lock nach 5 Fehlversuchen (30 Min)

```python
# Beispiel: Rate Limit erreicht
{
  "error": "Account gesperrt. Noch 25 Minuten."
}
```

#### ✅ **2. Session Management**
- **Auto-Logout bei Inaktivität** (Standard: 30 Min)
- **Absolute Session-Timeout** (Standard: 24 Std)
- **Session-Token-Rotation**
- Session-Tracking in Datenbank

#### ✅ **3. Passwort-Reset via Email**
- **Forgot-Password-Flow**
- Sichere Token-Generierung (1 Std Gültigkeit)
- Email-Benachrichtigung mit Reset-Link
- Passwort-Mindestlänge: 8 Zeichen

```bash
POST /api/auth/forgot-password
{
  "email": "admin@homelab.local"
}
```

### 📧 **Email-System**

#### ✅ **4. Email-Benachrichtigungen (SMTP)**
- **Service-Down-Notifications**
- **Incident-Alerts**
- **Passwort-Reset-Emails**
- **Willkommens-Emails** (optional)
- **Email-Queue** (bei Fehlern)

**Unterstützte SMTP-Provider:**
- Gmail (mit App-Passwort)
- Outlook/Office 365
- Yahoo Mail
- Eigener SMTP-Server
- Postfix/Sendmail

### 🔍 **Monitoring & Health Checks**

#### ✅ **5. Echte HTTP/HTTPS Health Checks**
- **Nicht nur Port-Check!** Echte HTTP-Requests
- **Response-Time-Messung**
- **Status-Code-Validierung**
- **Custom Health-Check-URLs**
- **Flexible Intervalle** (Standard: 5 Min)

```python
# Health Check Konfiguration
{
  "health_check_enabled": true,
  "health_check_url": "https://service.local/health",
  "health_check_method": "GET",
  "expected_status_code": 200,
  "health_check_interval": 300
}
```

#### ✅ **6. SSL-Zertifikat-Überwachung**
- **Automatische SSL-Prüfung** bei HTTPS-Services
- **Ablaufdatum-Tracking**
- **Warnung bei Ablauf < 30 Tage**
- **Zertifikat-Details** (Issuer, Serial, etc.)

### 🔎 **Suche & Organisation**

#### ✅ **7. Globale Suche**
- **Services** durchsuchen (Name, URL, Beschreibung)
- **Incidents** durchsuchen
- **Notes** durchsuchen
- **Tags** filtern
- **Mindestlänge:** 2 Zeichen

```bash
GET /api/search?q=docker&type=all
```

### 🔧 **System & Verwaltung**

#### ✅ **8. Datenbank-Migrations-System**
- **Automatische Schema-Updates**
- **Versions-Tracking**
- **Rollback-Fähigkeit** (manuell)
- **Keine Daten-Verluste** bei Updates

```sql
-- Schema-Version-Tracking
schema_version:
  version: 4
  description: "V4 Schema - Ultimate Edition"
  applied_at: 2025-12-26
```

#### ✅ **9. Webhook & Alert-System**
- **Webhooks für Events** (Service Down, Incident, etc.)
- **Discord/Slack-Integration**
- **Custom Webhooks**
- **HMAC-Signatur** für Sicherheit
- **Alert-Rules mit Cooldown**

```javascript
// Webhook Payload
{
  "event": "service_down",
  "payload": {
    "service": {
      "id": "service-1",
      "name": "Plex",
      "url": "https://plex.local"
    },
    "data": {
      "error_message": "Timeout",
      "timestamp": "2025-12-26T10:30:00"
    }
  }
}
```

#### ✅ **10. Automatische Backups mit Scheduler**
- **Geplante Backups** (täglich, wöchentlich)
- **Backup-Rotation** (behalte X neueste)
- **Email-Queue-Processing**
- **Stats-Update** alle 10 Minuten
- **Session-Cleanup** stündlich

---

## 🚀 Schnellstart

### Option 1: Docker Compose (EMPFOHLEN)

```bash
# 1. Repository klonen
git clone https://github.com/yourusername/homelab-dashboard.git
cd homelab-dashboard/homelab-dashboard

# 2. .env Datei erstellen
cat > .env << EOF
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
EOF

# 3. Container starten
docker-compose -f docker-compose-v4.yml up -d

# 4. Logs anschauen
docker-compose -f docker-compose-v4.yml logs -f

# 5. Öffnen
# http://localhost:5000
# Username: admin
# Passwort: homelab2025
```

### Option 2: Unraid (CA Template)

1. **Community Applications** öffnen
2. Nach **"Homelab Dashboard V4"** suchen
3. **Install** klicken
4. **SMTP-Daten** eingeben (optional)
5. **Apply** klicken
6. Dashboard öffnen: `http://[UNRAID-IP]:5000`

### Option 3: Manuell

```bash
# 1. Python 3.11+ installieren
python3 --version

# 2. Dependencies installieren
pip install -r requirements-v4.txt

# 3. Backend starten
python backend-v4.py

# 4. Browser öffnen
# http://localhost:5000
```

---

## 📦 Installation

Detaillierte Installationsanweisungen findest du in **[INSTALLATION.md](./INSTALLATION.md)**.

### Systemanforderungen

**Minimal:**
- CPU: 1 Core
- RAM: 512 MB
- Disk: 1 GB
- Python: 3.11+
- OS: Linux, Docker, Unraid

**Empfohlen:**
- CPU: 2 Cores
- RAM: 1 GB
- Disk: 5 GB (für Backups)
- Python: 3.11+
- SMTP-Server (für Emails)

---

## ⚙️ Konfiguration

### Umgebungsvariablen

#### Email-Konfiguration

```bash
# Gmail (mit App-Passwort)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Outlook
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password

# Eigener Server
SMTP_HOST=mail.your-domain.com
SMTP_PORT=587
SMTP_USER=no-reply@your-domain.com
SMTP_PASSWORD=secure-password
```

#### Gmail App-Passwort erstellen

1. Google Account öffnen: https://myaccount.google.com
2. **Sicherheit** → **2-Faktor-Authentifizierung** (muss aktiviert sein!)
3. **App-Passwörter** → **Neue App** → **Sonstiges**
4. Name: "Homelab Dashboard"
5. **Passwort generieren** → Kopieren
6. In `.env` oder Docker Umgebungsvariable einfügen

#### Health Check Konfiguration

```bash
HEALTH_CHECK_INTERVAL=300    # 5 Minuten (in Sekunden)
HEALTH_CHECK_TIMEOUT=10      # 10 Sekunden Timeout
```

#### Backup-Konfiguration

```bash
AUTO_BACKUP_ENABLED=true     # Automatische Backups aktivieren
AUTO_BACKUP_TIME=02:00       # Uhrzeit (HH:MM)
AUTO_BACKUP_RETENTION=7      # Anzahl zu behaltender Backups
```

#### Session-Konfiguration

```python
# In backend-v4.py anpassen:
SESSION_TIMEOUT_MINUTES = 30          # Inaktivitäts-Timeout
SESSION_ABSOLUTE_TIMEOUT_HOURS = 24   # Absolute Session-Dauer
```

---

## 🎯 Neue Features im Detail

### 1. Email-Benachrichtigungen einrichten

#### Schritt 1: SMTP konfigurieren

**Docker Compose:**
```yaml
environment:
  - SMTP_HOST=smtp.gmail.com
  - SMTP_PORT=587
  - SMTP_USER=your-email@gmail.com
  - SMTP_PASSWORD=your-app-password
```

**Manuell:**
```bash
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
python backend-v4.py
```

#### Schritt 2: Email-Funktionen testen

```bash
# Passwort-Reset-Email testen
curl -X POST http://localhost:5000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@homelab.local"}'
```

#### Schritt 3: Service-Down-Notifications

Emails werden automatisch gesendet, wenn:
- Service offline geht
- SSL-Zertifikat in < 7 Tagen abläuft
- Incident erstellt wird

**Empfänger:** Alle User mit Rolle "admin"

### 2. Health Checks konfigurieren

#### Service mit Health Check erstellen

```json
{
  "id": "plex-server",
  "name": "Plex Media Server",
  "url": "https://plex.local:32400",
  "health_check_enabled": true,
  "health_check_url": "https://plex.local:32400/web/index.html",
  "health_check_method": "GET",
  "health_check_interval": 300,
  "expected_status_code": 200,
  "ssl_check_enabled": true
}
```

#### Health Check Modi

**1. Standard (URL = Service URL):**
```json
{
  "health_check_enabled": true
}
```

**2. Custom Health-Endpoint:**
```json
{
  "health_check_url": "https://service.local/api/health"
}
```

**3. HEAD-Request (schneller):**
```json
{
  "health_check_method": "HEAD"
}
```

**4. POST-Request:**
```json
{
  "health_check_method": "POST"
}
```

#### SSL-Zertifikat-Check

Automatisch aktiviert für HTTPS-Services:

```json
{
  "ssl_check_enabled": true  // Standard bei https://
}
```

**Daten:**
- Ablaufdatum
- Tage bis Ablauf
- Issuer (z.B. Let's Encrypt)
- Gültigkeitsstatus

### 3. Globale Suche verwenden

#### Web-Interface

1. **Suchfeld** oben rechts
2. Mindestens **2 Zeichen** eingeben
3. Enter drücken
4. Ergebnisse werden gefiltert

#### API

```bash
# Alles durchsuchen
GET /api/search?q=docker&type=all

# Nur Services
GET /api/search?q=plex&type=services

# Nur Incidents
GET /api/search?q=timeout&type=incidents

# Nur Tags
GET /api/search?q=media&type=tags
```

**Response:**
```json
{
  "services": [
    {
      "id": "plex",
      "name": "Plex",
      "url": "https://plex.local",
      "tags": ["media", "streaming"]
    }
  ],
  "incidents": [],
  "tags": [
    {
      "id": 1,
      "name": "media",
      "color": "blue"
    }
  ]
}
```

### 4. Webhooks einrichten

#### Discord Webhook

```bash
POST /api/webhooks
{
  "name": "Discord Alerts",
  "url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/TOKEN",
  "events": ["service_down", "incident_created"],
  "secret": null
}
```

#### Slack Webhook

```bash
POST /api/webhooks
{
  "name": "Slack Notifications",
  "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "events": ["all"],
  "secret": null
}
```

#### Custom Webhook mit HMAC

```bash
POST /api/webhooks
{
  "name": "Custom API",
  "url": "https://your-api.com/webhook",
  "events": ["service_down", "service_up"],
  "secret": "your-secret-key"
}
```

**Webhook erhält:**
```json
{
  "event": "service_down",
  "payload": {
    "service": {...},
    "data": {...},
    "timestamp": "2025-12-26T10:30:00"
  }
}

// Header:
X-Webhook-Signature: <HMAC-SHA256>
```

#### Verfügbare Events

- `service_down` - Service offline
- `service_up` - Service wieder online
- `incident_created` - Neues Incident
- `incident_resolved` - Incident behoben
- `ssl_expiring_soon` - SSL läuft ab
- `backup_completed` - Backup erstellt
- `backup_failed` - Backup fehlgeschlagen
- `user_created` - Neuer User
- `all` - Alle Events

### 5. Passwort zurücksetzen

#### Als User (Frontend)

1. **Login-Page** öffnen
2. **"Passwort vergessen?"** klicken
3. **Email eingeben**
4. Email-Postfach prüfen
5. **Reset-Link** klicken
6. **Neues Passwort** eingeben

#### Via API

```bash
# 1. Reset anfordern
POST /api/auth/forgot-password
{
  "email": "admin@homelab.local"
}

# 2. Email prüfen, Token kopieren

# 3. Passwort zurücksetzen
POST /api/auth/reset-password
{
  "token": "abc123...",
  "new_password": "NewSecurePassword123"
}
```

**Token-Gültigkeit:** 1 Stunde

### 6. Automatische Backups

#### Konfiguration

```bash
# .env oder docker-compose-v4.yml
AUTO_BACKUP_ENABLED=true
AUTO_BACKUP_TIME=02:00          # 2 Uhr nachts
AUTO_BACKUP_RETENTION=7         # Behalte 7 Backups
```

#### Manuelles Backup

```bash
POST /api/backup/create
Authorization: Bearer <session-token>

# Response
{
  "success": true,
  "filename": "homelab_backup_20251226_143000.zip",
  "size": 1048576
}
```

#### Backup wiederherstellen

```bash
# 1. Backups auflisten
GET /api/backup/list

# 2. Backup ID finden

# 3. Restore
POST /api/backup/restore/5
```

**ACHTUNG:** Erstellt automatisch ein Safety-Backup vor Restore!

#### Backup-Inhalt

```
homelab_backup_20251226_143000.zip
├── homelab.db              # Datenbank
└── screenshots/            # Alle Screenshots
    ├── service1.png
    └── service2.jpg
```

### 7. Alert-Rules erstellen

```bash
POST /api/alert-rules
{
  "name": "Critical Services Down",
  "condition_type": "service_down",
  "condition_value": null,
  "notification_channels": ["email", "webhook"],
  "cooldown_minutes": 60
}
```

**Cooldown:** Verhindert Spam (z.B. nicht öfter als 1x pro Stunde)

### 8. Datenbank-Migrationen

**Automatisch beim Start:**

```bash
# Backend erkennt alte Schema-Version
$ python backend-v4.py

Führe Schema-Migration durch (v3 → v4)...
✓ Schema aktualisiert
✓ Neue Tabellen erstellt:
  - rate_limits
  - password_reset_tokens
  - email_queue
  - webhooks
  - webhook_logs
  - alert_rules
  - user_sessions
```

**Manuelle Migration:**

```sql
-- Schema-Version prüfen
SELECT * FROM schema_version ORDER BY applied_at DESC LIMIT 1;

-- Tabellen prüfen
SELECT name FROM sqlite_master WHERE type='table';
```

### 9. Session Management

#### Auto-Logout bei Inaktivität

**Standard:** 30 Minuten

User wird ausgeloggt wenn:
- 30 Min keine Aktivität
- Browser-Tab inaktiv
- Keine API-Calls

#### Remember Me (noch nicht implementiert)

Aktuell: Sessions laufen nach 24 Std absolut ab.

#### Sessions anzeigen

```bash
GET /api/auth/sessions

# Response
{
  "sessions": [
    {
      "id": 1,
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0...",
      "last_activity": "2025-12-26 14:30:00",
      "expires_at": "2025-12-27 10:00:00"
    }
  ]
}
```

### 10. Rate Limiting

#### Login-Schutz

**Limit:** 5 Versuche pro Minute (pro IP)

Bei Überschreitung:
```json
{
  "error": "Too many requests. Try again later."
}
```

#### Account-Lock

**Nach 5 Fehlversuchen:**
- Account für 30 Minuten gesperrt
- Email-Benachrichtigung (wenn aktiviert)

```json
{
  "error": "Account gesperrt. Noch 25 Minuten."
}
```

**Entsperren:**
- Automatisch nach 30 Min
- Manuell via Admin

---

## 📚 API-Dokumentation

### Authentifizierung

#### Login

```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "homelab2025"
}

# Response
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@homelab.local"
  },
  "session_token": "abc123..."
}
```

#### Check Auth

```bash
GET /api/auth/check

# Response
{
  "authenticated": true,
  "user": {...}
}
```

#### Logout

```bash
POST /api/auth/logout

# Response
{
  "success": true
}
```

#### Passwort ändern

```bash
POST /api/auth/change-password
Content-Type: application/json

{
  "old_password": "homelab2025",
  "new_password": "NewSecure123"
}
```

### Services

#### Alle Services

```bash
GET /api/services

# Response
[
  {
    "id": "plex",
    "name": "Plex",
    "url": "https://plex.local",
    "is_online": true,
    "response_time": 250,
    "ssl_valid": true,
    "ssl_days_remaining": 89,
    "uptime_percentage": 99.5,
    "tags": ["media", "streaming"]
  }
]
```

### Suche

#### Global Search

```bash
GET /api/search?q=docker&type=all

# Response
{
  "services": [...],
  "incidents": [...],
  "tags": [...]
}
```

### Webhooks

#### Erstellen

```bash
POST /api/webhooks
Content-Type: application/json

{
  "name": "Discord",
  "url": "https://discord.com/api/webhooks/...",
  "events": ["service_down"],
  "secret": null
}
```

#### Liste

```bash
GET /api/webhooks

# Response
[
  {
    "id": 1,
    "name": "Discord",
    "url": "https://...",
    "events": ["service_down"],
    "is_active": true,
    "last_triggered": "2025-12-26 10:30:00"
  }
]
```

#### Löschen

```bash
DELETE /api/webhooks/1
```

### System

#### System Status

```bash
GET /api/system/status

# Response
{
  "total_services": 10,
  "online_services": 9,
  "offline_services": 1,
  "active_incidents": 1,
  "ssl_expiring_soon": 2,
  "pending_emails": 0,
  "email_enabled": true,
  "auto_backup_enabled": true,
  "health_check_interval": 300,
  "version": "V4 Ultimate"
}
```

---

## 🔧 Troubleshooting

### Problem: Emails werden nicht gesendet

**Mögliche Ursachen:**

1. **SMTP nicht konfiguriert**
   ```bash
   # Prüfen
   docker-compose -f docker-compose-v4.yml exec homelab-dashboard env | grep SMTP

   # Sollte zeigen:
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=***
   ```

2. **Gmail: App-Passwort fehlt**
   - Normales Gmail-Passwort funktioniert NICHT
   - App-Passwort erstellen (siehe Konfiguration oben)

3. **Firewall blockiert Port 587**
   ```bash
   # Testen
   telnet smtp.gmail.com 587
   ```

4. **Email-Queue prüfen**
   ```bash
   # Im Container
   sqlite3 homelab.db "SELECT * FROM email_queue WHERE sent = 0;"
   ```

**Lösung:**
```bash
# Email-Queue manuell verarbeiten
# Wird automatisch alle 5 Minuten versucht
```

### Problem: Health Checks schlagen fehl

**Symptome:**
- Alle Services "offline"
- Response-Time: null
- Error: "Timeout"

**Mögliche Ursachen:**

1. **Container kann Services nicht erreichen**
   ```bash
   # Testen
   docker-compose -f docker-compose-v4.yml exec homelab-dashboard curl https://plex.local
   ```

2. **SSL-Zertifikat ungültig**
   ```bash
   # Health Check ignoriert SSL-Fehler (verify=False)
   # Aber Service könnte trotzdem Probleme haben
   ```

3. **Timeout zu kurz**
   ```bash
   # Erhöhen
   HEALTH_CHECK_TIMEOUT=30
   ```

**Lösung:**
```bash
# Netzwerk-Modus ändern (docker-compose-v4.yml)
network_mode: host
```

### Problem: Automatische Backups funktionieren nicht

**Prüfen:**

```bash
# 1. Backup-Einstellungen
docker-compose -f docker-compose-v4.yml exec homelab-dashboard env | grep BACKUP

# 2. Backup-Verzeichnis
ls -la data/backups/

# 3. Logs
docker-compose -f docker-compose-v4.yml logs | grep -i backup
```

**Manuelles Backup:**
```bash
curl -X POST http://localhost:5000/api/backup/create \
  -H "Cookie: session=..." \
  -H "Content-Type: application/json"
```

### Problem: Rate Limit erreicht

**Symptom:**
```json
{
  "error": "Too many requests. Try again later."
}
```

**Lösung:**
- Warte 1 Minute
- Oder: Rate Limit in backend-v4.py anpassen:

```python
limiter = Limiter(
    app=app,
    default_limits=["200 per hour"],  # Von 200 auf 500 erhöhen
)

# Login-Limit
@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per minute")  # Von 5 auf 10 erhöhen
```

### Problem: Datenbank-Fehler nach Update

**Symptom:**
```
sqlite3.OperationalError: no such table: webhooks
```

**Lösung:**
```bash
# Manuell Migrationen laufen lassen
python backend-v4.py
# Erkennt automatisch alte Version und migriert
```

**Oder manuell:**
```sql
sqlite3 homelab.db

-- Schema-Version prüfen
SELECT * FROM schema_version;

-- Fehlende Tabellen manuell erstellen (siehe init_db() in backend-v4.py)
CREATE TABLE IF NOT EXISTS webhooks (...);
```

---

## 🔄 Migration von V3

### Automatische Migration

V4 erkennt V3-Datenbank und migriert **automatisch**:

```bash
# Einfach V4 starten
python backend-v4.py

# Ausgabe:
Führe Schema-Migration durch (v3 → v4)...
✓ Schema aktualisiert
✓ Datenbank-Version: 4
```

**Neue Tabellen:**
- `rate_limits`
- `password_reset_tokens`
- `email_queue`
- `webhooks`
- `webhook_logs`
- `alert_rules`
- `user_sessions`
- `schema_version`

**Erweiterte Tabellen:**
- `users` → neue Felder (email_verified, two_factor_*, failed_login_attempts, etc.)
- `services` → Health Check Felder
- `service_status` → SSL-Felder
- `service_stats` → 24h/7d Uptime

### Manuelle Migration

Falls automatische Migration fehlschlägt:

```bash
# 1. Backup erstellen
cp homelab.db homelab_v3_backup.db

# 2. Python starten (interaktiv)
python

# 3. Migration manuell ausführen
from backend_v4 import init_db
init_db()
exit()

# 4. V4 starten
python backend-v4.py
```

### Rollback auf V3

```bash
# 1. V4 stoppen
docker-compose -f docker-compose-v4.yml down

# 2. V3-Backup wiederherstellen
cp homelab_v3_backup.db homelab.db

# 3. V3 starten
python backend-v3.py
```

---

## ✅ Best Practices

### 1. Sicherheit

✅ **Passwort sofort ändern**
```bash
# Nach erstem Login
POST /api/auth/change-password
{
  "old_password": "homelab2025",
  "new_password": "Super$ecure123!"
}
```

✅ **Email aktivieren**
- Passwort-Reset möglich
- Benachrichtigungen bei Problemen

✅ **Regelmäßige Backups**
```bash
AUTO_BACKUP_ENABLED=true
AUTO_BACKUP_TIME=02:00
AUTO_BACKUP_RETENTION=14  # 2 Wochen
```

✅ **Reverse Proxy mit SSL**
```nginx
# nginx
server {
    listen 443 ssl http2;
    server_name dashboard.your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
    }
}
```

### 2. Performance

✅ **Health Check Intervall anpassen**
```bash
# Viele Services? Intervall erhöhen
HEALTH_CHECK_INTERVAL=600  # 10 Minuten statt 5
```

✅ **Backup-Zeitpunkt optimieren**
```bash
# Nachts wenn wenig Traffic
AUTO_BACKUP_TIME=03:00
```

✅ **Alte Uptime-History löschen**
```sql
-- Behalte nur 30 Tage
DELETE FROM uptime_history
WHERE checked_at < datetime('now', '-30 days');
```

### 3. Monitoring

✅ **Webhooks für wichtige Events**
```bash
# Discord/Slack für Alerts
POST /api/webhooks
{
  "name": "Critical Alerts",
  "url": "https://...",
  "events": ["service_down", "ssl_expiring_soon"]
}
```

✅ **Email für Admins**
```bash
# Alle Admins bekommen Emails bei:
- Service Down
- SSL < 7 Tage
- Backup Failed
```

✅ **System Status prüfen**
```bash
# Täglich
GET /api/system/status
```

### 4. Wartung

✅ **Logs regelmäßig prüfen**
```bash
docker-compose -f docker-compose-v4.yml logs --tail=100 -f
```

✅ **Disk Space überwachen**
```bash
# Backup-Größe
du -sh data/backups/

# Alte Backups manuell löschen falls nötig
```

✅ **Uptime-History begrenzen**
```bash
# Automatisch via Cron oder manuell
sqlite3 homelab.db "DELETE FROM uptime_history WHERE checked_at < datetime('now', '-90 days');"
```

---

## ❓ FAQ

### Wie viele Services kann ich hinzufügen?

**Unbegrenzt!** Aber:
- Health Checks dauern länger bei vielen Services
- Empfohlen: < 100 Services pro Instanz
- Bei mehr: Intervall erhöhen oder mehrere Instanzen

### Kann ich V4 parallel zu V3 laufen lassen?

**Ja!** Unterschiedliche Ports verwenden:

```yaml
# docker-compose-v4.yml
ports:
  - "5001:5000"  # V4 auf Port 5001

# V3 bleibt auf Port 5000
```

### Welche Datenbank wird verwendet?

**SQLite3** - serverless, keine Extra-Installation nötig.

**Vorteile:**
- Einfach
- Schnell für kleine/mittlere Deployments
- Backups = eine Datei kopieren

**Für große Deployments:** PostgreSQL/MySQL möglich (Code-Änderungen nötig)

### Kann ich eigene Themes erstellen?

**Ja!** Via API:

```bash
POST /api/themes/custom
{
  "name": "My Dark Theme",
  "colors": {
    "primary": "#1a1a1a",
    "secondary": "#2d2d2d",
    "accent": "#00ff00"
  },
  "fonts": {
    "body": "Arial",
    "heading": "Helvetica"
  }
}
```

### Wie funktioniert die Webhook-Signatur?

**HMAC-SHA256:**

```python
import hmac
import hashlib
import json

payload = {...}
secret = "your-secret"

signature = hmac.new(
    secret.encode(),
    json.dumps(payload).encode(),
    hashlib.sha256
).hexdigest()

# Kommt im Header: X-Webhook-Signature
```

### Kann ich HTTPS erzwingen?

**Ja!** Über Reverse Proxy:

```nginx
# nginx - HTTP → HTTPS Redirect
server {
    listen 80;
    server_name dashboard.local;
    return 301 https://$server_name$request_uri;
}
```

### Werden Passwörter verschlüsselt?

**Gehashed mit SHA-256.**

**Achtung:** Für Production besser **bcrypt** oder **argon2** verwenden!

```python
# Aktuell (backend-v4.py)
password_hash = hashlib.sha256(password.encode()).hexdigest()

# Besser (TODO)
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Kann ich 2FA aktivieren?

**Vorbereitet in DB**, aber noch **nicht implementiert**.

Tabelle `users` hat Felder:
- `two_factor_enabled`
- `two_factor_secret`

Implementation kommt in V4.1!

---

## 📞 Support & Community

### Probleme melden

**GitHub Issues:** https://github.com/yourusername/homelab-dashboard/issues

**Bitte angeben:**
- V4 Version
- Betriebssystem (Docker/Unraid/manuell)
- Logs (letzte 50 Zeilen)
- Fehlermeldung
- Schritte zur Reproduktion

### Dokumentation

- **Installation:** [INSTALLATION.md](./INSTALLATION.md)
- **Changelog:** [CHANGELOG.md](./CHANGELOG.md)
- **API-Docs:** Siehe oben

### Community

- **Discord:** (Link einfügen)
- **Reddit:** r/homelab
- **Forum:** (Link einfügen)

---

## 🎉 Viel Erfolg mit V4 Ultimate!

**Feedback & Feature-Requests** sind willkommen!

---

**Version:** 4.0 Ultimate
**Erstellt:** 2025-12-26
**Autor:** Homelab Dashboard Team
**Lizenz:** MIT
