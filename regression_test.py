import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_regression_suite():
    # Sane dimensionality based on actual embedding statistics
    brain = FellaBrain(dim=256) 
    frontier = FrontierManifold(brain)
    
    # 1. Baseline Knowledge
    corpus = [
        ["apple", "is", "red"], ["apple", "is", "tasty"], ["apple", "is", "fruit"],
        ["sky", "is", "blue"], ["car", "is", "fast"], ["car", "is", "machine"],
        ["turtle", "is", "slow"], ["cheetah", "is", "fast"],
        ["bird", "is", "swift"], ["bird", "flies", "high"],
        ["water", "is", "wet"], ["fire", "is", "hot"],
        # Dilute grammar
        ["dummy1", "is", "the", "thing1"], ["dummy2", "of", "the", "thing2"],
        ["dummy3", "is", "the", "thing3"], ["dummy4", "of", "the", "thing4"]
    ] * 5 # Repeat to harden clusters
    
    for c in corpus:
        brain.record_event(c)
        
    # 2. Teach Spectrons
    q1 = brain.record_event(["what", "color", "is", "apple"])
    q2 = brain.record_event(["what", "color", "is", "sky"])
    q3 = brain.record_event(["what", "is", "the", "speed", "of", "car"])
    q4 = brain.record_event(["what", "is", "the", "speed", "of", "turtle"])
    
    frontier.form_spectron([q1, q2])
    frontier.form_spectron([q3, q4])
    
    # 3. Generative Rule
    y, t, r, w_id = frontier.formulate_thought("what is the speed of cheetah")
    frontier.process_correction(t, r, "cheetah is a fast machine", w_id)

    print("=========================================")
    print("FRONTIER MANIFOLD: REGRESSION SUITE")
    print("=========================================")
    
    prompts = [
        "what color is apple",                           # T1: Simple 1-word target
        "what color is the big red apple",               # T2: Multi-word target isolation
        "what is the speed of cheetah",                  # T3: Generative exact match
        "what is the speed of turtle",                   # T4: Generative substitution (fast -> slow)
        "what is the speed of bird",                     # T5: Substitution threshold check (swift vs fast)
        "random babble words completely unknown",        # T6: Out of distribution (should fail gracefully)
    ]
    
    for p in prompts:
        frontier.formulate_thought(p)

if __name__ == "__main__":
    run_regression_suite()
