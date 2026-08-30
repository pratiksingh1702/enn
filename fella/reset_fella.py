"""
FELLA Brain Reset Script: Total Memory Cleanse
==============================================
Resets FELLA to a pristine, unlearned state:
- Deletes fella_checkpoint.json
- Initializes a blank 4D StackedSubstrate with only base alphabet (Z=0) and Self/Uncertainty anchors (Z=4)
- Empties all associative memory bank records
- Saves fresh unlearned state back to fella_checkpoint.json
"""

import os
import sys
from fella.fella_brain import FellaBrain

def reset_fella_memory():
    checkpoint_path = "fella_checkpoint.json"
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)
        print(f"[RESET] Deleted existing checkpoint '{checkpoint_path}'")
        
    print("[RESET] Initializing clean, unlearned FELLA brain substrate...")
    brain = FellaBrain(dim=16)
    
    # Ensure memory bank is completely clear
    brain.lang.memory_bank = []
    
    # Save pristine blank state
    brain.save_state(checkpoint_path)
    print(f"[SAVE] Preserved fresh unlearned state in '{checkpoint_path}'")
    
    # Summary report
    n_count = len(brain.substrate.neurons)
    syn_count = sum(len(n.synapses) for n in brain.substrate.neurons.values())
    mem_count = len(brain.lang.memory_bank)
    
    print("\n" + "=" * 60)
    print("FELLA MEMORY RESET COMPLETE")
    print("=" * 60)
    print(f"  • Substrate Neurons : {n_count} (Base Alphabet & Anchors only)")
    print(f"  • Synaptic Bridges  : {syn_count}")
    print(f"  • Associative Memory: {mem_count} (Blank Memory Bank)")
    print("=" * 60)

if __name__ == "__main__":
    reset_fella_memory()
