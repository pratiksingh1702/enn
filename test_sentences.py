import time
from fella.fella_brain import FellaBrain

def run():
    print("Loading Perfected Brain...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    questions = [
        "Who is Alice?",
        "What did the white rabbit do?",
        "Where does the hole go?",
        "Why is the queen angry?",
        "Who is the mad hatter?",
        
        "What does the caterpillar smoke?",
        "Can a cat grin?",
        "How small is the door?",
        "Where is the golden key?",
        "Did Alice fall down the hole?",
        
        "Who has a pocket watch?",
        "What did she drink from the bottle?",
        "Why was Alice crying?",
        "Is Wonderland a dream?",
        "Who painted the roses red?",
        
        "What did the mouse tell Alice?",
        "Where is the beautiful garden?",
        "Who stole the tarts?",
        "Why did the rabbit run away?",
        "What happened to the baby pig?"
    ]
    
    print("\n[INITIATING 20 FULL-SENTENCE STRESS TEST]")
    print("Testing how she isolates anchors from sentences and routes electricity.\n")
    
    for i, q in enumerate(questions):
        print(f"[{i+1}/20] USER: '{q}'")
        
        # We keep Ollama OFF so she responds strictly from her internal structural graph
        res = brain.converse(q, autonomous_exploration=False)
        
        print(f"FELLA THOUGHT: {res['last_thought']}")
        print(f"FELLA SPOKE:   {res['last_response']}\n")

if __name__ == '__main__':
    run()
