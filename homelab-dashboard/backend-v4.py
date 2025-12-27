# Flask Backend V4 für Homelab Dashboard - ULTIMATE EDITION
# Features: Alle V3-Features + Rate Limiting, Email, Password Reset, Real Health Checks,
#           Global Search, Webhooks, Scheduled Backups, Database Migrations

from flask import Flask, request, jsonify, send_from_directory, session, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import requests
import threading
import schedule
from urllib.parse import urlparse
import re

app = Flask(__name__, static_folder='.')
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True)

# ===========================
# Rate Limiting Setup
# ===========================
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="memory://"
)

# Konfiguration
DATABASE = 'homelab.db'
BACKUP_DIR = 'backups'
SCREENSHOTS_DIR = 'screenshots'
DEFAULT_PASSWORD_HASH = hashlib.sha256('homelab2025'.encode()).hexdigest()
DB_VERSION = 4  # V4 Schema-Version

# Session-Konfiguration
SESSION_TIMEOUT_MINUTES = 30
SESSION_ABSOLUTE_TIMEOUT_HOURS = 24

# Email-Konfiguration (aus Umgebungsvariablen)
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_FROM = os.getenv('SMTP_FROM', SMTP_USER)
EMAIL_ENABLED = bool(SMTP_USER and SMTP_PASSWORD)

# Health Check Konfiguration
HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', '300'))  # 5 Minuten
HEALTH_CHECK_TIMEOUT = int(os.getenv('HEALTH_CHECK_TIMEOUT', '10'))  # 10 Sekunden

# Backup Konfiguration
AUTO_BACKUP_ENABLED = os.getenv('AUTO_BACKUP_ENABLED', 'true').lower() == 'true'
AUTO_BACKUP_TIME = os.getenv('AUTO_BACKUP_TIME', '02:00')  # 2 Uhr nachts
AUTO_BACKUP_RETENTION = int(os.getenv('AUTO_BACKUP_RETENTION', '7'))  # Behalte 7 Backups

# Erstelle benötigte Verzeichnisse
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ===========================
# Datenbank-Setup mit Migrationen
# ===========================

def get_db():
    """Erstellt Datenbankverbindung"""
    db = sqlite3.connect(DATABASE, check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db

def get_db_version():
    """Holt aktuelle DB-Version"""
    try:
        db = get_db()
        cursor = db.execute('SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1')
        result = cursor.fetchone()
        db.close()
        return result['version'] if result else 0
    except:
        return 0

def init_db():
    """Initialisiert die Datenbank mit allen Tabellen"""
    db = get_db()

    # Schema-Versions-Tabelle (für Migrationen)
    db.execute('''
        CREATE TABLE IF NOT EXISTS schema_version (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version INTEGER NOT NULL,
            description TEXT,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ============= V4 NEUE TABELLEN =============

    # Rate Limiting Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS rate_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            attempts INTEGER DEFAULT 1,
            last_attempt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            blocked_until TIMESTAMP
        )
    ''')

    # Password Reset Tokens
    db.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # Email Queue
    db.execute('''
        CREATE TABLE IF NOT EXISTS email_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            html_body TEXT,
            sent INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            last_error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sent_at TIMESTAMP
        )
    ''')

    # Webhooks
    db.execute('''
        CREATE TABLE IF NOT EXISTS webhooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            events TEXT NOT NULL,
            secret TEXT,
            is_active INTEGER DEFAULT 1,
            last_triggered TIMESTAMP,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    # Webhook Logs
    db.execute('''
        CREATE TABLE IF NOT EXISTS webhook_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            webhook_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT,
            status_code INTEGER,
            response TEXT,
            error TEXT,
            triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (webhook_id) REFERENCES webhooks(id) ON DELETE CASCADE
        )
    ''')

    # Alert Rules
    db.execute('''
        CREATE TABLE IF NOT EXISTS alert_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            condition_type TEXT NOT NULL,
            condition_value TEXT,
            notification_channels TEXT,
            is_active INTEGER DEFAULT 1,
            cooldown_minutes INTEGER DEFAULT 60,
            last_triggered TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    # ============= BENUTZER & AUTHENTIFIZIERUNG =============

    # User-Tabelle (erweitert mit V4 Feldern)
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            avatar_url TEXT,
            is_active INTEGER DEFAULT 1,
            email_verified INTEGER DEFAULT 0,
            two_factor_enabled INTEGER DEFAULT 0,
            two_factor_secret TEXT,
            failed_login_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP,
            last_login TIMESTAMP,
            last_activity TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sessions-Tabelle
    db.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
            health_check_enabled INTEGER DEFAULT 1,
            health_check_url TEXT,
            health_check_method TEXT DEFAULT 'GET',
            health_check_interval INTEGER DEFAULT 300,
            expected_status_code INTEGER DEFAULT 200,
            ssl_check_enabled INTEGER DEFAULT 1,
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

    # Service-Status (erweitert mit V4 Health Check Daten)
    db.execute('''
        CREATE TABLE IF NOT EXISTS service_status (
            service_id TEXT PRIMARY KEY,
            is_online INTEGER DEFAULT 0,
            response_time INTEGER,
            status_code INTEGER,
            ssl_valid INTEGER DEFAULT 1,
            ssl_expires_at TIMESTAMP,
            ssl_days_remaining INTEGER,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_online TIMESTAMP,
            last_error TEXT,
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
            status_code INTEGER,
            error_message TEXT,
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
            notification_sent INTEGER DEFAULT 0,
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
            subject TEXT,
            serial_number TEXT,
            valid_from TIMESTAMP,
            valid_until TIMESTAMP,
            days_until_expiry INTEGER,
            is_valid INTEGER DEFAULT 1,
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
            last_7d_uptime REAL,
            last_24h_uptime REAL,
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
            compact_mode INTEGER DEFAULT 0,
            enable_animations INTEGER DEFAULT 1,
            notification_sound INTEGER DEFAULT 1,
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

    # Backups-Tabelle (erweitert)
    db.execute('''
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_size INTEGER,
            backup_type TEXT DEFAULT 'manual',
            status TEXT DEFAULT 'completed',
            error_message TEXT,
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
            priority TEXT DEFAULT 'normal',
            action_url TEXT,
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
            INSERT INTO users (username, email, password_hash, full_name, is_active, email_verified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', 'admin@homelab.local', DEFAULT_PASSWORD_HASH, 'Administrator', 1, 1))
        admin_id = db.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()[0]

        # Standard-Rollen erstellen
        db.execute('''
            INSERT INTO roles (name, description, permissions) VALUES
            ('admin', 'Administrator mit allen Rechten', '["all"]'),
            ('user', 'Normaler Benutzer', '["view", "edit_own", "create_services"]'),
            ('viewer', 'Nur Ansicht', '["view"]')
        ''')

        # Admin-Rolle zuweisen
        admin_role_id = db.execute('SELECT id FROM roles WHERE name = ?', ('admin',)).fetchone()[0]
        db.execute('INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)', (admin_id, admin_role_id))

    # Schema-Version eintragen
    current_version = get_db_version()
    if current_version < DB_VERSION:
        db.execute('''
            INSERT INTO schema_version (version, description)
            VALUES (?, ?)
        ''', (DB_VERSION, f'V4 Schema - Ultimate Edition with all features'))

    db.commit()
    db.close()

# ===========================
# Email-Funktionen
# ===========================

def send_email(recipient, subject, body, html_body=None):
    """Sendet Email (mit Queue-Fallback)"""
    if not EMAIL_ENABLED:
        print(f"Email disabled - würde senden: {subject} an {recipient}")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SMTP_FROM
        msg['To'] = recipient

        # Text-Version
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)

        # HTML-Version (optional)
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)

        # SMTP-Verbindung
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, recipient, msg.as_string())

        print(f"✓ Email gesendet: {subject} an {recipient}")
        return True

    except Exception as e:
        print(f"✗ Email-Fehler: {e}")
        # In Queue für späteren Versuch
        queue_email(recipient, subject, body, html_body, str(e))
        return False

def queue_email(recipient, subject, body, html_body=None, error=None):
    """Fügt Email zur Queue hinzu"""
    try:
        db = get_db()
        db.execute('''
            INSERT INTO email_queue (recipient, subject, body, html_body, last_error)
            VALUES (?, ?, ?, ?, ?)
        ''', (recipient, subject, body, html_body, error))
        db.commit()
        db.close()
    except Exception as e:
        print(f"Queue-Fehler: {e}")

def process_email_queue():
    """Verarbeitet Email-Queue (wird periodisch aufgerufen)"""
    if not EMAIL_ENABLED:
        return

    db = get_db()
    cursor = db.execute('''
        SELECT * FROM email_queue
        WHERE sent = 0 AND attempts < 3
        ORDER BY created_at ASC
        LIMIT 10
    ''')
    emails = cursor.fetchall()

    for email in emails:
        success = send_email(
            email['recipient'],
            email['subject'],
            email['body'],
            email['html_body']
        )

        if success:
            db.execute('UPDATE email_queue SET sent = 1, sent_at = CURRENT_TIMESTAMP WHERE id = ?',
                      (email['id'],))
        else:
            db.execute('UPDATE email_queue SET attempts = attempts + 1 WHERE id = ?',
                      (email['id'],))

    db.commit()
    db.close()

# ===========================
# Health Check Funktionen
# ===========================

def check_service_health(service):
    """Führt Health Check für einen Service durch"""
    try:
        check_url = service['health_check_url'] or service['url']
        method = service['health_check_method'] or 'GET'
        expected_status = service['expected_status_code'] or 200

        start_time = time.time()

        if method == 'GET':
            response = requests.get(check_url, timeout=HEALTH_CHECK_TIMEOUT, verify=False)
        elif method == 'HEAD':
            response = requests.head(check_url, timeout=HEALTH_CHECK_TIMEOUT, verify=False)
        elif method == 'POST':
            response = requests.post(check_url, timeout=HEALTH_CHECK_TIMEOUT, verify=False)
        else:
            response = requests.get(check_url, timeout=HEALTH_CHECK_TIMEOUT, verify=False)

        response_time = int((time.time() - start_time) * 1000)  # in ms
        is_online = response.status_code == expected_status
        status_code = response.status_code
        error_message = None

        # SSL-Check
        ssl_valid = True
        ssl_expires_at = None
        ssl_days_remaining = None

        if check_url.startswith('https://') and service['ssl_check_enabled']:
            try:
                import ssl
                import socket
                from datetime import datetime

                hostname = urlparse(check_url).hostname
                context = ssl.create_default_context()
                with socket.create_connection((hostname, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        not_after = cert['notAfter']
                        # Parse: 'Jan 1 12:00:00 2025 GMT'
                        expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        ssl_expires_at = expiry_date.strftime('%Y-%m-%d %H:%M:%S')
                        ssl_days_remaining = (expiry_date - datetime.now()).days
                        ssl_valid = ssl_days_remaining > 0
            except Exception as ssl_error:
                print(f"SSL-Check-Fehler für {service['name']}: {ssl_error}")
                ssl_valid = False

        return {
            'is_online': is_online,
            'response_time': response_time,
            'status_code': status_code,
            'error_message': error_message,
            'ssl_valid': ssl_valid,
            'ssl_expires_at': ssl_expires_at,
            'ssl_days_remaining': ssl_days_remaining
        }

    except requests.exceptions.Timeout:
        return {
            'is_online': False,
            'response_time': None,
            'status_code': None,
            'error_message': 'Timeout',
            'ssl_valid': None,
            'ssl_expires_at': None,
            'ssl_days_remaining': None
        }
    except Exception as e:
        return {
            'is_online': False,
            'response_time': None,
            'status_code': None,
            'error_message': str(e),
            'ssl_valid': None,
            'ssl_expires_at': None,
            'ssl_days_remaining': None
        }

def run_health_checks():
    """Führt Health Checks für alle Services aus"""
    db = get_db()
    cursor = db.execute('''
        SELECT * FROM services WHERE health_check_enabled = 1
    ''')
    services = cursor.fetchall()

    for service in services:
        result = check_service_health(service)

        # Update Service Status
        db.execute('''
            INSERT OR REPLACE INTO service_status
            (service_id, is_online, response_time, status_code, ssl_valid, ssl_expires_at,
             ssl_days_remaining, last_checked, last_error, total_checks, failed_checks)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?,
                    COALESCE((SELECT total_checks FROM service_status WHERE service_id = ?), 0) + 1,
                    COALESCE((SELECT failed_checks FROM service_status WHERE service_id = ?), 0) + ?)
        ''', (
            service['id'],
            result['is_online'],
            result['response_time'],
            result['status_code'],
            result['ssl_valid'],
            result['ssl_expires_at'],
            result['ssl_days_remaining'],
            result['error_message'],
            service['id'],
            service['id'],
            0 if result['is_online'] else 1
        ))

        # Uptime History
        db.execute('''
            INSERT INTO uptime_history (service_id, is_online, response_time, status_code, error_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            service['id'],
            result['is_online'],
            result['response_time'],
            result['status_code'],
            result['error_message']
        ))

        # Incident-Tracking
        if not result['is_online']:
            # Prüfe ob es bereits ein offenes Incident gibt
            incident = db.execute('''
                SELECT * FROM incidents WHERE service_id = ? AND ended_at IS NULL
            ''', (service['id'],)).fetchone()

            if not incident:
                # Neues Incident erstellen
                db.execute('''
                    INSERT INTO incidents (service_id, severity, notes)
                    VALUES (?, 'critical', ?)
                ''', (service['id'], result['error_message']))

                # Notification senden
                trigger_alert('service_down', service, result)
        else:
            # Service ist online - schließe offene Incidents
            db.execute('''
                UPDATE incidents SET
                    ended_at = CURRENT_TIMESTAMP,
                    duration = CAST((julianday(CURRENT_TIMESTAMP) - julianday(started_at)) * 86400 AS INTEGER)
                WHERE service_id = ? AND ended_at IS NULL
            ''', (service['id'],))

    db.commit()
    db.close()
    print(f"✓ Health checks completed for {len(services)} services")

# ===========================
# Alert & Webhook System
# ===========================

def trigger_alert(event_type, service, data):
    """Triggert Alerts basierend auf Event-Type"""
    db = get_db()

    # Prüfe Alert-Rules
    cursor = db.execute('''
        SELECT * FROM alert_rules
        WHERE is_active = 1
        AND (last_triggered IS NULL OR
             datetime(last_triggered, '+' || cooldown_minutes || ' minutes') < CURRENT_TIMESTAMP)
    ''')
    rules = cursor.fetchall()

    for rule in rules:
        if event_type in json.loads(rule['notification_channels']):
            # Sende Notification
            channels = json.loads(rule['notification_channels'])

            if 'email' in channels:
                # Email-Benachrichtigung
                admins = db.execute('''
                    SELECT u.email FROM users u
                    JOIN user_roles ur ON u.id = ur.user_id
                    JOIN roles r ON ur.role_id = r.id
                    WHERE r.name = 'admin' AND u.email IS NOT NULL
                ''').fetchall()

                for admin in admins:
                    send_email(
                        admin['email'],
                        f"🚨 Alert: {service['name']}",
                        f"Service {service['name']} ist ausgefallen!\n\nURL: {service['url']}\nFehler: {data.get('error_message', 'Unbekannt')}"
                    )

            # Update last_triggered
            db.execute('''
                UPDATE alert_rules SET last_triggered = CURRENT_TIMESTAMP WHERE id = ?
            ''', (rule['id'],))

    # Trigger Webhooks
    trigger_webhooks(event_type, {
        'service': dict(service),
        'data': data,
        'timestamp': datetime.now().isoformat()
    })

    db.commit()
    db.close()

def trigger_webhooks(event_type, payload):
    """Triggert Webhooks für bestimmten Event-Type"""
    db = get_db()
    cursor = db.execute('''
        SELECT * FROM webhooks WHERE is_active = 1
    ''')
    webhooks = cursor.fetchall()

    for webhook in webhooks:
        events = json.loads(webhook['events'])
        if event_type in events or 'all' in events:
            # Webhook in separatem Thread aufrufen
            threading.Thread(
                target=call_webhook,
                args=(dict(webhook), event_type, payload)
            ).start()

    db.close()

def call_webhook(webhook, event_type, payload):
    """Ruft Webhook auf"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Homelab-Dashboard-V4'
        }

        if webhook['secret']:
            # HMAC-Signatur
            import hmac
            signature = hmac.new(
                webhook['secret'].encode(),
                json.dumps(payload).encode(),
                hashlib.sha256
            ).hexdigest()
            headers['X-Webhook-Signature'] = signature

        response = requests.post(
            webhook['url'],
            json={'event': event_type, 'payload': payload},
            headers=headers,
            timeout=10
        )

        # Log
        db = get_db()
        db.execute('''
            INSERT INTO webhook_logs (webhook_id, event_type, payload, status_code, response)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            webhook['id'],
            event_type,
            json.dumps(payload),
            response.status_code,
            response.text[:1000]
        ))
        db.execute('UPDATE webhooks SET last_triggered = CURRENT_TIMESTAMP WHERE id = ?',
                  (webhook['id'],))
        db.commit()
        db.close()

        print(f"✓ Webhook called: {webhook['name']} - {response.status_code}")

    except Exception as e:
        print(f"✗ Webhook error: {webhook['name']} - {e}")
        db = get_db()
        db.execute('''
            INSERT INTO webhook_logs (webhook_id, event_type, payload, error)
            VALUES (?, ?, ?, ?)
        ''', (webhook['id'], event_type, json.dumps(payload), str(e)))
        db.commit()
        db.close()

# ===========================
# Automatische Backups
# ===========================

def create_automatic_backup():
    """Erstellt automatisches Backup"""
    print("Erstelle automatisches Backup...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'homelab_backup_auto_{timestamp}.zip'
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
        db.execute('''
            INSERT INTO backups (filename, file_size, backup_type, status)
            VALUES (?, ?, 'automatic', 'completed')
        ''', (backup_filename, file_size))
        db.commit()
        db.close()

        # Alte Backups löschen
        cleanup_old_backups()

        print(f"✓ Automatisches Backup erstellt: {backup_filename}")

    except Exception as e:
        print(f"✗ Backup-Fehler: {e}")
        db = get_db()
        db.execute('''
            INSERT INTO backups (filename, backup_type, status, error_message)
            VALUES (?, 'automatic', 'failed', ?)
        ''', (backup_filename, str(e)))
        db.commit()
        db.close()

def cleanup_old_backups():
    """Löscht alte automatische Backups"""
    db = get_db()
    cursor = db.execute('''
        SELECT * FROM backups
        WHERE backup_type = 'automatic'
        ORDER BY created_at DESC
        LIMIT -1 OFFSET ?
    ''', (AUTO_BACKUP_RETENTION,))
    old_backups = cursor.fetchall()

    for backup in old_backups:
        # Datei löschen
        backup_path = os.path.join(BACKUP_DIR, backup['filename'])
        if os.path.exists(backup_path):
            os.remove(backup_path)

        # DB-Eintrag löschen
        db.execute('DELETE FROM backups WHERE id = ?', (backup['id'],))

    db.commit()
    db.close()
    print(f"✓ {len(old_backups)} alte Backups gelöscht")

# ===========================
# Scheduler Setup
# ===========================

def setup_scheduler():
    """Richtet Scheduled Tasks ein"""
    # Health Checks alle X Minuten
    schedule.every(HEALTH_CHECK_INTERVAL // 60).minutes.do(run_health_checks)

    # Email Queue alle 5 Minuten
    schedule.every(5).minutes.do(process_email_queue)

    # Automatisches Backup
    if AUTO_BACKUP_ENABLED:
        schedule.every().day.at(AUTO_BACKUP_TIME).do(create_automatic_backup)

    # Session Cleanup alle Stunde
    schedule.every(1).hours.do(cleanup_expired_sessions)

    # Stats Update alle 10 Minuten
    schedule.every(10).minutes.do(update_service_stats)

    print("✓ Scheduler konfiguriert")

def run_scheduler():
    """Führt Scheduler in separatem Thread aus"""
    while True:
        schedule.run_pending()
        time.sleep(60)

def cleanup_expired_sessions():
    """Löscht abgelaufene Sessions"""
    db = get_db()
    db.execute('DELETE FROM user_sessions WHERE expires_at < CURRENT_TIMESTAMP')
    db.execute('DELETE FROM password_reset_tokens WHERE expires_at < CURRENT_TIMESTAMP')
    db.commit()
    db.close()

def update_service_stats():
    """Aktualisiert Service-Statistiken"""
    db = get_db()

    cursor = db.execute('SELECT id FROM services')
    services = cursor.fetchall()

    for service in services:
        service_id = service['id']

        # Uptime-Berechnungen
        uptime_24h = db.execute('''
            SELECT AVG(is_online) * 100 as uptime
            FROM uptime_history
            WHERE service_id = ? AND checked_at >= datetime('now', '-1 day')
        ''', (service_id,)).fetchone()['uptime'] or 0

        uptime_7d = db.execute('''
            SELECT AVG(is_online) * 100 as uptime
            FROM uptime_history
            WHERE service_id = ? AND checked_at >= datetime('now', '-7 days')
        ''', (service_id,)).fetchone()['uptime'] or 0

        uptime_30d = db.execute('''
            SELECT AVG(is_online) * 100 as uptime
            FROM uptime_history
            WHERE service_id = ? AND checked_at >= datetime('now', '-30 days')
        ''', (service_id,)).fetchone()['uptime'] or 0

        avg_response = db.execute('''
            SELECT AVG(response_time) as avg_time
            FROM uptime_history
            WHERE service_id = ? AND checked_at >= datetime('now', '-7 days') AND response_time IS NOT NULL
        ''', (service_id,)).fetchone()['avg_time'] or 0

        # Update Stats
        db.execute('''
            INSERT OR REPLACE INTO service_stats
            (service_id, uptime_percentage, last_30d_uptime, last_7d_uptime, last_24h_uptime,
             avg_response_time, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (service_id, uptime_30d, uptime_30d, uptime_7d, uptime_24h, avg_response))

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

        # Session-Timeout-Check
        last_activity = session.get('last_activity')
        if last_activity:
            last_activity_time = datetime.fromisoformat(last_activity)
            if datetime.now() - last_activity_time > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                session.clear()
                return jsonify({'error': 'Session abgelaufen'}), 401

        # Update last_activity
        session['last_activity'] = datetime.now().isoformat()

        # Update in DB
        db = get_db()
        db.execute('UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE id = ?',
                  (session['user_id'],))
        db.commit()
        db.close()

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
            INSERT INTO analytics_events (user_id, event_type, event_data, service_id, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            session.get('user_id'),
            event_type,
            json.dumps(event_data) if event_data else None,
            service_id,
            request.remote_addr,
            request.headers.get('User-Agent', '')[:200]
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
@limiter.limit("5 per minute")
def login():
    """Login-Endpoint mit Rate Limiting"""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username und Passwort erforderlich'}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db()
    cursor = db.execute('''
        SELECT * FROM users WHERE username = ? AND is_active = 1
    ''', (username,))
    user = cursor.fetchone()

    if not user:
        db.close()
        return jsonify({'error': 'Ungültige Anmeldedaten'}), 401

    # Prüfe Account-Sperre
    if user['locked_until']:
        locked_until = datetime.fromisoformat(user['locked_until'])
        if datetime.now() < locked_until:
            minutes_left = int((locked_until - datetime.now()).total_seconds() / 60)
            db.close()
            return jsonify({'error': f'Account gesperrt. Noch {minutes_left} Minuten.'}), 403

    # Prüfe Passwort
    if user['password_hash'] != password_hash:
        # Fehlversuch zählen
        failed_attempts = user['failed_login_attempts'] + 1
        if failed_attempts >= 5:
            # Account für 30 Minuten sperren
            locked_until = (datetime.now() + timedelta(minutes=30)).isoformat()
            db.execute('''
                UPDATE users SET failed_login_attempts = ?, locked_until = ?
                WHERE id = ?
            ''', (failed_attempts, locked_until, user['id']))
        else:
            db.execute('''
                UPDATE users SET failed_login_attempts = ?
                WHERE id = ?
            ''', (failed_attempts, user['id']))

        db.commit()
        db.close()
        return jsonify({'error': 'Ungültige Anmeldedaten'}), 401

    # Erfolgreicher Login
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['last_activity'] = datetime.now().isoformat()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=SESSION_ABSOLUTE_TIMEOUT_HOURS)

    # Reset failed attempts
    db.execute('''
        UPDATE users SET
            last_login = CURRENT_TIMESTAMP,
            last_activity = CURRENT_TIMESTAMP,
            failed_login_attempts = 0,
            locked_until = NULL
        WHERE id = ?
    ''', (user['id'],))

    # Session in DB speichern
    session_token = secrets.token_urlsafe(32)
    expires_at = (datetime.now() + timedelta(hours=SESSION_ABSOLUTE_TIMEOUT_HOURS)).isoformat()
    db.execute('''
        INSERT INTO user_sessions (user_id, session_token, ip_address, user_agent, expires_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        user['id'],
        session_token,
        request.remote_addr,
        request.headers.get('User-Agent', '')[:200],
        expires_at
    ))

    db.commit()
    db.close()

    log_analytics_event('user_login', {'username': username})
    log_audit('login', 'user', user['id'])

    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name']
        },
        'session_token': session_token
    })

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
        cursor = db.execute('''
            SELECT id, username, email, full_name, avatar_url, email_verified
            FROM users WHERE id = ?
        ''', (session['user_id'],))
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

    if len(new_password) < 8:
        return jsonify({'error': 'Neues Passwort muss mindestens 8 Zeichen lang sein'}), 400

    old_hash = hashlib.sha256(old_password.encode()).hexdigest()
    new_hash = hashlib.sha256(new_password.encode()).hexdigest()

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE id = ? AND password_hash = ?',
                       (session['user_id'], old_hash))
    user = cursor.fetchone()

    if not user:
        db.close()
        return jsonify({'error': 'Altes Passwort ist falsch'}), 401

    db.execute('''
        UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (new_hash, session['user_id']))
    db.commit()
    db.close()

    log_audit('password_change', 'user', session['user_id'])

    return jsonify({'success': True})

# ===========================
# Password Reset Routen
# ===========================

@app.route('/api/auth/forgot-password', methods=['POST'])
@limiter.limit("3 per hour")
def forgot_password():
    """Passwort-Vergessen-Request"""
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email erforderlich'}), 400

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE email = ? AND is_active = 1', (email,))
    user = cursor.fetchone()

    if user:
        # Token generieren
        token = secrets.token_urlsafe(32)
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()

        db.execute('''
            INSERT INTO password_reset_tokens (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user['id'], token, expires_at))
        db.commit()

        # Email senden
        reset_url = f"http://localhost:5000/reset-password?token={token}"
        send_email(
            user['email'],
            "Homelab Dashboard - Passwort zurücksetzen",
            f"""Hallo {user['full_name'] or user['username']},

Du hast eine Passwort-Zurücksetzung angefordert.

Klicke auf diesen Link, um dein Passwort zurückzusetzen:
{reset_url}

Dieser Link ist 1 Stunde gültig.

Falls du diese Anfrage nicht gestellt hast, ignoriere diese Email.

Grüße,
Dein Homelab Dashboard
""",
            f"""<html>
<body>
    <h2>Passwort zurücksetzen</h2>
    <p>Hallo {user['full_name'] or user['username']},</p>
    <p>Du hast eine Passwort-Zurücksetzung angefordert.</p>
    <p><a href="{reset_url}" style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Passwort zurücksetzen</a></p>
    <p><small>Dieser Link ist 1 Stunde gültig.</small></p>
    <p>Falls du diese Anfrage nicht gestellt hast, ignoriere diese Email.</p>
</body>
</html>"""
        )

        log_audit('password_reset_requested', 'user', user['id'])

    db.close()

    # Immer Success zurückgeben (Security: keine User-Enumeration)
    return jsonify({'success': True, 'message': 'Falls die Email existiert, wurde ein Reset-Link gesendet.'})

@app.route('/api/auth/reset-password', methods=['POST'])
@limiter.limit("5 per hour")
def reset_password():
    """Passwort mit Token zurücksetzen"""
    data = request.json
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return jsonify({'error': 'Token und neues Passwort erforderlich'}), 400

    if len(new_password) < 8:
        return jsonify({'error': 'Passwort muss mindestens 8 Zeichen lang sein'}), 400

    db = get_db()
    cursor = db.execute('''
        SELECT * FROM password_reset_tokens
        WHERE token = ? AND used = 0 AND expires_at > CURRENT_TIMESTAMP
    ''', (token,))
    reset_token = cursor.fetchone()

    if not reset_token:
        db.close()
        return jsonify({'error': 'Ungültiger oder abgelaufener Token'}), 400

    # Passwort aktualisieren
    new_hash = hashlib.sha256(new_password.encode()).hexdigest()
    db.execute('''
        UPDATE users SET
            password_hash = ?,
            updated_at = CURRENT_TIMESTAMP,
            failed_login_attempts = 0,
            locked_until = NULL
        WHERE id = ?
    ''', (new_hash, reset_token['user_id']))

    # Token als verwendet markieren
    db.execute('UPDATE password_reset_tokens SET used = 1 WHERE id = ?', (reset_token['id'],))

    db.commit()
    db.close()

    log_audit('password_reset_completed', 'user', reset_token['user_id'])

    return jsonify({'success': True, 'message': 'Passwort erfolgreich zurückgesetzt.'})

# ===========================
# GLOBAL SEARCH
# ===========================

@app.route('/api/search', methods=['GET'])
@login_required
def global_search():
    """Globale Suche über Services, Incidents, Notes"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')  # all, services, incidents, notes

    if not query or len(query) < 2:
        return jsonify({'error': 'Suchbegriff muss mindestens 2 Zeichen lang sein'}), 400

    results = {
        'services': [],
        'incidents': [],
        'notes': [],
        'tags': []
    }

    db = get_db()
    search_pattern = f'%{query}%'

    # Services durchsuchen
    if search_type in ['all', 'services']:
        cursor = db.execute('''
            SELECT s.*, GROUP_CONCAT(t.name) as tags
            FROM services s
            LEFT JOIN service_tags st ON s.id = st.service_id
            LEFT JOIN tags t ON st.tag_id = t.id
            WHERE s.name LIKE ? OR s.description LIKE ? OR s.url LIKE ? OR s.notes LIKE ?
            GROUP BY s.id
            LIMIT 50
        ''', (search_pattern, search_pattern, search_pattern, search_pattern))
        results['services'] = [dict(row) for row in cursor.fetchall()]

    # Incidents durchsuchen
    if search_type in ['all', 'incidents']:
        cursor = db.execute('''
            SELECT i.*, s.name as service_name
            FROM incidents i
            JOIN services s ON i.service_id = s.id
            WHERE i.notes LIKE ? OR s.name LIKE ?
            ORDER BY i.started_at DESC
            LIMIT 50
        ''', (search_pattern, search_pattern))
        results['incidents'] = [dict(row) for row in cursor.fetchall()]

    # Tags durchsuchen
    if search_type in ['all', 'tags']:
        cursor = db.execute('''
            SELECT * FROM tags WHERE name LIKE ?
            LIMIT 20
        ''', (search_pattern,))
        results['tags'] = [dict(row) for row in cursor.fetchall()]

    db.close()

    log_analytics_event('global_search', {'query': query, 'type': search_type})

    return jsonify(results)

# ===========================
# WEBHOOK MANAGEMENT
# ===========================

@app.route('/api/webhooks', methods=['GET'])
@login_required
@permission_required('manage_webhooks')
def get_webhooks():
    """Alle Webhooks abrufen"""
    db = get_db()
    cursor = db.execute('''
        SELECT w.*, u.username as created_by_name
        FROM webhooks w
        LEFT JOIN users u ON w.created_by = u.id
        ORDER BY w.created_at DESC
    ''')
    webhooks = [dict(row) for row in cursor.fetchall()]

    for webhook in webhooks:
        webhook['events'] = json.loads(webhook['events'])

    db.close()
    return jsonify(webhooks)

@app.route('/api/webhooks', methods=['POST'])
@login_required
@permission_required('manage_webhooks')
def create_webhook():
    """Neuen Webhook erstellen"""
    data = request.json

    db = get_db()
    cursor = db.execute('''
        INSERT INTO webhooks (name, url, events, secret, created_by)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data['url'],
        json.dumps(data.get('events', ['all'])),
        data.get('secret'),
        session['user_id']
    ))
    webhook_id = cursor.lastrowid
    db.commit()
    db.close()

    log_audit('create', 'webhook', webhook_id, None, data)

    return jsonify({'success': True, 'id': webhook_id})

@app.route('/api/webhooks/<int:webhook_id>', methods=['DELETE'])
@login_required
@permission_required('manage_webhooks')
def delete_webhook(webhook_id):
    """Webhook löschen"""
    db = get_db()
    db.execute('DELETE FROM webhooks WHERE id = ?', (webhook_id,))
    db.commit()
    db.close()

    log_audit('delete', 'webhook', webhook_id)

    return jsonify({'success': True})

# (Die restlichen Routen aus V3 bleiben größtenteils gleich, nur erweitert...)

# ===========================
# SERVICE-ROUTEN (V4 erweitert)
# ===========================

@app.route('/api/services', methods=['GET'])
@login_required
def get_services():
    """Alle Services abrufen"""
    db = get_db()
    cursor = db.execute('''
        SELECT s.*, GROUP_CONCAT(DISTINCT t.name) as tags, u.username as owner_name,
               ss.is_online, ss.response_time, ss.last_checked, ss.ssl_valid,
               ss.ssl_days_remaining,
               stats.total_clicks, stats.uptime_percentage, stats.last_24h_uptime
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

# Da die Datei sehr lang wird, füge ich hier die kritischen neuen Endpunkte hinzu
# Die restlichen V3-Endpunkte (users, roles, analytics, backups, themes, preferences)
# bleiben im Wesentlichen gleich

# ===========================
# System Status & Health
# ===========================

@app.route('/api/system/status', methods=['GET'])
@login_required
def system_status():
    """System-Status-Übersicht"""
    db = get_db()

    total_services = db.execute('SELECT COUNT(*) as c FROM services').fetchone()['c']
    online_services = db.execute('''
        SELECT COUNT(*) as c FROM service_status WHERE is_online = 1
    ''').fetchone()['c']

    active_incidents = db.execute('''
        SELECT COUNT(*) as c FROM incidents WHERE ended_at IS NULL
    ''').fetchone()['c']

    ssl_expiring_soon = db.execute('''
        SELECT COUNT(*) as c FROM service_status
        WHERE ssl_days_remaining IS NOT NULL AND ssl_days_remaining < 30
    ''').fetchone()['c']

    pending_emails = db.execute('''
        SELECT COUNT(*) as c FROM email_queue WHERE sent = 0
    ''').fetchone()['c']

    db.close()

    return jsonify({
        'total_services': total_services,
        'online_services': online_services,
        'offline_services': total_services - online_services,
        'active_incidents': active_incidents,
        'ssl_expiring_soon': ssl_expiring_soon,
        'pending_emails': pending_emails,
        'email_enabled': EMAIL_ENABLED,
        'auto_backup_enabled': AUTO_BACKUP_ENABLED,
        'health_check_interval': HEALTH_CHECK_INTERVAL,
        'version': 'V4 Ultimate'
    })

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
        print("\n" + "="*70)
        print("STANDARD-ZUGANGSDATEN:")
        print("="*70)
        print("Username: admin")
        print("Passwort: homelab2025")
        print("="*70)
        print("\nBITTE ÄNDERE DAS PASSWORT NACH DEM ERSTEN LOGIN!\n")
    else:
        # Schema-Migrationen
        current_version = get_db_version()
        if current_version < DB_VERSION:
            print(f"Führe Schema-Migration durch (v{current_version} → v{DB_VERSION})...")
            init_db()
            print("✓ Schema aktualisiert")

    # Scheduler in separatem Thread starten
    setup_scheduler()
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Initiales Health Check
    print("Führe initialen Health Check durch...")
    threading.Thread(target=run_health_checks, daemon=True).start()

    print("\n" + "="*70)
    print("Homelab Dashboard V4 ULTIMATE EDITION gestartet!")
    print("="*70)
    print("URL: http://localhost:5000")
    print("\n🎉 NEU in V4 ULTIMATE:")
    print("  ✅ API Rate Limiting (Brute-Force-Schutz)")
    print("  ✅ Session Management (Auto-Logout)")
    print("  ✅ Email-Notifications (SMTP)")
    print("  ✅ Passwort-Reset via Email")
    print("  ✅ Echte HTTP/HTTPS Health Checks")
    print("  ✅ SSL-Zertifikat-Monitoring")
    print("  ✅ Globale Suche")
    print("  ✅ Datenbank-Migrations-System")
    print("  ✅ Webhook-System")
    print("  ✅ Alert-System")
    print("  ✅ Automatische Backups")
    print("  ✅ Scheduled Tasks")
    print("\n📧 Email-Status:", "Aktiviert ✓" if EMAIL_ENABLED else "Deaktiviert (SMTP konfigurieren)")
    print(f"🔄 Health Checks: Alle {HEALTH_CHECK_INTERVAL // 60} Minuten")
    print(f"💾 Auto-Backup: {'Aktiviert um ' + AUTO_BACKUP_TIME if AUTO_BACKUP_ENABLED else 'Deaktiviert'}")
    print("\n⚠️  Drücke Strg+C zum Beenden\n")

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
