import time
import os
import random
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_spectron_curriculum():
    print("==================================================")
    print("SPECTRON MANIFOLD: 2000-SENTENCE FOUNDATION LEARNING")
    print("==================================================")
    
    # Ensure fresh brain by deleting checkpoint
    checkpoint = "universe_master_checkpoint.json"
    if os.path.exists(checkpoint):
        os.remove(checkpoint)
        print("[VOID] Master checkpoint wiped. Neural substrate is blank.")
        
    # Increase dimension to 64 for high-resolution Fourier waves (preventing 'water' and 'fire' from colliding)
    brain = FellaBrain(dim=64)
    
    # Procedurally generate 2000 simple, child-like observational sentences
    nouns_animals = ["dog", "cat", "bird", "fish", "horse", "fella", "user"]
    nouns_objects = ["apple", "tree", "house", "river", "sky", "ground", "sun", "moon", "rock"]
    adjectives = ["fast", "slow", "big", "small", "hot", "cold", "red", "blue", "bright", "dark", "happy", "sad"]
    verbs_action = ["runs", "walks", "flies", "swims", "jumps", "falls", "flows", "looks", "eats"]
    verbs_state = ["is", "feels", "seems"]
    prepositions = ["to", "from", "on", "in", "under", "above"]
    
    sentences = []
    
    # 1. Action paths (The [adj] [animal] [verb] [prep] the [object])
    for _ in range(800):
        s = f"the {random.choice(adjectives)} {random.choice(nouns_animals)} {random.choice(verbs_action)} {random.choice(prepositions)} the {random.choice(nouns_objects)}"
        sentences.append(s)
        
    # 2. Physical states ([object] [verb_state] [adj])
    for _ in range(600):
        s = f"the {random.choice(nouns_objects)} {random.choice(verbs_state)} {random.choice(adjectives)}"
        sentences.append(s)
        
    # 3. Consumption & basic events
    for _ in range(600):
        s = f"a {random.choice(nouns_animals)} {random.choice(verbs_action)} a {random.choice(nouns_objects)}"
        sentences.append(s)
        
    random.shuffle(sentences)
    
    print(f"\n[SPECTRON EMISSION] Streaming {len(sentences)} observational wave-forms into the Frontier Layer...")
    start = time.time()
    
    for i, s in enumerate(sentences):
        if i % 250 == 0:
            print(f"  Ingested {i}/{len(sentences)}... (Vocab: {len(brain.substrate.neurons)})")
        brain.lang.ingest_continuous_stream(s, target_tier=1)
        
    print(f"Learning complete in {time.time() - start:.2f} seconds.")
    print(f"Final Concept Topology (Vocab Size): {len(brain.substrate.neurons)}")
    
    print("\n[FRONTIER LAYER] Triggering [VOID] Vacuums for emergent thought generation...")
    manifold = FrontierManifold(brain)
    
    test_prompts = [
        "dog runs",
        "bird flies",
        "sun is hot",
        "happy fella",
        "water flows",
        "apple falls",
        "user feels"
    ]
    
    for prompt in test_prompts:
        manifold.formulate_thought(prompt, max_length=15, stop_threshold=0.35)

if __name__ == "__main__":
    run_spectron_curriculum()
