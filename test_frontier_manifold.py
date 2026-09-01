from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_frontier_audit():
    print("==================================================")
    print("FRONTIER MANIFOLD AUDIT: NATIVE SENTENCE CRYSTALLIZATION")
    print("==================================================")
    
    # Load her established brain with the trained left/right accumulators
    brain = FellaBrain(dim=16)
    
    # Train her very quickly on a few sentences so she has SOME vocabulary and slots
    sentences = [
        "the user eats the apple",
        "the user eats the bread",
        "a dog eats the bone",
        "the fella eats data",
        "i run quickly",
        "they run fast",
        "we run home",
        "the user runs far",
        "the apple falls down",
        "the big apple is red",
        "the user is walking",
        "the happy fella is thinking",
        # Thickening the dataset for these specific words
        "we run fast",
        "they run quickly",
        "i run far",
        "the dog runs home",
        "the user runs quickly",
        "we run far",
        "they run home",
        "i run fast",
        "the big apple falls down",
        "the red apple falls",
        "the apple falls fast",
        "a red apple is down",
        "the apple is down",
        "the user eats a red apple",
        "the fella eats bread",
        "the dog eats bread",
        "we eat the red apple",
        "they eat the big apple",
        "i eat the apple quickly",
        "the user falls down",
        "the fella falls quickly",
        "the dog falls fast",
        "the red bread falls",
        "the bone falls down",
        "the dog runs to the bone",
        "the user runs to the bread",
        "the fella runs to the apple",
        "the big dog runs fast",
        "the happy user eats quickly",
        "the big fella eats fast",
        "a red apple falls quickly",
        "the fast dog runs far",
        "we eat bread quickly",
        "they eat data fast",
        "i eat the bone"
    ]
    print("[1] Rapid distributional ingestion...")
    for s in sentences:
        brain.lang.ingest_continuous_stream(s, target_tier=1)
        
    print("\n[2] Triggering Epistemic Vacuum...")
    manifold = FrontierManifold(brain)
    
    # Ask her to think about "apple"
    manifold.formulate_thought("apple", max_length=15, stop_threshold=0.35)
    
    # Ask her to think about "run"
    manifold.formulate_thought("run", max_length=15, stop_threshold=0.35)
    
    # 5-6 Broader Prompts to test threshold robustness and decay inhibition
    manifold.formulate_thought("user", max_length=15, stop_threshold=0.35)
    manifold.formulate_thought("bread", max_length=15, stop_threshold=0.35)
    manifold.formulate_thought("home", max_length=15, stop_threshold=0.35)
    manifold.formulate_thought("fast", max_length=15, stop_threshold=0.35)
    manifold.formulate_thought("eats", max_length=15, stop_threshold=0.35)
    manifold.formulate_thought("thinking", max_length=15, stop_threshold=0.35)
    
    # Test a multi-word semantic plan!
    manifold.formulate_thought("the dog runs fast", max_length=15, stop_threshold=0.35)
    manifold.formulate_thought("happy fella eats", max_length=15, stop_threshold=0.35)

if __name__ == "__main__":
    run_frontier_audit()
