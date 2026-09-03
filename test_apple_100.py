import os
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_apple_test():
    print("==================================================")
    print("APPLE TEST: 100 ITERATIONS OF FREE ENERGY")
    print("==================================================")
    
    # 1. Reset her (Fresh Brain)
    brain = FellaBrain(dim=64)
    print("[VOID] Brain reset to blank slate.")
    
    # 2. Give her 10 facts about apples
    apple_facts = [
        "apple is a fruit",
        "apple is red",
        "apple grows on a tree",
        "the fella eats the apple",
        "apple is sweet",
        "water makes the apple grow",
        "apple is round",
        "the woman likes the apple",
        "apple falls down to the ground",
        "apple is food"
    ]
    
    # We loop it a few times to build solid geometric grammar dents
    print("[INGESTION] Learning 10 facts about apples...")
    for _ in range(10):
        for fact in apple_facts:
            brain.lang.ingest_continuous_stream(fact, target_tier=1)
            
    print(f"[TOPOLOGY] Vocabulary Size: {len(brain.substrate.neurons)}")
    
    manifold = FrontierManifold(brain)
    question = "what is apple"
    
    print("\n[FRONTIER] Asking 'what is apple' 100 times...")
    unique_thoughts = {}
    
    for i in range(100):
        # We don't print every time to avoid console spam, just capture the output
        import sys
        import io
        
        # Suppress prints for the loop
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        sentence = manifold.formulate_thought(question, persona_concept="the fella thinks about")
        
        sys.stdout = old_stdout
        
        if sentence not in unique_thoughts:
            unique_thoughts[sentence] = 1
        else:
            unique_thoughts[sentence] += 1
            
    print("\n[RESULTS] Distribution of 100 thoughts:")
    for thought, count in sorted(unique_thoughts.items(), key=lambda x: x[1], reverse=True):
        print(f"[{count} times] : {thought}")

if __name__ == "__main__":
    run_apple_test()
