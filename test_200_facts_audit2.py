import os
import shutil
import time
from fella.fella_brain import FellaBrain

def run_200_facts_audit():
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
    
    categories = []
    adjectives = []
    for n in nouns:
        # Assign Category
        if n in ["apple", "fruit", "vegetable", "meat", "bread", "cheese"]: categories.append("food")
        elif n in ["dog", "cat", "bird"]: categories.append("animal")
        elif n in ["tree", "leaf", "branch", "root", "flower", "grass"]: categories.append("plant")
        elif n in ["sun", "moon", "star", "ocean", "river", "mountain", "cloud", "rain", "snow", "wind", "fire", "ice", "sand"]: categories.append("nature")
        elif n in ["car", "ship", "plane", "train"]: categories.append("vehicle")
        elif n in ["milk", "water", "juice", "tea", "coffee"]: categories.append("liquid")
        else: categories.append("object")
        
        # Assign Adjective
        if categories[-1] == "food": adjectives.append("tasty")
        elif categories[-1] == "animal": adjectives.append("alive")
        elif categories[-1] == "plant": adjectives.append("green")
        elif categories[-1] == "nature": adjectives.append("wild")
        elif categories[-1] == "vehicle": adjectives.append("fast")
        elif categories[-1] == "liquid": adjectives.append("wet")
        else: adjectives.append("solid")

    print("==================================================")
    print("INITIALIZING FELLA")
    print("==================================================")
    fella = FellaBrain(dim=16)

    print("\n[EPISTEMIC INIT]")`n    fella.converse("what is apple ?")`n    print("\n[TEACHING PHASE: 200 FACTS]")
    for i, noun in enumerate(nouns):
        # 2 Facts per noun
        cat = categories[i]
        adj = adjectives[i]
        fella.converse(f"{noun} is {cat}")
        fella.converse(f"{noun} is {adj}")

    print("\n==================================================")
    print("TESTING PHASE: 100 QUESTIONS")
    print("==================================================")
    for i, noun in enumerate(nouns):
        q = f"what is {noun} ?"
        fella.converse(q)
        print(f"[USER]: {q} -> [FELLA]: {fella.last_response}")

    print("\n==================================================")
    print("INNER VOICE (HEARTBEAT) PHASE")
    print("==================================================")
    print("[LEAVING FELLA ALONE FOR 12 SECONDS TO RUMINATE...]")
    time.sleep(12) # Wait for heartbeat to trigger

    print("\n==================================================")
    print("FINAL BRAIN STATE METRICS")
    print("==================================================")
    state = fella.wave_engine.get_brain_state()
    print(f"Total Neurons Mapped: {state['total_neurons']}")
    print(f"Hot Spectrons (Curiosity): {state['hot_spectrons']}")
    print(f"Catalysts (Operators): {state['catalysts']}")
    print(f"Mirrors (Identity): {state['mirrors']}")
    
    total_synapses = sum(len(n.synapses) for n in fella.substrate.neurons.values())
    print(f"Total Active Synaptic Edges: {total_synapses}")

if __name__ == "__main__":
    run_200_facts_audit()
