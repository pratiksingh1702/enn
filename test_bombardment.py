from fella.fella_brain import FellaBrain
import math

def run_bombardment():
    nouns = [
        "apple", "tree", "car", "dog", "cat", "bird", "sun", "moon", "star", "rock",
        "ocean", "river", "mountain", "cloud", "rain", "snow", "wind", "fire", "ice", "sand",
        "book", "chair", "table", "door", "window", "house", "city", "road", "bridge", "ship",
        "plane", "train", "wheel", "engine", "metal", "wood", "glass", "paper", "pen", "clock",
        "shoe", "shirt", "hat", "glove", "ring", "coin", "key", "lock", "box", "bag",
        "computer", "phone", "bottle", "keyboard", "mouse", "screen", "wire", "cable", "lamp", "desk",
        "wall", "floor", "ceiling", "roof", "brick", "stone", "dirt", "grass", "leaf", "branch",
        "root", "flower", "seed", "fruit", "vegetable", "meat", "bread", "cheese", "milk", "water",
        "juice", "tea", "coffee", "sugar", "salt", "pepper", "plate", "bowl", "cup", "fork",
        "knife", "spoon", "napkin", "towel", "soap", "brush", "comb", "mirror", "sink", "tub"
    ]

    print("==================================================")
    print("INITIALIZING FELLA (PURE TABULA RASA)")
    print("==================================================")
    import os, shutil
    if os.path.exists('memory_bank'): shutil.rmtree('memory_bank')
    fella = FellaBrain(dim=16)

    print("\n==================================================")
    print("PHASE 1: THE BOMBARDMENT (100 Epistemic Vacuums)")
    print("==================================================")
    for i, noun in enumerate(nouns):
        print(f"\n[USER]: what is {noun} ?")
        
        # Bypass stdout clutter for the loop by just calling it
        fella.converse(f"what is {noun} ?")
        
        print(f"[FELLA'S PHYSICAL RESPONSE]: {fella.last_response}")
        print(f"[FELLA'S INNER THOUGHT]: {fella.last_thought}")
        
        # Check Spectron Evolution
        what_n = fella.wave_engine._get_or_create_neuron("what")
        is_n = fella.wave_engine._get_or_create_neuron("is")
        
        if (i+1) % 10 == 0 or i == 0:
            print(f"   [EVOLUTION CHECK #{i+1}]")
            print(f"   -> 'what' node Phase: {what_n.phase:.2f} rad (Target is {math.pi:.2f}) | Hot Potential: {getattr(what_n, 'hot_potential', 0.0):.1f}")
            print(f"   -> 'is' node Catalyst Potential: {getattr(is_n, 'catalyst_potential', 0.0):.1f}")

    print("\n==================================================")
    print("PHASE 2: THE INNER VOICE (Silence & Rumination)")
    print("==================================================")
    print("User stops talking. FELLA is left alone with 100 unresolved vacuums.")
    print("Her Inner Voice automatically kicks in, ruminating on the most recent voids...\n")
    
    recent = [f"what is {n} ?" for n in nouns[-5:]]
    fella.wave_engine.run_inner_voice_rumination(recent)
    
    what_n = fella.wave_engine._get_or_create_neuron("what")
    print(f"\n   [POST-RUMINATION EVOLUTION CHECK]")
    print(f"   -> 'what' node Phase: {what_n.phase:.2f} rad | Hot Potential: {getattr(what_n, 'hot_potential', 0.0):.1f}")

    print("\n==================================================")
    print("PHASE 3: FINAL BRAIN STATE")
    print("==================================================")
    state = fella.wave_engine.get_brain_state()
    print(f"Total Neurons Mapped: {state['total_neurons']}")
    print(f"Hot Spectrons (Curiosity): {state['hot_spectrons']}")
    print(f"Catalysts (Operators): {state['catalysts']}")
    print(f"Mirrors (Identity): {state['mirrors']}")

if __name__ == "__main__":
    run_bombardment()
