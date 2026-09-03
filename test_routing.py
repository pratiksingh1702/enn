import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def test_routing():
    print("=========================================")
    print("ENN DUAL-PROCESS ENGINE: MAGNETIC ROUTING")
    print("=========================================")
    brain = FellaBrain(dim=128)
    frontier = FrontierManifold(brain)

    print("\\n--- INGESTING KNOWLEDGE ---")
    brain.record_event(["apple", "is", "red"])
    brain.record_event(["red", "is", "color"])
    
    brain.record_event(["apple", "is", "tasty"])
    brain.record_event(["tasty", "is", "flavor"])

    # Establish 'is' as structural glue, but dilute the universe so 'color' and 'flavor' stay <30%
    brain.record_event(["car", "is", "fast"])
    brain.record_event(["sky", "is", "blue"])
    brain.record_event(["water", "is", "wet"])
    brain.record_event(["sun", "is", "hot"])
    brain.record_event(["grass", "is", "green"])
    brain.record_event(["dirt", "is", "brown"])
    brain.record_event(["rock", "is", "hard"])
    brain.record_event(["ice", "is", "cold"])

    print("\\n--- TEACHING QUESTION STRUCTURES ---")
    q1 = brain.record_event(["what", "color", "is", "apple"])
    q2 = brain.record_event(["what", "color", "is", "car"])
    q3 = brain.record_event(["what", "color", "is", "sky"])
    frontier.form_spectron([q1, q2, q3])

    q4 = brain.record_event(["what", "flavor", "is", "apple"])
    q5 = brain.record_event(["what", "flavor", "is", "water"])
    q6 = brain.record_event(["what", "flavor", "is", "sky"])
    frontier.form_spectron([q4, q5, q6])

    print("\\n--- TEST 1: MAGNETIC ROUTING FOR 'COLOR' ---")
    # Because of the word 'color', the attractor should bias energy towards the 'red' path!
    frontier.formulate_thought("what color is apple")

    print("\\n--- TEST 2: MAGNETIC ROUTING FOR 'FLAVOR' ---")
    # Because of the word 'flavor', the attractor should bias energy towards the 'tasty' path!
    frontier.formulate_thought("what flavor is apple")
    
if __name__ == '__main__':
    test_routing()
