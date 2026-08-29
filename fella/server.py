"""
FELLA Server: REST API & 3D WebGL Visualization Daemon
======================================================
Serves the live 3D Stacked Z-Plane Visualizer and cognitive control endpoints.
Run with: python -m fella.server (Default Port: 8790)
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys
import threading
from typing import Optional, Dict, Any, List

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain
from fella.trainer import FellaTrainer

PORT = 8790
_brain_lock = threading.Lock()
_global_brain: Optional[FellaBrain] = None


def get_or_create_brain() -> FellaBrain:
    global _global_brain
    with _brain_lock:
        if _global_brain is None:
            checkpoint = "fella_checkpoint.json"
            if os.path.exists(checkpoint):
                try:
                    _global_brain = FellaBrain.load_state(checkpoint)
                except Exception:
                    _global_brain = FellaBrain(dim=16)
                    _global_brain.boot_foundations()
                    _global_brain.save_state(checkpoint)
            else:
                _global_brain = FellaBrain(dim=16)
                _global_brain.boot_foundations()
                _global_brain.save_state(checkpoint)
        return _global_brain


class FellaRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        
        if url.path == "/" or url.path == "/index.html":
            html_path = os.path.join(os.path.dirname(__file__), "visualizer.html")
            if os.path.exists(html_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "visualizer.html not found")
                return
                
        elif url.path == "/api/state":
            brain = get_or_create_brain()
            with _brain_lock:
                tel = brain.get_telemetry()
                # Package 3D coordinates for visualizer: (X_pos, Y_pos, Z_pos)
                neuron_list = []
                for n in brain.substrate.neurons.values():
                    # Projection: first 2 dims of X as local XY, Z as vertical axis
                    p_x = float(n.x[0] if len(n.x) > 0 else 0.0) * 12.0 - 6.0
                    p_y = float(n.y[0] if len(n.y) > 0 else 0.0) * 12.0 - 6.0
                    p_z = float(n.z) * 4.0  # Vertical stacking scale
                    
                    neuron_list.append({
                        "id": n.id,
                        "text": n.text,
                        "role": n.role,
                        "energy": n.energy,
                        "z_plane": float(n.z),
                        "pos_3d": [p_x, p_y, p_z],
                        "synapses": {str(k): float(v) for k, v in n.synapses.items()}
                    })
                    
                payload = {
                    "telemetry": tel,
                    "neurons": neuron_list,
                    "learned_insights": brain.learned_insights[-10:]
                }
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return
            
        super().do_GET()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}
            
        brain = get_or_create_brain()
        
        if url.path == "/api/converse":
            text = req_data.get("text", "")
            with _brain_lock:
                brain.converse(text)
                tel = brain.get_telemetry()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(tel).encode("utf-8"))
            return
            
        elif url.path == "/api/curiosity":
            with _brain_lock:
                res = brain.autonomous_curiosity_cycle()
                tel = brain.get_telemetry()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"result": res, "telemetry": tel}).encode("utf-8"))
            return
            
        elif url.path == "/api/dream":
            with _brain_lock:
                res = brain.dream_consolidation()
                tel = brain.get_telemetry()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"result": res, "telemetry": tel}).encode("utf-8"))
            return
            
        self.send_error(404, "Endpoint not found")


def run_server(port: int = PORT):
    brain = get_or_create_brain()
    server_address = ("", port)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(server_address, FellaRequestHandler) as httpd:
        print("=" * 70)
        print(f"🚀 FELLA 3D Live Visualization Server Running at: http://127.0.0.1:{port}")
        print("=" * 70)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down FELLA server...")


if __name__ == "__main__":
    run_server()
