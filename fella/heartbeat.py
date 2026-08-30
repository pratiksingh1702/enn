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
                
                # 2. Spontaneous Reactivation (Dreaming)
                neurons = list(self.brain.substrate.neurons.values())
                if len(neurons) > 10:
                    # Inject thermal noise into a random high-mass node
                    candidates = sorted(neurons, key=lambda n: getattr(n, 'mass', 1.0), reverse=True)
                    seed = random.choice(candidates[:5]) # Pick from top 5 massive nodes
                    
                    if seed.id != -1 and len(seed.synapses) > 0:
                        # Spontaneous activation traversal (thinking)
                        # We just let the broca motor cortex traverse it silently to consolidate weights
                        if hasattr(self.brain, 'lang') and hasattr(self.brain.lang, 'broca'):
                            # Add some random thermal noise to the wave
                            _ = self.brain.lang.broca.decode_neural_utterance(
                                seed_id=seed.id,
                                max_words=8,
                                query_text="<thermal_noise_dream>"
                            )
            except Exception as e:
                pass
