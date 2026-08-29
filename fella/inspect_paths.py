import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain

brain = FellaBrain.load_state('fella_checkpoint.json')

test_words = ['moon', 'volcanoes', 'stars', 'plants', 'gravity', 'fire', 'earth', 'speed']
for w in test_words:
    matching = [n for n in brain.substrate.neurons.values() if n.text.lower() == w]
    if matching:
        nid = matching[0].id
        tokens, score = brain.lang.simulate_and_evaluate_thoughts(nid, max_depth=8)
        sentence = brain.lang.assemble_closed_sentence(tokens, seed_word=w)
        print(f"Seed: '{w}' -> Path: {tokens} -> Output: \"{sentence}\"")
    else:
        print(f"Seed: '{w}' -> NOT FOUND IN NEURONS")
