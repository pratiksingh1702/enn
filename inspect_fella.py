import os
import json
import numpy as np
from fella.fella_brain import FellaBrain

def inspect_memory():
    print("==================================================")
    print("FELLA NEURAL ARCHITECTURE & MEMORY STATUS")
    print("==================================================")
    
    live_file = "fella_live_memory.json"
    master_file = "fella_checkpoint.json"
    
    # 1. Inspect Live Sensory Memory (Vision + Audio + Causal)
    print("\n--- [1] LIVE SENSORY MEMORY (run_live.py) ---")
    if os.path.exists(live_file):
        brain = FellaBrain(dim=256)
        brain.load_state(live_file)
        
        print(f"Status: ACTIVE / SAVED")
        print(f"Total Neurons in Matrix: {len(brain.neurons)}")
        print(f"Total Z-Events (Episodic Memories): {brain.z_counter}")
        print(f"Wave Matrix Shape: {brain.wave_matrix.shape}")
        
        visual_neurons = [k for k in brain.neurons.keys() if "FOCUS_" in k]
        audio_neurons = [k for k in brain.neurons.keys() if "temp_live" in k or "[A_" in k]
        cognitive_neurons = [k for k in brain.neurons.keys() if k not in visual_neurons and k not in audio_neurons]
        
        print(f"\nSensory Substrate:")
        print(f"  * Visual Saccade Coordinates: {len(visual_neurons)}")
        print(f"  * Acoustic Audio Snapshots:   {len(audio_neurons)}")
        print(f"  * Cognitive/Symbolic Vectors:  {len(cognitive_neurons)}")
        
        sorted_by_gravity = sorted(brain.neurons.values(), key=lambda n: len(n.z_events), reverse=True)
        print(f"\nTop 10 Gravitational Anchors (Most Reinforced Concepts):")
        for n in sorted_by_gravity[:10]:
            print(f"  - '{n.text}' | Bound to {len(n.z_events)} Z-events | Last accessed: Tick {n.last_accessed}")
    else:
        print(f"Status: No live session file found yet ({live_file}).")
        print("  * Run 'python run_live.py' to stream live YouTube video and audio into her senses.")

    # 2. Inspect Master Topological Substrate (fella_checkpoint.json)
    print("\n--- [2] MASTER TOPOLOGICAL SUBSTRATE (fella_checkpoint.json) ---")
    if os.path.exists(master_file):
        with open(master_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print(f"Entity Name:     {data.get('name', 'FELLA')}")
        print(f"Maturity Steps:  {data.get('age_steps', 'N/A')}")
        
        sub = data.get("substrate", {})
        neurons = sub.get("neurons", [])
        print(f"Total Substrate Neurons: {len(neurons)}")
        
        tf = data.get("trait_field", {})
        if tf:
            print(f"Active Trait:    {tf.get('active_trait')}")
            print(f"Trait Energies:")
            for trait, energy in tf.get("trait_energy", {}).items():
                bar = "#" * int(energy * 10)
                print(f"  - {trait:<14}: {energy:.4f} {bar}")
                
        # Sample vocabulary
        labels = [n.get('label') or n.get('text') for n in neurons if n.get('label') or n.get('text')]
        print(f"\nCore Language Sample ({len(labels)} total vocabulary):")
        print("  " + ", ".join(labels[:25]) + " ...")
    else:
        print(f"Master checkpoint '{master_file}' not found.")
        
    print("\n==================================================")

if __name__ == '__main__':
    inspect_memory()
