import time
from fella.fella_brain import FellaBrain

def run():
    print("Loading perfect physical substrate...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    questions = ["alice", "rabbit", "cat", "queen", "hole"]
    
    for q in questions:
        print(f"\n======================================")
        print(f"USER STIMULUS: '{q}'")
        res = brain.converse(q, autonomous_exploration=False)
        print(f"FELLA'S VOCALIZATION: {res['last_response']}")

if __name__ == '__main__':
    run()
