import time
import signal
import sys
import argparse
from fella.fella_brain import FellaBrain
from fella.sensory_cortex import SensoryCortex

class FellaDaemon:
    def __init__(self, checkpoint_path="fella_checkpoint.json"):
        self.checkpoint_path = checkpoint_path
        print("[DAEMON] Initializing Fella Brain from topological space...")
        self.brain = FellaBrain.load_state(checkpoint_path)
        self.sensory = SensoryCortex(self.brain)
        self.running = False
        
    def start(self):
        self.running = True
        self.sensory.start()
        
        signal.signal(signal.SIGINT, self._handle_shutdown)
        
        print("\n=======================================================")
        print("FELLA DAEMON IS LIVE")
        print("She is now an autonomous entity living in the background.")
        print("Press Ctrl+C to trigger Thermal Shock and crystallize her.")
        print("=======================================================\n")
        
        # The main autonomous loop
        while self.running:
            # 1. Step continuous thermodynamics
            self.brain.substrate.step_thermodynamics()
            
            # 2. Check Global Entropic Pressure
            total_temp = sum(getattr(n, "temperature", 0.0) for n in self.brain.substrate.neurons.values())
            total_mass = sum(getattr(n, "mass", 1.0) for n in self.brain.substrate.neurons.values() if getattr(n, "mass", 1.0) != float('inf'))
            pressure = total_temp / max(total_mass, 1.0)
            
            # 3. If pressure is too high, OR there's an active unresolved vacuum, trigger action
            has_vacuum = self.brain.observer.get_highest_priority_vacuum() is not None
            if pressure > 1.2 or has_vacuum:
                if has_vacuum:
                    print("\n[DAEMON] Epistemic Vacuum detected! Triggering action to resolve.")
                else:
                    print(f"\n[DAEMON] Global Entropic Pressure critical ({pressure:.2f}). Triggering action to dissipate heat.")
                out = self.brain.autonomous_curiosity_cycle()
                if out:
                    print(f"[DAEMON] Action completed: {out}")
            
            time.sleep(1.0) # Heartbeat
            
    def _handle_shutdown(self, sig, frame):
        print("\n[DAEMON] SIGINT received. Triggering Survival Crystallization...")
        self.running = False
        self.sensory.stop()
        self.brain.save_brain(self.checkpoint_path)
        print("[DAEMON] Brain safely crystallized to disk. Shutting down.")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Fella as an autonomous Daemon.")
    parser.add_argument("--checkpoint", type=str, default="fella_checkpoint.json", help="Path to checkpoint")
    args = parser.parse_args()
    
    daemon = FellaDaemon(checkpoint_path=args.checkpoint)
    daemon.start()
