from flask import Flask, render_template, jsonify, request, send_from_directory, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
from io import StringIO
import pytz

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def get_local_time():
    """Get current time in local timezone"""
    utc_now = datetime.utcnow()
    local_tz = pytz.timezone('Asia/Colombo')  # Sri Lanka timezone (GMT+5:30)
    local_time = utc_now.replace(tzinfo=pytz.UTC).astimezone(local_tz)
    return local_time

def format_timestamp(dt):
    """Format datetime for JSON response"""
    if not dt:
        return None
    if not dt.tzinfo:
        dt = pytz.UTC.localize(dt)
    local_tz = pytz.timezone('Asia/Colombo')
    local_time = dt.astimezone(local_tz)
    return local_time.isoformat()

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    entries = db.relationship('TimeEntry', backref='session', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': format_timestamp(self.start_time),
            'end_time': format_timestamp(self.end_time),
            'entry_count': len(self.entries)
        }

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'notes': self.notes,
            'start_time': format_timestamp(self.start_time),
            'end_time': format_timestamp(self.end_time)
        }

@app.route('/')
def index():
    active_session = Session.query.filter_by(end_time=None).first()
    if not active_session:
        return redirect(url_for('sessions'))
    return render_template('index.html', session_id=active_session.id)

@app.route('/sessions')
def sessions():
    return render_template('sessions.html')

@app.route('/sessions/new', methods=['POST'])
def new_session():
    # End any active session
    active_session = Session.query.filter_by(end_time=None).first()
    if active_session:
        active_session.end_time = datetime.utcnow()
        db.session.commit()
    
    # Create new session
    name = request.json.get('name', f'Session {get_local_time().strftime("%Y-%m-%d %H:%M")}')
    new_session = Session(name=name)
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify(new_session.to_dict())

@app.route('/sessions/<int:session_id>/end', methods=['POST'])
def end_session(session_id):
    session = Session.query.get_or_404(session_id)
    if not session.end_time:
        # End active task if any
        active_entry = TimeEntry.query.filter_by(session_id=session_id, end_time=None).first()
        if active_entry:
            active_entry.end_time = datetime.utcnow()
        
        session.end_time = datetime.utcnow()
        db.session.commit()
    
    return jsonify(session.to_dict())

@app.route('/sessions/list')
def list_sessions():
    sessions = Session.query.order_by(Session.start_time.desc()).all()
    return jsonify([session.to_dict() for session in sessions])

@app.route('/sessions/<int:session_id>/entries')
def get_session_entries(session_id):
    entries = TimeEntry.query.filter_by(session_id=session_id).order_by(TimeEntry.start_time.desc()).all()
    return jsonify([entry.to_dict() for entry in entries])

@app.route('/log', methods=['POST'])
def log_time():
    active_session = Session.query.filter_by(end_time=None).first()
    if not active_session:
        return jsonify({'error': 'No active session'}), 400

    data = request.json
    description = data.get('description', '').strip()
    
    # End previous active entry
    active_entry = TimeEntry.query.filter_by(session_id=active_session.id, end_time=None).first()
    if active_entry:
        active_entry.end_time = datetime.utcnow()
        db.session.commit()

    # If description is "stop" or empty, don't create new entry
    if description.lower() == 'stop' or not description:
        return jsonify({'status': 'stopped'})
    
    # Create new entry
    new_entry = TimeEntry(description=description, session_id=active_session.id)
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify(new_entry.to_dict())

@app.route('/stop', methods=['POST'])
def stop_time():
    active_session = Session.query.filter_by(end_time=None).first()
    if not active_session:
        return jsonify({'error': 'No active session'}), 400

    active_entry = TimeEntry.query.filter_by(session_id=active_session.id, end_time=None).first()
    if active_entry:
        active_entry.end_time = datetime.utcnow()
        db.session.commit()
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'no_active_task'})

@app.route('/sessions/<int:session_id>/export', methods=['POST'])
def export_session(session_id):
    session = Session.query.get_or_404(session_id)
    entries = TimeEntry.query.filter_by(session_id=session_id).order_by(TimeEntry.start_time).all()

    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Description', 'Start Time', 'End Time', 'Duration (minutes)'])
    
    local_tz = pytz.timezone('Asia/Colombo')
    
    for entry in entries:
        start_time = pytz.UTC.localize(entry.start_time).astimezone(local_tz)
        end_time = pytz.UTC.localize(entry.end_time).astimezone(local_tz) if entry.end_time else get_local_time()
        duration = (end_time - start_time).total_seconds() / 60
        writer.writerow([
            entry.description,
            start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end_time.strftime('%Y-%m-%d %H:%M:%S'),
            f'{duration:.2f}'
        ])
    
    # Prepare the CSV file for download
    output = si.getvalue()
    si.close()
    
    # Generate filename with session name and date
    filename = f'time_logs_{session.name}_{get_local_time().strftime("%Y-%m-%d")}.csv'
    
    return jsonify({
        'filename': filename,
        'content': output
    })

@app.route('/entries/<int:entry_id>/notes', methods=['POST'])
def update_entry_notes(entry_id):
    entry = TimeEntry.query.get_or_404(entry_id)
    data = request.json
    entry.notes = data.get('notes', '').strip() or None
    db.session.commit()
    return jsonify(entry.to_dict())

@app.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = TimeEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    
    # Don't allow deleting active sessions
    if not session.end_time:
        return jsonify({'error': 'Cannot delete active session'}), 400
        
    # Delete all time entries first
    TimeEntry.query.filter_by(session_id=session_id).delete()
    
    # Delete the session
    db.session.delete(session)
    db.session.commit()
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
