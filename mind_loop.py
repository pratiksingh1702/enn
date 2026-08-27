"""
ENN 4D: Autonomous Mind Loop (Continuous Consciousness & Idle Rumination)
Runs a continuous background heartbeat driving:
- Baseline Instability (Idle clock)
- Thermal Replay & Cross-Family Resonance (Wonder / Dreams)
- Epistemic Vacuum Resolution (Curiosity Satisfaction)
"""

import time
import queue
import threading
from typing import Optional, Callable, Dict, Any
from enn4d import ENN4D
from text_decoder import TextDecoder

class MindLoop:
    def __init__(self, system: ENN4D, decoder: Optional[TextDecoder] = None, tick_interval: float = 3.0):
        self.system = system
        self.decoder = decoder or TextDecoder()
        self.tick_interval = tick_interval
        
        self.thought_queue: queue.Queue = queue.Queue()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()
        self.last_user_event_time = time.time()
        self.on_thought_callback: Optional[Callable[[Dict[str, Any]], None]] = None

    def start(self):
        """Start the continuous living mind loop in a background thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="ENNMindLoop")
        self._thread.start()

    def stop(self):
        """Stop the background thread."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

    def mark_user_activity(self):
        """Reset the idle timer upon external user sensory input."""
        with self._lock:
            self.last_user_event_time = time.time()

    def get_lock(self) -> threading.RLock:
        return self._lock

    def _run_loop(self):
        while self._running:
            time.sleep(0.5)
            # Only ruminate if idle for more than tick_interval seconds
            time_since_input = time.time() - self.last_user_event_time
            if time_since_input >= self.tick_interval:
                with self._lock:
                    if len(self.system.neurons) >= 2:
                        thought = self.system.idle_step(noise_scale=0.04)
                        if thought:
                            if self.decoder and thought.get("type") == "reflection_insight":
                                thought["decoded_text"] = self.decoder.decode_insight(thought)
                            elif thought.get("type") == "epistemic_resolution":
                                thought["decoded_text"] = thought.get("message", "")
                                
                            self.thought_queue.put(thought)
                            if self.on_thought_callback:
                                try:
                                    self.on_thought_callback(thought)
                                except Exception:
                                    pass
                # Reset clock slightly so we pulse periodically
                self.last_user_event_time = time.time() - (self.tick_interval * 0.5)
