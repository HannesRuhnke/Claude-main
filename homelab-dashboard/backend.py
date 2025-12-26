# Flask Backend für Homelab Dashboard
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from functools import wraps
import sqlite3
import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
import subprocess
import platform
import socket

app = Flask(__name__, static_folder='.')
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True)

# Konfiguration
DATABASE = 'homelab.db'
DEFAULT_PASSWORD_HASH = hashlib.sha256('homelab2025'.encode()).hexdigest()

# ===========================
# Datenbank-Setup
# ===========================

def get_db():
    """Erstellt Datenbankverbindung"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialisiert die Datenbank"""
    db = get_db()

    # User-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Services-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL,
            icon TEXT,
            category TEXT,
            color TEXT,
            is_favorite INTEGER DEFAULT 0,
            notes TEXT,
            sort_order INTEGER DEFAULT 0,
            group_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tags-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT 'blue'
        )
    ''')

    # Service-Tags Zuordnung
    db.execute('''
        CREATE TABLE IF NOT EXISTS service_tags (
            service_id TEXT,
            tag_id INTEGER,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (service_id, tag_id)
        )
    ''')

    # Gruppen-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT DEFAULT 'fa-folder',
            color TEXT DEFAULT 'blue',
            sort_order INTEGER DEFAULT 0
        )
    ''')

    # Themes-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            colors TEXT NOT NULL,
            is_active INTEGER DEFAULT 0
        )
    ''')

    # Service-Status Cache
    db.execute('''
        CREATE TABLE IF NOT EXISTS service_status (
            service_id TEXT PRIMARY KEY,
            is_online INTEGER DEFAULT 0,
            response_time INTEGER,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
        )
    ''')

    # Standard-User erstellen wenn nicht vorhanden
    cursor = db.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                  ('admin', DEFAULT_PASSWORD_HASH))

    db.commit()
    db.close()

# ===========================
# Authentifizierung
# ===========================

def login_required(f):
    """Decorator für geschützte Routen"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Nicht authentifiziert'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ===========================
# Auth-Routen
# ===========================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login-Endpoint"""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username und Passwort erforderlich'}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?',
                       (username, password_hash))
    user = cursor.fetchone()
    db.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=7)
        return jsonify({'success': True, 'username': user['username']})

    return jsonify({'error': 'Ungültige Anmeldedaten'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout-Endpoint"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Prüft ob User eingeloggt ist"""
    if 'user_id' in session:
        return jsonify({'authenticated': True, 'username': session.get('username')})
    return jsonify({'authenticated': False}), 401

@app.route('/api/auth/change-password', methods=['POST'])
@login_required
def change_password():
    """Passwort ändern"""
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'error': 'Altes und neues Passwort erforderlich'}), 400

    old_hash = hashlib.sha256(old_password.encode()).hexdigest()
    new_hash = hashlib.sha256(new_password.encode()).hexdigest()

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE id = ? AND password_hash = ?',
                       (session['user_id'], old_hash))
    user = cursor.fetchone()

    if not user:
        db.close()
        return jsonify({'error': 'Altes Passwort ist falsch'}), 401

    db.execute('UPDATE users SET password_hash = ? WHERE id = ?',
              (new_hash, session['user_id']))
    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# Service-Routen
# ===========================

@app.route('/api/services', methods=['GET'])
@login_required
def get_services():
    """Alle Services abrufen"""
    db = get_db()
    cursor = db.execute('''
        SELECT s.*, GROUP_CONCAT(t.name) as tags
        FROM services s
        LEFT JOIN service_tags st ON s.id = st.service_id
        LEFT JOIN tags t ON st.tag_id = t.id
        GROUP BY s.id
        ORDER BY s.sort_order, s.name
    ''')
    services = [dict(row) for row in cursor.fetchall()]

    # Tags als Liste konvertieren
    for service in services:
        service['tags'] = service['tags'].split(',') if service['tags'] else []

    db.close()
    return jsonify(services)

@app.route('/api/services', methods=['POST'])
@login_required
def add_service():
    """Service hinzufügen"""
    data = request.json

    db = get_db()
    db.execute('''
        INSERT INTO services (id, name, description, url, icon, category, color, notes, group_id, is_favorite)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['id'], data['name'], data.get('description', ''),
        data['url'], data.get('icon', 'fa-cube'), data['category'],
        data.get('color', 'blue'), data.get('notes', ''),
        data.get('group_id'), data.get('is_favorite', 0)
    ))
    db.commit()
    db.close()

    return jsonify({'success': True, 'id': data['id']})

@app.route('/api/services/<service_id>', methods=['PUT'])
@login_required
def update_service(service_id):
    """Service aktualisieren"""
    data = request.json

    db = get_db()
    db.execute('''
        UPDATE services SET
            name = ?, description = ?, url = ?, icon = ?,
            category = ?, color = ?, notes = ?, group_id = ?,
            is_favorite = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        data['name'], data.get('description', ''), data['url'],
        data.get('icon', 'fa-cube'), data['category'], data.get('color', 'blue'),
        data.get('notes', ''), data.get('group_id'), data.get('is_favorite', 0),
        service_id
    ))
    db.commit()
    db.close()

    return jsonify({'success': True})

@app.route('/api/services/<service_id>', methods=['DELETE'])
@login_required
def delete_service(service_id):
    """Service löschen"""
    db = get_db()
    db.execute('DELETE FROM services WHERE id = ?', (service_id,))
    db.commit()
    db.close()

    return jsonify({'success': True})

@app.route('/api/services/<service_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(service_id):
    """Favorit umschalten"""
    data = request.json
    is_favorite = data.get('is_favorite', 0)

    db = get_db()
    db.execute('UPDATE services SET is_favorite = ? WHERE id = ?',
              (is_favorite, service_id))
    db.commit()
    db.close()

    return jsonify({'success': True})

@app.route('/api/services/reorder', methods=['POST'])
@login_required
def reorder_services():
    """Services neu sortieren"""
    data = request.json
    service_order = data.get('order', [])

    db = get_db()
    for index, service_id in enumerate(service_order):
        db.execute('UPDATE services SET sort_order = ? WHERE id = ?',
                  (index, service_id))
    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# Status-Check
# ===========================

@app.route('/api/services/<service_id>/check-status', methods=['POST'])
@login_required
def check_service_status(service_id):
    """Prüft Service-Status"""
    db = get_db()
    cursor = db.execute('SELECT url FROM services WHERE id = ?', (service_id,))
    service = cursor.fetchone()

    if not service:
        db.close()
        return jsonify({'error': 'Service nicht gefunden'}), 404

    url = service['url']
    is_online = False
    response_time = None

    try:
        # Extrahiere Host und Port aus URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        host = parsed.hostname or parsed.path.split(':')[0]
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)

        # Socket-basierter Check
        import time
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            is_online = True
            response_time = int((time.time() - start) * 1000)  # ms
    except Exception as e:
        print(f"Status check error for {service_id}: {e}")

    # Status in DB speichern
    db.execute('''
        INSERT OR REPLACE INTO service_status (service_id, is_online, response_time, last_checked)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (service_id, 1 if is_online else 0, response_time))
    db.commit()
    db.close()

    return jsonify({
        'service_id': service_id,
        'is_online': is_online,
        'response_time': response_time
    })

@app.route('/api/services/check-all-status', methods=['POST'])
@login_required
def check_all_status():
    """Prüft Status aller Services"""
    db = get_db()
    cursor = db.execute('SELECT id FROM services')
    services = cursor.fetchall()
    db.close()

    results = []
    for service in services:
        # Hier würde man normalerweise async checks machen
        # Für Simplizität synchron
        response = check_service_status(service['id'])
        results.append(response.json)

    return jsonify({'results': results})

@app.route('/api/services/status', methods=['GET'])
@login_required
def get_all_status():
    """Holt alle Status-Informationen"""
    db = get_db()
    cursor = db.execute('SELECT * FROM service_status')
    statuses = [dict(row) for row in cursor.fetchall()]
    db.close()

    return jsonify(statuses)

# ===========================
# Gruppen-Routen
# ===========================

@app.route('/api/groups', methods=['GET'])
@login_required
def get_groups():
    """Alle Gruppen abrufen"""
    db = get_db()
    cursor = db.execute('SELECT * FROM groups ORDER BY sort_order, name')
    groups = [dict(row) for row in cursor.fetchall()]
    db.close()

    return jsonify(groups)

@app.route('/api/groups', methods=['POST'])
@login_required
def add_group():
    """Gruppe hinzufügen"""
    data = request.json

    db = get_db()
    cursor = db.execute('''
        INSERT INTO groups (name, icon, color, sort_order)
        VALUES (?, ?, ?, ?)
    ''', (data['name'], data.get('icon', 'fa-folder'),
          data.get('color', 'blue'), data.get('sort_order', 0)))
    group_id = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({'success': True, 'id': group_id})

@app.route('/api/groups/<int:group_id>', methods=['PUT'])
@login_required
def update_group(group_id):
    """Gruppe aktualisieren"""
    data = request.json

    db = get_db()
    db.execute('''
        UPDATE groups SET name = ?, icon = ?, color = ?
        WHERE id = ?
    ''', (data['name'], data.get('icon', 'fa-folder'),
          data.get('color', 'blue'), group_id))
    db.commit()
    db.close()

    return jsonify({'success': True})

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
@login_required
def delete_group(group_id):
    """Gruppe löschen"""
    db = get_db()
    # Services in dieser Gruppe auf keine Gruppe setzen
    db.execute('UPDATE services SET group_id = NULL WHERE group_id = ?', (group_id,))
    db.execute('DELETE FROM groups WHERE id = ?', (group_id,))
    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# Tags-Routen
# ===========================

@app.route('/api/tags', methods=['GET'])
@login_required
def get_tags():
    """Alle Tags abrufen"""
    db = get_db()
    cursor = db.execute('SELECT * FROM tags ORDER BY name')
    tags = [dict(row) for row in cursor.fetchall()]
    db.close()

    return jsonify(tags)

@app.route('/api/tags', methods=['POST'])
@login_required
def add_tag():
    """Tag hinzufügen"""
    data = request.json

    db = get_db()
    try:
        cursor = db.execute('INSERT INTO tags (name, color) VALUES (?, ?)',
                          (data['name'], data.get('color', 'blue')))
        tag_id = cursor.lastrowid
        db.commit()
        db.close()
        return jsonify({'success': True, 'id': tag_id})
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({'error': 'Tag existiert bereits'}), 400

@app.route('/api/services/<service_id>/tags', methods=['POST'])
@login_required
def add_tag_to_service(service_id):
    """Tag zu Service hinzufügen"""
    data = request.json
    tag_id = data.get('tag_id')

    db = get_db()
    try:
        db.execute('INSERT INTO service_tags (service_id, tag_id) VALUES (?, ?)',
                  (service_id, tag_id))
        db.commit()
        db.close()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({'error': 'Tag bereits zugewiesen'}), 400

@app.route('/api/services/<service_id>/tags/<int:tag_id>', methods=['DELETE'])
@login_required
def remove_tag_from_service(service_id, tag_id):
    """Tag von Service entfernen"""
    db = get_db()
    db.execute('DELETE FROM service_tags WHERE service_id = ? AND tag_id = ?',
              (service_id, tag_id))
    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# Themes-Routen
# ===========================

@app.route('/api/themes', methods=['GET'])
@login_required
def get_themes():
    """Alle Themes abrufen"""
    db = get_db()
    cursor = db.execute('SELECT * FROM themes')
    themes = [dict(row) for row in cursor.fetchall()]
    db.close()

    return jsonify(themes)

@app.route('/api/themes', methods=['POST'])
@login_required
def add_theme():
    """Theme hinzufügen"""
    data = request.json

    db = get_db()
    cursor = db.execute('INSERT INTO themes (name, colors) VALUES (?, ?)',
                       (data['name'], json.dumps(data['colors'])))
    theme_id = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({'success': True, 'id': theme_id})

@app.route('/api/themes/<int:theme_id>/activate', methods=['POST'])
@login_required
def activate_theme(theme_id):
    """Theme aktivieren"""
    db = get_db()
    db.execute('UPDATE themes SET is_active = 0')
    db.execute('UPDATE themes SET is_active = 1 WHERE id = ?', (theme_id,))
    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# Import/Export
# ===========================

@app.route('/api/export', methods=['GET'])
@login_required
def export_config():
    """Konfiguration exportieren"""
    db = get_db()

    # Services
    cursor = db.execute('SELECT * FROM services')
    services = [dict(row) for row in cursor.fetchall()]

    # Groups
    cursor = db.execute('SELECT * FROM groups')
    groups = [dict(row) for row in cursor.fetchall()]

    # Tags
    cursor = db.execute('SELECT * FROM tags')
    tags = [dict(row) for row in cursor.fetchall()]

    db.close()

    config = {
        'version': '2.0',
        'exportDate': datetime.now().isoformat(),
        'services': services,
        'groups': groups,
        'tags': tags
    }

    return jsonify(config)

@app.route('/api/import', methods=['POST'])
@login_required
def import_config():
    """Konfiguration importieren"""
    data = request.json

    db = get_db()

    # Alte Daten löschen
    db.execute('DELETE FROM service_tags')
    db.execute('DELETE FROM services')
    db.execute('DELETE FROM groups')
    db.execute('DELETE FROM tags')

    # Services importieren
    if 'services' in data:
        for service in data['services']:
            db.execute('''
                INSERT INTO services (id, name, description, url, icon, category, color, notes, group_id, is_favorite, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                service.get('id'), service['name'], service.get('description', ''),
                service['url'], service.get('icon', 'fa-cube'), service['category'],
                service.get('color', 'blue'), service.get('notes', ''),
                service.get('group_id'), service.get('is_favorite', 0),
                service.get('sort_order', 0)
            ))

    # Groups importieren
    if 'groups' in data:
        for group in data['groups']:
            db.execute('''
                INSERT INTO groups (id, name, icon, color, sort_order)
                VALUES (?, ?, ?, ?, ?)
            ''', (group['id'], group['name'], group.get('icon', 'fa-folder'),
                  group.get('color', 'blue'), group.get('sort_order', 0)))

    # Tags importieren
    if 'tags' in data:
        for tag in data['tags']:
            db.execute('INSERT INTO tags (id, name, color) VALUES (?, ?, ?)',
                      (tag['id'], tag['name'], tag.get('color', 'blue')))

    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# Static Files
# ===========================

@app.route('/')
def index():
    """Serve index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

# ===========================
# Hauptprogramm
# ===========================

if __name__ == '__main__':
    # Datenbank initialisieren
    if not os.path.exists(DATABASE):
        print("Initialisiere Datenbank...")
        init_db()
        print("✓ Datenbank erstellt")
        print("\n" + "="*60)
        print("STANDARD-ZUGANGSDATEN:")
        print("="*60)
        print("Username: admin")
        print("Passwort: homelab2025")
        print("="*60)
        print("\nBITTE ÄNDERE DAS PASSWORT NACH DEM ERSTEN LOGIN!\n")
    else:
        # Prüfe ob Tabellen existieren
        try:
            db = get_db()
            db.execute('SELECT * FROM users LIMIT 1')
            db.close()
        except:
            print("Tabellen fehlen, initialisiere Datenbank...")
            init_db()

    print("\nHomelab Dashboard Backend gestartet!")
    print("URL: http://localhost:5000")
    print("\nDrücke Strg+C zum Beenden\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
