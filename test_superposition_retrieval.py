import os
import shutil
from fella.fella_brain import FellaBrain

def run_superposition_test():
    if os.path.exists('memory_bank'):
        shutil.rmtree('memory_bank')

    print("==================================================")
    print("INITIALIZING FELLA")
    print("==================================================")
    fella = FellaBrain(dim=16)

    print("\n[TEACHING PHASE: Sequential Accumulation]")
    
    # Teach Apple
    fella.converse("what is apple ?")
    fella.converse("apple is fruit")
    fella.converse("apple is sweet")
    fella.converse("apple is red")
    fella.converse("apple is tasty")
    print("Taught: apple is (fruit, sweet, red, tasty)")
    
    # Teach Tub
    fella.converse("what is tub ?")
    fella.converse("tub is object")
    fella.converse("tub is white")
    fella.converse("tub is plastic")
    print("Taught: tub is (object, white, plastic)")

    print("\n==================================================")
    print("TESTING PHASE: WAVE SUPERPOSITION")
    print("==================================================")
    
    fella.converse("what is apple ?")
    print(f"[USER]: what is apple ? -> [FELLA]: {fella.last_response}")
    
    fella.converse("what is tub ?")
    print(f"[USER]: what is tub ? -> [FELLA]: {fella.last_response}")

if __name__ == "__main__":
    run_superposition_test()
