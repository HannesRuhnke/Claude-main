// ===========================
// API Base URL
// ===========================
const API_BASE = '/api';

// ===========================
// Service Manager Class (Backend-Version)
// ===========================
class ServiceManager {
    constructor() {
        this.services = [];
        this.groups = [];
        this.tags = [];
        this.statuses = {};
        this.currentFilter = 'all';
        this.currentGroupFilter = null;
        this.currentTagFilter = null;
        this.searchTerm = '';
        this.sessionStartTime = Date.now();
        this.draggedElement = null;
        this.init();
    }

    async init() {
        try {
            // Check authentication first
            const isAuth = await this.checkAuth();
            if (!isAuth) {
                window.location.href = 'login.html';
                return;
            }

            // Always setup event listeners first - even if data loading fails
            this.setupEventListeners();
            this.loadTheme();
            this.startClock();
            this.startUptimeCounter();

            // Load data and render (can fail gracefully)
            await this.loadData();
            this.renderServices();
            this.updateStats();
            this.startStatusChecks();
        } catch (error) {
            console.error('Initialization error:', error);
            // Ensure event listeners are set up even if there's an error
            this.setupEventListeners();
            this.loadTheme();
        }
    }

    // ===========================
    // Authentication
    // ===========================
    async checkAuth() {
        try {
            const response = await fetch(`${API_BASE}/auth/check`, {
                credentials: 'include'
            });
            return response.ok;
        } catch (error) {
            console.error('Auth check failed:', error);
            return false;
        }
    }

    async logout() {
        try {
            await fetch(`${API_BASE}/auth/logout`, {
                method: 'POST',
                credentials: 'include'
            });
            window.location.href = 'login.html';
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }

    // ===========================
    // Data Loading
    // ===========================
    async loadData() {
        try {
            const [servicesRes, groupsRes, tagsRes, statusRes] = await Promise.all([
                fetch(`${API_BASE}/services`, { credentials: 'include' }),
                fetch(`${API_BASE}/groups`, { credentials: 'include' }),
                fetch(`${API_BASE}/tags`, { credentials: 'include' }),
                fetch(`${API_BASE}/services/status`, { credentials: 'include' })
            ]);

            this.services = await servicesRes.json();
            this.groups = await groupsRes.json();
            this.tags = await tagsRes.json();
            const statuses = await statusRes.json();

            // Convert status array to object
            this.statuses = {};
            statuses.forEach(status => {
                this.statuses[status.service_id] = status;
            });
        } catch (error) {
            console.error('Failed to load data:', error);
        }
    }

    // ===========================
    // Service Operations
    // ===========================
    async addService(serviceData) {
        try {
            const response = await fetch(`${API_BASE}/services`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(serviceData)
            });

            if (response.ok) {
                await this.loadData();
                this.renderServices();
                this.updateStats();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Add service failed:', error);
            return false;
        }
    }

    async updateService(id, serviceData) {
        try {
            const response = await fetch(`${API_BASE}/services/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(serviceData)
            });

            if (response.ok) {
                await this.loadData();
                this.renderServices();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Update service failed:', error);
            return false;
        }
    }

    async deleteService(id) {
        try {
            const response = await fetch(`${API_BASE}/services/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });

            if (response.ok) {
                await this.loadData();
                this.renderServices();
                this.updateStats();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Delete service failed:', error);
            return false;
        }
    }

    async toggleFavorite(id, isFavorite) {
        try {
            const response = await fetch(`${API_BASE}/services/${id}/favorite`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ is_favorite: isFavorite ? 1 : 0 })
            });

            if (response.ok) {
                await this.loadData();
                this.renderServices();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Toggle favorite failed:', error);
            return false;
        }
    }

    async reorderServices(serviceOrder) {
        try {
            const response = await fetch(`${API_BASE}/services/reorder`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ order: serviceOrder })
            });

            return response.ok;
        } catch (error) {
            console.error('Reorder failed:', error);
            return false;
        }
    }

    // ===========================
    // Status Checks
    // ===========================
    async checkServiceStatus(serviceId) {
        try {
            const response = await fetch(`${API_BASE}/services/${serviceId}/check-status`, {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                const status = await response.json();
                this.statuses[serviceId] = status;
                this.updateServiceStatusDisplay(serviceId);
            }
        } catch (error) {
            console.error(`Status check failed for ${serviceId}:`, error);
        }
    }

    async checkAllStatuses() {
        const statusBtn = document.getElementById('check-all-status');
        if (statusBtn) {
            statusBtn.disabled = true;
            statusBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Prüfe...';
        }

        for (const service of this.services) {
            await this.checkServiceStatus(service.id);
        }

        if (statusBtn) {
            statusBtn.disabled = false;
            statusBtn.innerHTML = '<i class="fas fa-sync"></i> Alle Status prüfen';
        }
    }

    startStatusChecks() {
        // Check all statuses every 5 minutes
        setInterval(() => {
            this.checkAllStatuses();
        }, 5 * 60 * 1000);
    }

    updateServiceStatusDisplay(serviceId) {
        const card = document.querySelector(`[data-id="${serviceId}"]`);
        if (!card) return;

        const statusIndicator = card.querySelector('.status-indicator');
        if (!statusIndicator) return;

        const status = this.statuses[serviceId];
        if (status) {
            statusIndicator.className = `status-indicator ${status.is_online ? 'online' : 'offline'}`;
            statusIndicator.title = status.is_online
                ? `Online (${status.response_time}ms)`
                : 'Offline';
        }
    }

    // ===========================
    // Groups
    // ===========================
    async addGroup(groupData) {
        try {
            const response = await fetch(`${API_BASE}/groups`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(groupData)
            });

            if (response.ok) {
                await this.loadData();
                this.renderGroupFilters();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Add group failed:', error);
            return false;
        }
    }

    // ===========================
    // Tags
    // ===========================
    async addTag(tagData) {
        try {
            const response = await fetch(`${API_BASE}/tags`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(tagData)
            });

            if (response.ok) {
                await this.loadData();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Add tag failed:', error);
            return false;
        }
    }

    async addTagToService(serviceId, tagId) {
        try {
            const response = await fetch(`${API_BASE}/services/${serviceId}/tags`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ tag_id: tagId })
            });

            if (response.ok) {
                await this.loadData();
                this.renderServices();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Add tag to service failed:', error);
            return false;
        }
    }

    // ===========================
    // Rendering
    // ===========================
    renderServices() {
        const grid = document.getElementById('services-grid');
        const filteredServices = this.getFilteredServices();

        if (filteredServices.length === 0) {
            grid.innerHTML = this.getEmptyState();
            return;
        }

        grid.innerHTML = filteredServices.map(service => this.createServiceCard(service)).join('');
        this.attachCardEventListeners();
        this.setupDragAndDrop();
    }

    getFilteredServices() {
        return this.services.filter(service => {
            const matchesCategory = this.currentFilter === 'all' || service.category === this.currentFilter;
            const matchesGroup = !this.currentGroupFilter || service.group_id === this.currentGroupFilter;
            const matchesTag = !this.currentTagFilter || (service.tags && service.tags.includes(this.currentTagFilter));
            const matchesSearch = service.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                                (service.description && service.description.toLowerCase().includes(this.searchTerm.toLowerCase()));
            const matchesFavorite = this.currentFilter !== 'favorites' || service.is_favorite === 1;

            return matchesCategory && matchesGroup && matchesTag && matchesSearch && matchesFavorite;
        });
    }

    createServiceCard(service) {
        const status = this.statuses[service.id];
        const statusClass = status ? (status.is_online ? 'online' : 'offline') : 'unknown';
        const statusTitle = status
            ? (status.is_online ? `Online (${status.response_time}ms)` : 'Offline')
            : 'Status unbekannt';

        const favoriteIcon = service.is_favorite ? 'fas fa-star' : 'far fa-star';
        const tagsHtml = service.tags && service.tags.length > 0
            ? service.tags.map(tag => `<span class="service-tag">${tag}</span>`).join('')
            : '';

        return `
            <div class="service-card color-${service.color}" data-id="${service.id}" draggable="true">
                <div class="status-indicator ${statusClass}" title="${statusTitle}"></div>
                <div class="service-header">
                    <div class="service-icon">
                        <i class="fas ${service.icon}"></i>
                    </div>
                    <div class="service-actions">
                        <button class="service-action-btn favorite-btn" data-id="${service.id}" title="Favorit">
                            <i class="${favoriteIcon}"></i>
                        </button>
                        <button class="service-action-btn check-status-btn" data-id="${service.id}" title="Status prüfen">
                            <i class="fas fa-sync"></i>
                        </button>
                        <button class="service-action-btn edit-service" data-id="${service.id}" title="Bearbeiten">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                </div>
                <div class="service-body">
                    <h3>${this.escapeHtml(service.name)}</h3>
                    <p>${this.escapeHtml(service.description) || 'Keine Beschreibung'}</p>
                    ${service.notes ? `<div class="service-notes"><i class="fas fa-sticky-note"></i> ${this.escapeHtml(service.notes)}</div>` : ''}
                    <div class="service-meta">
                        <span class="service-category">${this.getCategoryName(service.category)}</span>
                        ${tagsHtml}
                    </div>
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

    // ===========================
    // Drag and Drop
    // ===========================
    setupDragAndDrop() {
        const cards = document.querySelectorAll('.service-card');

        cards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                this.draggedElement = card;
                card.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('dragging');
                this.draggedElement = null;
            });

            card.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';

                const afterElement = this.getDragAfterElement(document.getElementById('services-grid'), e.clientY);
                const grid = document.getElementById('services-grid');

                if (afterElement == null) {
                    grid.appendChild(this.draggedElement);
                } else {
                    grid.insertBefore(this.draggedElement, afterElement);
                }
            });

            card.addEventListener('drop', async (e) => {
                e.preventDefault();
                // Get new order
                const cards = [...document.querySelectorAll('.service-card')];
                const newOrder = cards.map(c => c.dataset.id);
                await this.reorderServices(newOrder);
            });
        });
    }

    getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.service-card:not(.dragging)')];

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;

            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    // ===========================
    // Event Listeners
    // ===========================
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

        // Favorite buttons
        document.querySelectorAll('.favorite-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                const id = btn.dataset.id;
                const service = this.services.find(s => s.id === id);
                if (service) {
                    await this.toggleFavorite(id, !service.is_favorite);
                }
            });
        });

        // Status check buttons
        document.querySelectorAll('.check-status-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                const id = btn.dataset.id;
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                await this.checkServiceStatus(id);
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-sync"></i>';
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

    // ===========================
    // Modal Management
    // ===========================
    openAddModal() {
        const modal = document.getElementById('add-service-modal');
        modal.classList.add('active');
        document.getElementById('add-service-form').reset();

        // Populate groups dropdown
        this.populateGroupsDropdown('service-group');
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
        document.getElementById('edit-service-notes').value = service.notes || '';

        this.populateGroupsDropdown('edit-service-group', service.group_id);

        modal.classList.add('active');
    }

    closeEditModal() {
        const modal = document.getElementById('edit-service-modal');
        modal.classList.remove('active');
    }

    populateGroupsDropdown(selectId, selectedGroupId = null) {
        const select = document.getElementById(selectId);
        if (!select) return;

        select.innerHTML = '<option value="">Keine Gruppe</option>';
        this.groups.forEach(group => {
            const option = document.createElement('option');
            option.value = group.id;
            option.textContent = group.name;
            if (selectedGroupId && group.id === selectedGroupId) {
                option.selected = true;
            }
            select.appendChild(option);
        });
    }

    // ===========================
    // Stats & Updates
    // ===========================
    updateStats() {
        document.getElementById('services-online').textContent = this.services.length;

        // Count online services
        const onlineCount = Object.values(this.statuses).filter(s => s.is_online).length;
        document.getElementById('services-status').textContent = `${onlineCount}/${this.services.length}`;
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

    // ===========================
    // Filter & Search
    // ===========================
    setFilter(category) {
        this.currentFilter = category;
        this.renderServices();

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`)?.classList.add('active');
    }

    setSearch(term) {
        this.searchTerm = term;
        this.renderServices();
    }

    renderGroupFilters() {
        const container = document.getElementById('group-filters');
        if (!container) return;

        container.innerHTML = this.groups.map(group => `
            <button class="filter-btn group-filter-btn" data-group="${group.id}">
                <i class="fas ${group.icon}"></i> ${group.name}
            </button>
        `).join('');

        // Attach event listeners
        document.querySelectorAll('.group-filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const groupId = parseInt(btn.dataset.group);
                this.currentGroupFilter = this.currentGroupFilter === groupId ? null : groupId;
                this.renderServices();

                btn.classList.toggle('active');
            });
        });
    }

    // ===========================
    // Theme Management
    // ===========================
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
        if (icon) {
            icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    // ===========================
    // Import/Export
    // ===========================
    async exportConfig() {
        try {
            const response = await fetch(`${API_BASE}/export`, {
                credentials: 'include'
            });

            if (response.ok) {
                const config = await response.json();
                const dataStr = JSON.stringify(config, null, 2);
                const dataBlob = new Blob([dataStr], { type: 'application/json' });
                const url = URL.createObjectURL(dataBlob);

                const link = document.createElement('a');
                link.href = url;
                link.download = `homelab-config-${Date.now()}.json`;
                link.click();

                URL.revokeObjectURL(url);
            }
        } catch (error) {
            console.error('Export failed:', error);
        }
    }

    async importConfig(file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const config = JSON.parse(e.target.result);

                if (confirm('Dies wird alle aktuellen Services ersetzen. Fortfahren?')) {
                    const response = await fetch(`${API_BASE}/import`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        credentials: 'include',
                        body: JSON.stringify(config)
                    });

                    if (response.ok) {
                        await this.loadData();
                        this.renderServices();
                        this.updateStats();
                        alert('Konfiguration erfolgreich importiert!');
                    } else {
                        alert('Import fehlgeschlagen!');
                    }
                }
            } catch (error) {
                alert('Fehler beim Lesen der Datei: ' + error.message);
            }
        };
        reader.readAsText(file);
    }

    // ===========================
    // Event Listeners Setup
    // ===========================
    setupEventListeners() {
        // Sidebar menu toggle
        const menuBtn = document.getElementById('menu-btn');
        const sidebar = document.getElementById('sidebar');
        const sidebarOverlay = document.getElementById('sidebar-overlay');
        const closeSidebar = document.getElementById('close-sidebar');

        if (menuBtn && sidebar && sidebarOverlay) {
            menuBtn.addEventListener('click', () => {
                sidebar.classList.add('active');
                sidebarOverlay.classList.add('active');
            });

            closeSidebar?.addEventListener('click', () => {
                sidebar.classList.remove('active');
                sidebarOverlay.classList.remove('active');
            });

            sidebarOverlay.addEventListener('click', () => {
                sidebar.classList.remove('active');
                sidebarOverlay.classList.remove('active');
            });
        }

        // Navigation items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');

                // Handle navigation actions
                const navId = item.id;
                if (navId === 'nav-settings') {
                    this.openSettingsModal();
                }

                // Close sidebar on mobile after selecting
                sidebar?.classList.remove('active');
                sidebarOverlay?.classList.remove('active');
            });
        });

        // Theme toggle
        const themeBtn = document.getElementById('theme-toggle-btn');
        if (themeBtn) {
            themeBtn.addEventListener('click', () => this.toggleTheme());
        }

        // Logout button
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }

        // Add service button
        const addBtn = document.getElementById('add-service-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.openAddModal());
        }

        // Check all status button
        const checkAllBtn = document.getElementById('check-all-status');
        if (checkAllBtn) {
            checkAllBtn.addEventListener('click', () => this.checkAllStatuses());
        }

        // Close modals
        document.getElementById('close-modal-btn')?.addEventListener('click', () => this.closeAddModal());
        document.getElementById('close-edit-modal-btn')?.addEventListener('click', () => this.closeEditModal());
        document.getElementById('cancel-btn')?.addEventListener('click', () => this.closeAddModal());
        document.getElementById('cancel-edit-btn')?.addEventListener('click', () => this.closeEditModal());

        // Close modal on background click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        });

        // Add service form
        document.getElementById('add-service-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                id: Date.now().toString(36) + Math.random().toString(36).substr(2),
                name: document.getElementById('service-name').value,
                description: document.getElementById('service-description').value,
                url: document.getElementById('service-url').value,
                icon: document.getElementById('service-icon').value,
                category: document.getElementById('service-category').value,
                color: document.getElementById('service-color').value,
                notes: document.getElementById('service-notes')?.value || '',
                group_id: document.getElementById('service-group')?.value || null,
                is_favorite: 0
            };
            const success = await this.addService(formData);
            if (success) {
                this.closeAddModal();
            }
        });

        // Edit service form
        document.getElementById('edit-service-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('edit-service-id').value;
            const formData = {
                name: document.getElementById('edit-service-name').value,
                description: document.getElementById('edit-service-description').value,
                url: document.getElementById('edit-service-url').value,
                icon: document.getElementById('edit-service-icon').value,
                category: document.getElementById('edit-service-category').value,
                color: document.getElementById('edit-service-color').value,
                notes: document.getElementById('edit-service-notes')?.value || '',
                group_id: document.getElementById('edit-service-group')?.value || null
            };
            const success = await this.updateService(id, formData);
            if (success) {
                this.closeEditModal();
            }
        });

        // Delete service
        document.getElementById('delete-service-btn')?.addEventListener('click', async () => {
            const id = document.getElementById('edit-service-id').value;
            if (confirm('Möchtest du diesen Service wirklich löschen?')) {
                const success = await this.deleteService(id);
                if (success) {
                    this.closeEditModal();
                }
            }
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;
                if (category) {
                    this.setFilter(category);
                }
            });
        });

        // Search
        document.getElementById('search-input')?.addEventListener('input', (e) => {
            this.setSearch(e.target.value);
        });

        // Export config
        document.getElementById('export-config')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.exportConfig();
        });

        // Import config
        document.getElementById('import-config-link')?.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('import-config')?.click();
        });

        document.getElementById('import-config')?.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.importConfig(file);
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAddModal();
                this.closeEditModal();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('search-input')?.focus();
            }
        });
    }

    // ===========================
    // Utility functions
    // ===========================
    getCategoryName(category) {
        const names = {
            media: 'Media',
            automation: 'Automation',
            network: 'Netzwerk',
            monitoring: 'Monitoring',
            storage: 'Storage',
            other: 'Sonstiges',
            favorites: 'Favoriten'
        };
        return names[category] || category;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // ===========================
    // Settings Modal
    // ===========================
    openSettingsModal() {
        const modal = document.getElementById('settings-modal');
        if (modal) {
            modal.classList.add('active');
            this.setupSettingsListeners();
        }
    }

    closeSettingsModal() {
        const modal = document.getElementById('settings-modal');
        if (modal) {
            modal.classList.remove('active');
        }
    }

    setupSettingsListeners() {
        // Close button
        document.getElementById('close-settings-btn')?.addEventListener('click', () => this.closeSettingsModal());

        // Tab switching
        document.querySelectorAll('.settings-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const targetTab = tab.dataset.tab;

                // Update active tab
                document.querySelectorAll('.settings-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Update active content
                document.querySelectorAll('.settings-tab-content').forEach(c => c.classList.remove('active'));
                document.getElementById(`tab-${targetTab}`)?.classList.add('active');
            });
        });

        // Password change form
        document.getElementById('change-password-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const currentPassword = document.getElementById('current-password').value;
            const newPassword = document.getElementById('new-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            if (newPassword !== confirmPassword) {
                alert('Die Passwörter stimmen nicht überein!');
                return;
            }

            try {
                const response = await fetch(`${API_BASE}/auth/change-password`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({
                        current_password: currentPassword,
                        new_password: newPassword
                    })
                });

                if (response.ok) {
                    alert('Passwort erfolgreich geändert!');
                    document.getElementById('change-password-form').reset();
                } else {
                    const data = await response.json();
                    alert(data.error || 'Fehler beim Ändern des Passworts');
                }
            } catch (error) {
                alert('Fehler beim Ändern des Passworts');
            }
        });
    }
}

// ===========================
// Initialize App
// ===========================
let serviceManager;

document.addEventListener('DOMContentLoaded', () => {
    serviceManager = new ServiceManager();
});
