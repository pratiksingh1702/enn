from fella.fella_entity import FellaEntity
import numpy as np

def test_causal_reasoning():
    print("=========================================")
    print("PHASE 6: TEMPORAL CAUSAL VECTORS (REASONING)")
    print("=========================================")
    
    fella = FellaEntity(dim=256)
    
    # 1. Initialize concepts
    words = ["lightning", "thunder", "rain", "puddles", "slip", "fall", "pain"]
    for w in words:
        fella.brain.get_or_create(w)
        
    print("\n[ENVIRONMENT] Teaching causal sequence over time...")
    # 2. She experiences the world moving forward in time
    # Sequence 1: Lightning -> Thunder -> Rain -> Puddles
    fella.perceive(["lightning"])
    fella.perceive(["thunder"])
    fella.perceive(["rain"])
    fella.perceive(["puddles"])
    
    # Let time break (reset active concepts)
    fella.causal_cortex.active_concepts = []
    
    # Sequence 2: Rain -> Puddles -> Slip -> Fall -> Pain
    fella.perceive(["rain"])
    fella.perceive(["puddles"])
    fella.perceive(["slip"])
    fella.perceive(["fall"])
    fella.perceive(["pain"])

    print("[ENGINE] Temporal Adjacency Matrix (Causal Tethers) established.")
    
    # 3. Test multi-step reasoning
    print("\n[DEEP REASONING TEST]")
    print("If she sees 'lightning', what does she deduce will happen flowing into the future?")
    
    start_idx = fella.brain.matrix_keys.index("lightning")
    
    # Simulate step-by-step into the future
    for step in range(1, 6):
        future_state = fella.causal_cortex.simulate_future([start_idx], steps=step)
        top_indices = np.argsort(future_state)[::-1]
        
        print(f"\n[t + {step}]")
        for idx in top_indices:
            if future_state[idx] > 0:
                word = fella.brain.matrix_keys[idx]
                print(f" -> Predicted Event: '{word}' (Probability: {future_state[idx]*100:.1f}%)")

if __name__ == '__main__':
    test_causal_reasoning()
