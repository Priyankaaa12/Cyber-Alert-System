from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Threat types with realistic properties
THREATS = [
    {"type": "SYN Flood", "severity": 4, "port": 80},
    {"type": "SSH Brute Force", "severity": 3, "port": 22},
    {"type": "SQL Injection", "severity": 5, "port": 3306},
    {"type": "Port Scan", "severity": 2, "port": "Multiple"}
]

def generate_mock_threat():
    """Auto-generate threats every 5-10 seconds"""
    while True:
        threat = random.choice(THREATS)
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        socketio.emit('new_alert', {
            'ip': ip,
            'type': threat["type"],
            'severity': threat["severity"],
            'port': threat["port"],
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'location': {
                'lat': random.uniform(-90, 90),
                'lon': random.uniform(-180, 180)
            }
        })
        time.sleep(random.randint(5, 10))

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/block/<ip>')
def block_ip(ip):
    return jsonify({
        "status": "success", 
        "message": f"Blocked {ip}",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == "__main__":
    # Start mock threat generator in background
    threading.Thread(target=generate_mock_threat, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)