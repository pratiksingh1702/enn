import os
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_predictive_test():
    print("==================================================")
    print("FINAL TEST: PREDICTIVE THERMODYNAMIC EQUILIBRIUM")
    print("==================================================")
    
    checkpoint = "universe_master_checkpoint.json"
    
    # Increase dimension to 64 for high-resolution Fourier waves
    brain = FellaBrain(dim=64)
    
    # We load the brain if it exists, otherwise we quickly train it
    if os.path.exists(checkpoint):
        print("[VOID] Loading existing Spectron topology...")
        brain.substrate.load_from_disk(checkpoint)
    else:
        print("[VOID] Neural substrate is blank. Ingesting curriculum...")
        sentences = [
            "the big dog runs fast to the house",
            "the small cat walks to the tree",
            "water is cold and flows down the river",
            "fire is hot and burns the wood",
            "the fella is happy and thinks about the network",
            "the user is happy and thinks about the data",
            "the red apple falls down to the ground",
            "the green leaf falls down to the river",
            "the fast man runs to the big house",
            "the small woman walks to the river"
        ] * 40 # Ingest a 400-sentence curriculum to build solid clusters
        
        for i, s in enumerate(sentences):
            brain.lang.ingest_continuous_stream(s, target_tier=1)
            
        print(f"Final Concept Topology (Vocab Size): {len(brain.substrate.neurons)}")
    
    print("\n[FRONTIER LAYER] Triggering Free Energy Intent Waves...")
    manifold = FrontierManifold(brain)
    
    # These concepts trigger a deep network resonance, forming a Gist Wave, 
    # then emit words until equilibrium is hit.
    test_prompts = [
        "what is apple",
        "fast dog",
        "happy fella"
    ]
    
    for prompt in test_prompts:
        manifold.formulate_thought(prompt, persona_concept="the fella thinks about")

if __name__ == "__main__":
    run_predictive_test()
