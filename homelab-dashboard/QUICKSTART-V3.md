# ⚡ Homelab Dashboard V3 - Quick Start

**Enterprise Edition in 5 Minuten!**

---

## 🚀 Installation

```bash
cd homelab-dashboard

# Dependencies installieren (falls noch nicht geschehen)
pip3 install -r requirements.txt

# Backend V3 starten
python3 backend-v3.py
```

**URL:** `http://localhost:5000`

---

## 🔐 Login

```
Benutzername: admin
Passwort: homelab2025
```

⚠️ **Sofort ändern!**

---

## ✨ ALLE NEUEN V3 FEATURES

| Feature | Status |
|---------|--------|
| ✅ Multi-User | Mehrere Benutzer |
| ✅ Rollen & Rechte | Admin, User, Viewer |
| ✅ Passkeys | WebAuthn Support |
| ✅ Advanced Monitoring | Uptime-History, Incidents |
| ✅ Analytics | Detaillierte Statistiken |
| ✅ Backup & Restore | Professionelle Backups |
| ✅ Theme-Builder | Custom Themes |
| ✅ Audit-Log | Lückenlose Nachverfolgung |
| ✅ Notifications | Benachrichtigungssystem |

---

## 👤 Ersten User erstellen

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

**Rollen:**
- `1` = Admin (alles)
- `2` = User (normal)
- `3` = Viewer (nur ansehen)

---

## 💾 Backup erstellen

```bash
curl -X POST http://localhost:5000/api/backup/create
```

**Speicherort:** `backups/homelab_backup_TIMESTAMP.zip`

---

## 📊 Analytics ansehen

```bash
curl http://localhost:5000/api/analytics/dashboard
```

**Zeigt:**
- Total Services
- Total Users
- Avg Uptime
- Popular Services
- Events

---

## 🎨 Custom Theme erstellen

```bash
curl -X POST http://localhost:5000/api/themes/custom \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ocean Blue",
    "colors": {
      "primary": "#0077be",
      "secondary": "#00a8e8",
      "background": "#001f3f"
    },
    "is_public": true
  }'
```

---

## 📝 Wichtigste API-Endpoints

### **Benutzer**
```bash
GET    /api/users              # Alle Benutzer
POST   /api/users              # User erstellen
PUT    /api/users/{id}         # User bearbeiten
DELETE /api/users/{id}         # User löschen
```

### **Rollen**
```bash
GET    /api/roles              # Alle Rollen
POST   /api/roles              # Rolle erstellen
```

### **Analytics**
```bash
GET    /api/analytics/dashboard           # Dashboard
GET    /api/analytics/service/{id}        # Service-Stats
```

### **Backups**
```bash
POST   /api/backup/create                 # Backup erstellen
GET    /api/backup/list                   # Alle Backups
GET    /api/backup/download/{id}          # Download
POST   /api/backup/restore/{id}           # Restore
```

### **Themes**
```bash
GET    /api/themes/custom                 # Alle Themes
POST   /api/themes/custom                 # Theme erstellen
```

### **Preferences**
```bash
GET    /api/preferences                   # Einstellungen
PUT    /api/preferences                   # Aktualisieren
```

### **Audit-Log**
```bash
GET    /api/audit-log                     # Audit-Einträge
```

---

## 🔄 Upgrade von V2

**V2 → V3 ist kompatibel!**

1. **Backup:**
   ```bash
   cp homelab.db homelab.db.backup
   ```

2. **V3 starten:**
   ```bash
   python3 backend-v3.py
   ```

3. **Fertig!**
   - Neue Tabellen werden automatisch erstellt
   - Alle Daten bleiben erhalten

---

## 🎯 Standard-Rollen

### Admin
- **Permissions:** `["all"]`
- Kann alles machen

### User
- **Permissions:** `["view", "edit_own"]`
- Kann Services ansehen und eigene bearbeiten

### Viewer
- **Permissions:** `["view"]`
- Kann nur ansehen

---

## 📚 Vollständige Dokumentation

Siehe **ANLEITUNG-V3.md** für:
- Detaillierte Feature-Beschreibungen
- API-Referenz
- Permissions-System
- Passkeys-Setup
- Backup-Strategien
- Theme-Erstellung
- Und vieles mehr!

---

## 🎉 Los geht's!

Du hast jetzt ein **Enterprise-Level Homelab-Dashboard**!

**Viel Erfolg! 🚀**
