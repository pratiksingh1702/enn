import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def final_test():
    print("=========================================")
    print("FELLA ENN: FINAL ARCHITECTURAL TEST")
    print("=========================================")
    brain = FellaBrain(dim=128)
    frontier = FrontierManifold(brain)

    print("\\n--- PHASE 1: GENESIS (Pure Tabula Rasa) ---")
    # Teach her about animals and speeds
    brain.record_event(["cheetah", "is", "fast"])
    brain.record_event(["cheetah", "is", "animal"])
    brain.record_event(["turtle", "is", "slow"])
    brain.record_event(["turtle", "is", "animal"])
    
    # Dilute structural words so they mathematically become grammar (>30% freq)
    brain.record_event(["apple", "is", "the", "fruit"])
    brain.record_event(["car", "is", "the", "machine"])
    brain.record_event(["sky", "is", "the", "blue"])
    brain.record_event(["sun", "is", "the", "hot"])
    brain.record_event(["water", "is", "the", "wet"])

    print("\\n--- PHASE 2: PATTERN ABSTRACTION (No Regex) ---")
    q1 = brain.record_event(["what", "is", "the", "speed", "of", "cheetah"])
    q2 = brain.record_event(["what", "is", "the", "speed", "of", "car"])
    q3 = brain.record_event(["what", "is", "the", "speed", "of", "apple"])
    
    # Watch her mathematically extract: 'what is the speed of [VOID]'
    frontier.form_spectron([q1, q2, q3])

    print("\\n--- PHASE 3: MAGNETIC ROUTING & Z-AXIS SLICING ---")
    # The attractor will be "speed", steering her thought wave!
    y, t, r = frontier.formulate_thought("what is the speed of cheetah")

    print("\\n--- PHASE 4: PHASE-LOCKED CORRECTION ---")
    # We teach her a rule. She doesn't use [CONCEPT] strings. 
    # She geometrically saves the x_wave for 'fast' and 'animal' into the slots.
    frontier.process_correction(t, r, "cheetah is a fast animal")

    print("\\n--- PHASE 5: TRANSFER LEARNING (Pure Geometry) ---")
    # We ask about a completely different animal.
    # She will isolate 'turtle', spread energy to retrieve 'slow' and 'animal'.
    # Because 'slow' geometrically aligns with the 'fast' slot (both are speeds/adjectives),
    # she will map it perfectly and generate the correct English sentence!
    frontier.formulate_thought("what is the speed of turtle")

if __name__ == '__main__':
    final_test()
