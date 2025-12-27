#!/usr/bin/env python3
"""
Password Security Suite - Backend API
Provides password generation, strength checking, and security analysis
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import secrets
import string
import hashlib
import requests
import re
import math
from collections import Counter
import json

app = Flask(__name__, static_folder='.')
CORS(app)

# ===========================
# Word Lists for Passphrases
# ===========================
COMMON_WORDS = [
    "apple", "banana", "cherry", "dragon", "eagle", "forest", "galaxy", "harbor",
    "island", "jungle", "kingdom", "lemon", "mountain", "nebula", "ocean", "planet",
    "quantum", "river", "sunset", "thunder", "universe", "valley", "whisper", "xenon",
    "yellow", "zephyr", "anchor", "bridge", "castle", "desert", "engine", "falcon",
    "garden", "helmet", "ignite", "jasper", "knight", "ladder", "marble", "nature",
    "orange", "purple", "quartz", "rocket", "silver", "turtle", "unicorn", "violet",
    "winter", "wizard", "bronze", "coffee", "diamond", "emerald", "feline", "golden",
    "hammer", "indigo", "jacket", "kitten", "lantern", "magnet", "noodle", "osprey",
    "parrot", "quiver", "rabbit", "salmon", "travel", "uplift", "velvet", "walrus",
    "yellow", "zigzag", "artist", "ballet", "candle", "dancer", "eclipse", "flight",
    "guitar", "heaven", "insect", "jigsaw", "kettle", "lizard", "mirror", "nectar",
    "oyster", "pickle", "quiets", "riddle", "scroll", "temple", "upward", "vision",
    "waffle", "yogurt", "zenith", "attack", "butter", "carbon", "decode", "ethics"
]

# ===========================
# Password Generation
# ===========================
class PasswordGenerator:
    """Generate secure passwords with various options"""

    @staticmethod
    def generate(
        length=16,
        use_uppercase=True,
        use_lowercase=True,
        use_digits=True,
        use_symbols=True,
        exclude_ambiguous=False,
        exclude_similar=False,
        custom_chars=""
    ):
        """Generate a random password with specified criteria"""

        # Build character pool
        chars = ""

        if custom_chars:
            chars = custom_chars
        else:
            if use_lowercase:
                chars += string.ascii_lowercase
            if use_uppercase:
                chars += string.ascii_uppercase
            if use_digits:
                chars += string.digits
            if use_symbols:
                chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

            # Remove ambiguous characters
            if exclude_ambiguous:
                ambiguous = "il1Lo0O"
                chars = ''.join(c for c in chars if c not in ambiguous)

            # Remove similar looking characters
            if exclude_similar:
                similar = "il1Lo0O"
                chars = ''.join(c for c in chars if c not in similar)

        if not chars:
            raise ValueError("No characters available for password generation")

        # Generate password
        password = ''.join(secrets.choice(chars) for _ in range(length))

        return password

    @staticmethod
    def generate_passphrase(
        num_words=4,
        separator="-",
        capitalize=True,
        add_number=True
    ):
        """Generate a memorable passphrase"""

        words = [secrets.choice(COMMON_WORDS) for _ in range(num_words)]

        if capitalize:
            words = [w.capitalize() for w in words]

        passphrase = separator.join(words)

        if add_number:
            passphrase += separator + str(secrets.randbelow(9999)).zfill(4)

        return passphrase

    @staticmethod
    def generate_pin(length=4):
        """Generate a random PIN"""
        return ''.join(str(secrets.randbelow(10)) for _ in range(length))

    @staticmethod
    def generate_memorable(length=12):
        """Generate a more memorable password with pattern"""
        # Pattern: Consonant-Vowel-Consonant structure
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"

        password = ""
        for i in range(length // 2):
            password += secrets.choice(consonants)
            password += secrets.choice(vowels)

        # Add some numbers and capitalize
        password = password.capitalize()
        password += str(secrets.randbelow(999)).zfill(3)

        return password


# ===========================
# Password Strength Checker
# ===========================
class PasswordStrengthChecker:
    """Analyze password strength and provide feedback"""

    # Common passwords list (subset)
    COMMON_PASSWORDS = [
        "password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567",
        "letmein", "trustno1", "dragon", "baseball", "iloveyou", "master", "sunshine",
        "ashley", "bailey", "passw0rd", "shadow", "123123", "654321", "superman",
        "qazwsx", "michael", "football", "welcome", "jesus", "ninja", "mustang"
    ]

    @staticmethod
    def check_strength(password):
        """
        Analyze password strength and return detailed metrics
        Returns: dict with score (0-100), strength level, and feedback
        """

        if not password:
            return {
                "score": 0,
                "strength": "Very Weak",
                "feedback": ["Password is empty"],
                "details": {}
            }

        score = 0
        feedback = []
        details = {}

        # Length check
        length = len(password)
        details["length"] = length

        if length < 8:
            feedback.append("Password is too short (minimum 8 characters)")
        elif length < 12:
            score += 10
            feedback.append("Consider using at least 12 characters")
        elif length < 16:
            score += 20
        else:
            score += 30

        # Character variety
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))

        details["has_lowercase"] = has_lower
        details["has_uppercase"] = has_upper
        details["has_digits"] = has_digit
        details["has_symbols"] = has_symbol

        char_variety = sum([has_lower, has_upper, has_digit, has_symbol])

        if char_variety == 1:
            feedback.append("Use different character types (uppercase, lowercase, numbers, symbols)")
        elif char_variety == 2:
            score += 10
            feedback.append("Add more character variety")
        elif char_variety == 3:
            score += 20
        else:
            score += 30

        # Entropy calculation
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += 32

        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        details["entropy"] = round(entropy, 2)

        if entropy < 28:
            feedback.append("Very low entropy - easily crackable")
        elif entropy < 36:
            score += 5
        elif entropy < 60:
            score += 15
        else:
            score += 25

        # Check for common patterns
        lower_pass = password.lower()

        # Common passwords
        if lower_pass in PasswordStrengthChecker.COMMON_PASSWORDS:
            feedback.append("This is a commonly used password!")
            score = max(0, score - 30)
            details["is_common"] = True
        else:
            details["is_common"] = False

        # Sequential characters
        if any(seq in lower_pass for seq in ['123', 'abc', 'qwerty', '987', 'zyx']):
            feedback.append("Avoid sequential characters")
            score = max(0, score - 10)
            details["has_sequential"] = True
        else:
            details["has_sequential"] = False

        # Repeated characters
        if re.search(r'(.)\1{2,}', password):
            feedback.append("Avoid repeated characters (e.g., 'aaa', '111')")
            score = max(0, score - 10)
            details["has_repeated"] = True
        else:
            details["has_repeated"] = False

        # Check for common words
        common_words = ['password', 'admin', 'user', 'login', 'welcome']
        if any(word in lower_pass for word in common_words):
            feedback.append("Avoid common words like 'password' or 'admin'")
            score = max(0, score - 15)

        # Character distribution (more varied = better)
        char_freq = Counter(password)
        unique_ratio = len(char_freq) / length if length > 0 else 0
        details["unique_char_ratio"] = round(unique_ratio, 2)

        if unique_ratio > 0.8:
            score += 10
        elif unique_ratio < 0.5:
            feedback.append("Too many repeated characters")
            score = max(0, score - 5)

        # Bonus points
        if length >= 20:
            score += 5
            feedback.append("Excellent length!")

        # Cap score at 100
        score = min(100, score)

        # Determine strength level
        if score < 20:
            strength = "Very Weak"
        elif score < 40:
            strength = "Weak"
        elif score < 60:
            strength = "Fair"
        elif score < 80:
            strength = "Strong"
        else:
            strength = "Very Strong"

        details["score"] = score
        details["strength"] = strength

        # Estimated crack time
        crack_time = PasswordStrengthChecker.estimate_crack_time(entropy)
        details["crack_time"] = crack_time

        # If no issues, add positive feedback
        if not feedback:
            feedback.append("Excellent password!")

        return {
            "score": score,
            "strength": strength,
            "feedback": feedback,
            "details": details
        }

    @staticmethod
    def estimate_crack_time(entropy):
        """Estimate time to crack password based on entropy"""
        # Assuming 10 billion guesses per second (modern GPU)
        guesses_per_second = 10_000_000_000

        total_combinations = 2 ** entropy
        seconds = total_combinations / (2 * guesses_per_second)  # Average case

        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds/60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds/3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds/86400)} days"
        elif seconds < 31536000 * 100:
            return f"{int(seconds/31536000)} years"
        elif seconds < 31536000 * 1000:
            return "Centuries"
        elif seconds < 31536000 * 1000000:
            return "Millennia"
        else:
            return "Beyond human comprehension"


# ===========================
# Breach Check (Have I Been Pwned)
# ===========================
class BreachChecker:
    """Check if password has been exposed in data breaches"""

    HIBP_API_URL = "https://api.pwnedpasswords.com/range/"

    @staticmethod
    def check_password(password):
        """
        Check password against Have I Been Pwned database
        Uses k-anonymity to protect the password
        """
        try:
            # Hash the password
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]

            # Query API with first 5 chars
            response = requests.get(
                f"{BreachChecker.HIBP_API_URL}{prefix}",
                timeout=5
            )

            if response.status_code != 200:
                return {
                    "error": "Could not connect to breach database",
                    "breached": False
                }

            # Check if suffix exists in response
            hashes = response.text.splitlines()
            for hash_line in hashes:
                hash_suffix, count = hash_line.split(':')
                if hash_suffix == suffix:
                    return {
                        "breached": True,
                        "count": int(count),
                        "message": f"⚠️ This password has been exposed {count} times in data breaches!"
                    }

            return {
                "breached": False,
                "message": "✓ Password not found in breach databases"
            }

        except requests.exceptions.Timeout:
            return {
                "error": "Request timed out",
                "breached": False
            }
        except Exception as e:
            return {
                "error": str(e),
                "breached": False
            }


# ===========================
# API Routes
# ===========================

@app.route('/')
def index():
    """Serve main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/generate/password', methods=['POST'])
def generate_password():
    """Generate a random password"""
    data = request.json or {}

    try:
        password = PasswordGenerator.generate(
            length=data.get('length', 16),
            use_uppercase=data.get('use_uppercase', True),
            use_lowercase=data.get('use_lowercase', True),
            use_digits=data.get('use_digits', True),
            use_symbols=data.get('use_symbols', True),
            exclude_ambiguous=data.get('exclude_ambiguous', False),
            exclude_similar=data.get('exclude_similar', False),
            custom_chars=data.get('custom_chars', '')
        )

        # Also return strength analysis
        strength = PasswordStrengthChecker.check_strength(password)

        return jsonify({
            "password": password,
            "strength": strength
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/generate/passphrase', methods=['POST'])
def generate_passphrase():
    """Generate a memorable passphrase"""
    data = request.json or {}

    try:
        passphrase = PasswordGenerator.generate_passphrase(
            num_words=data.get('num_words', 4),
            separator=data.get('separator', '-'),
            capitalize=data.get('capitalize', True),
            add_number=data.get('add_number', True)
        )

        # Also return strength analysis
        strength = PasswordStrengthChecker.check_strength(passphrase)

        return jsonify({
            "passphrase": passphrase,
            "strength": strength
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/generate/pin', methods=['POST'])
def generate_pin():
    """Generate a random PIN"""
    data = request.json or {}

    try:
        pin = PasswordGenerator.generate_pin(
            length=data.get('length', 4)
        )

        return jsonify({
            "pin": pin
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/generate/memorable', methods=['POST'])
def generate_memorable():
    """Generate a memorable password"""
    data = request.json or {}

    try:
        password = PasswordGenerator.generate_memorable(
            length=data.get('length', 12)
        )

        strength = PasswordStrengthChecker.check_strength(password)

        return jsonify({
            "password": password,
            "strength": strength
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/check/strength', methods=['POST'])
def check_strength():
    """Check password strength"""
    data = request.json or {}
    password = data.get('password', '')

    strength = PasswordStrengthChecker.check_strength(password)

    return jsonify(strength)

@app.route('/api/check/breach', methods=['POST'])
def check_breach():
    """Check if password has been breached"""
    data = request.json or {}
    password = data.get('password', '')

    if not password:
        return jsonify({"error": "No password provided"}), 400

    result = BreachChecker.check_password(password)

    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    print("🔐 Password Security Suite Backend Starting...")
    print("📍 Access the application at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
