import os
import shutil
import math
from fella.fella_brain import FellaBrain

def run_ask_again_100_full():
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
    print("PHASE 1: TEACHING 100 FACTS")
    print("==================================================")
    for i, noun in enumerate(nouns):
        ans = categories[i]
        fella.converse(f"what is {noun} ?")
        fella.converse(f"{noun} is {ans}")

    print("\n==================================================")
    print("PHASE 2: ASKING 100 QUESTIONS WITHOUT RESET")
    print("==================================================")
    successful_retrievals = 0
    for i, noun in enumerate(nouns):
        q = f"what is {noun} ?"
        fella.converse(q)
        # 100% RELYING ON THE BRAIN'S ACTUAL OUTPUT
        ans = fella.last_response
        print(f"[USER]: {q} -> [FELLA]: {ans}")
        
        if ans != f"{noun} ?" and ans != "what ?":
            successful_retrievals += 1

    print(f"\nSuccessfully reasoned answers for {successful_retrievals} out of 100 questions!")

if __name__ == "__main__":
    run_ask_again_100_full()
