import time
from fella.fella_brain import FellaBrain

def run():
    print('[FELLA: STORYBOOK INGESTION PROTOCOL]')
    print('Loading physical substrate...')
    brain = FellaBrain.load_state('fella_checkpoint.json')
    print(f'Initial Neurons: {len(brain.substrate.neurons)}')
    
    storybook = [
        "The ancient forest holds many secrets.",
        "A wise king rules the green kingdom.",
        "Birds sing melodies in the high branches.",
        "The river flows silently through the valley.",
        "Wolves protect the borders of the kingdom.",
        "Magic glows softly in the dark shadows.",
        "The king watches the stars at night.",
        "Stars guide the wolves through the darkness.",
        "The river provides water for the animals.",
        "Peace reigns in the ancient forest."
    ]

    print("\n[STARTING AUTONOMOUS INGESTION]")
    print("Fella will read the storybook. If she encounters a concept she doesn't know,")
    print("she will autonomously halt, query her internal Mentor (Ollama) to learn it,")
    print("ingest the physical causal laws of that concept, and then continue reading.")
    
    for sentence in storybook:
        print(f"\n>> Reading: '{sentence}'")
        # Passing autonomous_exploration=True to allow self-guided learning of missing concepts
        brain.converse(sentence, autonomous_exploration=True)
        time.sleep(0.5)

    print("\n[STORYBOOK INGESTED]")
    print(f'Final Neurons: {len(brain.substrate.neurons)}')
    
    print("\n[TESTING COHERENCE]")
    questions = [
        "What does the king watch?",
        "What do stars do?",
        "Who protects the borders?"
    ]
    
    for q in questions:
        print(f"\nUser: {q}")
        res = brain.converse(q)
        print(f"FELLA: '{res['last_response']}'")
        
    print("\nSaving new brain state...")
    brain.save_state('fella_checkpoint.json')
    print("Saved successfully.")

if __name__ == '__main__':
    run()
