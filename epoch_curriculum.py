import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold
import time

def build_curriculum():
    events = []
    
    # EPOCH 1: NOUNS & ADJECTIVES (Ontology)
    fruits = ["apple", "banana", "grape", "orange", "berry", "cherry", "mango", "pear"]
    animals = ["dog", "cat", "cheetah", "turtle", "bird", "fish", "lion", "tiger", "bear"]
    vehicles = ["car", "truck", "plane", "boat", "train", "bike", "jet", "ship"]
    colors = ["red", "blue", "green", "yellow", "black", "white", "purple", "brown"]
    speeds = ["fast", "slow", "quick", "sluggish", "rapid", "swift", "brisk", "creeping"]
    
    # Teach her ontological clusters (Gravity)
    for f in fruits:
        events.extend([[f, "is", "fruit"], [f, "is", "food"], [f, "is", "sweet"]])
    for a in animals:
        events.extend([[a, "is", "animal"], [a, "is", "alive"]])
    for v in vehicles:
        events.extend([[v, "is", "vehicle"], [v, "is", "machine"]])
    for c in colors:
        events.append([c, "is", "color"])
    for s in speeds:
        events.append([s, "is", "speed"])
        
    # Teach her specific traits
    events.extend([
        ["cheetah", "is", "fast"], ["turtle", "is", "slow"], ["lion", "is", "fast"],
        ["dog", "is", "quick"], ["cat", "is", "fast"], ["bird", "is", "swift"],
        ["car", "is", "fast"], ["plane", "is", "rapid"], ["bike", "is", "slow"],
        ["apple", "is", "red"], ["banana", "is", "yellow"], ["grape", "is", "purple"]
    ])
    
    # Dilute structural glue words so they exceed 30% frequency
    for i in range(40):
        events.append([f"dummy{i}", "is", "the", f"thing{i}"])
        events.append([f"dummy{i}", "of", "the", f"thing{i}"])
        
    return events

def run_epoch_test():
    print("=========================================")
    print("FELLA ENN: MASS VOCABULARY INGESTION")
    print("=========================================")
    brain = FellaBrain(dim=128)
    frontier = FrontierManifold(brain)

    print("\\n--- INGESTING MASSIVE CURRICULUM ---")
    curriculum = build_curriculum()
    
    start_time = time.time()
    for sentence in curriculum:
        brain.record_event(sentence)
    end_time = time.time()
    
    print(f"Ingested {len(curriculum)} unique events.")
    print(f"Total vocabulary size: {len(brain.neurons)} words.")
    print(f"Brain compiled in {end_time - start_time:.2f} seconds.")
    
    print("\\n--- TEACHING GENERATIVE GRAMMAR ---")
    q1 = brain.record_event(["what", "is", "the", "speed", "of", "cheetah"])
    q2 = brain.record_event(["what", "is", "the", "speed", "of", "car"])
    q3 = brain.record_event(["what", "is", "the", "speed", "of", "turtle"])
    frontier.form_spectron([q1, q2, q3])
    
    # We teach her a rigid template by correcting her once!
    y, t, r = frontier.formulate_thought("what is the speed of cheetah")
    frontier.process_correction(t, r, "cheetah is a fast animal")

    print("\\n--- TRANSFER LEARNING ACROSS GEOMETRIC CLUSTERS ---")
    print("\\n[QUESTION 1: THE LION]")
    # Lion is fast, Lion is animal.
    # It should perfectly slot into the geometry.
    frontier.formulate_thought("what is the speed of lion")

    print("\\n[QUESTION 2: THE BIRD]")
    # Bird is swift. Swift is a speed. Fast is a speed.
    # Because 'swift' and 'fast' are clustered in the 128D space via 'speed',
    # she should mathematically substitute 'swift' for 'fast'!
    frontier.formulate_thought("what is the speed of bird")
    
    print("\\n[QUESTION 3: THE PLANE]")
    # Plane is rapid. Plane is vehicle.
    # She should mathematically substitute 'rapid' for 'fast' and 'vehicle' for 'animal'!
    frontier.formulate_thought("what is the speed of plane")

if __name__ == '__main__':
    run_epoch_test()
