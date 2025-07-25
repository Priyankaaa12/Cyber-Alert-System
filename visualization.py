import json
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime
import logging

THREAT_HISTORY_FILE = Path("data/threat_history.json")

def init_visualization():
    """Initialize visualization data storage"""
    THREAT_HISTORY_FILE.parent.mkdir(exist_ok=True)
    if not THREAT_HISTORY_FILE.exists():
        with open(THREAT_HISTORY_FILE, "w") as f:
            json.dump({"threats": [], "timeline": []}, f)

def update_threat_data(ip, threat_type, severity):
    """Update threat history with new detection"""
    try:
        data = json.loads(THREAT_HISTORY_FILE.read_text())
        
        # Add new threat
        data["threats"].append({
            "timestamp": datetime.now().isoformat(),
            "ip": ip,
            "type": threat_type,
            "severity": severity
        })
        
       
        data["timeline"] = [t for t in data["timeline"] 
                          if (datetime.now() - datetime.fromisoformat(t["timestamp"])).days < 1]
        data["timeline"].append({
            "timestamp": datetime.now().isoformat(),
            "count": len([t for t in data["threats"] 
                        if (datetime.now() - datetime.fromisoformat(t["timestamp"])).seconds < 3600])
        })
        
        THREAT_HISTORY_FILE.write_text(json.dumps(data, indent=2))
        return True
        
    except Exception as e:
        logging.error(f"Visualization update failed: {str(e)}")
        return False

def generate_threat_map(threats):
    """Generate Leaflet.js compatible map data"""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [0, 0]  
                },
                "properties": {
                    "ip": t["ip"],
                    "type": t["type"],
                    "severity": t["severity"]
                }
            } for t in threats
        ]
    }

def generate_timeline_figure():
    """Generate Plotly timeline visualization"""
    try:
        data = json.loads(THREAT_HISTORY_FILE.read_text())
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[datetime.fromisoformat(t["timestamp"]) for t in data["timeline"]],
            y=[t["count"] for t in data["timeline"]],
            mode='lines+markers',
            name='Threats/hour',
            line=dict(color='#ff2a6d', width=3)
        ))
        
        fig.update_layout(
            title='Threat Activity Timeline',
            xaxis_title='Time',
            yaxis_title='Threat Count',
            plot_bgcolor='rgba(13, 2, 33, 0.8)',
            paper_bgcolor='rgba(13, 2, 33, 0.8)',
            font=dict(color='#05d9e8')
        )
        
        return fig.to_json()
        
    except Exception as e:
        logging.error(f"Timeline generation failed: {str(e)}")
        return None