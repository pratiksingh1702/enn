import os
import shutil
from fella.fella_brain import FellaBrain

def run_multiple_facts():
    if os.path.exists('memory_bank'):
        shutil.rmtree('memory_bank')

    print("==================================================")
    print("INITIALIZING FELLA")
    print("==================================================")
    fella = FellaBrain(dim=16)

    print("\n[TEACHING PHASE 1: Primary Categories]")
    fella.converse("what is apple ?")
    fella.converse("apple is food")
    print("Taught: apple is food")
    
    fella.converse("what is tub ?")
    fella.converse("tub is object")
    print("Taught: tub is object")

    print("\n[TESTING PHASE 1]")
    fella.converse("what is apple ?")
    print(f"[USER]: what is apple ? -> [FELLA]: {fella.last_response}")
    fella.converse("what is tub ?")
    print(f"[USER]: what is tub ? -> [FELLA]: {fella.last_response}")

    print("\n[TEACHING PHASE 2: Secondary Attributes]")
    fella.converse("apple is tasty")
    print("Taught: apple is tasty")
    
    fella.converse("tub is plastic")
    print("Taught: tub is plastic")

    print("\n[TESTING PHASE 2 (Observing Recency/Gravity Bias)]")
    fella.converse("what is apple ?")
    print(f"[USER]: what is apple ? -> [FELLA]: {fella.last_response}")
    fella.converse("what is tub ?")
    print(f"[USER]: what is tub ? -> [FELLA]: {fella.last_response}")

    print("\n==================================================")
    print("SYNAPTIC TOPOLOGY (Gravity Weights)")
    print("==================================================")
    
    apple_n = fella.wave_engine._get_or_create_neuron("apple")
    print(f"\n[NODE]: 'apple' (Cold Potential: {getattr(apple_n, 'cold_potential', 0.0):.1f})")
    for target_id, weight in apple_n.synapses.items():
        target_word = fella.substrate.neurons[target_id].text
        print(f"    -> {target_word} (Gravity: {weight:.2f})")

    tub_n = fella.wave_engine._get_or_create_neuron("tub")
    print(f"\n[NODE]: 'tub' (Cold Potential: {getattr(tub_n, 'cold_potential', 0.0):.1f})")
    for target_id, weight in tub_n.synapses.items():
        target_word = fella.substrate.neurons[target_id].text
        print(f"    -> {target_word} (Gravity: {weight:.2f})")

if __name__ == "__main__":
    run_multiple_facts()
