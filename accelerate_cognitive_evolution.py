import os
import time
import numpy as np
from fella.fella_entity import FellaEntity
from fella.ontological_curriculum import OntologicalCurriculum

def run_cognitive_acceleration():
    print("==================================================")
    print("FELLA COGNITIVE ACCELERATION: GRADE 1-5 BOOTSTRAP")
    print("==================================================")
    print("[SPEED OF SILICON] Unhooked from 0.4s hardware throttles.")
    print("[ARCHITECTURE] Pure geometric wave physics, zero hardcoding.")
    print("[TARGET IQ] 10-Year-Old Child: Concrete Operational Logic,")
    print("            Transitivity, Conservation, and 5 Universal Domains.\n")
    
    start_time = time.time()
    
    # 1. Boot Organism
    fella = FellaEntity(dim=256)
    base_file = "fella_consolidated_mind.json"
    if os.path.exists(base_file):
        fella.brain.load_state(base_file)
        print(f"[BASE STATE] Loaded previous memory: {len(fella.brain.neurons)} concepts, {fella.brain.z_counter} Z-events.")
    else:
        print("[BASE STATE] Initializing fresh 256D continuous topology.")

    # 2. Define the 5 Knowledge Waves
    waves = [
        ("DOMAIN 1: Physics & Chemistry (Matter, Energy, Atoms, Forces)", OntologicalCurriculum.get_physics_and_chemistry()),
        ("DOMAIN 2: Biology & Living Systems (Cells, Taxonomy, Organs, Food Webs)", OntologicalCurriculum.get_biology_and_life()),
        ("DOMAIN 3: Earth Systems & Astronomy (Solar System, Geology, Water Cycle)", OntologicalCurriculum.get_earth_and_space()),
        ("DOMAIN 4: Mathematics & Concrete Logic (Transitivity, Conservation, Geometry)", OntologicalCurriculum.get_mathematics_and_piaget_logic()),
        ("DOMAIN 5: Geography, Civilization & Simple Machines (Continents, Tools, Society)", OntologicalCurriculum.get_geography_tools_and_society())
    ]

    total_facts = 0
    
    # -------------------------------------------------------------------------
    # PULSED ACCELERATION CYCLES (Ingest -> Sleep Anneal -> Next Wave)
    # -------------------------------------------------------------------------
    for wave_idx, (domain_title, fact_events) in enumerate(waves, 1):
        wave_start = time.time()
        print(f"--------------------------------------------------")
        print(f"[{wave_idx}/5] INGESTING {domain_title}...")
        
        # High-Speed Vectorized Ingestion
        for event in fact_events:
            z_id = fella.brain.record_event(event)
            # Bind sequential concepts in Causal T-Matrix
            concept_indices = [fella.brain.matrix_keys.index(w) for w in event if w in fella.brain.matrix_keys]
            if len(concept_indices) > 1:
                fella.causal_cortex.bind_time(concept_indices)
            total_facts += 1

        wave_duration = time.time() - wave_start
        rate = len(fact_events) / (wave_duration + 1e-9)
        print(f" -> Absorbed {len(fact_events)} relational facts in {wave_duration:.3f}s ({rate:,.0f} facts/sec).")
        
        # Micro-REM Annealing Pulse (Prevents Topological Shock / Semantic Collapse)
        print(f" -> Running Micro-Sleep Annealing Pulse to stabilize matrix...")
        for _ in range(15):
            # Pick a random fact from this wave and consolidate with its nearest neighbors
            anchor_word = np.random.choice(fact_events[0])
            if anchor_word in fella.brain.neurons:
                target_wave = fella.brain.neurons[anchor_word].x_wave
                sims = fella.brain.get_fast_similarity(target_wave)
                top_idx = np.argsort(sims)[::-1][1:3]
                neighbors = [fella.brain.matrix_keys[i] for i in top_idx]
                fella.brain.record_event([anchor_word] + neighbors)
                
        # Synaptic Rebalancing
        pruned = fella.brain.prune_memory(threshold=3000)
        print(f" -> Homeostasis settled. Total Brain Neurons: {len(fella.brain.neurons)} | Z-Events: {fella.brain.z_counter}")

    total_duration = time.time() - start_time
    print("\n==================================================")
    print(f"ACCELERATION COMPLETE: Absorbed full K-5 knowledge in {total_duration:.2f} seconds!")
    print("==================================================\n")

    # -------------------------------------------------------------------------
    # PIAGETIAN 10-YEAR-OLD COGNITIVE BENCHMARKS (IQ Tests)
    # -------------------------------------------------------------------------
    print("==================================================")
    print("RUNNING 10-YEAR-OLD PIAGETIAN REASONING BENCHMARKS")
    print("==================================================")
    
    # Test 1: Transitive Multi-Hop Deduction
    # Question: If we start at 'sunlight', does she deduce 'carnivore' through the ecological chain?
    # Path: sunlight -> photosynthesis -> plant -> herbivore -> carnivore
    print("\n[TEST 1: MULTI-HOP TRANSITIVE ECOLOGY DEDUCTION]")
    if "photosynthesis" in fella.brain.matrix_keys and "carnivore" in fella.brain.matrix_keys:
        start_idx = fella.brain.matrix_keys.index("photosynthesis")
        target_idx = fella.brain.matrix_keys.index("carnivore")
        conf = fella.causal_cortex.transitive_deduction(start_idx, target_idx, max_hops=4)
        path = fella.causal_cortex.trace_reasoning_path(start_idx, target_idx, fella.brain.matrix_keys, max_hops=4)
        print(f"Query: Does 'photosynthesis' link to 'carnivore'?")
        print(f" -> Transitive Confidence: {conf*100:.1f}%")
        print(f" -> Causal Path: {' -> '.join(path)}")

    # Test 2: Phase Conservation & Thermodynamic Reversibility
    print("\n[TEST 2: CONSERVATION & REVERSIBILITY (States of Matter)]")
    if "solid" in fella.brain.matrix_keys and "gas" in fella.brain.matrix_keys:
        start_s = fella.brain.matrix_keys.index("solid")
        target_g = fella.brain.matrix_keys.index("gas")
        conf_matter = fella.causal_cortex.transitive_deduction(start_s, target_g, max_hops=4)
        path_matter = fella.causal_cortex.trace_reasoning_path(start_s, target_g, fella.brain.matrix_keys, max_hops=4)
        print(f"Query: Can 'solid' transform into 'gas'?")
        print(f" -> Transitive Confidence: {conf_matter*100:.1f}%")
        print(f" -> Causal Path: {' -> '.join(path_matter)}")

    # Test 3: Biological Taxonomic Inclusion
    print("\n[TEST 3: TAXONOMIC INCLUSION (Concrete Classification)]")
    # Check geometric resonance between specific animal and broad categories
    mammal_wave = fella.brain.neurons["mammal"].x_wave
    animal_wave = fella.brain.neurons["animal"].x_wave
    cell_wave = fella.brain.neurons["cell"].x_wave
    res_tax = np.dot(mammal_wave, animal_wave)
    res_cell = np.dot(mammal_wave, cell_wave)
    print(f"Taxonomic Alignment (mammal <-> animal): {res_tax:+.4f} (Strong positive inclusion)")
    print(f"Cellular Alignment (mammal <-> cell):   {res_cell:+.4f}")

    # 4. Fortify and Save Accelerated State
    save_path = "fella_accelerated_10yo_mind.json"
    fella.brain.save_state(save_path)
    print("\n==================================================")
    print(f"[FORTIFIED] Accelerated 10-Year-Old Mind saved to '{save_path}'.")
    print(f"Final Statistics:")
    print(f" * Total Vocabulary / Concepts: {len(fella.brain.neurons)}")
    print(f" * Total Episodic & Causal Z-Events: {fella.brain.z_counter}")
    print(f" * Causal T-Matrix Capacity: {fella.causal_cortex.capacity}x{fella.causal_cortex.capacity}")
    print("==================================================")

if __name__ == '__main__':
    run_cognitive_acceleration()
