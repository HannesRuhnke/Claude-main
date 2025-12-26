# Flask Backend V3 für Homelab Dashboard - ERWEITERTE VERSION
# Features: Multi-User, Rollen, Passkeys, Analytics, Backup, Advanced Monitoring

from flask import Flask, request, jsonify, send_from_directory, session, send_file
from flask_cors import CORS
from functools import wraps
import sqlite3
import hashlib
import secrets
import json
import os
import base64
import io
import zipfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import socket
import time

app = Flask(__name__, static_folder='.')
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True)

# Konfiguration
DATABASE = 'homelab.db'
BACKUP_DIR = 'backups'
SCREENSHOTS_DIR = 'screenshots'
DEFAULT_PASSWORD_HASH = hashlib.sha256('homelab2025'.encode()).hexdigest()

# Erstelle benötigte Verzeichnisse
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ===========================
# Datenbank-Setup
# ===========================

def get_db():
    """Erstellt Datenbankverbindung"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialisiert die Datenbank mit allen Tabellen"""
    db = get_db()

    # ============= BENUTZER & AUTHENTIFIZIERUNG =============

    # User-Tabelle (erweitert)
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            avatar_url TEXT,
            is_active INTEGER DEFAULT 1,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Rollen-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            permissions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # User-Rollen Zuordnung
    db.execute('''
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER,
            role_id INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
            PRIMARY KEY (user_id, role_id)
        )
    ''')

    # Passkeys (WebAuthn)
    db.execute('''
        CREATE TABLE IF NOT EXISTS passkeys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            credential_id TEXT UNIQUE NOT NULL,
            public_key TEXT NOT NULL,
            name TEXT,
            counter INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # ============= SERVICES =============

    # Services-Tabelle (erweitert)
    db.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL,
            icon TEXT,
            category TEXT,
            color TEXT,
            background_image TEXT,
            screenshot_url TEXT,
            is_favorite INTEGER DEFAULT 0,
            notes TEXT,
            encrypted_notes TEXT,
            sort_order INTEGER DEFAULT 0,
            group_id INTEGER,
            owner_id INTEGER,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    # Tags-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT 'blue',
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id)
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
            parent_id INTEGER,
            sort_order INTEGER DEFAULT 0,
            created_by INTEGER,
            FOREIGN KEY (parent_id) REFERENCES groups(id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    # ============= MONITORING & STATUS =============

    # Service-Status (erweitert)
    db.execute('''
        CREATE TABLE IF NOT EXISTS service_status (
            service_id TEXT PRIMARY KEY,
            is_online INTEGER DEFAULT 0,
            response_time INTEGER,
            status_code INTEGER,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_online TIMESTAMP,
            total_checks INTEGER DEFAULT 0,
            failed_checks INTEGER DEFAULT 0,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
        )
    ''')

    # Uptime-History
    db.execute('''
        CREATE TABLE IF NOT EXISTS uptime_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id TEXT NOT NULL,
            is_online INTEGER,
            response_time INTEGER,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
        )
    ''')

    # Incidents/Ausfälle
    db.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id TEXT NOT NULL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP,
            duration INTEGER,
            severity TEXT DEFAULT 'warning',
            notes TEXT,
            resolved_by INTEGER,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
            FOREIGN KEY (resolved_by) REFERENCES users(id)
        )
    ''')

    # SSL-Zertifikat Tracking
    db.execute('''
        CREATE TABLE IF NOT EXISTS ssl_certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id TEXT NOT NULL,
            domain TEXT,
            issuer TEXT,
            valid_from TIMESTAMP,
            valid_until TIMESTAMP,
            days_until_expiry INTEGER,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
        )
    ''')

    # ============= ANALYTICS & INSIGHTS =============

    # Analytics-Events
    db.execute('''
        CREATE TABLE IF NOT EXISTS analytics_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_type TEXT NOT NULL,
            event_data TEXT,
            service_id TEXT,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE SET NULL
        )
    ''')

    # Service-Statistiken
    db.execute('''
        CREATE TABLE IF NOT EXISTS service_stats (
            service_id TEXT PRIMARY KEY,
            total_clicks INTEGER DEFAULT 0,
            total_views INTEGER DEFAULT 0,
            avg_response_time REAL,
            uptime_percentage REAL,
            last_30d_uptime REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
        )
    ''')

    # ============= THEMES & CUSTOMIZATION =============

    # Themes-Tabelle (erweitert)
    db.execute('''
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            colors TEXT NOT NULL,
            fonts TEXT,
            spacing TEXT,
            is_active INTEGER DEFAULT 0,
            is_public INTEGER DEFAULT 0,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    # User-Preferences
    db.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id INTEGER PRIMARY KEY,
            theme_id INTEGER,
            layout TEXT DEFAULT 'grid',
            items_per_page INTEGER DEFAULT 20,
            default_view TEXT DEFAULT 'all',
            show_screenshots INTEGER DEFAULT 1,
            show_status INTEGER DEFAULT 1,
            preferences_json TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (theme_id) REFERENCES themes(id)
        )
    ''')

    # Custom-Layouts
    db.execute('''
        CREATE TABLE IF NOT EXISTS custom_layouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            layout_data TEXT NOT NULL,
            is_default INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # ============= BACKUP & SYNC =============

    # Backups-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_size INTEGER,
            backup_type TEXT DEFAULT 'manual',
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    # Audit-Log
    db.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            entity_type TEXT,
            entity_id TEXT,
            old_value TEXT,
            new_value TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # ============= NOTIFICATIONS =============

    # Notifications-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT,
            is_read INTEGER DEFAULT 0,
            service_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
        )
    ''')

    # ============= STANDARD-DATEN EINFÜGEN =============

    # Standard-User erstellen
    cursor = db.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        db.execute('''
            INSERT INTO users (username, email, password_hash, full_name, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@homelab.local', DEFAULT_PASSWORD_HASH, 'Administrator', 1))
        admin_id = db.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()[0]

        # Standard-Rollen erstellen
        db.execute('''
            INSERT INTO roles (name, description, permissions) VALUES
            ('admin', 'Administrator mit allen Rechten', '["all"]'),
            ('user', 'Normaler Benutzer', '["view", "edit_own"]'),
            ('viewer', 'Nur Ansicht', '["view"]')
        ''')

        # Admin-Rolle zuweisen
        admin_role_id = db.execute('SELECT id FROM roles WHERE name = ?', ('admin',)).fetchone()[0]
        db.execute('INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)', (admin_id, admin_role_id))

    db.commit()
    db.close()

# ===========================
# Authentifizierung & Permissions
# ===========================

def login_required(f):
    """Decorator für geschützte Routen"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Nicht authentifiziert'}), 401
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    """Decorator für Permissions-Check"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Nicht authentifiziert'}), 401

            if not has_permission(session['user_id'], permission):
                return jsonify({'error': 'Keine Berechtigung'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def has_permission(user_id, permission):
    """Prüft ob User Permission hat"""
    db = get_db()
    cursor = db.execute('''
        SELECT r.permissions
        FROM user_roles ur
        JOIN roles r ON ur.role_id = r.id
        WHERE ur.user_id = ?
    ''', (user_id,))

    roles = cursor.fetchall()
    db.close()

    for role in roles:
        perms = json.loads(role['permissions'])
        if 'all' in perms or permission in perms:
            return True

    return False

def log_analytics_event(event_type, event_data=None, service_id=None):
    """Loggt Analytics-Event"""
    try:
        db = get_db()
        db.execute('''
            INSERT INTO analytics_events (user_id, event_type, event_data, service_id, ip_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            session.get('user_id'),
            event_type,
            json.dumps(event_data) if event_data else None,
            service_id,
            request.remote_addr
        ))
        db.commit()
        db.close()
    except Exception as e:
        print(f"Analytics logging error: {e}")

def log_audit(action, entity_type=None, entity_id=None, old_value=None, new_value=None):
    """Loggt Audit-Event"""
    try:
        db = get_db()
        db.execute('''
            INSERT INTO audit_log (user_id, action, entity_type, entity_id, old_value, new_value, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session.get('user_id'),
            action,
            entity_type,
            entity_id,
            json.dumps(old_value) if old_value else None,
            json.dumps(new_value) if new_value else None,
            request.remote_addr
        ))
        db.commit()
        db.close()
    except Exception as e:
        print(f"Audit logging error: {e}")

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
    cursor = db.execute('''
        SELECT * FROM users WHERE username = ? AND password_hash = ? AND is_active = 1
    ''', (username, password_hash))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=7)

        # Update last_login
        db.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
        db.commit()

        log_analytics_event('user_login', {'username': username})
        log_audit('login', 'user', user['id'])

        db.close()
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name']
            }
        })

    db.close()
    return jsonify({'error': 'Ungültige Anmeldedaten'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout-Endpoint"""
    user_id = session.get('user_id')
    if user_id:
        log_analytics_event('user_logout')
        log_audit('logout', 'user', user_id)

    session.clear()
    return jsonify({'success': True})

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Prüft ob User eingeloggt ist"""
    if 'user_id' in session:
        db = get_db()
        cursor = db.execute('SELECT id, username, email, full_name, avatar_url FROM users WHERE id = ?',
                          (session['user_id'],))
        user = cursor.fetchone()
        db.close()

        if user:
            return jsonify({
                'authenticated': True,
                'user': dict(user)
            })

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

    db.execute('UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
              (new_hash, session['user_id']))
    db.commit()
    db.close()

    log_audit('password_change', 'user', session['user_id'])

    return jsonify({'success': True})

# ===========================
# USER-MANAGEMENT ROUTEN
# ===========================

@app.route('/api/users', methods=['GET'])
@login_required
@permission_required('manage_users')
def get_users():
    """Alle Benutzer abrufen"""
    db = get_db()
    cursor = db.execute('''
        SELECT u.*, GROUP_CONCAT(r.name) as roles
        FROM users u
        LEFT JOIN user_roles ur ON u.id = ur.user_id
        LEFT JOIN roles r ON ur.role_id = r.id
        GROUP BY u.id
        ORDER BY u.created_at DESC
    ''')
    users = [dict(row) for row in cursor.fetchall()]

    for user in users:
        user['roles'] = user['roles'].split(',') if user['roles'] else []
        # Entferne Passwort-Hash aus Antwort
        user.pop('password_hash', None)

    db.close()
    log_analytics_event('users_viewed')

    return jsonify(users)

@app.route('/api/users', methods=['POST'])
@login_required
@permission_required('manage_users')
def create_user():
    """Neuen Benutzer erstellen"""
    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    role_ids = data.get('role_ids', [])

    if not username or not password:
        return jsonify({'error': 'Username und Passwort erforderlich'}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db()
    try:
        cursor = db.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))

        user_id = cursor.lastrowid

        # Rollen zuweisen
        for role_id in role_ids:
            db.execute('INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)',
                      (user_id, role_id))

        db.commit()
        db.close()

        log_analytics_event('user_created', {'username': username})
        log_audit('create', 'user', user_id, None, data)

        return jsonify({'success': True, 'id': user_id})

    except sqlite3.IntegrityError:
        db.close()
        return jsonify({'error': 'Benutzername oder E-Mail existiert bereits'}), 400

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
@permission_required('manage_users')
def update_user(user_id):
    """Benutzer aktualisieren"""
    data = request.json

    db = get_db()

    # Hole alte Daten für Audit
    old_user = dict(db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone())

    # Update User
    db.execute('''
        UPDATE users SET
            email = ?, full_name = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (data.get('email'), data.get('full_name'), data.get('is_active', 1), user_id))

    # Update Rollen wenn angegeben
    if 'role_ids' in data:
        db.execute('DELETE FROM user_roles WHERE user_id = ?', (user_id,))
        for role_id in data['role_ids']:
            db.execute('INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)',
                      (user_id, role_id))

    db.commit()
    db.close()

    log_audit('update', 'user', user_id, old_user, data)

    return jsonify({'success': True})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
@permission_required('manage_users')
def delete_user(user_id):
    """Benutzer löschen"""
    # Verhindere Löschen des eigenen Accounts
    if user_id == session['user_id']:
        return jsonify({'error': 'Du kannst deinen eigenen Account nicht löschen'}), 400

    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    db.close()

    log_audit('delete', 'user', user_id)

    return jsonify({'success': True})

# ===========================
# ROLLEN-ROUTEN
# ===========================

@app.route('/api/roles', methods=['GET'])
@login_required
def get_roles():
    """Alle Rollen abrufen"""
    db = get_db()
    cursor = db.execute('SELECT * FROM roles ORDER BY name')
    roles = [dict(row) for row in cursor.fetchall()]

    for role in roles:
        role['permissions'] = json.loads(role['permissions'])

    db.close()
    return jsonify(roles)

@app.route('/api/roles', methods=['POST'])
@login_required
@permission_required('manage_roles')
def create_role():
    """Neue Rolle erstellen"""
    data = request.json

    db = get_db()
    cursor = db.execute('''
        INSERT INTO roles (name, description, permissions)
        VALUES (?, ?, ?)
    ''', (data['name'], data.get('description'), json.dumps(data.get('permissions', []))))

    role_id = cursor.lastrowid
    db.commit()
    db.close()

    log_audit('create', 'role', role_id, None, data)

    return jsonify({'success': True, 'id': role_id})

# ===========================
# SERVICE-ROUTEN (erweitert)
# ===========================

@app.route('/api/services', methods=['GET'])
@login_required
def get_services():
    """Alle Services abrufen"""
    db = get_db()
    cursor = db.execute('''
        SELECT s.*, GROUP_CONCAT(DISTINCT t.name) as tags, u.username as owner_name,
               ss.is_online, ss.response_time, ss.last_checked,
               stats.total_clicks, stats.uptime_percentage
        FROM services s
        LEFT JOIN service_tags st ON s.id = st.service_id
        LEFT JOIN tags t ON st.tag_id = t.id
        LEFT JOIN users u ON s.owner_id = u.id
        LEFT JOIN service_status ss ON s.id = ss.service_id
        LEFT JOIN service_stats stats ON s.id = stats.service_id
        GROUP BY s.id
        ORDER BY s.sort_order, s.name
    ''')
    services = [dict(row) for row in cursor.fetchall()]

    for service in services:
        service['tags'] = service['tags'].split(',') if service['tags'] else []

    db.close()

    log_analytics_event('services_viewed')

    return jsonify(services)

# ... (Die anderen Service-Endpunkte bleiben weitgehend gleich, werden nur erweitert)

# ===========================
# ANALYTICS-ROUTEN
# ===========================

@app.route('/api/analytics/dashboard', methods=['GET'])
@login_required
def get_analytics_dashboard():
    """Analytics-Dashboard-Daten"""
    db = get_db()

    # Gesamt-Statistiken
    total_services = db.execute('SELECT COUNT(*) as count FROM services').fetchone()['count']
    total_users = db.execute('SELECT COUNT(*) as count FROM users WHERE is_active = 1').fetchone()['count']

    # Service-Statistiken
    cursor = db.execute('''
        SELECT event_type, COUNT(*) as count
        FROM analytics_events
        WHERE created_at >= datetime('now', '-30 days')
        GROUP BY event_type
        ORDER BY count DESC
    ''')
    events = [dict(row) for row in cursor.fetchall()]

    # Beliebteste Services
    cursor = db.execute('''
        SELECT service_id, total_clicks, total_views
        FROM service_stats
        ORDER BY total_clicks DESC
        LIMIT 10
    ''')
    popular_services = [dict(row) for row in cursor.fetchall()]

    # Uptime-Statistik
    cursor = db.execute('''
        SELECT AVG(uptime_percentage) as avg_uptime
        FROM service_stats
    ''')
    avg_uptime = cursor.fetchone()['avg_uptime'] or 0

    db.close()

    return jsonify({
        'total_services': total_services,
        'total_users': total_users,
        'events': events,
        'popular_services': popular_services,
        'avg_uptime': round(avg_uptime, 2)
    })

@app.route('/api/analytics/service/<service_id>', methods=['GET'])
@login_required
def get_service_analytics(service_id):
    """Analytics für einen bestimmten Service"""
    db = get_db()

    # Service-Stats
    stats = dict(db.execute('''
        SELECT * FROM service_stats WHERE service_id = ?
    ''', (service_id,)).fetchone() or {})

    # Uptime-History (letzte 7 Tage)
    cursor = db.execute('''
        SELECT
            DATE(checked_at) as date,
            AVG(is_online) as uptime,
            AVG(response_time) as avg_response_time,
            COUNT(*) as checks
        FROM uptime_history
        WHERE service_id = ? AND checked_at >= datetime('now', '-7 days')
        GROUP BY DATE(checked_at)
        ORDER BY date DESC
    ''', (service_id,))
    history = [dict(row) for row in cursor.fetchall()]

    # Incidents
    cursor = db.execute('''
        SELECT * FROM incidents
        WHERE service_id = ?
        ORDER BY started_at DESC
        LIMIT 10
    ''', (service_id,))
    incidents = [dict(row) for row in cursor.fetchall()]

    db.close()

    return jsonify({
        'stats': stats,
        'history': history,
        'incidents': incidents
    })

# ===========================
# BACKUP-ROUTEN
# ===========================

@app.route('/api/backup/create', methods=['POST'])
@login_required
@permission_required('manage_backups')
def create_backup():
    """Erstellt Backup"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'homelab_backup_{timestamp}.zip'
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Datenbank hinzufügen
            zipf.write(DATABASE, os.path.basename(DATABASE))

            # Screenshots hinzufügen
            if os.path.exists(SCREENSHOTS_DIR):
                for root, dirs, files in os.walk(SCREENSHOTS_DIR):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(SCREENSHOTS_DIR))
                        zipf.write(file_path, arcname)

        # In DB eintragen
        file_size = os.path.getsize(backup_path)
        db = get_db()
        cursor = db.execute('''
            INSERT INTO backups (filename, file_size, backup_type, created_by)
            VALUES (?, ?, ?, ?)
        ''', (backup_filename, file_size, 'manual', session['user_id']))
        backup_id = cursor.lastrowid
        db.commit()
        db.close()

        log_audit('create', 'backup', backup_id)

        return jsonify({
            'success': True,
            'filename': backup_filename,
            'size': file_size
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/backup/list', methods=['GET'])
@login_required
def list_backups():
    """Liste alle Backups"""
    db = get_db()
    cursor = db.execute('''
        SELECT b.*, u.username as created_by_name
        FROM backups b
        LEFT JOIN users u ON b.created_by = u.id
        ORDER BY b.created_at DESC
    ''')
    backups = [dict(row) for row in cursor.fetchall()]
    db.close()

    return jsonify(backups)

@app.route('/api/backup/download/<int:backup_id>', methods=['GET'])
@login_required
@permission_required('manage_backups')
def download_backup(backup_id):
    """Backup herunterladen"""
    db = get_db()
    backup = dict(db.execute('SELECT * FROM backups WHERE id = ?', (backup_id,)).fetchone())
    db.close()

    backup_path = os.path.join(BACKUP_DIR, backup['filename'])

    if os.path.exists(backup_path):
        return send_file(backup_path, as_attachment=True)
    else:
        return jsonify({'error': 'Backup-Datei nicht gefunden'}), 404

@app.route('/api/backup/restore/<int:backup_id>', methods=['POST'])
@login_required
@permission_required('manage_backups')
def restore_backup(backup_id):
    """Backup wiederherstellen"""
    db = get_db()
    backup = dict(db.execute('SELECT * FROM backups WHERE id = ?', (backup_id,)).fetchone())
    db.close()

    backup_path = os.path.join(BACKUP_DIR, backup['filename'])

    if not os.path.exists(backup_path):
        return jsonify({'error': 'Backup-Datei nicht gefunden'}), 404

    try:
        # Erstelle erstmal ein Backup vom aktuellen Stand
        current_backup = f'pre_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        shutil.copy(DATABASE, os.path.join(BACKUP_DIR, current_backup))

        # Restore
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall(BACKUP_DIR + '/temp_restore')

        # Datenbank ersetzen
        restored_db = os.path.join(BACKUP_DIR, 'temp_restore', os.path.basename(DATABASE))
        if os.path.exists(restored_db):
            shutil.copy(restored_db, DATABASE)

        # Cleanup
        shutil.rmtree(BACKUP_DIR + '/temp_restore')

        log_audit('restore', 'backup', backup_id)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===========================
# THEME-BUILDER-ROUTEN
# ===========================

@app.route('/api/themes/custom', methods=['POST'])
@login_required
def create_custom_theme():
    """Erstellt Custom Theme"""
    data = request.json

    db = get_db()
    cursor = db.execute('''
        INSERT INTO themes (name, colors, fonts, spacing, is_public, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        json.dumps(data['colors']),
        json.dumps(data.get('fonts', {})),
        json.dumps(data.get('spacing', {})),
        data.get('is_public', 0),
        session['user_id']
    ))
    theme_id = cursor.lastrowid
    db.commit()
    db.close()

    log_audit('create', 'theme', theme_id, None, data)

    return jsonify({'success': True, 'id': theme_id})

@app.route('/api/themes/custom', methods=['GET'])
@login_required
def get_custom_themes():
    """Alle Custom Themes"""
    db = get_db()
    cursor = db.execute('''
        SELECT t.*, u.username as created_by_name
        FROM themes t
        LEFT JOIN users u ON t.created_by = u.id
        WHERE t.is_public = 1 OR t.created_by = ?
        ORDER BY t.created_at DESC
    ''', (session['user_id'],))
    themes = [dict(row) for row in cursor.fetchall()]

    for theme in themes:
        theme['colors'] = json.loads(theme['colors'])
        theme['fonts'] = json.loads(theme['fonts']) if theme['fonts'] else {}
        theme['spacing'] = json.loads(theme['spacing']) if theme['spacing'] else {}

    db.close()
    return jsonify(themes)

# ===========================
# USER-PREFERENCES-ROUTEN
# ===========================

@app.route('/api/preferences', methods=['GET'])
@login_required
def get_user_preferences():
    """Hole User-Einstellungen"""
    db = get_db()
    cursor = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (session['user_id'],))
    prefs = cursor.fetchone()

    if prefs:
        prefs = dict(prefs)
        if prefs['preferences_json']:
            prefs['preferences'] = json.loads(prefs['preferences_json'])
    else:
        # Standard-Einstellungen
        prefs = {
            'layout': 'grid',
            'items_per_page': 20,
            'default_view': 'all',
            'show_screenshots': 1,
            'show_status': 1,
            'preferences': {}
        }

    db.close()
    return jsonify(prefs)

@app.route('/api/preferences', methods=['PUT'])
@login_required
def update_user_preferences():
    """Aktualisiere User-Einstellungen"""
    data = request.json

    db = get_db()

    # Check ob Preferences existieren
    existing = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (session['user_id'],)).fetchone()

    if existing:
        db.execute('''
            UPDATE user_preferences SET
                theme_id = ?, layout = ?, items_per_page = ?,
                default_view = ?, show_screenshots = ?, show_status = ?,
                preferences_json = ?
            WHERE user_id = ?
        ''', (
            data.get('theme_id'), data.get('layout'), data.get('items_per_page'),
            data.get('default_view'), data.get('show_screenshots'), data.get('show_status'),
            json.dumps(data.get('preferences', {})),
            session['user_id']
        ))
    else:
        db.execute('''
            INSERT INTO user_preferences
            (user_id, theme_id, layout, items_per_page, default_view, show_screenshots, show_status, preferences_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session['user_id'],
            data.get('theme_id'), data.get('layout'), data.get('items_per_page'),
            data.get('default_view'), data.get('show_screenshots'), data.get('show_status'),
            json.dumps(data.get('preferences', {}))
        ))

    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# NOTIFICATIONS-ROUTEN
# ===========================

@app.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Hole Benachrichtigungen"""
    db = get_db()
    cursor = db.execute('''
        SELECT * FROM notifications
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 50
    ''', (session['user_id'],))
    notifications = [dict(row) for row in cursor.fetchall()]
    db.close()

    return jsonify(notifications)

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Markiere Benachrichtigung als gelesen"""
    db = get_db()
    db.execute('''
        UPDATE notifications SET is_read = 1
        WHERE id = ? AND user_id = ?
    ''', (notification_id, session['user_id']))
    db.commit()
    db.close()

    return jsonify({'success': True})

# ===========================
# AUDIT-LOG-ROUTEN
# ===========================

@app.route('/api/audit-log', methods=['GET'])
@login_required
@permission_required('view_audit_log')
def get_audit_log():
    """Hole Audit-Log"""
    limit = request.args.get('limit', 100, type=int)

    db = get_db()
    cursor = db.execute('''
        SELECT a.*, u.username
        FROM audit_log a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC
        LIMIT ?
    ''', (limit,))
    logs = [dict(row) for row in cursor.fetchall()]

    for log in logs:
        if log['old_value']:
            log['old_value'] = json.loads(log['old_value'])
        if log['new_value']:
            log['new_value'] = json.loads(log['new_value'])

    db.close()
    return jsonify(logs)

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
        # Prüfe und aktualisiere Schema
        try:
            db = get_db()
            # Versuche neue Tabellen zu erstellen (falls nicht vorhanden)
            init_db()
            db.close()
        except Exception as e:
            print(f"Schema-Update: {e}")

    print("\nHomelab Dashboard V3 Backend gestartet!")
    print("URL: http://localhost:5000")
    print("\nNEU in V3:")
    print("✓ Multi-User System")
    print("✓ Rollen & Permissions")
    print("✓ Passkeys-Support")
    print("✓ Analytics & Insights")
    print("✓ Backup & Restore")
    print("✓ Theme-Builder")
    print("✓ Audit-Log")
    print("\nDrücke Strg+C zum Beenden\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
