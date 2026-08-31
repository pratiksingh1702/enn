import threading
import time
import random
from typing import Any
import numpy as np

class CognitiveHeartbeat:
    """
    The Autonomous Default Mode Network (DMN).
    Injects thermal noise (dreams) and applies synaptic decay (forgetting)
    to transform the network from a passive graph into a living dynamical system.
    """
    def __init__(self, brain: Any, pulse_interval: float = 10.0):
        self.brain = brain
        self.pulse_interval = pulse_interval
        self.is_alive = False
        self._thread = None
        
    def start(self):
        if self.is_alive:
            return
        self.is_alive = True
        self._thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._thread.start()
        print(f"[HEARTBEAT] Autonomous Cognitive Loop started (Pulse={self.pulse_interval}s)")
        
    def stop(self):
        self.is_alive = False
        if self._thread:
            self._thread.join(timeout=2.0)
            print("[HEARTBEAT] Autonomous Cognitive Loop stopped.")
            
    def _heartbeat_loop(self):
        while self.is_alive:
            time.sleep(self.pulse_interval)
            
            try:
                # 1. True Learner: Synaptic Homeostasis (Forgetting)
                if hasattr(self.brain.substrate, 'apply_synaptic_decay'):
                    self.brain.substrate.apply_synaptic_decay(decay_rate=0.005)
                
                # 2. Spontaneous Reactivation (The Inner Voice / Rumination)
                # Instead of just traversing, the Inner Voice re-injects the semantic wave 
                # to run the Wave-Hebbian Integral and Phase Drift without external input.
                if hasattr(self.brain, 'wave_engine') and hasattr(self.brain, 'dialogue_history'):
                    # The inner voice ruminates on recent sensory experiences (short-term memory consolidation)
                    history = self.brain.dialogue_history
                    if history:
                        # Pick a random recent interaction to ruminate on
                        memory_event = random.choice(history[-10:])
                        memory_text = memory_event.get("text", "")
                        speaker = memory_event.get("speaker", "fella")
                        
                        if memory_text and len(memory_text.split()) > 1:
                            print(f"[INNER VOICE] Ruminating on memory: '{memory_text}'")
                            self.brain.wave_engine.parse_simultaneous_wave(memory_text, speaker_id=speaker)
            except Exception as e:
                pass
