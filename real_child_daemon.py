"""
Real-World Conversational Child AI Daemon (Port 8766)
=====================================================
Server connecting Continuous Laptop Microphone (Hearing), Webcam (Vision),
and Speech Synthesis (Voice) to untouched ENN 4D Cognitive Substrate.
"""

import time
import json
import threading
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
import os

from real_child_brain import RealWorldChildBrain

child = RealWorldChildBrain(child_name="Aria")
state_lock = threading.Lock()


class ChildServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_POST(self):
        global child
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req_json = json.loads(post_data.decode('utf-8'))
        except Exception:
            req_json = {}

        if self.path == "/api/child/converse":
            speech = req_json.get("speech", "")
            v_feat = req_json.get("vision_features", [0.5, 0.5, 0.5, 0.1])
            
            with state_lock:
                state = child.converse_with_parent(user_speech=speech, vision_features=v_feat)
            
            res_body = json.dumps(state).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(res_body)

        elif self.path == "/api/child/praise":
            with state_lock:
                child.happiness = min(1.0, child.happiness + 0.15)
                child.system.update_aspiration(reward=3.0, current_pos_x=np.array([1.0, 1.0, 0.0, 1.0]))
                state = child.get_state_payload()
            
            res_body = json.dumps(state).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(res_body)

        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        global child
        if self.path == "/api/child/live_state":
            with state_lock:
                neurons_data = [
                    {
                        "x": n.x.tolist(),
                        "y": n.y.tolist(),
                        "text": n.text,
                        "role": n.role,
                        "energy": n.energy,
                        "synapses": n.synapses
                    } for n in child.system.world_field.neurons
                ]
                payload = child.get_state_payload()
                payload["neurons"] = neurons_data
            
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        elif self.path in ["/", "/index.html"]:
            try:
                with open("child_nursery.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error loading nursery: {e}".encode())
        else:
            self.send_response(404)
            self.end_headers()


def run_child_server():
    server_address = ("0.0.0.0", 8766)
    httpd = ThreadingHTTPServer(server_address, ChildServerHandler)
    print("👶 Real-World Conversational Child AI running at http://127.0.0.1:8766 ...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_child_server()
