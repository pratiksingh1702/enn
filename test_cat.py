import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_cat_test():
    print("=========================================")
    print("ENN DUAL-PROCESS ENGINE: CAT TEST")
    print("=========================================")
    brain = FellaBrain(dim=128)
    frontier = FrontierManifold(brain)

    # 1. Background knowledge to establish 'is' as a structural catalyst (freq > 30%)
    # If we only have 2 events, 'is' won't cross the threshold. We need a tiny baseline universe.
    brain.record_event(["apple", "is", "fruit"])
    brain.record_event(["car", "is", "fast"])
    brain.record_event(["sun", "is", "hot"])
    brain.record_event(["water", "is", "wet"])
    brain.record_event(["sky", "is", "blue"])

    print("\\n--- PHASE 1: TEACHING ABOUT CAT ---")
    brain.record_event(["cat", "is", "animal"])
    brain.record_event(["cat", "is", "mammal"])
    
    print("\\n--- PHASE 2: TEACHING THE '?' SHORT-HAND PATTERN ---")
    # A child doesn't hardcode "?", they learn it's a structural pattern for inquiry!
    q1 = brain.record_event(["apple", "?"])
    q2 = brain.record_event(["car", "?"])
    q3 = brain.record_event(["sun", "?"])
    
    # Engine organically forms Spectron for "[VOID] ?"
    frontier.form_spectron([q1, q2, q3])

    print("\\n--- PHASE 3: THE FRONTIER TEST ('cat ?') ---")
    # You asked to just input "cat ?"
    frontier.formulate_thought("cat ?")

if __name__ == '__main__':
    run_cat_test()
