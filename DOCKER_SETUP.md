# 🐳 Docker Hub Setup - Homelab Dashboard V4

**Komplette Anleitung um das Docker Image zu veröffentlichen und in Unraid zu nutzen**

---

## 📋 Inhaltsverzeichnis

1. [Übersicht](#übersicht)
2. [Docker Hub Account erstellen](#docker-hub-account-erstellen)
3. [GitHub Secrets konfigurieren](#github-secrets-konfigurieren)
4. [Automatischen Build triggern](#automatischen-build-triggern)
5. [Manuellen Build (optional)](#manuellen-build-optional)
6. [Unraid-Template anpassen](#unraid-template-anpassen)
7. [Image in Unraid nutzen](#image-in-unraid-nutzen)
8. [Troubleshooting](#troubleshooting)

---

## 📖 Übersicht

**Was wird gemacht:**
1. Docker Hub Account erstellen (kostenlos)
2. GitHub Repository mit Docker Hub verbinden
3. Automatischer Build bei jedem Push
4. Fertiges Image in Unraid nutzen

**Vorteile:**
- ✅ Kein lokales Bauen nötig
- ✅ Multi-Platform-Support (AMD64, ARM64, ARMv7)
- ✅ Automatische Updates
- ✅ Öffentlich verfügbar

---

## 🚀 Schritt 1: Docker Hub Account erstellen

### 1.1 Registrierung

1. Gehe zu: **https://hub.docker.com/signup**
2. **Email**, **Username**, **Passwort** eingeben
3. Email bestätigen

**Wichtig:** Merke dir deinen **Username** - z.B. `hannesruhnke`

### 1.2 Access Token erstellen

1. Einloggen: **https://hub.docker.com**
2. **Account Settings** → **Security** → **New Access Token**
3. Name: `GitHub Actions`
4. Permissions: **Read, Write, Delete**
5. **Generate** → Token kopieren (wird nur EINMAL angezeigt!)

**Token speichern:** Du brauchst ihn für GitHub!

Beispiel:
```
dckr_pat_abc123xyz456...
```

---

## 🔐 Schritt 2: GitHub Secrets konfigurieren

### 2.1 Repository Secrets hinzufügen

1. Gehe zu deinem GitHub Repository
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret** klicken

### 2.2 Secrets erstellen

**Secret 1: DOCKER_USERNAME**
- Name: `DOCKER_USERNAME`
- Value: Dein Docker Hub Username (z.B. `hannesruhnke`)
- **Add secret**

**Secret 2: DOCKER_PASSWORD**
- Name: `DOCKER_PASSWORD`
- Value: Dein Docker Hub Access Token (von Schritt 1.2)
- **Add secret**

**Ergebnis:**
```
✅ DOCKER_USERNAME = hannesruhnke
✅ DOCKER_PASSWORD = dckr_pat_abc123xyz456...
```

---

## 🎯 Schritt 3: Automatischen Build triggern

### 3.1 Dateien aktualisieren

**WICHTIG:** Ersetze Platzhalter in folgenden Dateien:

#### **1. unraid-template-v4-dockerhub.xml**

Ersetze `YOUR_DOCKERHUB_USERNAME` und `YOUR_GITHUB_USERNAME`:

```xml
<!-- Vor: -->
<Repository>YOUR_DOCKERHUB_USERNAME/homelab-dashboard:latest</Repository>
<Registry>https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/homelab-dashboard</Registry>

<!-- Nach (Beispiel): -->
<Repository>hannesruhnke/homelab-dashboard:latest</Repository>
<Registry>https://hub.docker.com/r/hannesruhnke/homelab-dashboard</Registry>
```

Alle Vorkommen ersetzen:
```bash
# In der Datei ersetzen (Linux/Mac):
sed -i 's/YOUR_DOCKERHUB_USERNAME/hannesruhnke/g' homelab-dashboard/unraid-template-v4-dockerhub.xml
sed -i 's/YOUR_GITHUB_USERNAME/HannesRuhnke/g' homelab-dashboard/unraid-template-v4-dockerhub.xml

# Oder manuell mit einem Editor
```

#### **2. DOCKER_README.md**

Gleiches Vorgehen - ersetze alle Platzhalter.

### 3.2 Änderungen committen

```bash
# Status prüfen
git status

# Dateien stagen
git add .github/workflows/docker-build.yml
git add homelab-dashboard/build-docker.sh
git add homelab-dashboard/DOCKER_README.md
git add homelab-dashboard/unraid-template-v4-dockerhub.xml
git add DOCKER_SETUP.md

# Commit
git commit -m "feat: Docker Hub Integration mit GitHub Actions

- GitHub Actions Workflow für automatischen Build
- Multi-Platform Support (amd64, arm64, armv7)
- Unraid-Template für Docker Hub Image
- Build-Skript für manuellen Build
- Docker Hub README

Images werden automatisch gebaut und gepusht bei jedem Push zu main/master!"

# Push
git push
```

### 3.3 Build beobachten

1. Gehe zu GitHub Repository
2. **Actions** Tab
3. Workflow **"Build and Push Docker Image"** sollte laufen

**Dauer:** 15-30 Minuten (Multi-Platform-Build)

**Status:**
- 🟡 Gelb = Läuft
- 🟢 Grün = Erfolgreich
- 🔴 Rot = Fehler (siehe Logs)

### 3.4 Docker Hub prüfen

Nach erfolgreichem Build:

1. Gehe zu: `https://hub.docker.com/r/hannesruhnke/homelab-dashboard`
2. Sollte **3 Tags** zeigen:
   - `latest`
   - `v4`
   - `v4-ultimate`

**Beispiel:**
```
https://hub.docker.com/r/hannesruhnke/homelab-dashboard
```

---

## 🛠️ Schritt 4: Manueller Build (Optional)

Falls du das Image **lokal bauen** willst (z.B. für Tests):

### 4.1 Build-Skript nutzen

```bash
cd homelab-dashboard

# Skript ausführbar machen
chmod +x build-docker.sh

# Starten
./build-docker.sh
```

### 4.2 Interaktive Optionen

Das Skript fragt:

**Docker Hub Username:**
```
? Docker Hub Username: hannesruhnke
```

**Login:**
```
Docker Hub Login...
Password: [Dein Docker Hub Passwort]
```

**Build-Option:**
```
1) Nur lokal bauen (schnell, nur amd64)
2) Multi-Platform bauen und pushen (langsam, amd64+arm64+armv7)  ← Für Unraid
3) Nur pushen (Image bereits gebaut)

Auswahl [1-3]: 2
```

**Option 2 wählen** für vollständiges Multi-Platform-Image!

**Dauer:** 10-20 Minuten

---

## 📦 Schritt 5: Unraid-Template anpassen

### 5.1 Template-URL erstellen

Dein Unraid-Template liegt auf GitHub:

```
https://raw.githubusercontent.com/HannesRuhnke/Claude-main/main/homelab-dashboard/unraid-template-v4-dockerhub.xml
```

**Beispiel:**
```
https://raw.githubusercontent.com/HannesRuhnke/Claude-main/main/homelab-dashboard/unraid-template-v4-dockerhub.xml
```

### 5.2 In Community Applications teilen (Optional)

Falls du das Template mit der Community teilen willst:

1. Fork: **https://github.com/Squidly271/CA-Templates**
2. Dein Template hinzufügen: `templates/homelab-dashboard.xml`
3. Pull Request erstellen

---

## 🎉 Schritt 6: Image in Unraid nutzen

### Option 1: Direkte Installation

1. Unraid WebUI öffnen
2. **Docker** Tab
3. **Add Container**
4. Bei **Repository:** eingeben:
   ```
   hannesruhnke/homelab-dashboard:latest
   ```
   Beispiel: `hannesruhnke/homelab-dashboard:latest`

5. **Port Mappings:**
   - Container Port: `5000`
   - Host Port: `5000`

6. **Volume Mappings:**
   - Container: `/app/homelab.db` → Host: `/mnt/user/appdata/homelab-dashboard/homelab.db`
   - Container: `/app/backups` → Host: `/mnt/user/appdata/homelab-dashboard/backups`
   - Container: `/app/screenshots` → Host: `/mnt/user/appdata/homelab-dashboard/screenshots`

7. **Environment Variables** (für Email):
   - `SMTP_USER=your-email@gmail.com`
   - `SMTP_PASSWORD=your-app-password`

8. **Apply** klicken

### Option 2: Template nutzen

1. **Community Applications** öffnen
2. **Template URL** hinzufügen:
   - Settings → Template Repositories
   - URL hinzufügen: `https://raw.githubusercontent.com/HannesRuhnke/Claude-main/main/homelab-dashboard/unraid-template-v4-dockerhub.xml`

3. **Apps** → Suche "Homelab Dashboard"
4. **Install** klicken
5. SMTP-Daten konfigurieren
6. **Apply**

### Option 3: docker-compose (Unraid 6.12+)

```yaml
# docker-compose.yml
version: '3.8'

services:
  homelab-dashboard:
    image: hannesruhnke/homelab-dashboard:latest
    container_name: homelab-dashboard
    ports:
      - "5000:5000"
    environment:
      - SMTP_USER=your-email@gmail.com
      - SMTP_PASSWORD=your-app-password
      - AUTO_BACKUP_ENABLED=true
    volumes:
      - /mnt/user/appdata/homelab-dashboard/homelab.db:/app/homelab.db
      - /mnt/user/appdata/homelab-dashboard/backups:/app/backups
      - /mnt/user/appdata/homelab-dashboard/screenshots:/app/screenshots
    restart: unless-stopped
```

```bash
# Starten
docker-compose up -d
```

---

## ✅ Schritt 7: Dashboard öffnen

Nach Installation:

1. Browser öffnen
2. URL: `http://UNRAID-IP:5000`
3. Login:
   - Username: `admin`
   - Passwort: `homelab2025`
4. **Passwort sofort ändern!**

---

## 🔧 Troubleshooting

### Problem: GitHub Actions Build schlägt fehl

**Fehler: "Error: Username and password required"**

**Lösung:**
```bash
# Prüfe GitHub Secrets:
# Settings → Secrets and variables → Actions

# Müssen vorhanden sein:
✅ DOCKER_USERNAME
✅ DOCKER_PASSWORD

# Neu erstellen falls falsch
```

**Fehler: "permission denied"**

**Lösung:**
```bash
# Buildx neu initialisieren (lokal)
docker buildx create --use
docker buildx inspect --bootstrap
```

### Problem: Image nicht auf Docker Hub

**Prüfen:**
1. GitHub Actions Log anschauen
2. Docker Hub Account prüfen: https://hub.docker.com/repositories

**Lösung:**
```bash
# Manuell pushen:
cd homelab-dashboard
./build-docker.sh
# Option 2 wählen
```

### Problem: Unraid kann Image nicht pullen

**Fehler:** "Error: manifest unknown"

**Lösung:**
1. Prüfe Repository-Name:
   ```
   # Richtig:
   hannesruhnke/homelab-dashboard:latest

   # Falsch:
   homelab-dashboard:latest
   docker.io/homelab-dashboard:latest
   ```

2. Auf Docker Hub prüfen ob Image existiert

3. In Unraid:
   ```bash
   # Terminal öffnen
   docker pull hannesruhnke/homelab-dashboard:latest
   ```

### Problem: Multi-Platform Build zu langsam

**Optimierung:**

```yaml
# .github/workflows/docker-build.yml
# Nur amd64 bauen (schneller):
platforms: linux/amd64

# Statt:
platforms: linux/amd64,linux/arm64,linux/arm/v7
```

### Problem: SMTP funktioniert nicht

**Prüfen:**
```bash
# In Unraid Terminal:
docker exec homelab-dashboard env | grep SMTP

# Sollte zeigen:
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=***
```

**Lösung:**
- Gmail: App-Passwort erstellen (https://myaccount.google.com/security)
- Outlook: App-Passwort erstellen
- 2FA muss aktiviert sein!

---

## 📊 Image-Informationen

### Tags

| Tag | Beschreibung | Update |
|-----|--------------|--------|
| `latest` | Neueste Version von main/master | Bei jedem Push |
| `v4` | V4 Ultimate | Bei jedem Push |
| `v4-ultimate` | V4 Ultimate | Bei jedem Push |
| `v4.0.0` | Spezifische Version | Bei Git Tag |

### Plattformen

| Plattform | Architektur | Geräte |
|-----------|-------------|--------|
| `linux/amd64` | x86_64 | Standard-PCs, Server, Unraid |
| `linux/arm64` | ARM 64-bit | Raspberry Pi 4, ARM-Server |
| `linux/arm/v7` | ARM 32-bit | Raspberry Pi 3 |

### Image-Größe

- **Compressed:** ~150 MB
- **Uncompressed:** ~400 MB

---

## 🎯 Zusammenfassung

**Was du gemacht hast:**

1. ✅ Docker Hub Account erstellt
2. ✅ GitHub Secrets konfiguriert
3. ✅ Automatischen Build aktiviert
4. ✅ Image auf Docker Hub veröffentlicht
5. ✅ Unraid-Template angepasst
6. ✅ Dashboard in Unraid installiert

**Ergebnis:**

- 🎉 **Fertiges Docker Image:** `hannesruhnke/homelab-dashboard:latest`
- 🎉 **Automatische Updates:** Bei jedem Push
- 🎉 **Multi-Platform:** AMD64, ARM64, ARMv7
- 🎉 **Unraid-Ready:** Direkt installierbar

---

## 🚀 Next Steps

1. **Services hinzufügen** im Dashboard
2. **Health Checks aktivieren**
3. **Email-Notifications testen**
4. **Webhooks einrichten** (Discord/Slack)
5. **Backups konfigurieren**

---

## 📞 Support

**Probleme?**

1. Check GitHub Actions Logs
2. Check Docker Hub Repository
3. Check Unraid Container Logs: `docker logs homelab-dashboard`

**GitHub Issues:** https://github.com/hannesruhnke/Claude-main/issues

---

**Viel Erfolg mit deinem Homelab Dashboard! 🎉**
