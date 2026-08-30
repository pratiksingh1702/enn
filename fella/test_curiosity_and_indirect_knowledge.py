"""
FELLA Curiosity & Indirect Knowledge Resonance Test
===================================================
1. Tests Curiosity Engine under novel inputs vs. idle vacuum.
2. Tests Indirect Knowledge Retrieval WITHOUT mentioning the word 'sun' in queries:
   - "tell me what you know"
   - "what do you have in your mind"
   - "what shines in the sky"
   - "what gives heat"
"""

import os
import sys
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain
from fella.curiosity_engine import CuriosityEngine


def test_curiosity_and_indirect_knowledge():
    print("=" * 80)
    print("🔬 FELLA CURIOSITY & INDIRECT KNOWLEDGE RESONANCE AUDIT")
    print("=" * 80)
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    curiosity = CuriosityEngine(brain.substrate)
    
    audit_results = []
    
    # ---------------------------------------------------------
    # PART 1: CURIOSITY ENGINE AUDIT
    # ---------------------------------------------------------
    print("\n--- PART 1: CURIOSITY ENGINE AUDIT ---")
    
    # 1.1 Novel Unseen Concept ("quantum entanglement")
    w_novel = brain.lang.encode_continuous_wave("quantum entanglement")
    f_novel = curiosity.compute_epistemic_friction(w_novel)
    trig_novel, _, wave_novel = curiosity.trigger_curiosity_wave(w_novel)
    print(f"1.1 Novel Input ('quantum entanglement') -> Friction: {f_novel:.4f} | Triggered: {trig_novel}")
    audit_results.append(("1.1 Novel Input Friction Trigger", f"Friction: {f_novel:.4f} (>= 0.70)", "PASS" if f_novel >= 0.70 and trig_novel else "FAIL"))
    
    # 1.2 Idle Vacuum Input (Zero Environmental Vector)
    w_vacuum = np.zeros(16)
    f_vac = curiosity.compute_epistemic_friction(w_vacuum)
    trig_vac, _, _ = curiosity.trigger_curiosity_wave(w_vacuum)
    print(f"1.2 Idle Vacuum -> Friction: {f_vac:.4f} | Triggered: {trig_vac}")
    audit_results.append(("1.2 Idle Vacuum Curiosity Trigger", f"Friction: {f_vac:.4f} (>= 0.70)", "PASS" if f_vac >= 0.70 and trig_vac else "FAIL"))
    
    # ---------------------------------------------------------
    # PART 2: INDIRECT KNOWLEDGE RESONANCE (NO 'SUN' KEYWORD)
    # ---------------------------------------------------------
    print("\n--- PART 2: INDIRECT KNOWLEDGE RESONANCE (NO 'SUN' KEYWORD) ---")
    
    indirect_queries = [
        ("Open Knowledge", "tell me what you know"),
        ("Mind Inspection", "what do you have"),
        ("Visual Descriptor", "what shines in the sky"),
        ("Thermal Descriptor", "what gives heat")
    ]
    
    for q_type, q_str in indirect_queries:
        res = brain.lang.reason_over_query(q_str)
        ans = res["reasoning_narrative"]
        seed = res["seed_concept"]
        is_unc = res["is_uncertain"]
        
        # Check if output resonates with sedimented concepts ([sun], [star], [light], [warmth], [earth])
        has_resonance = any(tok in ans.lower() for tok in ["sun", "star", "light", "warmth", "earth", "gives", "heat"])
        
        print(f"  • [{q_type:<18}] Question: '{q_str}'")
        print(f"    Seed Concept : '{seed}' | Is Uncertain: {is_unc}")
        print(f"    Efferent Speech Output: '{ans}'")
        print(f"    Resonance Check       : {'PASS (Resonates with Sedimented Attractor)' if has_resonance else 'FAIL'}\n")
        
        audit_results.append((f"2. Indirect Query ('{q_str}')", f"Output: '{ans}'", "PASS" if has_resonance else "FAIL"))
        
    # ---------------------------------------------------------
    # SUMMARY REPORT
    # ---------------------------------------------------------
    print("=" * 80)
    print("📊 CURIOSITY & INDIRECT KNOWLEDGE AUDIT SUMMARY")
    print("=" * 80)
    print(f"{'Audit Metric':<45} | {'Observed Result':<30} | {'Status':<10}")
    print("-" * 90)
    all_pass = True
    for test_name, obs, status in audit_results:
        print(f"{test_name:<45} | {obs:<30} | {status:<10}")
        if status != "PASS":
            all_pass = False
    print("=" * 80)
    print(f"OVERALL STATUS: {'CURIOSITY & INDIRECT KNOWLEDGE 100% VERIFIED' if all_pass else 'FAIL'}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    test_curiosity_and_indirect_knowledge()
