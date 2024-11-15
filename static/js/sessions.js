class SessionsManager {
    constructor() {
        this.sessionList = document.getElementById('session-list');
        this.newSessionButton = document.getElementById('new-session-button');
        this.setupEventListeners();
        this.startPeriodicRefresh();
    }

    setupEventListeners() {
        this.newSessionButton.addEventListener('click', () => this.createNewSession());
    }

    startPeriodicRefresh() {
        this.fetchSessions();
        setInterval(() => this.fetchSessions(), 60000); // Refresh every minute
    }

    async createNewSession() {
        const sessionName = prompt('Enter session name (or leave empty for auto-generated name):');
        if (sessionName === null) return; // User cancelled

        try {
            await fetchJSON('/sessions/new', {
                method: 'POST',
                body: JSON.stringify({ name: sessionName })
            });
            window.location.href = '/';
        } catch (error) {
            alert('Failed to create session: ' + error.message);
        }
    }

    async deleteSession(sessionId, event) {
        event.stopPropagation();
        if (!confirm('Are you sure you want to delete this session? This action cannot be undone.')) return;

        try {
            await fetchJSON(`/sessions/${sessionId}`, { method: 'DELETE' });
            this.fetchSessions();
        } catch (error) {
            alert('Failed to delete session: ' + error.message);
        }
    }

    async endSession(sessionId, event) {
        event.stopPropagation();
        if (!confirm('Are you sure you want to end this session?')) return;

        try {
            await fetchJSON(`/sessions/${sessionId}/end`, { method: 'POST' });
            this.fetchSessions();
        } catch (error) {
            alert('Failed to end session: ' + error.message);
        }
    }

    async exportSession(sessionId, sessionName, event) {
        event.stopPropagation();
        try {
            const data = await fetchJSON(`/sessions/${sessionId}/export`);
            downloadCSV(data.content, data.filename);
        } catch (error) {
            alert('Failed to export session: ' + error.message);
        }
    }

    openSession(sessionId) {
        window.location.href = `/?session=${sessionId}`;
    }

    async fetchSessions() {
        try {
            const sessions = await fetchJSON('/sessions/list');
            this.renderSessions(sessions);
        } catch (error) {
            console.error('Failed to fetch sessions:', error);
        }
    }

    renderSessions(sessions) {
        this.sessionList.innerHTML = sessions.map(session => this.renderSessionCard(session)).join('');
    }

    renderSessionCard(session) {
        return `
            <div class="session-card ${!session.end_time ? 'active' : ''}" 
                 onclick="sessionsManager.openSession(${session.id})">
                <div class="session-header">
                    <h3 class="session-name">${session.name}</h3>
                    ${!session.end_time ? '<span class="active-indicator">Active</span>' : ''}
                </div>
                <div class="session-info">
                    <div>Started: ${formatDateTime(session.start_time)}</div>
                    ${session.end_time ? 
                        `<div>Ended: ${formatDateTime(session.end_time)}</div>
                         <div class="session-duration">Duration: ${formatDuration(session.start_time, session.end_time)}</div>` : 
                        `<div class="session-duration">Duration: ${formatDuration(session.start_time)}</div>`}
                    <div>Entries: ${session.entry_count}</div>
                </div>
                <div class="card-buttons" onclick="event.stopPropagation()">
                    <button class="export-button" 
                            onclick="sessionsManager.exportSession(${session.id}, '${session.name}', event)">
                        Export CSV
                    </button>
                    ${!session.end_time ? 
                        `<button class="end-button" 
                                onclick="sessionsManager.endSession(${session.id}, event)">
                            End Session
                         </button>` : 
                        `<button class="delete-button" 
                                onclick="sessionsManager.deleteSession(${session.id}, event)">
                            Delete Session
                         </button>`}
                </div>
            </div>
        `;
    }
}

// Initialize on page load
let sessionsManager;
document.addEventListener('DOMContentLoaded', () => {
    sessionsManager = new SessionsManager();
});
