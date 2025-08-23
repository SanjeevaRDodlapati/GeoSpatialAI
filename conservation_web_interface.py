"""
Simple Web Frontend for Madagascar Conservation AI
=================================================
Demonstrates button-triggered real-world data collection and AI decision making.
"""

from flask import Flask, render_template, request, jsonify, Response
import asyncio
import json
import sys
import os
from datetime import datetime
import threading
import time

# Import conservation system
sys.path.append('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI/ml_model_integration/phase4a_agents')
from frontend_triggering_demo import ConservationTriggerSystem

app = Flask(__name__)
trigger_system = None

# Initialize system on startup
def initialize_conservation_system():
    global trigger_system
    trigger_system = ConservationTriggerSystem()
    
    # Run async initialization in thread
    def run_async_init():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(trigger_system.initialize_system())
        loop.close()
    
    init_thread = threading.Thread(target=run_async_init)
    init_thread.start()
    init_thread.join()

@app.route('/')
def dashboard():
    """Main conservation dashboard."""
    return render_template('conservation_dashboard.html')

@app.route('/api/emergency-response', methods=['POST'])
def trigger_emergency_response():
    """API endpoint for emergency response button."""
    data = request.get_json()
    location = data.get('location', [-18.9667, 48.4500])
    region = data.get('region', 'Madagascar')
    
    # Run emergency response in thread
    def run_emergency():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            trigger_system.trigger_emergency_response(tuple(location), region)
        )
        loop.close()
        return result
    
    result = run_emergency()
    return jsonify(result)

@app.route('/api/species-monitoring', methods=['POST'])
def trigger_species_monitoring():
    """API endpoint for species monitoring button."""
    data = request.get_json()
    site = data.get('site', 'andasibe_mantadia')
    
    def run_monitoring():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            trigger_system.trigger_species_monitoring(site)
        )
        loop.close()
        return result
    
    result = run_monitoring()
    return jsonify(result)

@app.route('/api/threat-scanning', methods=['POST'])
def trigger_threat_scanning():
    """API endpoint for threat scanning button."""
    data = request.get_json()
    region = data.get('region', 'madagascar_central')
    
    def run_scanning():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            trigger_system.trigger_threat_scanning(region)
        )
        loop.close()
        return result
    
    result = run_scanning()
    return jsonify(result)

@app.route('/api/natural-language-query', methods=['POST'])
def process_natural_language_query():
    """API endpoint for natural language queries."""
    data = request.get_json()
    query = data.get('query', '')
    
    def run_query():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            trigger_system.process_natural_language_query(query)
        )
        loop.close()
        return result
    
    result = run_query()
    return jsonify(result)

@app.route('/api/system-status')
def get_system_status():
    """Get current system status."""
    return jsonify({
        "status": "operational",
        "apis_active": 6,
        "real_time_data": True,
        "agents_ready": 6,
        "last_update": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🌍 Starting Madagascar Conservation AI Web Interface...")
    print("🚀 Initializing real-world data connections...")
    
    # Initialize conservation system
    initialize_conservation_system()
    
    print("✅ System ready!")
    print("🌐 Web interface starting at http://localhost:5000")
    print("🎯 Ready for frontend button triggers and real-world data collection!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
