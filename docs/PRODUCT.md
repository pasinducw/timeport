# TimePort

A sophisticated local time tracking application that combines the simplicity of text-based input with powerful automation and intelligence features.

## Core Concept

TimePort is designed as a local-first application that runs on your computer, leveraging the full capabilities of your operating system while providing a clean web-based interface. It's built to be your intelligent time-tracking companion that understands your work context and automates the tedious parts of time tracking.

## Key Features

### 1. Smart Text Input
- Natural language time entry processing
- Automatic inference of:
  - Client information
  - Project context
  - Relevant tags
  - Standardized entry descriptions
- Context-aware suggestions based on previous entries

### 2. OS-Level Integration
- Idle time detection using system APIs
- Application usage tracking
- Optional screenshot capabilities for activity verification
- System tray integration for quick access

### 3. Intelligent Automation
- Automatic work context detection
- Smart task switching based on active applications
- Idle time handling and categorization
- Activity pattern recognition
- Automated entry categorization

### 4. Local-First Architecture
- Runs completely on your local machine
- Web interface served locally
- No external dependencies for core functionality
- Full access to system-level features
- Secure by design - no data leaves your computer unless explicitly configured

### 5. Third-Party Integration
- Primary integration with Clockify
- Extensible integration framework for other time tracking tools
- Configurable sync settings
- Conflict resolution handling
- Offline-first with sync capabilities

## How It Works

### 1. Input Processing
```
User Input: "Working on client dashboard for ABC Corp"
↓
Intelligent Processing:
- Client: ABC Corp
- Project: Dashboard
- Category: Development
- Standardized Description: "ABC Corp - Dashboard Development"
```

### 2. Activity Monitoring
- Runs in the background monitoring system activity
- Detects active applications and windows
- Identifies idle periods
- Can capture screenshots (optional, privacy-respecting)

### 3. Data Flow
```
Local Activity → Processing Engine → Local Database → Integration Layer → External Services
```

## Privacy and Security

- All data stored locally
- No cloud dependencies
- Optional screenshot storage with encryption
- Configurable data retention policies
- Integration credentials stored securely in system keychain

## System Requirements

- Operating System: macOS (initially)
- Python 3.8 or higher
- Modern web browser
- Sufficient disk space for local data storage

## Configuration

### Basic Setup
```bash
# Example configuration in .env
SCREENSHOT_ENABLED=false
IDLE_TIMEOUT=300  # 5 minutes
SYNC_INTERVAL=900 # 15 minutes
```

### Integration Setup
```bash
# Example Clockify configuration
CLOCKIFY_API_KEY=your_api_key
CLOCKIFY_WORKSPACE=your_workspace_id
SYNC_ENABLED=true
```

## Future Enhancements

### Near-term
- Enhanced activity detection
- Improved text processing accuracy
- Additional third-party integrations
- Advanced reporting capabilities

### Long-term
- Machine learning for better context understanding
- Automated time categorization
- Pattern-based suggestions
- Cross-platform support

## Integration Capabilities

### Current: Clockify
- Bi-directional sync
- Workspace mapping
- Project/Client synchronization
- Tag mapping
- Conflict resolution

### Planned Integrations
- Toggl
- Harvest
- JIRA Tempo
- Custom integration framework

## Best Practices

### Time Entry
- Use consistent terminology
- Include client/project context when possible
- Regular sync intervals
- Regular breaks for accurate tracking

### System Resources
- Configure screenshot retention
- Set appropriate idle timeouts
- Regular database maintenance
- Backup configuration

## Technical Architecture

### Components
1. Local Python Server
   - Flask-based web server
   - SQLite database
   - System API integration
   - Background task processing

2. Web Interface
   - Single-page application
   - Real-time updates
   - Offline capabilities
   - Responsive design

3. Integration Layer
   - API abstraction
   - Queue management
   - Error handling
   - Sync management

4. Intelligence Engine
   - Text processing
   - Pattern recognition
   - Context analysis
   - Activity classification
