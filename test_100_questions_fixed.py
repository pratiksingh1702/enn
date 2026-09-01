import json
import math
from fella.fella_brain import FellaBrain

def test_questions():
    print("[1] Waking Fella from checkpoint...")
    fella = FellaBrain.load_state("fella_checkpoint.json")
    print("Successfully loaded Fella!")

    # 1.5 Inject Primordial DNA to restore Hot Spectrons that died due to the serialization bug!
    print("[2] Restoring Primordial DNA (Hot Spectrons)...")
    hot_words = ["?", "what", "where", "who", "why", "how"]
    for word in hot_words:
        node = fella.wave_engine._get_or_create_neuron(word)
        node.phase = math.pi
        node.hot_potential = 100.0
        
    fella.save_brain("fella_checkpoint.json")

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

    print("\n[3] Asking 100 Questions")
    for n in nouns:
        q = f"what is {n} ?"
        fella.converse(q)
        print(f"[USER]: {q} -> [FELLA]: {fella.last_response}")

if __name__ == "__main__":
    test_questions()
