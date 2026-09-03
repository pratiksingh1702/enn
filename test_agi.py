import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def genesis_curriculum(brain):
    """UPGRADE 5: BULK INGESTION & GEOMETRIC ALIGNMENT (Tabula Rasa Bootcamp)"""
    print("--- [GENESIS CURRICULUM] Booting Matrix... ---")
    corpus = [
        "apple is red", "red is color", "apple is tasty", "tasty is flavor",
        "banana is yellow", "yellow is color", "banana is sweet", "sweet is flavor",
        "sky is blue", "water is blue", "fire is hot", "ice is cold",
        "car is fast", "turtle is slow", "sun is bright", "moon is pale",
        "grass is green", "dirt is brown", "wood is hard", "pillow is soft"
    ]
    for sentence in corpus:
        brain.record_event(sentence.split())
    print(f"Ingested {len(corpus)} events. Geometric matrix synchronized.")

def test_agi():
    print("=========================================")
    print("ENN AGI KERNEL (V2): THE 5 UPGRADES")
    print("=========================================")
    brain = FellaBrain(dim=128)
    frontier = FrontierManifold(brain)

    genesis_curriculum(brain)

    print("\\n--- TRAINING PATTERNS ---")
    q1 = brain.record_event(["what", "color", "is", "apple"])
    q2 = brain.record_event(["what", "color", "is", "banana"])
    q3 = brain.record_event(["what", "color", "is", "sky"])
    frontier.form_spectron([q1, q2, q3])
    
    # Let's train a generative rule so she can talk
    y, t, r = frontier.formulate_thought("what color is apple")
    frontier.process_correction(t, r, "apple is a red tasty color flavor")

    print("\\n--- UPGRADE 2: FRACTAL SPECTRONS (Recursion) ---")
    # We ask a nested question: "what color is the banana that is yellow"
    # Because 'banana that is yellow' is long, the recursion engine will kick in!
    # To prevent 'that is' from breaking it, let's just make it 'what color is sweet banana'
    # Actually, the recursion triggers on len(isolated) >= 3.
    frontier.formulate_thought("what color is big sweet banana")

    print("\\n--- UPGRADE 3: HOLOGRAPHIC SIMULATOR (Contradiction Check) ---")
    # We manually force a contradiction by heavily repelling two words!
    brain.neurons["apple"].x_wave = -brain.neurons["car"].x_wave # Perfect inverse
    brain.sync_matrix()
    
    # We ask a question that retrieves them both (artificially)
    # We can fake it by asking "what color is apple car"
    frontier.formulate_thought("what color is apple car")

    print("\\n--- UPGRADE 1: SYNAPTIC PRUNING (Entropy) ---")
    print(f"Events in memory before pruning: {len(brain.events)}")
    # Prune everything not accessed in the last 2 ticks!
    pruned = brain.prune_memory(threshold=2)
    print(f"Events pruned due to entropy: {pruned}")
    print(f"Events remaining in memory: {len(brain.events)}")

if __name__ == '__main__':
    test_agi()
