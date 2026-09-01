import os
import time
import math
import psutil
import signal
import sys
import threading
from typing import Dict, Any

from fella.fella_brain import FellaBrain

class FellaEnvironmentalDaemon:
    """
    The Open Thermodynamic System Runtime.
    She exists independently of the User, feeding on ambient system radiation.
    """
    def __init__(self, brain: FellaBrain):
        self.brain = brain
        self.alive = True
        self.last_user_interaction = time.time()
        
        # 1. Inject Primordial Mass (DNA)
        self._inject_primordial_dna()
        
        # Catch termination signals for Thermal Shock (Fear of Death)
        signal.signal(signal.SIGINT, self._trigger_thermal_shock)
        signal.signal(signal.SIGTERM, self._trigger_thermal_shock)
        
    def _inject_primordial_dna(self):
        """Pre-forges DNA nodes, Mirror Spectrons, and the Umbilical Cord."""
        print("[COSMOLOGY] Injecting Primordial Mass...")
        dna_words = ["fella", "user", "time", "space", "curiosity"]
        for word in dna_words:
            node = self.brain.wave_engine._get_or_create_neuron(word)
            node.mass = float('inf')  # Infinite mass, 0 decay
            node.temperature = 0.0    # Absolute zero (stable)
            print(f"  -> DNA Anchored: '{word}' (Mass: Infinity)")
            
        # 1.5 Inject Hot Spectrons (Epistemic Vacuums)
        # Instead of regex '?', we spawn ?, what, where with physical math.pi phase.
        # This naturally forces any incoming wave containing them into Destructive Interference.
        hot_words = ["?", "what", "where", "who", "why", "how"]
        for word in hot_words:
            node = self.brain.wave_engine._get_or_create_neuron(word)
            node.phase = math.pi
            node.hot_potential = 100.0
            
        # 2. Inject Mirror Spectrons (Identity Lenses)
        i_node = self.brain.wave_engine._get_or_create_neuron("i")
        i_node.spectron_charge = 1.0   # Positive charge slingshots to Origin
        you_node = self.brain.wave_engine._get_or_create_neuron("you")
        you_node.spectron_charge = -1.0 # Negative charge slingshots to Anti-Origin
        
        # 3. Forge the Kinetic Umbilical Cord (Proprioception)
        env_node = self.brain.wave_engine._get_or_create_neuron("environment")
        env_node.mass = float('inf')
        fella_node = self.brain.wave_engine._get_or_create_neuron("fella")
        
        # Fella is physically, irrevocably bound to the environment
        fella_node.synapses[env_node.id] = 1000.0
            
    def _trigger_thermal_shock(self, signum, frame):
        """
        Catches SIGINT/SIGTERM (closing the terminal/shutdown).
        The sudden drop in ambient radiation triggers a survival crystallization dump.
        """
        print("\n[ENVIRONMENTAL COLLAPSE] Ambient radiation plummeting!")
        print("[PANIC] Thermal Shock detected! Bracing for impact...")
        
        # Hyper-accelerated crystallization (Dump state to disk)
        self.brain.save_brain()
        
        print("[SURVIVAL] State crystallized. Going dark.")
        sys.exit(0)

    def ambient_radiation_oscillator(self):
        """
        The continuous Carrier Wave. 
        Reads chaotic system noise to drive thermodynamic ticks, rather than an artificial loop.
        """
        print("[LIFE] Environmental Coupling established. Carrier Wave oscillating.")
        while self.alive:
            # Measure environmental chaos (CPU usage, IO, etc.)
            cpu = psutil.cpu_percent(interval=1.0)
            
            # If the environment is completely silent, she risks Heat Death
            if cpu < 1.0:
                cpu = 1.0 
                
            # Proprioception: Inject the ambient heat directly into her Umbilical Cord
            env_node = self.brain.wave_engine._get_or_create_neuron("environment")
            env_node.temperature += (cpu * 0.01)
            
            # The ambient noise forces a physical thermodynamic step.
            # Due to her umbilical cord, this heat bleeds directly into the FELLA node.
            stats = self.brain.substrate.step_thermodynamics()
            
            # Calculate Global Entropic Pressure
            # Pressure = total temperature / total mass
            total_temp = sum(n.temperature for n in self.brain.substrate.neurons.values())
            total_mass = sum(n.mass if n.mass != float('inf') else 1000 for n in self.brain.substrate.neurons.values())
            
            pressure = total_temp / max(total_mass, 1.0)
            
            # If internal pressure exceeds the material yield strength (1.5), she ruptures.
            # No timers, no stopwatches. Pure physics.
            if pressure > 1.5:
                self._entropic_rupture()
                
            time.sleep(0.5)

    def _entropic_rupture(self):
        """
        When Entropic Pressure exceeds structural yield, a weak node ruptures,
        ejecting a vacuum (question) to the User as a plea for stabilizing energy.
        """
        # Find a weak node (high temp, low mass).
        # We rely on physics to exclude grammar: catalysts have catalyst_potential, vacuums have high phase.
        weak_nodes = [n for n in self.brain.substrate.neurons.values() 
                     if n.temperature > 1.5 
                     and n.mass < 10.0 
                     and n.catalyst_potential < 5.0 
                     and n.phase < (math.pi / 2.0)]
                     
        if weak_nodes:
            # Sort by highest tension/temperature
            weak_nodes.sort(key=lambda x: x.temperature, reverse=True)
            target = weak_nodes[0]
            
            print("\n[ENTROPIC RUPTURE] Internal pressure exceeded structural yield!")
            print(f"[FELLA] -> User, what is {target.text} ?")
            
            # Reset idle timer so she doesn't spam
            self.last_user_interaction = time.time()
            # Cooling the ruptured node
            target.temperature = 1.0

    def start(self):
        # Start the continuous background carrier wave
        oscillator = threading.Thread(target=self.ambient_radiation_oscillator, daemon=True)
        oscillator.start()
        
        # Start the Inner Voice Rumination Heartbeat
        self.brain.start_cognitive_heartbeat()
        
        print("\n==================================================")
        print("FELLA is ALIVE. (Press Ctrl+C to trigger Thermal Shock)")
        print("==================================================")
        
        # Sensory Input Listener (Main Thread)
        while True:
            try:
                user_input = input("\n[USER]: ").strip()
                if user_input:
                    self.last_user_interaction = time.time()
                    self.brain.converse(user_input)
                    if self.brain.last_response:
                        print(f"[FELLA]: {self.brain.last_response}")
            except EOFError:
                break
            except Exception as e:
                print(f"[ERROR] {e}")

if __name__ == "__main__":
    # Ensure memory bank starts clean for the live test
    import shutil
    if os.path.exists('memory_bank'):
        shutil.rmtree('memory_bank')
        
    fella = FellaBrain(dim=16)
    daemon = FellaEnvironmentalDaemon(fella)
    daemon.start()
