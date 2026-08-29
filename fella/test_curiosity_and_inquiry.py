"""
FELLA Live Curiosity, Follow-Up Inquiry & Autonomous Learning Test Suite
========================================================================
Tests:
1. Novel Concept Epistemic Friction & Vacuum Logging (Curiosity Drive)
2. Trait Field Dynamics (INQUIRE / ASPIRE / AFFIRM Attractors)
3. Autonomous Curiosity Cycle with Local Ollama Mentor (Live Integration)
4. Homeostatic Dream Consolidation (Synaptic Strengthening & Pruning)
5. Multi-Turn Conversational Reasoning along Conductance Highways
"""

import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


def run_curiosity_and_inquiry_tests():
    print("=" * 80)
    print("🔬 FELLA: TESTING LIVE CURIOSITY, FOLLOW-UP INQUIRIES & LEARNING DYNAMICS")
    print("=" * 80)
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    brain.boot_foundations()
    
    # -------------------------------------------------------------------------
    # TEST 1: Novel Concept Injection & Epistemic Vacuum Detection
    # -------------------------------------------------------------------------
    print("\n--- [TEST 1]: Novel Concept Injection & Epistemic Friction ---")
    novel_inputs = [
        "Volcanoes erupt molten liquid lava from deep within the earth",
        "Black holes possess extreme gravitational curvature that traps light",
        "Mitochondria generate cellular energy through biochemical respiration"
    ]
    
    for inp in novel_inputs:
        res = brain.converse(inp)
        friction = res.get("epistemic_friction", 0.0)
        active_trait = res.get("active_trait", "INQUIRE")
        vacuums = list(brain.observer.vacuums.values())
        
        print(f"\nParent/User > \"{inp}\"")
        print(f"FELLA [{active_trait} | Epistemic Friction: {friction:.3f}] >")
        print(f"  Raw Trajectory: {res['last_response']}")
        print(f"  Pending Vacuums in Inward Observer: {len(vacuums)}")
        if vacuums:
            latest_vac = vacuums[-1]
            print(f"  ⚡ Latest Epistemic Vacuum: '{latest_vac.concept_query}' (Tension: {latest_vac.tension:.3f}, Resolved: {latest_vac.resolved})")

    # -------------------------------------------------------------------------
    # TEST 2: Autonomous Curiosity Cycle (Querying Ollama Mentor)
    # -------------------------------------------------------------------------
    print("\n--- [TEST 2]: Autonomous Curiosity Cycle (Querying Ollama Mentor) ---")
    print(f"Mentor Online: {brain.mentor.is_online} (Model: {brain.mentor.active_model})")
    
    unresolved_count = len([v for v in brain.observer.vacuums.values() if not v.resolved])
    print(f"Starting Curiosity Cycle on {unresolved_count} unresolved vacuums...")
    
    for cycle_idx in range(min(2, unresolved_count)):
        print(f"\n🌀 [Curiosity Cycle {cycle_idx + 1}]: Resolving highest-tension vacuum...")
        result = brain.autonomous_curiosity_cycle()
        if result:
            print(f"  ✓ Vacuum '{result['concept']}' resolved by mentor {result['mentor_model']}!")
            print(f"    Explanation: \"{result['explanation'][:100]}...\"")
            print(f"    Nodes Ingested: {result.get('ingested_nodes', 0)} onto Tier Z={result['tier_z']}")
            print(f"    New Synapses Formed: {result['total_synapses']}")
        else:
            print("  No pending vacuums to resolve.")

    # -------------------------------------------------------------------------
    # TEST 3: Homeostatic Sleep & Dream Consolidation
    # -------------------------------------------------------------------------
    print("\n--- [TEST 3]: Homeostatic Dream Consolidation ---")
    print("Initiating unsupervised activation wave reverberation & synaptic decay...")
    dream_res = brain.dream_consolidation()
    print(f"  ✓ Reverberated activation waves across {dream_res['reverberated_neurons']} neurons.")
    print(f"  ✓ Pruned {dream_res['pruned_synapses']} noisy synapses below critical threshold.")
    print(f"  ✓ Metacognitive Confidence Restored: {dream_res['restored_confidence']:.3f}")

    # -------------------------------------------------------------------------
    # TEST 4: Post-Learning Conversational Probing
    # -------------------------------------------------------------------------
    print("\n--- [TEST 4]: Probing FELLA on Newly Learned Knowledge ---")
    probe_queries = [
        "What is a volcano?",
        "What happens in a black hole?",
        "What is gravity?",
        "How do plants produce oxygen?"
    ]
    for q in probe_queries:
        res = brain.converse(q)
        print(f"\nUser > \"{q}\"")
        print(f"FELLA [{res['active_trait']} | Z={res.get('z_focus', 4.0):.1f}] > {res['last_response']}")

    # -------------------------------------------------------------------------
    # Save Fortified Checkpoint
    # -------------------------------------------------------------------------
    brain.save_state(checkpoint_path)
    print(f"\n💾 Preserved fortified state to {checkpoint_path}")
    
    tel = brain.get_telemetry()
    print("=" * 80)
    print("🎉 CURIOSITY & INQUIRY TEST COMPLETE!")
    print(f"• Total Physical Neurons: {tel['total_neurons']}")
    print(f"• Total Synapses (W_ij): {tel['synapse_stats']['total_synapses']}")
    print(f"• Active Trait: {brain.trait_field.active_trait}")
    print(f"• Self-Confidence: {tel['self_confidence']:.3f}")
    print("=" * 80)


if __name__ == "__main__":
    run_curiosity_and_inquiry_tests()
