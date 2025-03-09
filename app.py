from flask import Flask, session, flash, redirect, url_for, request
from config import Config
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.main_routes import main_bp
from routes.horizon1_routes import horizon1_bp
from routes.horizon2_routes import horizon2_bp
from routes.horizon3_routes import horizon3_bp
import os
import threading
import schedule
import time
from mupdate import update_measurements_with_api_data  # Import your function

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(main_bp)
app.register_blueprint(horizon1_bp)
app.register_blueprint(horizon2_bp)
app.register_blueprint(horizon3_bp)

@app.before_request
def update_last_activity():
    if 'user_id' in session:
        session['last_activity'] = os.times().elapsed  # Update activity time
    if 'last_activity' in session:
        last_activity = session['last_activity']
        current_time = os.times().elapsed
        if current_time - last_activity > app.config['PERMANENT_SESSION_LIFETIME'].total_seconds():
            session.clear()
            flash('Session expired due to inactivity', 'warning')
            return redirect(url_for('auth.login'))
    elif 'user_id' in session and request.endpoint != 'static':
        session['last_activity'] = os.times().elapsed

# Function to run scheduled tasks in a separate thread
def run_scheduler():
    schedule.every(0.1).minutes.do(update_measurements_with_api_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a background thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == '__main__':
    app.run(debug=True)