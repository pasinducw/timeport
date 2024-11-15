from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
from io import StringIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_time():
    data = request.json
    description = data.get('description', '').strip()
    
    # End previous active entry
    active_entry = TimeEntry.query.filter_by(end_time=None).first()
    if active_entry:
        active_entry.end_time = datetime.utcnow()
        db.session.commit()

    # If description is "stop" or empty, don't create new entry
    if description.lower() == 'stop' or not description:
        return jsonify({'status': 'stopped'})
    
    # Create new entry
    new_entry = TimeEntry(description=description)
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify(new_entry.to_dict())

@app.route('/stop', methods=['POST'])
def stop_time():
    active_entry = TimeEntry.query.filter_by(end_time=None).first()
    if active_entry:
        active_entry.end_time = datetime.utcnow()
        db.session.commit()
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'no_active_task'})

@app.route('/entries', methods=['GET'])
def get_entries():
    # Get entries for today
    today = datetime.utcnow().date()
    entries = TimeEntry.query.filter(
        db.func.date(TimeEntry.start_time) == today
    ).order_by(TimeEntry.start_time.desc()).all()
    
    return jsonify([entry.to_dict() for entry in entries])

@app.route('/export', methods=['POST'])
def export_and_clear():
    # Get today's entries
    today = datetime.utcnow().date()
    entries = TimeEntry.query.filter(
        db.func.date(TimeEntry.start_time) == today
    ).order_by(TimeEntry.start_time).all()

    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Description', 'Start Time', 'End Time', 'Duration (minutes)'])
    
    for entry in entries:
        end_time = entry.end_time or datetime.utcnow()
        duration = (end_time - entry.start_time).total_seconds() / 60
        writer.writerow([
            entry.description,
            entry.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end_time.strftime('%Y-%m-%d %H:%M:%S'),
            f'{duration:.2f}'
        ])
    
    # End any active task
    active_entry = TimeEntry.query.filter_by(end_time=None).first()
    if active_entry:
        active_entry.end_time = datetime.utcnow()
    
    # Delete all entries from today
    TimeEntry.query.filter(
        db.func.date(TimeEntry.start_time) == today
    ).delete()
    
    db.session.commit()
    
    # Prepare the CSV file for download
    output = si.getvalue()
    si.close()
    
    # Generate filename with current date
    filename = f'time_logs_{today.strftime("%Y-%m-%d")}.csv'
    
    return jsonify({
        'filename': filename,
        'content': output
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
