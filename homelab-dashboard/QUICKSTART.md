# 🚀 Homelab Dashboard V2 - Quick Start

**In 3 Minuten zum laufenden Dashboard mit allen Features!**

---

## ⚡ Schnellstart

### 1. Dependencies installieren

```bash
cd homelab-dashboard
pip3 install -r requirements.txt
```

### 2. Dashboard starten

```bash
./start.sh
```

Oder manuell:
```bash
python3 backend.py
```

### 3. Im Browser öffnen

```
http://localhost:5000
```

---

## 🔐 Standard-Zugangsdaten

```
Benutzername: admin
Passwort: homelab2025
```

⚠️ **Ändere das Passwort nach dem ersten Login!**

---

## ✨ Alle neuen Features

| Feature | Beschreibung | Wie verwenden |
|---------|-------------|---------------|
| **Status-Checks** | Prüfe ob Services online sind | Klick auf🔄-Symbol |
| **Favoriten** | Markiere wichtige Services | Klick auf ⭐-Symbol |
| **Notizen** | Füge Notizen zu Services hinzu | Beim Erstellen/Bearbeiten |
| **Tags** | Tagge Services | Über API |
| **Gruppen** | Organisiere in Ordnern | Über API/Dropdown |
| **Drag & Drop** | Verschiebe Services | Ziehen & Ablegen |
| **Custom Themes** | Eigene Farb-Themes | Über API |

---

## 📝 Ersten Service hinzufügen

1. Klicke **+ Button** (unten rechts)
2. Fülle aus:
   - Name: `Plex`
   - URL: `http://192.168.1.100:32400`
   - Icon: `fa-play`
   - Kategorie: `Media`
   - Farbe: `Orange`
   - Notizen: `Mein Media Server`
3. **Speichern**

---

## 🎯 Wichtigste Tastatur-Shortcuts

- `Strg/Cmd + K` → Suche fokussieren
- `Escape` → Modals schließen

---

## 🔧 Häufige Probleme

### Backend startet nicht?

```bash
sudo pip3 install -r requirements.txt
```

### Login funktioniert nicht?

Prüfe ob Backend läuft:
```bash
curl http://localhost:5000/api/auth/check
```

---

## 📚 Weitere Hilfe

- **Vollständige Anleitung**: `ANLEITUNG-V2.md`
- **API-Dokumentation**: Siehe `ANLEITUNG-V2.md` → API-Referenz

---

## 🎉 Fertig!

Du hast jetzt ein voll funktionsfähiges Homelab Dashboard mit:

✅ Login-System
✅ Service-Management
✅ Status-Checks
✅ Favoriten
✅ Notizen
✅ Drag & Drop
✅ Gruppen & Tags

**Viel Spaß! 🚀**
