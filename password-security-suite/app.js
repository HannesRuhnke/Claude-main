// ===========================
// API Configuration
// ===========================
const API_BASE = '/api';

// ===========================
// Tab Management
// ===========================
class TabManager {
    constructor() {
        this.init();
    }

    init() {
        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchTab(btn.dataset.tab);
            });
        });
    }

    switchTab(tabId) {
        // Update buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

        // Update panes
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');
    }
}

// ===========================
// Toast Notifications
// ===========================
class ToastManager {
    constructor() {
        this.toast = document.getElementById('toast');
    }

    show(message, type = 'success') {
        this.toast.textContent = message;
        this.toast.className = `toast ${type}`;
        this.toast.classList.add('show');

        setTimeout(() => {
            this.toast.classList.remove('show');
        }, 3000);
    }

    success(message) {
        this.show(message, 'success');
    }

    error(message) {
        this.show(message, 'error');
    }
}

// ===========================
// Password Generator
// ===========================
class PasswordGeneratorUI {
    constructor() {
        this.lengthSlider = document.getElementById('password-length');
        this.lengthValue = document.getElementById('length-value');
        this.generateBtn = document.getElementById('generate-btn');
        this.refreshBtn = document.getElementById('refresh-btn');
        this.copyBtn = document.getElementById('copy-btn');
        this.passwordDisplay = document.getElementById('generated-password');

        this.init();
    }

    init() {
        // Update length value display
        this.lengthSlider.addEventListener('input', (e) => {
            this.lengthValue.textContent = e.target.value;
        });

        // Generate button
        this.generateBtn.addEventListener('click', () => this.generate());
        this.refreshBtn.addEventListener('click', () => this.generate());

        // Copy button
        this.copyBtn.addEventListener('click', () => this.copy());

        // Generate initial password
        this.generate();
    }

    async generate() {
        const settings = {
            length: parseInt(this.lengthSlider.value),
            use_uppercase: document.getElementById('use-uppercase').checked,
            use_lowercase: document.getElementById('use-lowercase').checked,
            use_digits: document.getElementById('use-digits').checked,
            use_symbols: document.getElementById('use-symbols').checked,
            exclude_ambiguous: document.getElementById('exclude-ambiguous').checked,
            custom_chars: document.getElementById('custom-chars').value
        };

        try {
            const response = await fetch(`${API_BASE}/generate/password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });

            const data = await response.json();

            if (data.error) {
                toast.error(data.error);
                return;
            }

            this.passwordDisplay.value = data.password;
            this.displayStrength(data.strength);
            toast.success('Passwort generiert! 🎉');
        } catch (error) {
            toast.error('Fehler beim Generieren');
            console.error(error);
        }
    }

    displayStrength(strength) {
        const result = document.getElementById('strength-result');
        const fill = document.getElementById('strength-fill');
        const label = document.getElementById('strength-label');
        const score = document.getElementById('strength-score');
        const details = document.getElementById('strength-details');

        result.style.display = 'block';

        // Update bar
        fill.style.width = `${strength.score}%`;
        fill.className = 'strength-fill ' + this.getStrengthClass(strength.strength);

        // Update labels
        label.textContent = strength.strength;
        score.textContent = `${strength.score}/100`;

        // Update details
        let detailsHTML = `
            <div class="details-grid">
                <div class="detail-item">
                    <span class="detail-label">Entropie:</span>
                    <span>${strength.details.entropy} bits</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Crack-Zeit:</span>
                    <span>${strength.details.crack_time}</span>
                </div>
            </div>
        `;

        details.innerHTML = detailsHTML;
    }

    getStrengthClass(strength) {
        const map = {
            'Very Weak': 'strength-very-weak',
            'Weak': 'strength-weak',
            'Fair': 'strength-fair',
            'Strong': 'strength-strong',
            'Very Strong': 'strength-very-strong'
        };
        return map[strength] || 'strength-weak';
    }

    copy() {
        const password = this.passwordDisplay.value;
        if (!password || password === 'Klicke auf \'Generieren\'') {
            toast.error('Kein Passwort zum Kopieren!');
            return;
        }

        navigator.clipboard.writeText(password).then(() => {
            toast.success('Passwort kopiert! 📋');
        }).catch(() => {
            toast.error('Kopieren fehlgeschlagen');
        });
    }
}

// ===========================
// Password Checker
// ===========================
class PasswordCheckerUI {
    constructor() {
        this.passwordInput = document.getElementById('check-password');
        this.checkBtn = document.getElementById('check-btn');
        this.toggleBtn = document.getElementById('toggle-visibility');

        this.init();
    }

    init() {
        this.checkBtn.addEventListener('click', () => this.check());
        this.toggleBtn.addEventListener('click', () => this.toggleVisibility());

        // Check on Enter key
        this.passwordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.check();
        });
    }

    toggleVisibility() {
        const type = this.passwordInput.type === 'password' ? 'text' : 'password';
        this.passwordInput.type = type;
        this.toggleBtn.textContent = type === 'password' ? '👁️' : '🙈';
    }

    async check() {
        const password = this.passwordInput.value;

        if (!password) {
            toast.error('Bitte gib ein Passwort ein!');
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/check/strength`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });

            const data = await response.json();
            this.displayResults(data);
        } catch (error) {
            toast.error('Fehler bei der Prüfung');
            console.error(error);
        }
    }

    displayResults(data) {
        const result = document.getElementById('check-result');
        result.style.display = 'block';

        // Update strength bar
        const fill = document.getElementById('check-strength-fill');
        fill.style.width = `${data.score}%`;
        fill.className = 'strength-fill ' + this.getStrengthClass(data.strength);

        // Update labels
        document.getElementById('check-strength-label').textContent = data.strength;
        document.getElementById('check-strength-score').textContent = `${data.score}/100`;

        // Update details
        document.getElementById('detail-length').textContent = data.details.length;
        document.getElementById('detail-entropy').textContent = `${data.details.entropy} bits`;
        document.getElementById('detail-crack-time').textContent = data.details.crack_time;
        document.getElementById('detail-unique').textContent =
            `${Math.round(data.details.unique_char_ratio * 100)}%`;

        // Update character checks
        this.updateCheck('check-lowercase', data.details.has_lowercase);
        this.updateCheck('check-uppercase', data.details.has_uppercase);
        this.updateCheck('check-digits', data.details.has_digits);
        this.updateCheck('check-symbols', data.details.has_symbols);

        // Update feedback
        const feedbackList = document.getElementById('feedback-list');
        feedbackList.innerHTML = data.feedback
            .map(f => `<div class="feedback-item">${f}</div>`)
            .join('');
    }

    updateCheck(id, isActive) {
        const element = document.getElementById(id);
        const icon = element.querySelector('.icon');

        if (isActive) {
            element.classList.add('active');
            icon.textContent = '✓';
        } else {
            element.classList.remove('active');
            icon.textContent = '✗';
        }
    }

    getStrengthClass(strength) {
        const map = {
            'Very Weak': 'strength-very-weak',
            'Weak': 'strength-weak',
            'Fair': 'strength-fair',
            'Strong': 'strength-strong',
            'Very Strong': 'strength-very-strong'
        };
        return map[strength] || 'strength-weak';
    }
}

// ===========================
// Passphrase Generator
// ===========================
class PassphraseGeneratorUI {
    constructor() {
        this.numWordsSlider = document.getElementById('num-words');
        this.numWordsValue = document.getElementById('num-words-value');
        this.generateBtn = document.getElementById('generate-passphrase-btn');
        this.refreshBtn = document.getElementById('refresh-passphrase-btn');
        this.copyBtn = document.getElementById('copy-passphrase-btn');
        this.passphraseDisplay = document.getElementById('generated-passphrase');

        this.init();
    }

    init() {
        // Update num words display
        this.numWordsSlider.addEventListener('input', (e) => {
            this.numWordsValue.textContent = e.target.value;
        });

        // Generate button
        this.generateBtn.addEventListener('click', () => this.generate());
        this.refreshBtn.addEventListener('click', () => this.generate());

        // Copy button
        this.copyBtn.addEventListener('click', () => this.copy());

        // Generate initial passphrase
        this.generate();
    }

    async generate() {
        const settings = {
            num_words: parseInt(this.numWordsSlider.value),
            separator: document.getElementById('separator').value,
            capitalize: document.getElementById('capitalize').checked,
            add_number: document.getElementById('add-number').checked
        };

        try {
            const response = await fetch(`${API_BASE}/generate/passphrase`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });

            const data = await response.json();

            if (data.error) {
                toast.error(data.error);
                return;
            }

            this.passphraseDisplay.value = data.passphrase;
            this.displayStrength(data.strength);
            toast.success('Passphrase generiert! 🎉');
        } catch (error) {
            toast.error('Fehler beim Generieren');
            console.error(error);
        }
    }

    displayStrength(strength) {
        const result = document.getElementById('passphrase-strength');
        const fill = document.getElementById('passphrase-strength-fill');
        const label = document.getElementById('passphrase-strength-label');
        const score = document.getElementById('passphrase-strength-score');

        result.style.display = 'block';

        // Update bar
        fill.style.width = `${strength.score}%`;
        fill.className = 'strength-fill ' + this.getStrengthClass(strength.strength);

        // Update labels
        label.textContent = strength.strength;
        score.textContent = `${strength.score}/100`;
    }

    getStrengthClass(strength) {
        const map = {
            'Very Weak': 'strength-very-weak',
            'Weak': 'strength-weak',
            'Fair': 'strength-fair',
            'Strong': 'strength-strong',
            'Very Strong': 'strength-very-strong'
        };
        return map[strength] || 'strength-weak';
    }

    copy() {
        const passphrase = this.passphraseDisplay.value;
        if (!passphrase || passphrase === 'Klicke auf \'Generieren\'') {
            toast.error('Keine Passphrase zum Kopieren!');
            return;
        }

        navigator.clipboard.writeText(passphrase).then(() => {
            toast.success('Passphrase kopiert! 📋');
        }).catch(() => {
            toast.error('Kopieren fehlgeschlagen');
        });
    }
}

// ===========================
// Breach Checker
// ===========================
class BreachCheckerUI {
    constructor() {
        this.passwordInput = document.getElementById('breach-password');
        this.checkBtn = document.getElementById('breach-check-btn');
        this.toggleBtn = document.getElementById('toggle-breach-visibility');

        this.init();
    }

    init() {
        this.checkBtn.addEventListener('click', () => this.check());
        this.toggleBtn.addEventListener('click', () => this.toggleVisibility());

        // Check on Enter key
        this.passwordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.check();
        });
    }

    toggleVisibility() {
        const type = this.passwordInput.type === 'password' ? 'text' : 'password';
        this.passwordInput.type = type;
        this.toggleBtn.textContent = type === 'password' ? '👁️' : '🙈';
    }

    async check() {
        const password = this.passwordInput.value;

        if (!password) {
            toast.error('Bitte gib ein Passwort ein!');
            return;
        }

        const result = document.getElementById('breach-result');
        result.style.display = 'block';
        result.innerHTML = '<p>🔍 Prüfe Datenbanken...</p>';
        result.className = 'breach-result';

        try {
            const response = await fetch(`${API_BASE}/check/breach`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });

            const data = await response.json();
            this.displayResults(data);
        } catch (error) {
            toast.error('Fehler bei der Prüfung');
            result.innerHTML = '<p>❌ Verbindungsfehler</p>';
            result.className = 'breach-result breach-error';
            console.error(error);
        }
    }

    displayResults(data) {
        const result = document.getElementById('breach-result');

        if (data.error) {
            result.innerHTML = `<p>⚠️ ${data.error}</p>`;
            result.className = 'breach-result breach-error';
            return;
        }

        if (data.breached) {
            result.innerHTML = `
                <p style="font-size: 2rem; margin-bottom: 1rem;">⚠️</p>
                <p>${data.message}</p>
                <p style="margin-top: 1rem; font-size: 0.9rem;">
                    Dieses Passwort sollte NICHT verwendet werden!
                </p>
            `;
            result.className = 'breach-result breach-found';
            toast.error('Passwort kompromittiert!');
        } else {
            result.innerHTML = `
                <p style="font-size: 2rem; margin-bottom: 1rem;">✓</p>
                <p>${data.message}</p>
                <p style="margin-top: 1rem; font-size: 0.9rem;">
                    Dieses Passwort wurde in keinem bekannten Datenleck gefunden.
                </p>
            `;
            result.className = 'breach-result breach-safe';
            toast.success('Passwort sicher!');
        }
    }
}

// ===========================
// Initialize Application
// ===========================
let toast;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    const tabManager = new TabManager();
    toast = new ToastManager();
    const passwordGen = new PasswordGeneratorUI();
    const passwordChecker = new PasswordCheckerUI();
    const passphraseGen = new PassphraseGeneratorUI();
    const breachChecker = new BreachCheckerUI();

    console.log('🔐 Password Security Suite loaded successfully!');
});
