#!/bin/bash

echo "=================================="
echo "  Homelab Dashboard - Start"
echo "=================================="
echo ""

# Prüfe ob Python 3 installiert ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "Bitte installiere Python 3: sudo apt install python3"
    exit 1
fi

# Prüfe ob pip installiert ist
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 ist nicht installiert!"
    echo "Bitte installiere pip3: sudo apt install python3-pip"
    exit 1
fi

# Prüfe ob requirements.txt existiert
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt nicht gefunden!"
    exit 1
fi

# Installiere Dependencies
echo "📦 Installiere Python-Dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "⚠️  Installation mit sudo versuchen..."
    sudo pip3 install -r requirements.txt
fi

echo "✓ Dependencies installiert"
echo ""

# Prüfe ob Datenbank existiert
if [ ! -f "homelab.db" ]; then
    echo "🗄️  Erstelle neue Datenbank..."
    echo ""
    echo "=================================="
    echo "  STANDARD-ZUGANGSDATEN"
    echo "=================================="
    echo "  Username: admin"
    echo "  Passwort: homelab2025"
    echo "=================================="
    echo ""
    echo "⚠️  BITTE ÄNDERE DAS PASSWORT NACH DEM ERSTEN LOGIN!"
    echo ""
fi

# Starte Backend
echo "🚀 Starte Backend auf Port 5000..."
echo ""
echo "Dashboard verfügbar unter:"
echo "👉 http://localhost:5000"
echo ""
echo "Drücke Strg+C zum Beenden"
echo ""

python3 backend.py
