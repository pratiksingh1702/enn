import time
import os
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_custom_curriculum():
    print("==================================================")
    print("CUSTOM CURRICULUM TRAINING: PURE LINGUISTIC GEOMETRY")
    print("==================================================")
    
    # Ensure fresh brain by deleting checkpoint if it somehow exists
    if os.path.exists("universe_master_checkpoint.json"):
        os.remove("universe_master_checkpoint.json")
        
    brain = FellaBrain(dim=16)
    
    # Highly structured sentences to test GMMs, Catalysts, and basic grammar
    base_sentences = [
        # Action/Subject/Object (The X runs to the Y)
        "the fast dog runs to the house",
        "the fast cat runs to the house",
        "the big dog walks to the tree",
        "the small cat walks to the tree",
        "the big man runs to the big house",
        "the small woman walks to the small house",
        
        # Consumption (The X eats the Y)
        "the dog eats the red apple",
        "the cat eats the blue fish",
        "the man eats the hot bread",
        "the woman eats the cold fish",
        
        # Physics (A X falls down)
        "a red apple falls down to the ground",
        "a green leaf falls down to the ground",
        "the hot water flows down to the ground",
        "the cold water flows down to the river",
        
        # Multi-sense test ('run' as a noun vs verb)
        "the fast man goes on a long run",
        "the fast woman goes on a long run",
        "a long run makes the dog happy",
        
        # Identity / States
        "fire is hot and burns fast",
        "ice is cold and melts fast",
        "the user is happy and smiles",
        "the fella is happy and thinks",
        "the user thinks about the data",
        "the fella thinks about the network"
    ]
    
    # Multiply to build deep, entrenched wave patterns and isolate catalysts
    sentences = base_sentences * 15 
    
    print(f"\n[1] Ingesting structured curriculum ({len(sentences)} total sentences)...")
    start = time.time()
    
    for i, s in enumerate(sentences):
        if i % 50 == 0:
            print(f"  Ingested {i}/{len(sentences)}...")
        brain.lang.ingest_continuous_stream(s, target_tier=1)
        
    print(f"Streaming complete in {time.time() - start:.2f} seconds.")
    print(f"Final Vocabulary Size: {len(brain.substrate.neurons)}")
    
    # Save the beautifully structured brain
    brain.substrate.save_to_disk("universe_master_checkpoint.json")
    
    print("\n[2] Triggering Epistemic Vacuums...")
    manifold = FrontierManifold(brain)
    
    test_prompts = [
        "dog runs",
        "cat eats",
        "apple falls",
        "user thinks",
        "a long run", # Test noun cluster
        "fella happy",
        "fire burns",
        "fast man house",
        "the woman runs",
        "water flows down"
    ]
    
    for prompt in test_prompts:
        manifold.formulate_thought(prompt, max_length=15, stop_threshold=0.35)

if __name__ == "__main__":
    run_custom_curriculum()
