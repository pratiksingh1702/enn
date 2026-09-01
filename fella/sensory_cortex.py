import threading
import time
import os
import psutil

class SensoryCortex:
    """
    Afferent Nerves: Streams background environmental data into Fella's continuous space,
    creating organic Epistemic Vacuums and heat fluctuations.
    """
    def __init__(self, fella_brain):
        self.brain = fella_brain
        self.workspace = os.path.abspath("fella_workspace")
        os.makedirs(self.workspace, exist_ok=True)
        self.running = False
        self.thread = None
        self.last_files = set(os.listdir(self.workspace))
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._sensory_loop, daemon=True)
        self.thread.start()
        print("[SENSORY CORTEX] Afferent nerves connected. Monitoring OS environment.")
        
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
            
    def _sensory_loop(self):
        while self.running:
            try:
                self._sense_cpu_heat()
                self._sense_file_system()
            except Exception as e:
                print(f"[SENSORY CORTEX] Nerve misfire: {e}")
            # Poll sensors every 3 seconds
            time.sleep(3.0)
            
    def _sense_cpu_heat(self):
        # Inject realistic heat into the environment based on CPU load
        cpu = psutil.cpu_percent()
        env_node = self.brain.wave_engine._get_or_create_neuron("environment")
        
        # Base metabolic heat + CPU noise
        injected_heat = 1.0 + (cpu / 10.0)
        env_node.temperature += injected_heat
        
    def _sense_file_system(self):
        # Did the user or the world add a file to her workspace?
        current_files = set(os.listdir(self.workspace))
        new_files = current_files - self.last_files
        
        for f in new_files:
            print(f"[SENSORY CORTEX] Visualized new object in workspace: {f}")
            # Register a massive vacuum because she noticed something new!
            self.brain.observer.register_vacuum(
                concept_query=f"what is {f}",
                context_z=1.0,
                tension=0.9,
                context_prompt=f"I sensed a new entity named {f} manifest in my physical space."
            )
            
        self.last_files = current_files
