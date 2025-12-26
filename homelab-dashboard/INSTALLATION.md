# 📦 Homelab Dashboard V3 - Installation Guide

**Vollständige Installations-Anleitung für alle Plattformen**

---

## 📋 Inhaltsverzeichnis

1. [Schnellstart (empfohlen)](#schnellstart-docker-compose)
2. [Docker Installation](#docker-installation)
3. [Docker Compose](#docker-compose-empfohlen)
4. [Unraid Installation](#unraid-installation)
5. [Manuelle Installation](#manuelle-installation)
6. [Apache Reverse Proxy](#apache-reverse-proxy)
7. [Nginx Reverse Proxy](#nginx-reverse-proxy)
8. [Systemd Service](#systemd-service)
9. [SSL/TLS Setup](#ssltls-setup)
10. [Erste Schritte nach Installation](#erste-schritte)
11. [Troubleshooting](#troubleshooting)

---

## 🚀 Schnellstart (Docker Compose)

**Die einfachste Methode!**

```bash
# 1. Repository klonen
git clone <repository-url>
cd homelab-dashboard

# 2. Data-Verzeichnis erstellen
mkdir -p data/{backups,screenshots}

# 3. Docker Compose starten
docker-compose up -d

# 4. Logs ansehen
docker-compose logs -f
```

**Fertig!** Dashboard läuft auf: `http://localhost:5000`

**Login:**
- Username: `admin`
- Passwort: `homelab2025`

⚠️ **WICHTIG**: Passwort sofort ändern!

---

## 🐳 Docker Installation

### Option 1: Mit vorgefertigtem Image (wenn verfügbar)

```bash
# Image pullen
docker pull homelab-dashboard:latest

# Container starten
docker run -d \
  --name homelab-dashboard \
  --restart unless-stopped \
  -p 5000:5000 \
  -v $(pwd)/data/homelab.db:/app/homelab.db \
  -v $(pwd)/data/backups:/app/backups \
  -v $(pwd)/data/screenshots:/app/screenshots \
  homelab-dashboard:latest
```

### Option 2: Image selbst bauen

```bash
# Repository klonen
git clone <repository-url>
cd homelab-dashboard

# Image bauen
docker build -t homelab-dashboard:latest .

# Container starten
docker run -d \
  --name homelab-dashboard \
  --restart unless-stopped \
  -p 5000:5000 \
  -v $(pwd)/data/homelab.db:/app/homelab.db \
  -v $(pwd)/data/backups:/app/backups \
  -v $(pwd)/data/screenshots:/app/screenshots \
  homelab-dashboard:latest
```

### Container-Verwaltung

```bash
# Logs ansehen
docker logs -f homelab-dashboard

# Container stoppen
docker stop homelab-dashboard

# Container starten
docker start homelab-dashboard

# Container neustarten
docker restart homelab-dashboard

# Container löschen
docker rm -f homelab-dashboard

# In Container einloggen (Debug)
docker exec -it homelab-dashboard sh
```

---

## 📦 Docker Compose (Empfohlen)

### docker-compose.yml

Die Datei ist bereits im Repository enthalten!

```yaml
version: '3.8'

services:
  homelab-dashboard:
    build: .
    container_name: homelab-dashboard
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./data/homelab.db:/app/homelab.db
      - ./data/backups:/app/backups
      - ./data/screenshots:/app/screenshots
    environment:
      - FLASK_ENV=production
    networks:
      - homelab

networks:
  homelab:
    driver: bridge
```

### Installation

```bash
# 1. Repository klonen
git clone <repository-url>
cd homelab-dashboard

# 2. Verzeichnisse erstellen
mkdir -p data/backups data/screenshots

# 3. Starten
docker-compose up -d

# 4. Status prüfen
docker-compose ps

# 5. Logs ansehen
docker-compose logs -f

# 6. Stoppen
docker-compose down

# 7. Update (neue Version)
docker-compose pull
docker-compose up -d --build
```

### Ports ändern

In `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Ändere 8080 zu deinem gewünschten Port
```

### Ressourcen-Limits

Bereits in `docker-compose.yml` enthalten:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

---

## 📦 Unraid Installation

### Methode 1: Template installieren (Einfachste Methode)

1. **Template hinzufügen:**
   - Öffne Unraid WebUI
   - Gehe zu **Docker** → **Add Container**
   - Klicke auf **Template repositories**
   - Füge hinzu: `https://github.com/YOUR-USERNAME/homelab-dashboard`

2. **Container installieren:**
   - Suche nach "Homelab Dashboard"
   - Klicke auf **Install**
   - Passe Einstellungen an (siehe unten)
   - Klicke auf **Apply**

### Methode 2: Manuell (Custom Container)

1. **Gehe zu Docker → Add Container**

2. **Basis-Einstellungen:**
   ```
   Name: Homelab-Dashboard
   Repository: homelab-dashboard:latest
   Network Type: Bridge
   ```

3. **Port-Mapping:**
   ```
   Container Port: 5000
   Host Port: 5000
   ```

4. **Pfad-Mappings:**
   ```
   Container Path: /app/homelab.db
   Host Path: /mnt/user/appdata/homelab-dashboard/homelab.db
   Access Mode: Read/Write

   Container Path: /app/backups
   Host Path: /mnt/user/appdata/homelab-dashboard/backups
   Access Mode: Read/Write

   Container Path: /app/screenshots
   Host Path: /mnt/user/appdata/homelab-dashboard/screenshots
   Access Mode: Read/Write
   ```

5. **Umgebungsvariablen:**
   ```
   FLASK_ENV: production
   PUID: 99
   PGID: 100
   ```

6. **Docker Hub Alternative (wenn Image verfügbar):**
   ```
   Repository: username/homelab-dashboard:latest
   ```

### Methode 3: Build on Unraid

Falls kein vorgefertigtes Image:

```bash
# SSH zu Unraid
ssh root@unraid-ip

# Repository klonen
cd /mnt/user/appdata
git clone <repository-url> homelab-dashboard
cd homelab-dashboard

# Image bauen
docker build -t homelab-dashboard:latest .

# Dann über WebUI hinzufügen (Methode 2)
```

### Unraid-Pfade

**Empfohlene Pfade:**
```
Database: /mnt/user/appdata/homelab-dashboard/homelab.db
Backups:  /mnt/user/appdata/homelab-dashboard/backups
Screenshots: /mnt/user/appdata/homelab-dashboard/screenshots
```

### Auto-Start

In Docker-Container-Einstellungen:
```
Restart Policy: unless-stopped
```

---

## 💻 Manuelle Installation

### Voraussetzungen

```bash
# System-Pakete (Ubuntu/Debian)
sudo apt update
sudo apt install -y python3 python3-pip git

# System-Pakete (CentOS/RHEL)
sudo yum install -y python3 python3-pip git

# System-Pakete (Arch)
sudo pacman -S python python-pip git
```

### Installation

```bash
# 1. Repository klonen
git clone <repository-url>
cd homelab-dashboard

# 2. Virtual Environment erstellen (empfohlen)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# 3. Dependencies installieren
pip3 install -r requirements.txt

# 4. Verzeichnisse erstellen
mkdir -p backups screenshots

# 5. Backend starten
python3 backend-v3.py
```

**Dashboard läuft auf:** `http://localhost:5000`

### Im Hintergrund laufen lassen

```bash
# Mit nohup
nohup python3 backend-v3.py > homelab.log 2>&1 &

# Mit screen
screen -S homelab
python3 backend-v3.py
# Ctrl+A, dann D zum Detachen

# Mit tmux
tmux new -s homelab
python3 backend-v3.py
# Ctrl+B, dann D zum Detachen
```

---

## 🌐 Apache Reverse Proxy

### Installation

```bash
# Apache installieren (falls nicht vorhanden)
sudo apt install apache2

# Module aktivieren
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_wstunnel
sudo a2enmod headers
sudo a2enmod rewrite
sudo a2enmod ssl  # für HTTPS
```

### Konfiguration

```bash
# Config-Datei kopieren
sudo cp apache-config.conf /etc/apache2/sites-available/homelab-dashboard.conf

# ODER manuell erstellen:
sudo nano /etc/apache2/sites-available/homelab-dashboard.conf
# (Inhalt siehe apache-config.conf)

# Site aktivieren
sudo a2ensite homelab-dashboard.conf

# Apache testen
sudo apache2ctl configtest

# Apache neuladen
sudo systemctl reload apache2
```

### Hosts-Datei (optional)

Für lokalen Zugriff via `homelab.local`:

```bash
# /etc/hosts bearbeiten
sudo nano /etc/hosts

# Hinzufügen:
127.0.0.1  homelab.local
```

**Zugriff:** `http://homelab.local`

---

## 🔒 Nginx Reverse Proxy

### Installation

```bash
# Nginx installieren
sudo apt install nginx

# Oder auf CentOS/RHEL
sudo yum install nginx
```

### Konfiguration

```bash
# Config-Datei kopieren
sudo cp nginx-config.conf /etc/nginx/sites-available/homelab-dashboard

# Symlink erstellen
sudo ln -s /etc/nginx/sites-available/homelab-dashboard /etc/nginx/sites-enabled/

# Nginx testen
sudo nginx -t

# Nginx neuladen
sudo systemctl reload nginx
```

### Hosts-Datei (optional)

```bash
sudo nano /etc/hosts

# Hinzufügen:
127.0.0.1  homelab.local
```

**Zugriff:** `http://homelab.local`

---

## ⚙️ Systemd Service

Für automatischen Start beim Booten:

### Service-Datei erstellen

```bash
sudo nano /etc/systemd/system/homelab-dashboard.service
```

**Inhalt:**
```ini
[Unit]
Description=Homelab Dashboard V3
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/homelab-dashboard
Environment="PATH=/opt/homelab-dashboard/venv/bin"
ExecStart=/opt/homelab-dashboard/venv/bin/python3 backend-v3.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Service aktivieren

```bash
# Daemon neu laden
sudo systemctl daemon-reload

# Service aktivieren (Auto-Start)
sudo systemctl enable homelab-dashboard

# Service starten
sudo systemctl start homelab-dashboard

# Status prüfen
sudo systemctl status homelab-dashboard

# Logs ansehen
sudo journalctl -u homelab-dashboard -f

# Service stoppen
sudo systemctl stop homelab-dashboard

# Service neustarten
sudo systemctl restart homelab-dashboard
```

---

## 🔐 SSL/TLS Setup

### Let's Encrypt (Empfohlen)

#### Mit Certbot (Apache)

```bash
# Certbot installieren
sudo apt install certbot python3-certbot-apache

# Zertifikat erstellen
sudo certbot --apache -d homelab.yourdomain.com

# Auto-Renewal testen
sudo certbot renew --dry-run
```

#### Mit Certbot (Nginx)

```bash
# Certbot installieren
sudo apt install certbot python3-certbot-nginx

# Zertifikat erstellen
sudo certbot --nginx -d homelab.yourdomain.com
```

### Self-Signed Certificate

Für lokales Homelab:

```bash
# Zertifikat erstellen
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/homelab.key \
  -out /etc/ssl/certs/homelab.crt

# Während der Erstellung:
Country: DE
State: NRW
City: Deine Stadt
Organization: Homelab
Common Name: homelab.local
```

**Dann in Apache/Nginx Config verwenden** (siehe Beispiel-Configs)

---

## 🎯 Erste Schritte

### 1. Dashboard öffnen

```
http://localhost:5000
```

Oder mit Reverse Proxy:
```
http://homelab.local
```

### 2. Login

```
Username: admin
Passwort: homelab2025
```

### 3. Passwort ändern

**Über API:**
```bash
curl -X POST http://localhost:5000/api/auth/change-password \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "homelab2025",
    "new_password": "dein-neues-sicheres-passwort"
  }'
```

### 4. Ersten User erstellen

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "sicheres-passwort",
    "full_name": "John Doe",
    "email": "john@example.com",
    "role_ids": [2]
  }'
```

### 5. Ersten Service hinzufügen

Über WebUI:
1. Klicke auf **+ Button** (unten rechts)
2. Fülle Formular aus
3. Speichern

### 6. Backup erstellen

```bash
curl -X POST http://localhost:5000/api/backup/create
```

---

## 🔧 Troubleshooting

### Container startet nicht

```bash
# Logs prüfen
docker logs homelab-dashboard

# Oder mit Docker Compose
docker-compose logs

# Häufige Ursachen:
# - Port 5000 bereits belegt
# - Volumes nicht korrekt gemountet
# - Permissions-Probleme
```

**Lösung Port-Konflikt:**
```bash
# Port ändern in docker-compose.yml
ports:
  - "8080:5000"  # Statt 5000:5000
```

### Permission-Fehler

```bash
# Volumes-Rechte korrigieren
sudo chown -R 1000:1000 data/

# Oder für Unraid
sudo chown -R 99:100 /mnt/user/appdata/homelab-dashboard/
```

### Datenbank-Fehler

```bash
# Datenbank neu initialisieren
docker exec -it homelab-dashboard python3 -c "from backend-v3 import init_db; init_db()"
```

### Backend erreichbar aber Login geht nicht

```bash
# Prüfe ob Session-Cookies funktionieren
# Chrome DevTools → Application → Cookies

# Session-Secret neu generieren
# In docker-compose.yml:
environment:
  - SECRET_KEY=neuer-zufälliger-key
```

### Nginx 502 Bad Gateway

```bash
# Prüfe ob Backend läuft
curl http://localhost:5000

# Nginx-Logs prüfen
sudo tail -f /var/log/nginx/error.log

# Häufig: SELinux blockiert
sudo setsebool -P httpd_can_network_connect 1
```

### Apache funktioniert nicht

```bash
# Module aktiviert?
sudo a2enmod proxy proxy_http headers rewrite

# Config-Test
sudo apache2ctl configtest

# Logs prüfen
sudo tail -f /var/log/apache2/error.log
```

### Update auf neue Version

**Docker:**
```bash
# Image neu bauen
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Manuell:**
```bash
git pull
pip3 install -r requirements.txt --upgrade
sudo systemctl restart homelab-dashboard
```

---

## 📊 Ressourcen-Anforderungen

### Minimum

- **CPU**: 1 Core
- **RAM**: 256 MB
- **Disk**: 100 MB (+ Backups/Screenshots)

### Empfohlen

- **CPU**: 2 Cores
- **RAM**: 512 MB
- **Disk**: 1 GB (+ Backups/Screenshots)

### Docker Resource Limits

In `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

---

## 🌐 Netzwerk-Konfiguration

### Firewall (ufw)

```bash
# Port öffnen
sudo ufw allow 5000/tcp

# Oder für Reverse Proxy
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### Firewall (firewalld)

```bash
# Port öffnen
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

---

## 🎉 Fertig!

Du hast jetzt ein **professionelles Homelab-Dashboard** installiert!

**Nächste Schritte:**
1. Passwort ändern
2. Weitere Benutzer erstellen
3. Services hinzufügen
4. Backup-Routine einrichten
5. HTTPS einrichten (Production)

**Viel Erfolg! 🚀**
