// ===========================
// Service Manager Class
// ===========================
class ServiceManager {
    constructor() {
        this.services = [];
        this.currentFilter = 'all';
        this.searchTerm = '';
        this.sessionStartTime = Date.now();
        this.loadFromLocalStorage();
        this.init();
    }

    init() {
        this.renderServices();
        this.updateStats();
        this.startClock();
        this.startUptimeCounter();
        this.setupEventListeners();
        this.loadTheme();
    }

    // Local Storage Management
    loadFromLocalStorage() {
        const saved = localStorage.getItem('homelabServices');
        if (saved) {
            this.services = JSON.parse(saved);
        } else {
            // Default services if none exist
            this.services = this.getDefaultServices();
            this.saveToLocalStorage();
        }
    }

    saveToLocalStorage() {
        localStorage.setItem('homelabServices', JSON.stringify(this.services));
    }

    getDefaultServices() {
        return [
            {
                id: this.generateId(),
                name: 'Beispiel Service',
                description: 'Dies ist ein Beispiel - klicke auf Bearbeiten',
                url: 'http://localhost:8080',
                icon: 'fa-cube',
                category: 'other',
                color: 'blue'
            }
        ];
    }

    // Service Operations
    addService(serviceData) {
        const service = {
            id: this.generateId(),
            ...serviceData
        };
        this.services.push(service);
        this.saveToLocalStorage();
        this.renderServices();
        this.updateStats();
    }

    updateService(id, serviceData) {
        const index = this.services.findIndex(s => s.id === id);
        if (index !== -1) {
            this.services[index] = { id, ...serviceData };
            this.saveToLocalStorage();
            this.renderServices();
        }
    }

    deleteService(id) {
        this.services = this.services.filter(s => s.id !== id);
        this.saveToLocalStorage();
        this.renderServices();
        this.updateStats();
    }

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // Rendering
    renderServices() {
        const grid = document.getElementById('services-grid');
        const filteredServices = this.getFilteredServices();

        if (filteredServices.length === 0) {
            grid.innerHTML = this.getEmptyState();
            return;
        }

        grid.innerHTML = filteredServices.map(service => this.createServiceCard(service)).join('');
        this.attachCardEventListeners();
    }

    getFilteredServices() {
        return this.services.filter(service => {
            const matchesCategory = this.currentFilter === 'all' || service.category === this.currentFilter;
            const matchesSearch = service.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                                service.description.toLowerCase().includes(this.searchTerm.toLowerCase());
            return matchesCategory && matchesSearch;
        });
    }

    createServiceCard(service) {
        return `
            <div class="service-card color-${service.color}" data-id="${service.id}">
                <div class="service-header">
                    <div class="service-icon">
                        <i class="fas ${service.icon}"></i>
                    </div>
                    <div class="service-actions">
                        <button class="service-action-btn edit-service" data-id="${service.id}" title="Bearbeiten">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                </div>
                <div class="service-body">
                    <h3>${this.escapeHtml(service.name)}</h3>
                    <p>${this.escapeHtml(service.description) || 'Keine Beschreibung'}</p>
                    <span class="service-category">${this.getCategoryName(service.category)}</span>
                    <div class="service-url">${this.escapeHtml(service.url)}</div>
                </div>
            </div>
        `;
    }

    getEmptyState() {
        if (this.searchTerm) {
            return `
                <div class="empty-state">
                    <i class="fas fa-search"></i>
                    <h3>Keine Services gefunden</h3>
                    <p>Versuche einen anderen Suchbegriff</p>
                </div>
            `;
        }
        return `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <h3>Keine Services in dieser Kategorie</h3>
                <p>Füge neue Services hinzu mit dem + Button</p>
            </div>
        `;
    }

    attachCardEventListeners() {
        // Card clicks to open URL
        document.querySelectorAll('.service-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.service-action-btn')) {
                    const id = card.dataset.id;
                    const service = this.services.find(s => s.id === id);
                    if (service) {
                        window.open(service.url, '_blank');
                    }
                }
            });
        });

        // Edit buttons
        document.querySelectorAll('.edit-service').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = btn.dataset.id;
                this.openEditModal(id);
            });
        });
    }

    // Modal Management
    openAddModal() {
        const modal = document.getElementById('add-service-modal');
        modal.classList.add('active');
        document.getElementById('add-service-form').reset();
    }

    closeAddModal() {
        const modal = document.getElementById('add-service-modal');
        modal.classList.remove('active');
    }

    openEditModal(id) {
        const service = this.services.find(s => s.id === id);
        if (!service) return;

        const modal = document.getElementById('edit-service-modal');
        document.getElementById('edit-service-id').value = service.id;
        document.getElementById('edit-service-name').value = service.name;
        document.getElementById('edit-service-description').value = service.description || '';
        document.getElementById('edit-service-url').value = service.url;
        document.getElementById('edit-service-icon').value = service.icon;
        document.getElementById('edit-service-category').value = service.category;
        document.getElementById('edit-service-color').value = service.color;

        modal.classList.add('active');
    }

    closeEditModal() {
        const modal = document.getElementById('edit-service-modal');
        modal.classList.remove('active');
    }

    // Stats & Updates
    updateStats() {
        document.getElementById('services-online').textContent = this.services.length;
    }

    startClock() {
        const updateClock = () => {
            const now = new Date();
            const timeString = now.toLocaleTimeString('de-DE', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            document.getElementById('current-time').textContent = timeString;
        };
        updateClock();
        setInterval(updateClock, 1000);
    }

    startUptimeCounter() {
        const updateUptime = () => {
            const uptime = Date.now() - this.sessionStartTime;
            const hours = Math.floor(uptime / 3600000);
            const minutes = Math.floor((uptime % 3600000) / 60000);
            const seconds = Math.floor((uptime % 60000) / 1000);

            let uptimeString = '';
            if (hours > 0) {
                uptimeString = `${hours}h ${minutes}m`;
            } else if (minutes > 0) {
                uptimeString = `${minutes}m ${seconds}s`;
            } else {
                uptimeString = `${seconds}s`;
            }

            document.getElementById('uptime-display').textContent = uptimeString;
        };
        updateUptime();
        setInterval(updateUptime, 1000);
    }

    // Filter & Search
    setFilter(category) {
        this.currentFilter = category;
        this.renderServices();

        // Update active button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');
    }

    setSearch(term) {
        this.searchTerm = term;
        this.renderServices();
    }

    // Theme Management
    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        this.updateThemeIcon(newTheme);
    }

    updateThemeIcon(theme) {
        const icon = document.querySelector('#theme-toggle-btn i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }

    // Import/Export
    exportConfig() {
        const config = {
            version: '1.0',
            exportDate: new Date().toISOString(),
            services: this.services
        };

        const dataStr = JSON.stringify(config, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `homelab-config-${Date.now()}.json`;
        link.click();

        URL.revokeObjectURL(url);
    }

    importConfig(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const config = JSON.parse(e.target.result);
                if (config.services && Array.isArray(config.services)) {
                    if (confirm('Dies wird alle aktuellen Services ersetzen. Fortfahren?')) {
                        this.services = config.services;
                        this.saveToLocalStorage();
                        this.renderServices();
                        this.updateStats();
                        alert('Konfiguration erfolgreich importiert!');
                    }
                } else {
                    alert('Ungültige Konfigurationsdatei!');
                }
            } catch (error) {
                alert('Fehler beim Lesen der Datei: ' + error.message);
            }
        };
        reader.readAsText(file);
    }

    // Event Listeners Setup
    setupEventListeners() {
        // Theme toggle
        document.getElementById('theme-toggle-btn').addEventListener('click', () => {
            this.toggleTheme();
        });

        // Add service button
        document.getElementById('add-service-btn').addEventListener('click', () => {
            this.openAddModal();
        });

        // Close modals
        document.getElementById('close-modal-btn').addEventListener('click', () => {
            this.closeAddModal();
        });
        document.getElementById('close-edit-modal-btn').addEventListener('click', () => {
            this.closeEditModal();
        });
        document.getElementById('cancel-btn').addEventListener('click', () => {
            this.closeAddModal();
        });
        document.getElementById('cancel-edit-btn').addEventListener('click', () => {
            this.closeEditModal();
        });

        // Close modal on background click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        });

        // Add service form
        document.getElementById('add-service-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = {
                name: document.getElementById('service-name').value,
                description: document.getElementById('service-description').value,
                url: document.getElementById('service-url').value,
                icon: document.getElementById('service-icon').value,
                category: document.getElementById('service-category').value,
                color: document.getElementById('service-color').value
            };
            this.addService(formData);
            this.closeAddModal();
        });

        // Edit service form
        document.getElementById('edit-service-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const id = document.getElementById('edit-service-id').value;
            const formData = {
                name: document.getElementById('edit-service-name').value,
                description: document.getElementById('edit-service-description').value,
                url: document.getElementById('edit-service-url').value,
                icon: document.getElementById('edit-service-icon').value,
                category: document.getElementById('edit-service-category').value,
                color: document.getElementById('edit-service-color').value
            };
            this.updateService(id, formData);
            this.closeEditModal();
        });

        // Delete service
        document.getElementById('delete-service-btn').addEventListener('click', () => {
            const id = document.getElementById('edit-service-id').value;
            if (confirm('Möchtest du diesen Service wirklich löschen?')) {
                this.deleteService(id);
                this.closeEditModal();
            }
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.setFilter(btn.dataset.category);
            });
        });

        // Search
        document.getElementById('search-input').addEventListener('input', (e) => {
            this.setSearch(e.target.value);
        });

        // Export config
        document.getElementById('export-config').addEventListener('click', (e) => {
            e.preventDefault();
            this.exportConfig();
        });

        // Import config
        document.getElementById('import-config-link').addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('import-config').click();
        });

        document.getElementById('import-config').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.importConfig(file);
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Escape to close modals
            if (e.key === 'Escape') {
                this.closeAddModal();
                this.closeEditModal();
            }
            // Ctrl/Cmd + K to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('search-input').focus();
            }
        });
    }

    // Utility functions
    getCategoryName(category) {
        const names = {
            media: 'Media',
            automation: 'Automation',
            network: 'Netzwerk',
            monitoring: 'Monitoring',
            storage: 'Storage',
            other: 'Sonstiges'
        };
        return names[category] || category;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// ===========================
// Initialize App
// ===========================
let serviceManager;

document.addEventListener('DOMContentLoaded', () => {
    serviceManager = new ServiceManager();

    // Add loading animation
    document.body.classList.add('loaded');
});

// Service Worker for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable service worker
        // navigator.serviceWorker.register('/sw.js');
    });
}
