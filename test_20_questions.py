import time
from fella.fella_brain import FellaBrain

def run():
    print("Loading Perfected Brain...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    questions = [
        # Core Alice Entities
        "alice", 
        "rabbit", 
        "hole", 
        "cat", 
        "queen",
        
        # Actions & Objects
        "eat", 
        "drink", 
        "door", 
        "key", 
        "garden",
        
        # Compound / Variants
        "white rabbit", 
        "falling down", 
        "small door", 
        "angry queen", 
        "beautiful garden",
        
        # Concepts
        "time", 
        "crying", 
        "dream", 
        "wonderland", 
        "waking"
    ]
    
    print("\n[INITIATING 20-QUESTION STRESS TEST]")
    print("Testing Emergent Sentence Generation based purely on Physics\n")
    
    for i, q in enumerate(questions):
        print(f"[{i+1}/20] USER STIMULUS: '{q}'")
        
        # We turn Ollama OFF for the test so we only measure her current physical graph capabilities
        res = brain.converse(q, autonomous_exploration=False)
        
        print(f"FELLA THOUGHT: {res['last_thought']}")
        print(f"FELLA SPOKE:   {res['last_response']}\n")

if __name__ == '__main__':
    run()
