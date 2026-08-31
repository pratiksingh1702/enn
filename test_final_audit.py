import os
import shutil
import time
from fella.fella_brain import FellaBrain

def run_final_audit():
    if os.path.exists('memory_bank'):
        shutil.rmtree('memory_bank')

    print("==================================================")
    print("INITIALIZING FELLA")
    print("==================================================")
    fella = FellaBrain(dim=16)

    print("\n[TEACHING COMPLEX OBJECT]")
    fella.converse("what is apple ?")
    fella.converse("apple is fruit")
    fella.converse("apple is sweet")
    fella.converse("apple is red")
    
    print("\n[LEAVING FELLA ALONE FOR HEARTBEAT TO RUMINATE...]")
    time.sleep(12)  # Wait for a heartbeat pulse (pulse is 10s)

    print("\n[TESTING RETRIEVAL]")
    fella.converse("what is apple ?")
    print(f"[USER]: what is apple ? -> [FELLA]: {fella.last_response}")

    print("\n==================================================")
    print("FINAL BRAIN STATE METRICS")
    print("==================================================")
    state = fella.wave_engine.get_brain_state()
    print(f"Total Neurons Mapped: {state['total_neurons']}")
    print(f"Hot Spectrons (Curiosity): {state['hot_spectrons']}")
    print(f"Catalysts (Operators): {state['catalysts']}")
    print(f"Mirrors (Identity): {state['mirrors']}")
    
    # Calculate total active synapses
    total_synapses = sum(len(n.synapses) for n in fella.substrate.neurons.values())
    print(f"Total Active Synaptic Edges: {total_synapses}")

if __name__ == "__main__":
    run_final_audit()
