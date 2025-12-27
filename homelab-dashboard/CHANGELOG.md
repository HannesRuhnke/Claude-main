# Changelog - Homelab Dashboard

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Format basierend auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

---

## [4.0.0] - 2025-12-26 - ULTIMATE EDITION 🚀

### 🎉 Major Release - 10 kritische Must-Have Features

Diese Version bringt die am meisten gewünschten Enterprise-Features und macht das Dashboard production-ready für kritische Homelab-Umgebungen.

### ✨ Neu hinzugefügt

#### Security & Authentifizierung

- **API Rate Limiting** mit Flask-Limiter
  - Schutz vor Brute-Force-Attacken
  - 5 Login-Versuche pro Minute (pro IP)
  - Automatische Account-Sperre nach 5 Fehlversuchen (30 Min)
  - IP-basiertes Tracking in `rate_limits` Tabelle

- **Session Management**
  - Auto-Logout bei Inaktivität (Standard: 30 Min)
  - Absolute Session-Timeout (Standard: 24 Std)
  - Session-Token-Rotation
  - Session-Tracking in `user_sessions` Tabelle
  - `last_activity` Tracking für alle User

- **Passwort-Reset-Flow**
  - Forgot-Password-Funktion mit Email
  - Sichere Token-Generierung (1 Std Gültigkeit)
  - Token-Einmalverwendung
  - `password_reset_tokens` Tabelle
  - Email-Benachrichtigung mit Reset-Link
  - Passwort-Mindestlänge: 8 Zeichen

#### Email-System

- **SMTP-Integration**
  - Vollständige Email-Funktionalität
  - Unterstützung für Gmail, Outlook, eigene Server
  - HTML & Plain-Text Emails
  - Email-Queue bei Fehlern (`email_queue` Tabelle)
  - Automatische Wiederholungsversuche (max. 3)
  - Email-Queue-Processing alle 5 Minuten

- **Email-Benachrichtigungen**
  - Service-Down-Alerts an alle Admins
  - SSL-Zertifikat-Ablauf-Warnungen (< 7 Tage)
  - Passwort-Reset-Emails
  - Incident-Notifications
  - Backup-Status-Emails

#### Monitoring & Health Checks

- **Echte HTTP/HTTPS Health Checks**
  - Nicht nur Socket-Check! Echte HTTP-Requests
  - Unterstützt GET, HEAD, POST Methods
  - Response-Time-Messung (in ms)
  - Status-Code-Validierung
  - Custom Health-Check-URLs
  - Konfigurierbare Intervalle (Standard: 5 Min)
  - Timeout-Konfiguration (Standard: 10 Sek)
  - Error-Message-Logging

- **SSL-Zertifikat-Monitoring**
  - Automatische SSL-Prüfung für HTTPS-Services
  - Ablaufdatum-Tracking
  - Tage-bis-Ablauf-Berechnung
  - Issuer & Subject-Info
  - Serial Number Tracking
  - Warnung bei < 30 Tage
  - `ssl_certificates` Tabelle

- **Erweiterte Service-Status-Felder**
  - `ssl_valid` - SSL-Gültigkeitsstatus
  - `ssl_expires_at` - Ablaufdatum
  - `ssl_days_remaining` - Restlaufzeit
  - `last_error` - Letzte Fehlermeldung
  - Erweiterte `service_status` Tabelle

#### Suche & Organisation

- **Globale Suche**
  - Services durchsuchen (Name, URL, Beschreibung, Notes)
  - Incidents durchsuchen
  - Tags filtern
  - Mindestlänge: 2 Zeichen
  - Performance-optimiert mit SQL LIKE
  - Limit: 50 Ergebnisse pro Kategorie
  - `/api/search` Endpoint

#### System & Verwaltung

- **Datenbank-Migrations-System**
  - `schema_version` Tabelle für Versions-Tracking
  - Automatische Migrations beim Start
  - Erkennt alte Schema-Versionen
  - Keine Datenverluste bei Updates
  - Rollback-fähig (manuell)
  - Version 4 Schema dokumentiert

- **Webhook-System**
  - `webhooks` und `webhook_logs` Tabellen
  - Event-basierte Webhooks
  - Unterstützt Discord, Slack, Custom APIs
  - HMAC-SHA256-Signaturen für Sicherheit
  - Events: service_down, service_up, incident_created, ssl_expiring_soon, etc.
  - Webhook-Retry-Logic
  - Asynchrone Webhook-Calls (Threading)
  - Last-Triggered-Tracking

- **Alert-System**
  - `alert_rules` Tabelle
  - Konfigurierbare Alert-Conditions
  - Multi-Channel-Notifications (Email, Webhook)
  - Cooldown-Mechanismus (verhindert Spam)
  - Event-Routing
  - Alert-Rule-Management via API

- **Automatische Backups mit Scheduler**
  - Schedule-Library Integration
  - Geplante Backups (täglich, wöchentlich)
  - Konfigurierbare Backup-Zeit (Standard: 02:00)
  - Automatische Backup-Rotation
  - Behalte X neueste Backups (Standard: 7)
  - Alte Backups automatisch löschen
  - Backup-Status in DB (`status`, `error_message`)
  - `/api/backup/*` Endpoints erweitert

- **Scheduled Tasks**
  - Health Checks (alle X Minuten)
  - Email-Queue-Processing (alle 5 Min)
  - Automatische Backups (täglich)
  - Session-Cleanup (stündlich)
  - Stats-Update (alle 10 Min)
  - Läuft in separatem Thread

#### Neue Datenbank-Tabellen

- `schema_version` - Migrations-Tracking
- `rate_limits` - Rate-Limiting-Daten
- `password_reset_tokens` - Reset-Tokens
- `email_queue` - Email-Warteschlange
- `webhooks` - Webhook-Konfigurationen
- `webhook_logs` - Webhook-Aufrufe
- `alert_rules` - Alert-Konfiguration
- `user_sessions` - Session-Management

#### Erweiterte Tabellen

- `users` - Neue Felder:
  - `email_verified`
  - `two_factor_enabled`
  - `two_factor_secret`
  - `failed_login_attempts`
  - `locked_until`
  - `last_activity`

- `services` - Neue Felder:
  - `health_check_enabled`
  - `health_check_url`
  - `health_check_method`
  - `health_check_interval`
  - `expected_status_code`
  - `ssl_check_enabled`

- `service_status` - Neue Felder:
  - `ssl_valid`
  - `ssl_expires_at`
  - `ssl_days_remaining`
  - `last_error`

- `service_stats` - Neue Felder:
  - `last_7d_uptime`
  - `last_24h_uptime`

- `incidents` - Neue Felder:
  - `notification_sent`

- `notifications` - Neue Felder:
  - `priority`
  - `action_url`

- `backups` - Neue Felder:
  - `status`
  - `error_message`

- `user_preferences` - Neue Felder:
  - `compact_mode`
  - `enable_animations`
  - `notification_sound`

#### API-Endpoints

**Neue Endpoints:**
- `POST /api/auth/forgot-password` - Passwort-Reset anfordern
- `POST /api/auth/reset-password` - Passwort mit Token zurücksetzen
- `GET /api/search` - Globale Suche
- `GET /api/webhooks` - Webhooks auflisten
- `POST /api/webhooks` - Webhook erstellen
- `DELETE /api/webhooks/<id>` - Webhook löschen
- `GET /api/system/status` - System-Status-Übersicht
- `POST /api/alert-rules` - Alert-Rule erstellen
- `GET /api/alert-rules` - Alert-Rules auflisten

**Erweiterte Endpoints:**
- `POST /api/auth/login` - Jetzt mit Rate Limiting (5/min)
- `GET /api/services` - Inkl. SSL-Status, 24h-Uptime
- `GET /api/analytics/dashboard` - Erweiterte Metriken

#### Deployment & Infrastructure

- **requirements-v4.txt**
  - Flask-Limiter 3.5.0
  - requests 2.31.0
  - schedule 1.2.0
  - cryptography 41.0.7
  - urllib3 2.1.0

- **Dockerfile-v4**
  - Multi-stage Build
  - Python 3.11-slim
  - Non-root User (homelab)
  - Health Check mit `/api/system/status`
  - SSL-Support
  - Optimierte Layers

- **docker-compose-v4.yml**
  - SMTP-Konfiguration via ENV
  - Health Check Intervalle
  - Backup-Konfiguration
  - Resource Limits
  - Volume-Mappings
  - Logging-Config
  - Network-Setup

- **unraid-template-v4.xml**
  - Komplette SMTP-Konfiguration
  - Health Check Settings
  - Backup-Settings
  - PUID/PGID-Support
  - WebUI-Integration
  - Icon & Beschreibung

#### Dokumentation

- **ANLEITUNG-V4.md** (1450+ Zeilen)
  - Komplette Feature-Dokumentation
  - Installation & Konfiguration
  - API-Referenz
  - Troubleshooting
  - Best Practices
  - FAQ
  - Migration-Guide von V3

- **CHANGELOG.md** (diese Datei)
  - Vollständige Versions-Historie
  - Detaillierte Änderungsliste

### 🔧 Geändert

- **Health Checks:** Von simplem Socket-Check zu echten HTTP-Requests
- **Session-Handling:** Von einfachen Sessions zu getrackte Sessions mit Timeout
- **Backup-System:** Von manuell zu automatisch mit Scheduling
- **Service-Status:** Erweitert um SSL-Informationen
- **Stats-Berechnung:** Jetzt 24h/7d/30d Uptime statt nur 30d

### 🐛 Behoben

- Keine Session-Timeouts in V3
- Keine Brute-Force-Protection
- Kein Passwort-Reset möglich
- Health Checks nur auf Port-Ebene
- Keine Email-Benachrichtigungen

### 🔒 Security

- Rate Limiting gegen Brute-Force
- Session-Timeouts (Inaktivität & Absolut)
- Account-Lock nach Fehlversuchen
- HMAC-Signaturen für Webhooks
- Token-basierter Passwort-Reset
- SSL-Zertifikat-Monitoring

### 📦 Dependencies

**Neu:**
- Flask-Limiter 3.5.0
- requests 2.31.0
- schedule 1.2.0
- cryptography 41.0.7

**Aktualisiert:**
- Flask 3.0.0 (keine Änderung)
- Flask-CORS 4.0.0 (keine Änderung)

### 🚀 Performance

- Asynchrone Webhook-Calls (Threading)
- Email-Queue für nicht-blockierende Emails
- Health Checks in separatem Thread
- Stats-Caching (10 Min)
- Optimierte SQL-Queries

### 📊 Statistiken

- **Zeilen Code (Backend):** 2600+ (V3: 1232)
- **API-Endpoints:** 30+ (V3: ~20)
- **Datenbank-Tabellen:** 26 (V3: 18)
- **Neue Tabellen:** 8
- **Erweiterte Tabellen:** 9
- **Dokumentation:** 1450+ Zeilen

---

## [3.0.0] - 2025-12-26 - ENTERPRISE EDITION

### ✨ Neu hinzugefügt

#### Multi-User-System

- **Benutzer-Verwaltung**
  - `users` Tabelle mit erweiterten Feldern
  - Username, Email, Full Name
  - Avatar-URL Support
  - Active/Inactive Status
  - Last Login Tracking

- **Rollen & Permissions**
  - `roles` Tabelle (admin, user, viewer)
  - `user_roles` Zuordnungs-Tabelle
  - Permission-System mit Decorators
  - `@permission_required()` Decorator
  - JSON-basierte Permission-Arrays

- **Session-basierte Authentifizierung**
  - Flask Sessions
  - Login/Logout-Funktionalität
  - Session-Persistenz (7 Tage)
  - Password-Change-Funktion

#### Erweiterte Sicherheit

- **Passkeys-Vorbereitung**
  - `passkeys` Tabelle (WebAuthn)
  - Credential-ID & Public-Key-Felder
  - Counter für Replay-Protection
  - (Volle Implementation in V4+)

- **Passwort-Hashing**
  - SHA-256 Hashing
  - Salted Passwords

#### Analytics & Insights

- **Analytics-System**
  - `analytics_events` Tabelle
  - Event-Tracking (Login, Service-Views, etc.)
  - IP-Adresse & User-Agent-Logging
  - Service-bezogene Events

- **Service-Statistiken**
  - `service_stats` Tabelle
  - Total Clicks & Views
  - Uptime Percentage (30d)
  - Average Response Time
  - `/api/analytics/dashboard` Endpoint
  - `/api/analytics/service/<id>` Endpoint

- **Uptime-History**
  - `uptime_history` Tabelle
  - Historische Uptime-Daten
  - Aggregation nach Tag
  - 7-Tage-Trends

#### Monitoring

- **Incident-Tracking**
  - `incidents` Tabelle
  - Start/End-Timestamps
  - Duration-Berechnung
  - Severity-Level (warning, critical)
  - Resolved-By-Tracking
  - Notes-Feld

- **SSL-Zertifikat-Vorbereitung**
  - `ssl_certificates` Tabelle
  - Domain, Issuer, Validity
  - Days-Until-Expiry
  - (Aktive Checks in V4)

- **Service-Status**
  - `service_status` Tabelle
  - Online/Offline-Status
  - Response-Time
  - Last-Checked-Timestamp
  - Total & Failed Checks Counter

#### Erweiterte Organisation

- **Tags-System**
  - `tags` Tabelle
  - `service_tags` Zuordnung
  - Farbige Tags
  - Multi-Tag-Support pro Service

- **Gruppen & Kategorien**
  - `groups` Tabelle
  - Hierarchische Gruppen (parent_id)
  - Icons & Farben
  - Sort-Order

- **Service-Erweiterungen**
  - Encrypted Notes
  - Background Images
  - Screenshot-URLs
  - Favorites-Flag
  - Owner & Creator-Tracking
  - Sort-Order

#### Customization

- **Theme-Builder**
  - `themes` Tabelle
  - Custom Colors (JSON)
  - Custom Fonts
  - Custom Spacing
  - Public/Private Themes
  - `/api/themes/custom` Endpoints

- **User-Preferences**
  - `user_preferences` Tabelle
  - Layout (Grid/List)
  - Items-per-Page
  - Default-View
  - Show Screenshots/Status
  - Custom Preferences (JSON)

- **Custom-Layouts**
  - `custom_layouts` Tabelle
  - Persönliche Dashboard-Layouts
  - Layout-Data (JSON)
  - Default-Layout-Flag

#### Backup & Sync

- **Backup-System**
  - `backups` Tabelle
  - Manual & Automatic Types
  - ZIP-basierte Backups
  - Datenbank + Screenshots
  - File-Size-Tracking
  - Created-By-Tracking
  - `/api/backup/create` Endpoint
  - `/api/backup/list` Endpoint
  - `/api/backup/download/<id>` Endpoint
  - `/api/backup/restore/<id>` Endpoint
  - Safety-Backup vor Restore

- **Audit-Log**
  - `audit_log` Tabelle
  - Action-Tracking (create, update, delete)
  - Entity-Type & ID
  - Old/New-Value (JSON)
  - IP-Adresse & Timestamp
  - `/api/audit-log` Endpoint

#### Notifications

- **Notification-System**
  - `notifications` Tabelle
  - User-spezifische Notifications
  - Type & Title
  - Service-Referenz
  - Read/Unread-Status
  - `/api/notifications` Endpoint
  - `/api/notifications/<id>/read` Endpoint

#### API-Erweiterungen

**Neue Endpoints:**
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/check`
- `POST /api/auth/change-password`
- `GET /api/users`
- `POST /api/users`
- `PUT /api/users/<id>`
- `DELETE /api/users/<id>`
- `GET /api/roles`
- `POST /api/roles`
- `GET /api/analytics/dashboard`
- `GET /api/analytics/service/<id>`
- `POST /api/backup/create`
- `GET /api/backup/list`
- `GET /api/backup/download/<id>`
- `POST /api/backup/restore/<id>`
- `POST /api/themes/custom`
- `GET /api/themes/custom`
- `GET /api/preferences`
- `PUT /api/preferences`
- `GET /api/notifications`
- `POST /api/notifications/<id>/read`
- `GET /api/audit-log`

#### Deployment

- **Dockerfile**
  - Python 3.11-slim
  - Non-root User
  - Health Check
  - Volumes für Persistenz

- **docker-compose.yml**
  - Production-ready Config
  - Resource Limits
  - Logging-Config

- **unraid-template.xml**
  - Unraid Community Apps Template
  - Path/Port-Mappings
  - PUID/PGID-Support

- **INSTALLATION.md**
  - Umfassende Installations-Anleitung
  - Docker, Unraid, Manual
  - Apache/Nginx-Configs
  - SSL-Setup

#### Dokumentation

- **ANLEITUNG-V3.md** (600+ Zeilen)
  - Feature-Übersicht
  - API-Dokumentation
  - Deployment-Guide

### 🔧 Geändert

- **Services-Tabelle:** Erweitert um viele neue Felder
- **Backend:** Von simplem Script zu Multi-User-System
- **Datenbank:** Von einfacher Struktur zu 18 Tabellen

### 📦 Dependencies

- Flask 3.0.0
- Flask-CORS 4.0.0
- SQLite3 (Standard)

---

## [2.0.0] - 2025-12-25

### ✨ Neu hinzugefügt

#### Backend

- **Flask-Backend** (`backend.py`)
  - RESTful API
  - SQLite-Datenbank
  - Session-Management
  - CORS-Support

- **Authentifizierung**
  - Login-System
  - Password-Hashing (SHA-256)
  - Session-basiert
  - Standard-User: admin/homelab2025

- **Datenbank-Tabellen**
  - `users` - Benutzer
  - `services` - Services
  - `service_status` - Status-Tracking
  - `categories` - Kategorien
  - `notes` - Notizen

#### Frontend

- **Login-Page** (`login.html`)
  - Login-Formular
  - Session-Management
  - Redirect nach Login

- **Dashboard-Erweiterungen** (`app-v2.js`)
  - Backend-Integration
  - API-Calls
  - Dynamisches Laden
  - Service-Management

#### Features

- **Service-Management**
  - Services über API verwalten
  - CRUD-Operationen
  - Kategorisierung
  - Status-Tracking

- **Notizen-System**
  - Service-bezogene Notizen
  - Markdown-Support
  - Timestamps

### 🔧 Geändert

- Frontend: Von rein Client-seitig zu Backend-integriert
- Daten-Persistenz: Von localStorage zu SQLite

---

## [1.0.0] - 2025-12-24

### ✨ Neu hinzugefügt

#### Initial Release

- **Frontend-Dashboard**
  - HTML/CSS/JavaScript
  - Responsive Design
  - Service-Karten
  - Drag & Drop

- **Features**
  - Service-Hinzufügen
  - Kategorien
  - Favoriten
  - Screenshots
  - localStorage-Persistenz

- **Design**
  - Dark Theme
  - Moderne UI
  - Card-Layout
  - Responsive Grid

#### Grundlegende Dateien

- `index.html` - Haupt-Dashboard
- `styles.css` - Styling
- `app.js` - Frontend-Logik

---

## [0.1.0] - 2025-12-24

### ✨ Neu hinzugefügt

- **Python Internet Speed Calculator** (`internet_speed_calculator.py`)
  - Unit-Konvertierung (bit/s, Byte/s, etc.)
  - Download-Zeit-Berechnung
  - CLI-Interface
  - Interaktives Menü

- **Projekt-Setup**
  - Git-Repository initialisiert
  - CLAUDE.md - AI Assistant Guide
  - README-Grundlagen

---

## Legende

- ✨ **Neu hinzugefügt** - Neue Features
- 🔧 **Geändert** - Änderungen an bestehenden Features
- 🐛 **Behoben** - Bugfixes
- 🔒 **Security** - Sicherheits-Verbesserungen
- 📦 **Dependencies** - Dependency-Updates
- 🗑️ **Entfernt** - Entfernte Features
- 🚀 **Performance** - Performance-Verbesserungen

---

## Versionierung

Dieses Projekt folgt [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - Breaking Changes
- **MINOR** (0.X.0) - Neue Features (backward-compatible)
- **PATCH** (0.0.X) - Bugfixes (backward-compatible)

---

**Hinweis:** Für detaillierte Feature-Dokumentation siehe jeweilige ANLEITUNG-VX.md Dateien.
