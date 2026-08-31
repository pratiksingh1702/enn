import time
from fella.fella_brain import FellaBrain

def run():
    print("Loading Perfected Brain...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    print("\n[PHASE 1: SEMANTIC GROUNDING]")
    print("Teaching her true explanations, not just narrative fragments...\n")
    
    definitions = [
        "A queen is a powerful female monarch who rules a kingdom.",
        "A hole is a deep empty opening or dark space in the ground.",
        "Crying means shedding tears because of sad or painful emotions.",
        "A rabbit is a small fast furry animal with long ears.",
        "The story is a confusing dream about nonsense and madness."
    ]
    
    for d in definitions:
        print(f"TEACHING: {d}")
        # Turn Ollama off so she relies purely on her own CLIP vector math to wire the nodes
        brain.converse(d, autonomous_exploration=False)
        
    print("\n[PHASE 2: THE USER'S EVALUATION TEST]")
    
    tests = [
        "what is a queen ?",
        "what is a hole ?",
        "what is crying ?",
        "what is a rabbit ?",
        "what do you think about the story ?"
    ]
    
    for t in tests:
        print(f"\n======================================")
        print(f"USER STIMULUS: '{t}'")
        res = brain.converse(t, autonomous_exploration=False)
        print(f"FELLA THOUGHT: {res['last_thought']}")
        print(f"FELLA SPOKE:   {res['last_response']}")
        
    print("\nSaving semantically grounded brain...")
    brain.save_state('fella_checkpoint.json')

if __name__ == '__main__':
    run()
