import os
import shutil
from fella.fella_brain import FellaBrain

def run_ask_again():
    if os.path.exists('memory_bank'):
        shutil.rmtree('memory_bank')

    nouns = ["apple", "car", "dog"]
    categories = ["fruit", "vehicle", "animal"]

    print("==================================================")
    print("INITIALIZING FELLA")
    print("==================================================")
    fella = FellaBrain(dim=16)

    print("\n==================================================")
    print("PHASE 1: TEACHING")
    print("==================================================")
    for i, noun in enumerate(nouns):
        ans = categories[i]
        fella.converse(f"what is {noun} ?")
        fella.converse(f"{noun} is {ans}")
        print(f"Taught: {noun} is {ans}")

    print("\n==================================================")
    print("PHASE 2: ASKING AGAIN (WITHOUT RESET)")
    print("==================================================")
    for noun in nouns:
        print(f"\n[USER]: what is {noun} ?")
        fella.converse(f"what is {noun} ?")
        print(f"[FELLA RESPONSE]: {fella.last_response}")
        
    print("\n==================================================")
    print("PHASE 3: BRAIN STATE")
    print("==================================================")
    state = fella.wave_engine.get_brain_state()
    print(state)
    
    what_n = fella.wave_engine._get_or_create_neuron("what")
    is_n = fella.wave_engine._get_or_create_neuron("is")
    apple_n = fella.wave_engine._get_or_create_neuron("apple")
    print(f"'what' Cold: {getattr(what_n, 'cold_potential', 0.0)}")
    print(f"'is' Cold: {getattr(is_n, 'cold_potential', 0.0)}")
    print(f"'apple' Cold: {getattr(apple_n, 'cold_potential', 0.0)}")

if __name__ == "__main__":
    run_ask_again()
