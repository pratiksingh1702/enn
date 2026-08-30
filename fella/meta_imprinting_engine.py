"""
FELLA Meta-Learning Imprinting Engine (5 Cycles x 20,000 Patterns = 100,000 Exposures)
=====================================================================================
100% Pure Continuous ENN Physics:
- Extracts structural frequency patterns into compressed attractors (PEL).
- Binds directional Hebbian synaptic highways W_ij across 5 hierarchical categories.
- Runs 5 full consolidation cycles with homeostatic anti-Hebbian wave pruning.
- Benchmarks pattern generalization and first-principles counterfactual reasoning.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import time
import json
import numpy as np
from typing import Dict, Any, List
from fella.fella_brain import FellaBrain
from fella.pattern_engine import PatternExtractionLayer, PatternReasoningEngine
from fella.meta_curriculum_generator import MetaPatternCurriculumGenerator


def run_meta_imprinting_pipeline(num_cycles: int = 5):
    print("=" * 80)
    print("🌌 FELLA: META-LEARNING PATTERN ARCHITECTURE IMPRINTING PIPELINE")
    print(f"   Target: {num_cycles} Cycles x 20,000 Patterns = {num_cycles * 20000:,} Pattern Trajectories")
    print("=" * 80)
    
    t_start = time.time()
    
    # 1. Initialize Substrate & Meta-Learning Engine
    brain = FellaBrain.load_state("fella_checkpoint.json")
    pel = PatternExtractionLayer(dim=brain.substrate.dim)
    re_engine = PatternReasoningEngine(pel, brain.substrate)
    
    print(f"\n📂 Initial Substrate State: {len(brain.substrate.neurons)} Living Neurons | Axiomatic Basins: {len(pel.attractors)}")
    
    # 2. Generate 20,000 Pattern Curriculum
    print("\n📚 Generating 20,000 Structured Pattern Curriculum...")
    gen = MetaPatternCurriculumGenerator(seed=42)
    curriculum = gen.generate_full_20k_curriculum()
    print(f"✓ Generated {len(curriculum):,} unique grounded pattern sentences across 5 categories.")
    
    # 3. Execute 5 Full Imprinting Cycles
    for cycle in range(1, num_cycles + 1):
        c_start = time.time()
        print(f"\n" + "#" * 80)
        print(f"⚡ CYCLE {cycle}/{num_cycles}: Imprinting 20,000 Pattern Trajectories...")
        print("#" * 80)
        
        lr = 0.55 * (0.88 ** (cycle - 1))
        
        # Batch ingestion with pattern extraction
        batch_size = 500
        for b_idx in range(0, len(curriculum), batch_size):
            batch = curriculum[b_idx:b_idx + batch_size]
            for sentence in batch:
                ingested = brain.lang.ingest_continuous_stream(sentence, target_tier=3, learning_rate=lr)
                if len(ingested) >= 3:
                    # Extract continuous wave harmonics into PEL
                    wave_seq = [n.x for n in ingested]
                    pattern_sig = pel.extract_harmonic_signature(wave_seq)
                    pel.bind_or_reinforce_pattern(pattern_sig, tier_z=3, neuron_ids=[n.id for n in ingested])
                    
        # Homeostatic wave consolidation after each cycle
        print(f"🌙 Running Homeostatic Wave Consolidation after Cycle {cycle}...")
        brain.substrate.consolidate_homeostatic_wave(threshold=0.08, decay=0.04)
        
        elapsed = time.time() - c_start
        n_count = len(brain.substrate.neurons)
        syn_stats = brain.substrate.get_synapse_stats()
        pat_count = len(pel.attractors)
        print(f"✓ Cycle {cycle} Complete in {elapsed:.2f}s! Neurons: {n_count} | Synapses: {syn_stats['total_synapses']} | Pattern Attractors: {pat_count}")
        
    # 4. First-Principles Causal Benchmark
    print("\n" + "=" * 80)
    print("🏆 FINAL FIRST-PRINCIPLES & MULTI-HOP CAUSAL REASONING BENCHMARK")
    print("=" * 80)
    
    test_queries = [
        "What is the sun?",
        "What is water?",
        "What is air?",
        "What is friendship?",
        "What is gravity?",
        "What is a black hole?",
        "What is quantum computing?"
    ]
    
    print("\n--- Direct Energy Discharge Query Recall ---")
    for q in test_queries:
        res = brain.lang.reason_over_query(q)
        print(f"Q: {q}")
        print(f"   FELLA: \"{res['reasoning_narrative']}\" (Score: {res['evaluation_score']:.3f} | Drafts: {res['rejected_count'] + 1})\n")
        
    # 5. First-Principles Counterfactual Reasoning Test
    print("--- First-Principles Axiomatic Causal Trajectories ---")
    for seed_word in ["sun", "water", "gravity", "friendship"]:
        seed_neurons = [n.id for n in brain.substrate.neurons.values() if n.text.lower() == seed_word and n.tier_z > 0]
        if seed_neurons:
            sid = seed_neurons[0]
            causal_path_ids = re_engine.infer_first_principles_trajectory(sid, axiomatic_type="axiom_causality")
            causal_tokens = [brain.substrate.neurons[nid].text for nid in causal_path_ids if nid in brain.substrate.neurons]
            print(f"Concept: '{seed_word}' -> Causal Flow: {' -> '.join(causal_tokens)}")
            
    # 6. Save Fortified Checkpoint
    brain.save_state("fella_checkpoint.json")
    total_time = time.time() - t_start
    print(f"\n💾 Preserved Fortified Meta-Learning State in 'fella_checkpoint.json' (Total Time: {total_time:.2f}s)")
    print("🎉 100,000-Exposure Meta-Learning Pattern Protocol Complete!")


if __name__ == "__main__":
    run_meta_imprinting_pipeline(num_cycles=5)

