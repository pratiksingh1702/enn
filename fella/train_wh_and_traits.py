"""
FELLA WH-Operators & Core ENN Trait Dynamics Trainer
===================================================
1. Grounds all 8 WH Question Operators (Who, What, Where, When, Why, How, Which, Whose)
2. Dynamically exercises and activates all 5 Core ENN Trait Attractors:
   - INQUIRE: Epistemic exploration of WH questions
   - IDENTITY: Self-awareness and core identity anchoring
   - SYNTHESIZE: Cross-tier integration (Physics <-> Biology <-> Causality)
   - ASPIRE: Drive for cognitive mastery and higher confidence
   - CAUTION: Syntactic error checking and uncertainty verification
3. Consolidates the complete mind state into fella_checkpoint.json
"""

import os
import sys
import time
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


def run_wh_and_traits_training():
    print("=" * 80)
    print("🌟 FELLA: GROUNDING ALL WH-OPERATORS & ACTIVATING ALL CORE ENN TRAITS")
    print("=" * 80)
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    brain.boot_foundations()
    
    # -------------------------------------------------------------------------
    # PART 1: Grounding WH-Inquisitive Concepts & Functional Operators
    # -------------------------------------------------------------------------
    print("\n[Part 1/3]: Grounding WH Inquisitive Operators into Cognitive Manifold...")
    wh_assertions = [
        "Who inquires about actors identities and living beings",
        "What inquires about definitions properties and physical matter",
        "Where inquires about spatial locations environments and space",
        "When inquires about time cycles and temporal moments",
        "Why inquires about scientific causal laws and reasons",
        "How inquires about dynamic processes mechanisms and transformations",
        "Which inquires about selecting distinct concepts",
        "Whose inquires about social bonds and relationships"
    ]
    for s in wh_assertions:
        brain.lang.ingest_continuous_stream(s, target_tier=4)
        print(f"  ✓ Grounded Operator: \"{s}\"")

    # -------------------------------------------------------------------------
    # PART 2: Systematically Exercising All 5 Core ENN Trait Attractors
    # -------------------------------------------------------------------------
    print("\n[Part 2/3]: Exercising All 5 Core ENN Trait Attractors...")
    
    trait_scenarios = [
        ("INQUIRE", np.array([0.95, 0.2, 0.85, 0.3]), "Why does heat from the sun evaporate water?"),
        ("IDENTITY", np.array([0.15, 0.3, 0.2, 0.95]), "Who are you and what is your mind?"),
        ("SYNTHESIZE", np.array([0.3, 0.95, 0.65, 0.8]), "How do sunlight and water combine in photosynthesis?"),
        ("ASPIRE", np.array([0.85, 0.85, 0.95, 0.7]), "You are learning and mastering language beautifully!"),
        ("CAUTION", np.array([0.1, 0.1, 0.2, 0.15]), "The radiating sun is the")
    ]
    
    for trait_name, drive_vector, test_input in trait_scenarios:
        # Step trait field with drive
        active_trait = brain.trait_field.step(external_drive=drive_vector)
        res = brain.converse(test_input)
        print(f"\n  🌀 [Target Trait: {trait_name}] -> Active Trait: {res['active_trait']}")
        print(f"     Input > \"{test_input}\"")
        print(f"     FELLA > {res['last_response']}")

    # -------------------------------------------------------------------------
    # PART 3: Comprehensive WH-Word Interactive Verification Suite
    # -------------------------------------------------------------------------
    print("\n[Part 3/3]: Running Interactive WH-Word Verification Suite...")
    wh_test_suite = [
        ("WHO", "Who are you?"),
        ("WHO", "Who are friends?"),
        ("WHAT", "What is the sun?"),
        ("WHAT", "What is gravity?"),
        ("WHERE", "Where do stars glow?"),
        ("WHERE", "Where does water flow?"),
        ("WHEN", "When does the sun radiate light?"),
        ("WHEN", "When do stars glow?"),
        ("WHY", "Why do objects fall?"),
        ("WHY", "Why does the sun provide warmth?"),
        ("HOW", "How do plants grow?"),
        ("HOW", "How does rain form?")
    ]
    
    for category, query in wh_test_suite:
        res = brain.converse(query)
        print(f"\n  [{category}] Query > \"{query}\"")
        print(f"  FELLA [{res['active_trait']} | Z={res.get('z_focus', 4.0):.1f}] > {res['last_response']}")

    # Final Dream Consolidation
    print("\n🌙 Consolidating Mind State via Homeostatic Dream...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Reverberated activation waves across {dream_res['reverberated_neurons']} neurons.")
    
    # Save fortified checkpoint
    brain.save_state(checkpoint_path)
    print(f"\n💾 Preserved fully activated state to {checkpoint_path}")
    
    tel = brain.get_telemetry()
    print("=" * 80)
    print(f"🎉 WH-OPERATORS GROUNDED & ALL TRAITS ACTIVATED!")
    print(f"• Total Active Neurons: {tel['total_neurons']}")
    print(f"• Total Synapses: {tel['synapse_stats']['total_synapses']}")
    print(f"• Dominant Trait: {brain.trait_field.active_trait}")
    print(f"• Metacognitive Confidence: {tel['self_confidence']:.3f}")
    print("=" * 80)


if __name__ == "__main__":
    run_wh_and_traits_training()
