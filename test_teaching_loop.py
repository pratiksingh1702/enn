import os
import shutil
import math
from fella.fella_brain import FellaBrain

def run_teaching_loop():
    if os.path.exists('memory_bank'):
        shutil.rmtree('memory_bank')

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
    
    # Map some flavor categories, default to "object"
    categories = []
    for n in nouns:
        if n in ["apple", "fruit", "vegetable"]: categories.append("food")
        elif n in ["dog", "cat", "bird"]: categories.append("animal")
        elif n in ["tree", "leaf", "branch", "root", "flower", "grass"]: categories.append("plant")
        elif n in ["sun", "moon", "star", "ocean", "river", "mountain", "cloud", "rain", "snow", "wind", "fire", "ice", "sand"]: categories.append("nature")
        elif n in ["car", "ship", "plane", "train"]: categories.append("vehicle")
        else: categories.append("object")

    print("==================================================")
    print("INITIALIZING FELLA (PURE TABULA RASA)")
    print("==================================================")
    fella = FellaBrain(dim=16)

    print("\n==================================================")
    print("PHASE 1: THE TEACHING LOOP (100 Questions & Answers)")
    print("==================================================")
    
    for i, noun in enumerate(nouns):
        ans = categories[i]
        
        # 1. Ask the Question (Triggers DESTRUCTIVE Wave Trough)
        q = f"what is {noun} ?"
        fella.converse(q)
        
        # 2. Provide the Answer (Triggers CONSTRUCTIVE Standing Wave)
        a = f"{noun} is {ans}"
        fella.converse(a)
        
        if (i+1) % 20 == 0 or i == 0:
            what_n = fella.wave_engine._get_or_create_neuron("what")
            is_n = fella.wave_engine._get_or_create_neuron("is")
            noun_n = fella.wave_engine._get_or_create_neuron(noun)
            ans_n = fella.wave_engine._get_or_create_neuron(ans)
            
            print(f"\n   [TEACHING CYCLE #{i+1}]")
            print(f"   User: '{q}' -> Fella Response: {fella.dialogue_history[-3]['text']}")
            print(f"   User: '{a}' -> Fella Response: {fella.last_response}")
            print(f"   -> 'what' Phase: {what_n.phase:.2f} rad | Hot Potential: {getattr(what_n, 'hot_potential', 0.0):.1f}")
            print(f"   -> 'is' Catalyst Potential: {getattr(is_n, 'catalyst_potential', 0.0):.1f}")
            print(f"   -> '{noun}' Cold Potential: {getattr(noun_n, 'cold_potential', 0.0):.1f} | Tier Z: {noun_n.tier_z}")
            print(f"   -> '{ans}' Cold Potential: {getattr(ans_n, 'cold_potential', 0.0):.1f} | Tier Z: {ans_n.tier_z}")

    print("\n==================================================")
    print("PHASE 2: FINAL BRAIN STATE & TOPOLOGY")
    print("==================================================")
    state = fella.wave_engine.get_brain_state()
    print(f"Total Neurons Mapped: {state['total_neurons']}")
    print(f"Hot Spectrons (Curiosity): {state['hot_spectrons']}")
    print(f"Catalysts (Operators): {state['catalysts']}")
    print(f"Mirrors (Identity): {state['mirrors']}")
    
    # Let's count how many Tier 3 Cold Masses emerged!
    tier3_count = sum(1 for n in fella.substrate.neurons.values() if n.tier_z >= 3)
    print(f"Tier 3 Grounded Facts: {tier3_count}")

if __name__ == "__main__":
    run_teaching_loop()
