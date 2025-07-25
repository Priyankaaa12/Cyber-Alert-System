# Severity thresholds
from ..config import HIGH_RISK_PORTS, SCAN_THRESHOLDS
HIGH_RISK_PORTS = [22, 3389, 80, 443]
SCAN_THRESHOLDS = {"Low": 5, "Medium": 15, "High": 30}

# Ignore list (e.g., your IP)
IGNORE_IPS = ["192.168.9.160"]