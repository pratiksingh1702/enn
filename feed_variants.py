import json
import sys
from fella.fella_brain import FellaBrain

try:
    print("[1] Waking Fella from checkpoint...")
    fella = FellaBrain.load_state("fella_checkpoint.json")
    print("Successfully loaded Fella!")
except Exception as e:
    print("Failed to load fella_checkpoint.json. Initiating new FellaBrain.")
    fella = FellaBrain(dim=16)

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

# Generate some quick variants
print("\n[2] Direct Brain Feed (Variant Injection)")
variants_taught = 0
for n in nouns:
    if n == "apple": variant = "round"
    elif n == "tub": variant = "plastic"
    elif n in ["dog", "cat"]: variant = "furry"
    elif n in ["ocean", "river", "water"]: variant = "fluid"
    elif n in ["sun", "fire"]: variant = "burning"
    elif n in ["rock", "stone", "brick"]: variant = "hard"
    elif n in ["car", "train", "plane"]: variant = "noisy"
    else: variant = "complex"
    
    fact = f"{n} is {variant}"
    fella.converse(fact)
    variants_taught += 1
    if variants_taught % 20 == 0:
        print(f"  ... Injected {variants_taught} variant facts...")

print(f"\n[3] Feed Complete. Taught {variants_taught} variant facts.")

# Print some topological stats
print("\n[4] Network Topology Analysis")
apple_n = fella.wave_engine._get_or_create_neuron("apple")
print(f"\n[NODE]: 'apple' (Mass: {getattr(apple_n, 'mass', 0.0):.1f})")
print("  Synaptic Connections:")
for target_id, weight in apple_n.synapses.items():
    target_word = fella.substrate.neurons[target_id].text
    print(f"    -> {target_word} (Gravity: {weight:.2f})")
    
tub_n = fella.wave_engine._get_or_create_neuron("tub")
print(f"\n[NODE]: 'tub' (Mass: {getattr(tub_n, 'mass', 0.0):.1f})")
print("  Synaptic Connections:")
for target_id, weight in tub_n.synapses.items():
    target_word = fella.substrate.neurons[target_id].text
    print(f"    -> {target_word} (Gravity: {weight:.2f})")

# Save
fella.save_brain("fella_checkpoint.json")
print("\n[5] Crystalized new structure back to fella_checkpoint.json.")
