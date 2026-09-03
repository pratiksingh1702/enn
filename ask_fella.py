import json
import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold
from fella.causal_cortex import CausalCortex

def test_and_ask():
    print("==================================================")
    print("TESTING FELLA: WHAT DID SHE LEARN?")
    print("==================================================")
    
    # 1. Load Live Sensory Memory
    live_file = "fella_live_memory.json"
    brain = FellaBrain(dim=256)
    brain.load_state(live_file)
    frontier = FrontierManifold(brain)
    
    print(f"[STATUS] Loaded {len(brain.neurons)} neurons and {brain.z_counter} memories from live session.")
    
    # 2. Test Causal Prediction: What does the audio predict?
    print("\n--- [TEST 1: SENSORY CAUSAL RECALL] ---")
    print("Question to Fella: When you hear the show's audio [A_6563], what visual scenes do you recall?")
    
    audio_neuron = brain.neurons.get("[A_6563]")
    if audio_neuron:
        # Find which visual events co-occurred or are most tightly bound to this audio
        connected_z = audio_neuron.z_events
        print(f" -> Audio Anchor is gravitationally bound to {len(connected_z)} episodic memories.")
        
        # Calculate which visual coordinates resonate highest with the audio wave
        saccade_neurons = [n for k, n in brain.neurons.items() if k.startswith("[FOCUS_")]
        resonances = []
        for sn in saccade_neurons:
            # Gravitational resonance (dot product)
            dot = np.dot(audio_neuron.x_wave, sn.x_wave)
            resonances.append((sn.text, dot))
            
        resonances.sort(key=lambda x: x[1], reverse=True)
        print(f"\nTop 5 Visual Scenes Most Gravitationally Bound to the Show's Audio:")
        for name, res in resonances[:5]:
            print(f" * Scene {name} | Resonance: {res:.4f}")

    # 3. Test Environmental Entropy (Curiosity)
    print("\n--- [TEST 2: WHAT SHOCKED HER ATTENTION?] ---")
    print("Question to Fella: Where were the strongest spikes of visual change on the screen?")
    
    # Group coordinates and find clusters
    coords = {}
    for k in brain.neurons.keys():
        if k.startswith("[FOCUS_"):
            parts = k.replace("[FOCUS_", "").replace("]", "").split("_")
            x, y = int(parts[0]), int(parts[1])
            # Grid into 200x200 blocks
            grid_key = f"Region ({x//300 * 300}, {y//200 * 200})"
            coords[grid_key] = coords.get(grid_key, 0) + 1
            
    sorted_regions = sorted(coords.items(), key=lambda x: x[1], reverse=True)
    for region, count in sorted_regions[:5]:
        print(f" * {region}: {count} curiosity focus events (Hotspot)")

    # 4. Ask Language Formulation
    print("\n--- [TEST 3: COGNITIVE REFLECTION] ---")
    print("Checking internal thermodynamic oscillator and epistemic tension...")
    unstable = sorted(brain.neurons.values(), key=lambda n: len(n.z_events))
    most_isolated = [n.text for n in unstable[:5]]
    print(f" -> Concepts with highest unresolved curiosity (isolated in topology):")
    print(f"    {most_isolated}")
    print(f"\n -> Total Episodic Timeline Depth: {brain.z_counter} continuous moments.")
    print("==================================================")

if __name__ == '__main__':
    test_and_ask()
