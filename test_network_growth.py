import os
import shutil
from fella.fella_brain import FellaBrain

def run_network_growth():
    if os.path.exists('memory_bank'):
        shutil.rmtree('memory_bank')

    sentences = [
        # Building the Apple network
        "apple is red",
        "apple is fruit",
        "apple is sweet",
        "apple is round",
        "apple is crisp",
        
        # Building the Sun network
        "sun is hot",
        "sun is bright",
        "sun is star",
        "sun is yellow",
        
        # Building the Ocean network
        "ocean is deep",
        "ocean is blue",
        "ocean is water",
        "ocean is cold"
    ]

    print("==================================================")
    print("INITIALIZING FELLA (PURE TABULA RASA)")
    print("==================================================")
    fella = FellaBrain(dim=16)

    print("\n==================================================")
    print("PHASE 1: GRAPH CONSTRUCTION (No Questions Asked)")
    print("==================================================")
    
    for s in sentences:
        print(f"\n[USER]: {s}")
        fella.converse(s)
        
    print("\n==================================================")
    print("PHASE 2: NETWORK TOPOLOGY ANALYSIS")
    print("==================================================")
    
    # Analyze Apple
    apple_n = fella.wave_engine._get_or_create_neuron("apple")
    print(f"\n[NODE]: 'apple'")
    print(f"  Cold Potential (Mass): {getattr(apple_n, 'cold_potential', 0.0):.1f}")
    print(f"  Synaptic Connections out of 'apple':")
    for target_id, weight in apple_n.synapses.items():
        target_word = fella.substrate.neurons[target_id].text
        print(f"    -> {target_word} (Weight: {weight:.1f})")

    # Analyze Is
    is_n = fella.wave_engine._get_or_create_neuron("is")
    print(f"\n[NODE]: 'is'")
    print(f"  Catalyst Potential (Operator): {getattr(is_n, 'catalyst_potential', 0.0):.1f}")
    print(f"  Synaptic Connections out of 'is':")
    for target_id, weight in is_n.synapses.items():
        target_word = fella.substrate.neurons[target_id].text
        print(f"    -> {target_word} (Weight: {weight:.1f})")

    # Final Brain State
    print("\n==================================================")
    print("PHASE 3: FINAL BRAIN STATE")
    print("==================================================")
    state = fella.wave_engine.get_brain_state()
    print(f"Total Neurons Mapped: {state['total_neurons']}")
    print(f"Hot Spectrons (Curiosity): {state['hot_spectrons']}")
    print(f"Catalysts (Operators): {state['catalysts']}")
    print(f"Mirrors (Identity): {state['mirrors']}")

if __name__ == "__main__":
    run_network_growth()
