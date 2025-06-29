#!/usr/bin/env python3
"""
Dream.OS Cell Phone - Web Backend Server
========================================

Simple HTTP server to handle web GUI requests and communicate with the Agent Cell Phone system.
"""

import json
import sys
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from agent_cell_phone import AgentCellPhone, MsgTag
    ACP_AVAILABLE = True
except ImportError:
    ACP_AVAILABLE = False
    print("Warning: Agent Cell Phone module not available")

class WebBackendHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the web backend."""
    
    def __init__(self, *args, **kwargs):
        self.acp = None
        if ACP_AVAILABLE:
            try:
                self.acp = AgentCellPhone()
            except Exception as e:
                print(f"Warning: Could not initialize Agent Cell Phone: {e}")
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests."""
        # Parse the URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path.lstrip('/')
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            data = {}
        
        # Handle different endpoints
        if path == 'send':
            response = self.handle_send(data)
        elif path == 'broadcast':
            response = self.handle_broadcast(data)
        elif path == 'scripts':
            response = self.handle_scripts(data)
        elif path == 'tests':
            response = self.handle_tests(data)
        elif path == 'status':
            response = self.handle_status()
        else:
            response = {'success': False, 'message': f'Unknown endpoint: {path}'}
        
        # Send response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_send(self, data):
        """Handle individual agent message sending."""
        if not self.acp:
            return {'success': False, 'message': 'Agent Cell Phone not available'}
        
        try:
            agent = data.get('agent', 'agent-1')
            message = data.get('message', '')
            tag_str = data.get('tag', 'NORMAL')
            
            # Convert tag string to MsgTag enum
            tag_map = {
                'NORMAL': MsgTag.NORMAL,
                'RESUME': MsgTag.RESUME,
                'SYNC': MsgTag.SYNC,
                'RESTORE': MsgTag.RESTORE,
                'VERIFY': MsgTag.VERIFY,
                'REPAIR': MsgTag.REPAIR
            }
            tag = tag_map.get(tag_str, MsgTag.NORMAL)
            
            self.acp.send(agent, message, tag)
            return {'success': True, 'message': f'Message sent to {agent}'}
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def handle_broadcast(self, data):
        """Handle broadcast message sending."""
        if not self.acp:
            return {'success': False, 'message': 'Agent Cell Phone not available'}
        
        try:
            message = data.get('message', '')
            tag_str = data.get('tag', 'NORMAL')
            
            # Convert tag string to MsgTag enum
            tag_map = {
                'NORMAL': MsgTag.NORMAL,
                'RESUME': MsgTag.RESUME,
                'SYNC': MsgTag.SYNC,
                'RESTORE': MsgTag.RESTORE,
                'VERIFY': MsgTag.VERIFY,
                'REPAIR': MsgTag.REPAIR
            }
            tag = tag_map.get(tag_str, MsgTag.NORMAL)
            
            self.acp.broadcast(message, tag)
            return {'success': True, 'message': 'Broadcast sent to all agents'}
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def handle_scripts(self, data):
        """Handle script management."""
        action = data.get('action', '')
        
        try:
            if action == 'start':
                # Start scripts
                env = os.environ.copy()
                env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
                
                subprocess.Popen([sys.executable, "scripts/agent_messenger.py"], env=env)
                subprocess.Popen([sys.executable, "scripts/agent_onboarding_sequence.py"], env=env)
                subprocess.Popen([sys.executable, "scripts/send_to_agents.py"], env=env)
                
                return {'success': True, 'message': 'All scripts started'}
                
            elif action == 'stop':
                # Stop scripts
                if os.name == 'nt':  # Windows
                    subprocess.run(["taskkill", "/f", "/im", "python.exe"], 
                                 capture_output=True, text=True)
                else:  # Unix/Linux
                    subprocess.run(["pkill", "-f", "scripts/"], 
                                 capture_output=True, text=True)
                
                return {'success': True, 'message': 'All scripts stopped'}
                
            elif action == 'restart':
                # Restart scripts
                self.handle_scripts({'action': 'stop'})
                time.sleep(1)
                self.handle_scripts({'action': 'start'})
                
                return {'success': True, 'message': 'All scripts restarted'}
                
            else:
                return {'success': False, 'message': f'Unknown script action: {action}'}
                
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def handle_tests(self, data):
        """Handle test execution."""
        action = data.get('action', '')
        
        if action == 'run':
            try:
                # Set PYTHONPATH to include src directory
                env = os.environ.copy()
                env['PYTHONPATH'] = os.path.join(os.getcwd(), 'src') + os.pathsep + env.get('PYTHONPATH', '')
                
                result = subprocess.run([sys.executable, "tests/test_harness.py", "--mode", "demo"], 
                                      env=env, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    return {'success': True, 'message': 'Test suite completed successfully'}
                else:
                    return {'success': False, 'message': f'Test suite failed: {result.stderr}'}
                    
            except subprocess.TimeoutExpired:
                return {'success': False, 'message': 'Test suite timed out'}
            except Exception as e:
                return {'success': False, 'message': str(e)}
        else:
            return {'success': False, 'message': f'Unknown test action: {action}'}
    
    def handle_status(self):
        """Handle status requests."""
        if self.acp:
            try:
                agents = self.acp.get_available_agents()
                return {
                    'success': True, 
                    'message': f'Connected to {len(agents)} agents',
                    'agents': agents
                }
            except Exception as e:
                return {'success': False, 'message': str(e)}
        else:
            return {'success': False, 'message': 'Agent Cell Phone not available'}
    
    def log_message(self, format, *args):
        """Override to reduce logging noise."""
        pass

def run_server(port=8080):
    """Run the web backend server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebBackendHandler)
    print(f"🌐 Web backend server running on port {port}")
    print(f"📱 Access the web GUI at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Dream.OS Cell Phone Web Backend Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on (default: 8080)')
    
    args = parser.parse_args()
    run_server(args.port) 