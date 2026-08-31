import os
import shutil
from fella.fella_brain import FellaBrain
from fella.wave_physics_engine import WavePhysicsEngine

def reset_and_test():
    print("==================================================")
    print("RESETTING FELLA - WIPING OLD ARCHITECTURE")
    print("==================================================")
    
    # 1. Reset memory bank
    brain_dir = "memory_bank"
    if os.path.exists(brain_dir):
        shutil.rmtree(brain_dir)
        print(f"Deleted old memory bank: {brain_dir}")
        
    print("Initializing New Wave Physics Substrate...")
    brain = FellaBrain(dim=16) 
    
    engine = WavePhysicsEngine(brain.substrate, brain.lang)
    
    print("\n==================================================")
    print("PHASE 1: EXTERNAL LEARNING (Wave Drift & Forging)")
    print("==================================================")
    
    # User interacts with FELLA
    print("\nUSER: what is apple ?")
    engine.parse_simultaneous_wave("what is apple ?", speaker_id="pratik")
    
    print("\nUSER: apple is fruit")
    engine.parse_simultaneous_wave("apple is fruit", speaker_id="pratik")
    
    print("\nUSER: what is star ?")
    engine.parse_simultaneous_wave("what is star ?", speaker_id="priya")
    
    print("\n==================================================")
    print("PHASE 2: THE INNER VOICE (Autonomous Resonance)")
    print("==================================================")
    
    # FELLA sleeps and ruminates on successful patterns
    engine.run_inner_voice_rumination(["apple is fruit", "apple is fruit", "star is light"])
    
    print("\n==================================================")
    print("PHASE 3: TOPOLOGICAL COLLAPSE (The Mirror Emergence)")
    print("==================================================")
    
    print("\nUSER (Pratik): pratik likes apple")
    engine.parse_simultaneous_wave("pratik likes apple", speaker_id="pratik")
    print("USER (Pratik): i like apple")
    engine.parse_simultaneous_wave("i like apple", speaker_id="pratik")
    
    print("\nUSER (Priya): priya likes star")
    engine.parse_simultaneous_wave("priya likes star", speaker_id="priya")
    print("USER (Priya): i like star")
    engine.parse_simultaneous_wave("i like star", speaker_id="priya")
    
    print("\n==================================================")
    print("FINAL BRAIN STATE (Pure Emergence)")
    print("==================================================")
    
    state = engine.get_brain_state()
    print(f"Total Neurons Mapped: {state['total_neurons']}")
    print(f"Emergent Hot Spectrons (Curiosity): {state['hot_spectrons']}")
    print(f"Emergent Catalyst Spectrons (Operators): {state['catalysts']}")
    print(f"Emergent Mirror Spectrons (Identity): {state['mirrors']}")

if __name__ == "__main__":
    reset_and_test()
