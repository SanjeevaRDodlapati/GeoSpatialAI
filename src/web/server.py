#!/usr/bin/env python3
"""
🔍 Madagascar Conservation AI - TRACED Web Server
================================================
This version includes full debugging and traces every action
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import urllib.parse
from datetime import datetime
import sys
import os

# Add project root to path to import our API modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# Import the conservation API functions
try:
    # Try new structure first
    try:
        from src.api.conservation_apis import (
            trigger_location_analysis,
            trigger_emergency_response,
            trigger_species_monitoring,
            trigger_threat_scanning
        )
    except ImportError:
        # Fallback to original for compatibility
        from working_real_api_wrappers import (
            trigger_location_analysis,
            trigger_emergency_response,
            trigger_species_monitoring,
            trigger_threat_scanning
        )
    REAL_API_AVAILABLE = True
    print("✅ Conservation API modules loaded successfully!")
except ImportError as e:
    print(f"⚠️ Could not import conservation API modules: {e}")
    REAL_API_AVAILABLE = False

class TracedConservationHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Override to add timestamps and better formatting"""
        print(f"🌐 [{datetime.now().strftime('%H:%M:%S')}] {format % args}")
    
    def do_GET(self):
        print(f"\n🔍 GET Request: {self.path}")
        
        # Handle URLs with VS Code parameters
        path = self.path.split('?')[0]  # Remove query parameters for routing
        
        if path == '/' or path == '/index.html':
            self.serve_dashboard()
        elif path == '/debug':
            self.serve_debug_page()
        elif path == '/api/system-status':
            self.serve_system_status()
        elif self.path.startswith('/api/location-analysis'):
            self.handle_location_analysis_get()
        else:
            print(f"❌ 404 - Path not found: {self.path}")
            self.send_error(404)
    
    def do_POST(self):
        print(f"\n🔍 POST Request: {self.path}")
        
        # Read POST data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        
        print(f"📊 POST Data Length: {content_length}")
        if post_data:
            try:
                data = json.loads(post_data.decode('utf-8'))
                print(f"📋 POST Data: {json.dumps(data, indent=2)}")
            except:
                print(f"📋 POST Data (raw): {post_data}")
        
        if self.path == '/api/emergency-response':
            self.handle_emergency_response(post_data)
        elif self.path == '/api/species-monitoring':
            self.handle_species_monitoring(post_data)
        elif self.path == '/api/threat-scanning':
            self.handle_threat_scanning(post_data)
        elif self.path == '/api/location-analysis':
            self.handle_location_analysis_post(post_data)
        elif self.path == '/api/natural-language-query':
            self.handle_natural_language_query(post_data)
        else:
            print(f"❌ 404 - POST path not found: {self.path}")
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serve the main conservation dashboard."""
        print("🏠 Serving dashboard...")
        try:
            with open('dashboard_real_map.html', 'r') as f:
                html_content = f.read()
            
            # Inject JavaScript debugging
            debug_js = """
            <script>
            // Add debugging to all fetch calls
            const originalFetch = window.fetch;
            window.fetch = function(...args) {
                console.log('🌐 Frontend Fetch:', args[0], args[1]);
                return originalFetch.apply(this, args)
                    .then(response => {
                        console.log('✅ Response:', response.status, response.statusText);
                        return response;
                    })
                    .catch(error => {
                        console.error('❌ Fetch Error:', error);
                        throw error;
                    });
            };
            
            // Override the analyzeLocation function to actually call the API
            window.analyzeLocation = function(lat, lng, locationName) {
                console.log('🎯 Analyzing location:', lat, lng, locationName);
                
                // Validate global coordinates
                if (lat < -90 || lat > 90 || lng < -180 || lng > 180) {
                    showResult('❌ Invalid Location', 
                        `📍 COORDINATES: ${lat}, ${lng}\\n\\n` +
                        `⚠️ ERROR: Invalid global coordinates!\\n\\n` +
                        `🌍 Valid coordinate ranges:\\n` +
                        `  • Latitude: -90 to 90\\n` +
                        `  • Longitude: -180 to 180\\n\\n` +
                        `Please select a valid location anywhere on Earth.`
                    );
                    return;
                }
                
                // Store location data globally for action buttons
                window.lastSelectedLat = lat;
                window.lastSelectedLng = lng;
                window.lastSelectedLocation = locationName;
                
                fetch('/api/location-analysis', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({lat: lat, lng: lng, location: locationName})
                })
                .then(response => response.json())
                .then(data => {
                    console.log('📊 Location analysis result:', data);
                    showResult('🗺️ Real Location Analysis: ' + locationName, data.analysis);
                })
                .catch(error => {
                    console.error('❌ Location analysis error:', error);
                    showResult('❌ Error', 'Failed to analyze location: ' + error.message);
                });
            };
            
            // Override action functions to call real APIs with location data
            window.triggerEmergencyResponse = function() {
                console.log('🚨 Triggering emergency response...');
                var requestData = {};
                if (window.lastSelectedLat && window.lastSelectedLng) {
                    requestData = {
                        lat: window.lastSelectedLat,
                        lng: window.lastSelectedLng,
                        location: window.lastSelectedLocation || 'Selected Location'
                    };
                    console.log('📍 Using location data:', requestData);
                }
                fetch('/api/emergency-response', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(requestData)
                })
                .then(response => response.json())
                .then(data => showResult('🚨 Emergency Response', data.analysis))
                .catch(error => showResult('❌ Error', 'Emergency response failed: ' + error.message));
            };
            
            window.startSpeciesMonitoring = function() {
                console.log('🔍 Starting species monitoring...');
                var requestData = {};
                if (window.lastSelectedLat && window.lastSelectedLng) {
                    requestData = {
                        lat: window.lastSelectedLat,
                        lng: window.lastSelectedLng,
                        location: window.lastSelectedLocation || 'Selected Location'
                    };
                    console.log('📍 Using location data:', requestData);
                }
                fetch('/api/species-monitoring', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(requestData)
                })
                .then(response => response.json())
                .then(data => showResult('🔍 Species Monitoring', data.analysis))
                .catch(error => showResult('❌ Error', 'Species monitoring failed: ' + error.message));
            };
            
            window.scanForThreats = function() {
                console.log('⚠️ Scanning for threats...');
                var requestData = {};
                if (window.lastSelectedLat && window.lastSelectedLng) {
                    requestData = {
                        lat: window.lastSelectedLat,
                        lng: window.lastSelectedLng,
                        location: window.lastSelectedLocation || 'Selected Location'
                    };
                    console.log('📍 Using location data:', requestData);
                }
                fetch('/api/threat-scanning', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(requestData)
                })
                .then(response => response.json())
                .then(data => showResult('⚠️ Threat Scanning', data.analysis))
                .catch(error => showResult('❌ Error', 'Threat scanning failed: ' + error.message));
            };
            </script>
            """
            
            # Insert debug JavaScript before closing body tag
            html_content = html_content.replace('</body>', debug_js + '</body>')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(html_content.encode())
            print("✅ Dashboard served successfully")
            
        except FileNotFoundError:
            print("❌ Dashboard file not found!")
            self.send_error(404, "Dashboard file not found")
    
    def serve_debug_page(self):
        """Serve the debug test page"""
        print("🔧 Serving debug page...")
        try:
            with open('debug_test.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(html_content.encode())
            print("✅ Debug page served successfully")
            
        except FileNotFoundError:
            print("❌ Debug page file not found!")
            self.send_error(404, "Debug page file not found")
    
    def handle_location_analysis_get(self):
        """Handle GET request for location analysis (for URL params)"""
        print("🗺️ Processing location analysis (GET)...")
        
        # Parse URL parameters
        url_parts = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(url_parts.query)
        
        lat = params.get('lat', [None])[0]
        lng = params.get('lng', [None])[0]
        location = params.get('location', ['Unknown'])[0]
        
        print(f"📍 Location: {location} ({lat}, {lng})")
        
        if lat and lng and REAL_API_AVAILABLE:
            try:
                result = trigger_location_analysis(float(lat), float(lng), location)
                self.send_json_response({"status": "success", "analysis": result})
            except Exception as e:
                print(f"❌ Error in location analysis: {e}")
                self.send_json_response({"status": "error", "message": str(e)})
        else:
            # Fallback response
            result = f"📍 LOCATION: {location}\n🔍 Coordinates: {lat}, {lng}\n⚠️ Using fallback analysis (real API not available)"
            self.send_json_response({"status": "fallback", "analysis": result})
    
    def handle_location_analysis_post(self, post_data):
        """Handle POST request for location analysis"""
        print("🗺️ Processing location analysis (POST)...")
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            lat = data.get('lat')
            lng = data.get('lng') 
            location = data.get('location', 'Unknown')
            
            print(f"📍 Location: {location} ({lat}, {lng})")
            
            if REAL_API_AVAILABLE:
                print("🔄 Calling real API...")
                result = trigger_location_analysis(lat, lng, location)
                self.send_json_response({"status": "success", "analysis": result})
            else:
                print("⚠️ Using fallback response...")
                result = f"📍 REAL LOCATION ANALYSIS\n\nLocation: {location}\nCoordinates: {lat}, {lng}\n\n🔄 PROCESSING:\n• Connecting to GBIF API...\n• Analyzing NASA satellite data...\n• Processing USGS geological data...\n\n✅ Analysis would be performed here with real APIs"
                self.send_json_response({"status": "fallback", "analysis": result})
                
        except Exception as e:
            print(f"❌ Error processing location analysis: {e}")
            self.send_json_response({"status": "error", "message": str(e)})
    
    def handle_emergency_response(self, post_data):
        """Handle emergency response with location data if available."""
        print("🚨 Processing emergency response...")
        
        # Try to get location data from POST
        lat, lng, location_name = None, None, "Emergency Zone"
        if post_data:
            try:
                data = json.loads(post_data.decode('utf-8'))
                lat = data.get('lat')
                lng = data.get('lng')
                location_name = data.get('location', 'Emergency Zone')
                print(f"📍 Emergency response for: {location_name} ({lat}, {lng})")
            except:
                print("⚠️ No location data provided, using default emergency scan")
        
        if REAL_API_AVAILABLE:
            try:
                print("🔄 Calling real emergency response API...")
                result = trigger_emergency_response(lat, lng, location_name)
                self.send_json_response({"status": "success", "analysis": result})
            except Exception as e:
                print(f"❌ Error in emergency response: {e}")
                self.send_json_response({"status": "error", "message": str(e)})
        else:
            result = "🚨 EMERGENCY RESPONSE ACTIVATED\n\n⚠️ Real API not available - using demonstration mode"
            self.send_json_response({"status": "fallback", "analysis": result})
    
    def handle_species_monitoring(self, post_data):
        """Handle species monitoring with location data if available."""
        print("🔍 Processing species monitoring...")
        
        # Try to get location data from POST
        lat, lng, location_name = None, None, "Monitoring Site"
        if post_data:
            try:
                data = json.loads(post_data.decode('utf-8'))
                lat = data.get('lat')
                lng = data.get('lng')
                location_name = data.get('location', 'Monitoring Site')
                print(f"📍 Species monitoring for: {location_name} ({lat}, {lng})")
            except:
                print("⚠️ No location data provided, using default monitoring site")
        
        if REAL_API_AVAILABLE:
            try:
                print("🔄 Calling real species monitoring API...")
                result = trigger_species_monitoring(lat, lng, location_name)
                self.send_json_response({"status": "success", "analysis": result})
            except Exception as e:
                print(f"❌ Error in species monitoring: {e}")
                self.send_json_response({"status": "error", "message": str(e)})
        else:
            result = "🔍 SPECIES MONITORING STARTED\n\n⚠️ Real API not available - using demonstration mode"
            self.send_json_response({"status": "fallback", "analysis": result})
    
    def handle_threat_scanning(self, post_data):
        """Handle threat scanning with location data if available."""
        print("⚠️ Processing threat scanning...")
        
        # Try to get location data from POST
        lat, lng, location_name = None, None, "Threat Scan Area"
        if post_data:
            try:
                data = json.loads(post_data.decode('utf-8'))
                lat = data.get('lat')
                lng = data.get('lng')
                location_name = data.get('location', 'Threat Scan Area')
                print(f"📍 Threat scanning for: {location_name} ({lat}, {lng})")
            except:
                print("⚠️ No location data provided, using multi-site scan")
        
        if REAL_API_AVAILABLE:
            try:
                print("🔄 Calling real threat scanning API...")
                result = trigger_threat_scanning(lat, lng, location_name)
                self.send_json_response({"status": "success", "analysis": result})
            except Exception as e:
                print(f"❌ Error in threat scanning: {e}")
                self.send_json_response({"status": "error", "message": str(e)})
        else:
            result = "⚠️ THREAT SCANNING INITIATED\n\n⚠️ Real API not available - using demonstration mode"
            self.send_json_response({"status": "fallback", "analysis": result})
    
    def handle_natural_language_query(self, post_data):
        """Handle natural language query"""
        print("💬 Processing natural language query...")
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            query = data.get('query', '')
            print(f"🤔 Query: {query}")
            
            result = f"💬 QUERY PROCESSED: '{query}'\n\n🤖 Analysis would be performed here with real AI processing"
            self.send_json_response({"status": "success", "analysis": result})
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            self.send_json_response({"status": "error", "message": str(e)})
    
    def serve_system_status(self):
        """Serve system status with real checks"""
        print("📊 Checking system status...")
        
        status = {
            "status": "operational",
            "apis_active": 6 if REAL_API_AVAILABLE else 0,
            "agents_ready": 6 if REAL_API_AVAILABLE else 0,
            "real_api_available": REAL_API_AVAILABLE,
            "last_update": datetime.now().isoformat()
        }
        
        print(f"📈 Status: {status}")
        self.send_json_response(status)
    
    def send_json_response(self, data):
        """Send JSON response with proper headers"""
        json_data = json.dumps(data, indent=2)
        print(f"📤 Sending response: {json_data[:200]}...")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json_data.encode())

def run_traced_server():
    """Run the traced conservation web server"""
    print("🔍 Global Conservation AI - TRACED Web Server")
    print("=" * 60)
    print(f"🚀 Starting traced web server...")
    print(f"📊 Real API Available: {REAL_API_AVAILABLE}")
    print(f"🌐 URL: http://localhost:8000")
    print(f"🔍 Full debugging enabled!")
    print("=" * 60)
    
    server = HTTPServer(('localhost', 8000), TracedConservationHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Traced server stopped")

if __name__ == '__main__':
    run_traced_server()
