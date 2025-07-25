# utils/firewall.py (Windows-specific version)
import os
import platform
import subprocess
import logging

def block_ip(ip):
    """Block IP on Windows using native firewall"""
    try:
        if platform.system() != "Windows":
            logging.warning("Windows firewall commands only work on Windows")
            return False

        # Validate IP format
        parts = ip.split('.')
        if len(parts) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            raise ValueError(f"Invalid IP: {ip}")

        # PowerShell command
        command = [
            "powershell",
            "-Command",
            f"New-NetFirewallRule -DisplayName 'BLOCK {ip}' "
            f"-Direction Inbound -RemoteAddress {ip} -Action Block -Enabled True"
        ]

        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        logging.info(f"Blocked {ip} successfully")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to block {ip}: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Error blocking {ip}: {str(e)}")
        return False