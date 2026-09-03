import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def test_physics_engine():
    print("=========================================")
    print("ENN DUAL-PROCESS ENGINE: ADVANCED PHYSICS")
    print("=========================================")
    brain = FellaBrain(dim=128)
    frontier = FrontierManifold(brain)

    print("\\n--- FIX 4: GEOMETRIC DRIFT (TABULA RASA) ---")
    brain.record_event(["apple", "is", "fruit"])
    brain.record_event(["apple", "is", "red"])
    brain.record_event(["car", "is", "fast"])
    brain.record_event(["sky", "is", "blue"])
    brain.record_event(["sun", "is", "hot"])
    brain.record_event(["water", "is", "wet"])

    # Show the drift
    sim_apple_fruit = np.dot(brain.neurons["apple"].x_wave, brain.neurons["fruit"].x_wave)
    sim_apple_car = np.dot(brain.neurons["apple"].x_wave, brain.neurons["car"].x_wave)
    print(f"Similarity (apple, fruit) [Attracted via Z-event]: {sim_apple_fruit:.3f}")
    print(f"Similarity (apple, car) [Repelled via Dark Energy]: {sim_apple_car:.3f}")

    print("\\n--- FIX 1: ELASTIC SPRING TENSION (Dynamic Convolution) ---")
    q1 = brain.record_event(["what", "is", "apple"])
    q2 = brain.record_event(["what", "is", "car"])
    q3 = brain.record_event(["what", "is", "sky"])
    frontier.form_spectron([q1, q2, q3])
    
    # We ask a STRETCHED question!
    print("\\nAsking dynamically stretched question...")
    y, target, retrieved = frontier.formulate_thought("what exactly in the world is apple")
    
    print("\\n--- FIX 2: CONSERVATION OF ENERGY (Multi-Hop) ---")
    # Let's add a second hop! 
    brain.record_event(["fruit", "is", "food"])
    brain.record_event(["food", "is", "good"])
    # If energy splits correctly, it will retrieve 'food' but heavily dilute 'is'
    y, target, retrieved = frontier.formulate_thought("what is apple")

    print("\\n--- FIX 3: PHASE SHIFTING (Syntactic Locking) ---")
    # The grammar correction
    frontier.process_correction(target, retrieved, "apple is a red tasty fruit food")
    
    # Now ask for a different target with multiple components
    brain.record_event(["banana", "is", "yellow"])
    brain.record_event(["banana", "is", "fruit"])
    
    print("\\nGenerating output for banana based on the phase-locked template...")
    frontier.formulate_thought("what is banana")
    
if __name__ == '__main__':
    test_physics_engine()
