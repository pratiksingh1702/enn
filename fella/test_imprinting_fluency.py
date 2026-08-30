"""
FELLA: Resonant Imprinting Fluency & Coherence Evaluation Suite
==============================================================
Exhaustively evaluates FELLA's 4D continuous field post-imprinting across:
1. Simple Kernels & SVO Structure
2. Complex Subordination & Causal Explanations
3. Semantic Conceptual Grounding (Sun, Stars, Water, Gravity, Friends, Volcanoes, Plants, Lightning)
4. Conversational Reasoning & Q&A
5. Epistemic Humility on Unknown Concepts
"""

import sys
import os
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


FLUENCY_TEST_BATTERY = [
    # 1. Core Physical Entities & Laws
    ("What is the sun?", ["sun", "star", "radiates", "light", "warms", "earth"]),
    ("What is the moon?", ["moon", "satellite", "orbits", "earth", "space"]),
    ("What is gravity?", ["gravity", "force", "attracts", "matter", "center"]),
    ("What is a black hole?", ["black", "holes", "curvature", "traps", "light"]),
    ("What is water?", ["water", "flows", "clouds", "rain", "evaporates"]),
    ("What are stars?", ["stars", "glow", "plasma", "cosmos", "constellations"]),
    ("What is fire?", ["fire", "emits", "heat", "light", "transforming"]),
    ("What is lightning?", ["lightning", "discharges", "electrical", "energy", "clouds"]),
    ("How do plants grow?", ["plants", "grow", "absorbing", "sunlight", "photosynthesis", "oxygen"]),
    ("What is friendship?", ["friends", "friend", "trust", "kindness", "social", "bonds"]),
    
    # 2. Causal & Scientific Questions
    ("Why does water evaporate into clouds?", ["water", "evaporates", "thermal", "clouds"]),
    ("How does the sun warm the planet earth?", ["sun", "radiates", "thermal", "energy", "warms", "earth"]),
    ("Why cannot light escape a black hole?", ["light", "escape", "gravitational", "curvature", "traps"]),
    ("How do clouds produce rain?", ["clouds", "condenses", "rain", "water"]),
    ("What produces oxygen on earth?", ["plants", "photosynthesis", "oxygen", "sunlight"]),
    
    # 3. Novel Concepts (Epistemic Humility)
    ("What is quantum entanglement?", ["uncertainty"]),
    ("How do airplanes fly in the sky?", ["uncertainty"]),
    ("What is artificial intelligence?", ["uncertainty"]),
    ("What are ancient pyramids in Egypt?", ["uncertainty"])
]


def run_fluency_evaluation(checkpoint_path: str = "fella_checkpoint.json"):
    print("=" * 80)
    print("🔬 FELLA POST-IMPRINTING COMPREHENSIVE FLUENCY BENCHMARK")
    print("=" * 80)
    
    brain = FellaBrain.load_state(checkpoint_path)
    print(f"📂 Checkpoint loaded! Neurons: {len(brain.substrate.neurons)} | Synapses: {brain.substrate.get_synapse_stats()['total_synapses']}\n")
    
    total = len(FLUENCY_TEST_BATTERY)
    passed = 0
    
    for idx, (query, expected_kws) in enumerate(FLUENCY_TEST_BATTERY, 1):
        res = brain.lang.reason_over_query(query)
        narrative = res["reasoning_narrative"]
        seed = res["seed_concept"]
        score = res["evaluation_score"]
        is_unc = res["is_uncertain"]
        rejections = res["rejected_count"]
        
        tokens = narrative.lower().split()
        hits = [kw for kw in expected_kws if any(kw.lower() in t for t in tokens)]
        
        is_pass = False
        if "uncertainty" in expected_kws:
            is_pass = is_unc or "uncertainty" in narrative.lower()
        else:
            is_pass = (len(hits) >= 1) and ("essential phenomenon" not in narrative.lower()) and len(tokens) >= 3
            
        if is_pass:
            passed += 1
            status = "✓ PASS"
        else:
            status = "✗ FLAWED"
            
        print(f"[{idx:02d}] Q: \"{query}\"")
        print(f"     FELLA Output : \"{narrative}\"")
        print(f"     Critic Info  : Seed '{seed}' | Score: {score:.3f} | Rejected: {rejections} | Status: {status} (Hits: {hits})\n")
        
    print("=" * 80)
    print(f"📊 FINAL SCORE: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 80)


if __name__ == "__main__":
    run_fluency_evaluation()
