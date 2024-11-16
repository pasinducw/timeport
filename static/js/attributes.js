/**
 * Manages projects, clients, and tags for time entries.
 */
class AttributeManager {
    constructor() {
        this.projects = [];
        this.clients = [];
        this.tags = [];
        this.setupEventListeners();
        this.loadAttributes();
    }

    setupEventListeners() {
        // Modal close buttons
        document.querySelectorAll('.modal-close').forEach(button => {
            button.addEventListener('click', () => this.closeModal());
        });

        // Project management
        document.getElementById('manage-projects-button').addEventListener('click', () => this.showProjectModal());
        document.getElementById('new-project-form').addEventListener('submit', (e) => this.handleNewProject(e));

        // Client management
        document.getElementById('manage-clients-button').addEventListener('click', () => this.showClientModal());
        document.getElementById('new-client-form').addEventListener('submit', (e) => this.handleNewClient(e));

        // Tag management
        document.getElementById('manage-tags-button').addEventListener('click', () => this.showTagModal());
        document.getElementById('new-tag-form').addEventListener('submit', (e) => this.handleNewTag(e));
    }

    async loadAttributes() {
        try {
            const [projects, clients, tags] = await Promise.all([
                fetchJSON('/projects'),
                fetchJSON('/clients'),
                fetchJSON('/tags')
            ]);
            
            this.projects = projects;
            this.clients = clients;
            this.tags = tags;
            
            this.updateProjectsList();
            this.updateClientsList();
            this.updateTagsList();
        } catch (error) {
            console.error('Failed to load attributes:', error);
        }
    }

    // Modal Management
    showModal(modalId) {
        document.getElementById(modalId).style.display = 'block';
    }

    closeModal() {
        document.querySelectorAll('.modal-overlay').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    // Project Management
    showProjectModal() {
        this.showModal('project-modal');
        this.updateProjectsList();
    }

    async handleNewProject(event) {
        event.preventDefault();
        const form = event.target;
        const name = form.querySelector('[name="name"]').value;
        const description = form.querySelector('[name="description"]').value;

        try {
            const project = await fetchJSON('/projects', {
                method: 'POST',
                body: JSON.stringify({ name, description })
            });
            
            this.projects.push(project);
            this.updateProjectsList();
            form.reset();
        } catch (error) {
            alert('Failed to create project: ' + error.message);
        }
    }

    async deleteProject(projectId) {
        if (!confirm('Are you sure you want to delete this project?')) return;

        try {
            await fetchJSON(`/projects/${projectId}`, { method: 'DELETE' });
            this.projects = this.projects.filter(p => p.id !== projectId);
            this.updateProjectsList();
        } catch (error) {
            alert('Failed to delete project: ' + error.message);
        }
    }

    updateProjectsList() {
        const list = document.getElementById('projects-list');
        if (!list) return;
        list.innerHTML = this.projects.map(project => `
            <div class="attribute-item">
                <div class="attribute-info">
                    <div class="attribute-name">${project.name}</div>
                    ${project.description ? `<div class="attribute-description">${project.description}</div>` : ''}
                </div>
                <div class="attribute-actions">
                    <button class="btn btn-danger" onclick="attributeManager.deleteProject(${project.id})">Delete</button>
                </div>
            </div>
        `).join('');
    }

    // Client Management
    showClientModal() {
        this.showModal('client-modal');
        this.updateClientsList();
    }

    async handleNewClient(event) {
        event.preventDefault();
        const form = event.target;
        const name = form.querySelector('[name="name"]').value;
        const email = form.querySelector('[name="email"]').value;
        const notes = form.querySelector('[name="notes"]').value;

        try {
            const client = await fetchJSON('/clients', {
                method: 'POST',
                body: JSON.stringify({ name, email, notes })
            });
            
            this.clients.push(client);
            this.updateClientsList();
            form.reset();
        } catch (error) {
            alert('Failed to create client: ' + error.message);
        }
    }

    async deleteClient(clientId) {
        if (!confirm('Are you sure you want to delete this client?')) return;

        try {
            await fetchJSON(`/clients/${clientId}`, { method: 'DELETE' });
            this.clients = this.clients.filter(c => c.id !== clientId);
            this.updateClientsList();
        } catch (error) {
            alert('Failed to delete client: ' + error.message);
        }
    }

    updateClientsList() {
        const list = document.getElementById('clients-list');
        if (!list) return;
        list.innerHTML = this.clients.map(client => `
            <div class="attribute-item">
                <div class="attribute-info">
                    <div class="attribute-name">${client.name}</div>
                    ${client.email ? `<div class="attribute-description">Email: ${client.email}</div>` : ''}
                    ${client.notes ? `<div class="attribute-description">${client.notes}</div>` : ''}
                </div>
                <div class="attribute-actions">
                    <button class="btn btn-danger" onclick="attributeManager.deleteClient(${client.id})">Delete</button>
                </div>
            </div>
        `).join('');
    }

    // Tag Management
    showTagModal() {
        this.showModal('tag-modal');
        this.updateTagsList();
    }

    async handleNewTag(event) {
        event.preventDefault();
        const form = event.target;
        const name = form.querySelector('[name="name"]').value;
        const color = form.querySelector('[name="color"]').value;

        try {
            const tag = await fetchJSON('/tags', {
                method: 'POST',
                body: JSON.stringify({ name, color })
            });
            
            this.tags.push(tag);
            this.updateTagsList();
            form.reset();
            form.querySelector('[name="color"]').value = '#808080'; // Reset color to default
        } catch (error) {
            alert('Failed to create tag: ' + error.message);
        }
    }

    async deleteTag(tagId) {
        if (!confirm('Are you sure you want to delete this tag?')) return;

        try {
            await fetchJSON(`/tags/${tagId}`, { method: 'DELETE' });
            this.tags = this.tags.filter(t => t.id !== tagId);
            this.updateTagsList();
        } catch (error) {
            alert('Failed to delete tag: ' + error.message);
        }
    }

    updateTagsList() {
        const list = document.getElementById('tags-list');
        if (!list) return;
        list.innerHTML = this.tags.map(tag => `
            <div class="attribute-item">
                <div class="attribute-info">
                    <span class="tag-color" style="background-color: ${tag.color}"></span>
                    <span class="attribute-name">${tag.name}</span>
                </div>
                <div class="attribute-actions">
                    <button class="btn btn-danger" onclick="attributeManager.deleteTag(${tag.id})">Delete</button>
                </div>
            </div>
        `).join('');
    }

    // Entry Attribute Management
    showProjectSelector(entryId, event) {
        event.stopPropagation();
        this.removeExistingSelectors();

        const selector = document.createElement('div');
        selector.className = 'attribute-selector';
        selector.innerHTML = `
            ${this.projects.map(project => `
                <div class="attribute-option" onclick="attributeManager.updateEntryProject(${entryId}, ${project.id})">
                    <i class="project-icon"></i>${project.name}
                </div>
            `).join('')}
            <div class="attribute-option" onclick="attributeManager.updateEntryProject(${entryId}, null)">
                <i class="remove-icon"></i>Remove Project
            </div>
        `;

        document.body.appendChild(selector);

        // Position the selector near the clicked element
        const rect = event.target.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        const selectorHeight = Math.min(300, (this.projects.length + 1) * 40); // +1 for Remove option

        // Position horizontally - center on the button
        selector.style.left = `${rect.left}px`;

        // Position vertically - above or below depending on space
        if (rect.bottom + selectorHeight + 10 <= viewportHeight) {
            // Enough space below - position below the button
            selector.style.top = `${rect.bottom + 5}px`;
        } else {
            // Not enough space below - position above the button
            selector.style.bottom = `${viewportHeight - rect.top + 5}px`;
        }

        // Close selector when clicking outside
        document.addEventListener('click', () => this.removeExistingSelectors(), { once: true });
    }

    showClientSelector(entryId, event) {
        event.stopPropagation();
        this.removeExistingSelectors();

        const selector = document.createElement('div');
        selector.className = 'attribute-selector';
        selector.innerHTML = `
            ${this.clients.map(client => `
                <div class="attribute-option" onclick="attributeManager.updateEntryClient(${entryId}, ${client.id})">
                    <i class="client-icon"></i>${client.name}
                </div>
            `).join('')}
            <div class="attribute-option" onclick="attributeManager.updateEntryClient(${entryId}, null)">
                <i class="remove-icon"></i>Remove Client
            </div>
        `;

        document.body.appendChild(selector);

        // Position the selector near the clicked element
        const rect = event.target.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        const selectorHeight = Math.min(300, (this.clients.length + 1) * 40); // +1 for Remove option

        // Position horizontally - center on the button
        selector.style.left = `${rect.left}px`;

        // Position vertically - above or below depending on space
        if (rect.bottom + selectorHeight + 10 <= viewportHeight) {
            // Enough space below - position below the button
            selector.style.top = `${rect.bottom + 5}px`;
        } else {
            // Not enough space below - position above the button
            selector.style.bottom = `${viewportHeight - rect.top + 5}px`;
        }

        // Close selector when clicking outside
        document.addEventListener('click', () => this.removeExistingSelectors(), { once: true });
    }

    showTagSelector(entryId, event) {
        event.stopPropagation();
        this.removeExistingSelectors();

        const selector = document.createElement('div');
        selector.className = 'attribute-selector';
        selector.innerHTML = this.tags.map(tag => `
            <div class="tag-selector-option" onclick="attributeManager.toggleEntryTag(${entryId}, ${tag.id}, true)">
                <span class="tag-color" style="background-color: ${tag.color}"></span>
                <span class="tag-name">${tag.name}</span>
            </div>
        `).join('');

        document.body.appendChild(selector);

        // Position the selector near the clicked element
        const rect = event.target.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        const selectorHeight = Math.min(300, this.tags.length * 40); // Approximate height

        // Position horizontally - center on the button
        selector.style.left = `${rect.left}px`;

        // Position vertically - above or below depending on space
        if (rect.bottom + selectorHeight + 10 <= viewportHeight) {
            // Enough space below - position below the button
            selector.style.top = `${rect.bottom + 5}px`;
        } else {
            // Not enough space below - position above the button
            selector.style.bottom = `${viewportHeight - rect.top + 5}px`;
        }

        // Close selector when clicking outside
        document.addEventListener('click', () => this.removeExistingSelectors(), { once: true });
    }

    positionSelector(selector, target) {
        const rect = target.getBoundingClientRect();
        const spaceBelow = window.innerHeight - rect.bottom;
        const spaceAbove = rect.top;

        // Position horizontally
        selector.style.left = rect.left + 'px';

        // Position vertically based on available space
        if (spaceBelow >= 200 || spaceBelow > spaceAbove) {
            selector.style.top = rect.bottom + 5 + 'px';
        } else {
            selector.style.bottom = (window.innerHeight - rect.top + 5) + 'px';
        }
    }

    removeExistingSelectors() {
        document.querySelectorAll('.attribute-selector').forEach(selector => {
            selector.remove();
        });
    }

    async updateEntryProject(entryId, projectId) {
        this.removeExistingSelectors();
        try {
            await fetchJSON(`/entries/${entryId}`, {
                method: 'PUT',
                body: JSON.stringify({ project_id: projectId === null ? 0 : projectId })
            });
            fetchEntries(); // Refresh the entries list
        } catch (error) {
            alert('Failed to update entry project: ' + error.message);
        }
    }

    async updateEntryClient(entryId, clientId) {
        this.removeExistingSelectors();
        try {
            await fetchJSON(`/entries/${entryId}`, {
                method: 'PUT',
                body: JSON.stringify({ client_id: clientId === null ? 0 : clientId })
            });
            fetchEntries(); // Refresh the entries list
        } catch (error) {
            alert('Failed to update entry client: ' + error.message);
        }
    }

    async toggleEntryTag(entryId, tagId, add = true) {
        this.removeExistingSelectors();
        try {
            if (add) {
                await fetchJSON(`/entries/${entryId}/tags/${tagId}`, { method: 'POST' });
            } else {
                await fetchJSON(`/entries/${entryId}/tags/${tagId}`, { method: 'DELETE' });
            }
            fetchEntries(); // Refresh the entries list
        } catch (error) {
            alert(`Failed to ${add ? 'add' : 'remove'} tag: ` + error.message);
        }
    }
}

// Initialize on page load
let attributeManager;
document.addEventListener('DOMContentLoaded', () => {
    attributeManager = new AttributeManager();
});
