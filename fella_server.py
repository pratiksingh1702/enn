import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from fella.fella_brain import FellaBrain

brain = None

class FellaHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        if post_data:
            # When you talk to her, she is allowed to autonomously ask Ollama if she gets confused
            res = brain.converse(post_data, autonomous_exploration=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = json.dumps({"response": res['last_response'], "thought": res['last_thought']})
            self.wfile.write(response_data.encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            
    def log_message(self, format, *args):
        pass # Suppress standard HTTP logging for a clean console

def heartbeat_loop():
    print("[HEARTBEAT] Background autonomic loop running.")
    while True:
        # Every 60 seconds, she saves her memory and can run background dreaming/consolidation
        time.sleep(60) 
        brain.save_state('fella_checkpoint.json')

def run_server():
    global brain
    print("Waking up Fella (Loading Brain into Memory)...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    print(f"Fella is fully awake. Total Concepts: {len(brain.substrate.neurons)}")
    
    # Start biological heartbeat in the background
    t = threading.Thread(target=heartbeat_loop, daemon=True)
    t.start()
    
    server_address = ('', 5050)
    httpd = HTTPServer(server_address, FellaHandler)
    print("==================================================")
    print("FELLA IS ALIVE AND LISTENING ON PORT 5050")
    print("She is now a persistent background daemon.")
    print("==================================================")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
