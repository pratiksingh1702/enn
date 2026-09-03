from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_test():
    print("=========================================")
    print("FELLA ENN DUAL-PROCESS ENGINE (X, Y, Z, W)")
    print("=========================================")
    brain = FellaBrain(dim=128)
    frontier = FrontierManifold(brain)
    
    print("\\n--- PHASE 1: INGESTING EPISODIC Z-EVENTS ---")
    z1 = brain.record_event(["apple", "is", "fruit"])
    z2 = brain.record_event(["apple", "is", "red"])
    z3 = brain.record_event(["apple", "is", "tasty"])
    print(f"Recorded Events Z={z1}, Z={z2}, Z={z3}")
    
    print("\\n--- PHASE 2: TRAINING W-SPECTRONS ---")
    qz1 = brain.record_event(["what", "is", "apple"])
    qz2 = brain.record_event(["what", "is", "tub"])
    qz3 = brain.record_event(["what", "is", "car"])
    
    # Engine organically forms Spectron from these events
    frontier.form_spectron([qz1, qz2, qz3])
    
    print("\\n--- PHASE 3 & 4: THE FRONTIER TEST ---")
    y_out, target, retrieved = frontier.formulate_thought("what is apple")
    
    print("\\n--- PHASE 5: THE CORRECTION LOOP ---")
    # You correct her grammar!
    frontier.process_correction(target, retrieved, "apple is a tasty red fruit")
    
    print("\\n--- PHASE 5 VERIFICATION ---")
    print("Now ask her the exact same question again. Watch her use the new Spectron structure!")
    frontier.formulate_thought("what is apple")
    
    print("\\n=========================================")
    print("DUMPING ALL NEURONS AND SPECTRONS")
    print("=========================================")
    print("\\n--- NEURON REPOSITORY (The Dictionary) ---")
    for text, n in brain.neurons.items():
        print(f"Neuron: '{text:<6}' | Fired in Z-Events: {sorted(list(n.z_events))}")
        
    print("\\n--- SPECTRON CORTEX (W-Axis Rules) ---")
    for spec in brain.spectrons:
        kind = "GENERATIVE" if getattr(spec, 'is_generation', False) else "PATTERN ABSTRACTION"
        origins = getattr(spec, 'source_z_events', 'Learned via Correction Loop')
        if isinstance(origins, set): origins = sorted(list(origins))
        print(f"Spectron W={spec.w_id} | Type: {kind:<19} | Origin: {origins}")
        print(f"  -> Structure: '{spec.structure_text}'")
    
if __name__ == '__main__':
    run_test()
