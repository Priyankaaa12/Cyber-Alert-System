# Import modules
from utils.mock_data import generate_alert
from utils.visualizations import update_threat_map, generate_timeline
from utils.firewall import block_ip
import time


while True:
    alert = generate_alert()  # Generate fake alerts
    print(alert)
    update_threat_map(alert["ip"], alert["severity"])
    generate_timeline(alert)
    time.sleep(5)  # Simulate real-time detection