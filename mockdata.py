import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HIGH_RISK_PORTS, SCAN_THRESHOLDS
import random, time, json
from config import HIGH_RISK_PORTS, SCAN_THRESHOLDS

def generate_alert():
    ip = f"192.168.1.{random.randint(1, 254)}"
    port = random.choice(HIGH_RISK_PORTS + [random.randint(1024, 49151)])
    packets = random.randint(1, 50)
    
    severity = "High" if port in HIGH_RISK_PORTS or packets > SCAN_THRESHOLDS["High"] else "Medium"
    return {"ip": ip, "port": port, "severity": severity, "packets": packets}