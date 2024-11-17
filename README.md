# Intelligent Time Tracker

A sophisticated local-first time tracking application that combines natural language input with OS-level intelligence to automate time tracking. It runs locally on your computer while providing a clean web interface, and can integrate with external time tracking services like Clockify.

![Time Tracker Interface](docs/screenshots/Time%20Tracker.jpeg)

## Key Features

- Smart text-based input with automatic inference of client, project, and tags
- OS-level activity tracking and idle detection
- Local-first architecture with web interface
- Intelligent automation and context detection
- Integration with external time tracking services (currently Clockify)
- Privacy-focused design - all data stays on your computer

## Quick Start

1. Clone the repository
```bash
git clone [repository-url]
cd intelligent-time-tracker
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure the application
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the application
```bash
python app.py
```

6. Open `http://localhost:5000` in your browser

## Documentation

- [Product Documentation](docs/PRODUCT.md) - Detailed feature and architecture documentation
- [Development Roadmap](docs/ROADMAP.md) - Future development plans and timeline

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

MIT License
