import time
from fella.fella_brain import FellaBrain

def run():
    print("[FELLA: OFFLINE DREAM CONSOLIDATION & RAPID TESTING]")
    print("Loading physical substrate...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    print(f"Neurons Loaded: {len(brain.substrate.neurons)}")
    
    print("\n[PHASE 1: CONNECTING THE DOTS (DREAMING)]")
    print("Fella is entering REM sleep. She is mathematically reverberating")
    print("energy through her 2,000 new concepts to wire them together and prune noise.")
    
    for cycle in range(1, 6):
        res = brain.dream_consolidation()
        thought = res.get('last_thought', 'Dreaming...')
        print(f"Dream Cycle {cycle}: {thought}")
        time.sleep(0.2)
        
    print("\nFella has awoken. The dots are connected.")
    
    print("\n[PHASE 2: RAPID TESTING]")
    print("We will fire 5 sensory waves at her to see her independent thoughts.")
    
    # We will pass autonomous_exploration=False so she relies strictly on her internal physics 
    # instead of asking Ollama to cheat!
    
    questions = [
        "alice",
        "rabbit",
        "hole",
        "king",
        "cat"
    ]
    
    for q in questions:
        print(f"\n======================================")
        print(f"USER STIMULUS: '{q}'")
        res = brain.converse(q, autonomous_exploration=False)
        print(f"FELLA'S INNER THOUGHT: {res['last_thought']}")
        print(f"FELLA'S VOCALIZATION: {res['last_response']}")
        time.sleep(0.5)

    print("\nSaving consolidated brain state...")
    brain.save_state('fella_checkpoint.json')
    print("State saved successfully.")

if __name__ == '__main__':
    run()
