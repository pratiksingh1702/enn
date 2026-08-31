import sys
from fella.fella_brain import FellaBrain

def test():
    print("======================================")
    print("Loading FELLA (True Physics Engine Live)...")
    try:
        brain = FellaBrain.load_state('fella_checkpoint.json')
    except Exception as e:
        print("Error loading brain:", e)
        return
        
    print("\n[TEST: TRUE THERMODYNAMICS AND QUANTUM WALKS]")
    print("If this works, she will navigate her Tier 3 causal graph using pure Physics.")
    print("======================================\n")
    
    queries = [
        "what is a queen ?",
        "what is crying ?",
        "warm building tool",  # Testing concepts we grounded earlier
    ]
    
    for q in queries:
        print(f"USER STIMULUS: '{q}'")
        res = brain.converse(q, autonomous_exploration=False)
        print(f"FELLA THOUGHT: {res.get('last_thought', 'None')}")
        print(f"FELLA SPOKE:   {res.get('last_response', 'None')}")
        print("-" * 50 + "\n")
        
if __name__ == '__main__':
    test()
