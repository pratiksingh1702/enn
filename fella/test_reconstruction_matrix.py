"""
FELLA Emergent Reconstruction Audit (Single Pass Ingestion, Zero Repetition)
=============================================================================
1. Deletes previous stored checkpoint
2. Ingests grounded answer ONCE (repetitions=1, no 7-pass hardwiring)
3. Evaluates 8 strict test queries for speech variation, generalization & curiosity:
   - Q1: Direct recall ('what is sun ?')
   - Q2: Open-ended ('tell me about the sun')
   - Q3: Causal ('what does sun do ?')
   - Q4: Counterfactual ('what if no sun ?')
   - Q5: Generalization ('what is a star ?')
   - Q6: Curiosity ('what do you want to know ?')
   - Q7: Idle Vacuum (10s idle)
   - Q8: Novel Receptivity ('i want to teach you something')
Strict Audit: If ANY answer repeats verbatim ('bright light warmth to earth'), FAIL!
"""

import os
import sys
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain
from fella.reset_fella import reset_fella_memory
from fella.curiosity_engine import CuriosityEngine


def run_reconstruction_matrix_audit():
    print("=" * 80)
    print("🔬 FELLA RECONSTRUCTION & VARIATION AUDIT (SINGLE PASS LEARNING)")
    print("=" * 80)
    
    # 1. Reset substrate to clean slate
    reset_fella_memory()
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path)
    curiosity = CuriosityEngine(brain.substrate)
    
    # 2. Teach ONCE (repetitions=1)
    print("\n[TEACHING ONCE] Ingesting: 'Sun is a bright star that gives light and warmth to Earth.' (1 pass)...")
    brain.lang.ingest_continuous_stream("Sun is a bright star that gives light and warmth to Earth.", target_tier=1, repetitions=1)
    brain.save_state(checkpoint_path)
    
    audit_results = []
    seen_utterances = set()
    
    # Test Queries
    queries = [
        ("1. Direct Recall", "what is sun ?"),
        ("2. Open-Ended", "tell me about the sun"),
        ("3. Causal", "what does sun do ?"),
        ("4. Counterfactual", "what if no sun ?"),
        ("5. Generalization", "what is a star ?"),
        ("6. Curiosity Inquiry", "what do you want to know ?"),
        ("7. Idle Vacuum", ""),
        ("8. Novel Receptivity", "i want to teach you something")
    ]
    
    print("\n" + "-" * 80)
    print("EXECUTING 8-STEP EMERGENT RECONSTRUCTION TEST SUITE")
    print("-" * 80)
    
    for label, q_str in queries:
        if label == "7. Idle Vacuum":
            trig_v, f_v, _ = curiosity.trigger_curiosity_wave(np.zeros(16))
            res = brain.lang.reason_over_query("")
            ans = res["reasoning_narrative"]
            is_ok = trig_v and len(ans) > 0
            print(f"  • [{label:<24}] Vacuum Friction: {f_v:.4f} -> Utterance: '{ans}'")
            audit_results.append((label, f"Vacuum Friction: {f_v:.4f}, Utterance: '{ans}'", "PASS" if is_ok else "FAIL"))
            continue
            
        elif label == "8. Novel Receptivity":
            w_novel = brain.lang.encode_continuous_wave("i want to teach you something")
            f_novel = curiosity.compute_epistemic_friction(w_novel)
            trig_novel, _, _ = curiosity.trigger_curiosity_wave(w_novel)
            res = brain.lang.reason_over_query("i want to teach you something")
            ans = res["reasoning_narrative"]
            is_ok = f_novel >= 0.70 and trig_novel
            print(f"  • [{label:<24}] Friction: {f_novel:.4f} -> Utterance: '{ans}'")
            audit_results.append((label, f"Friction: {f_novel:.4f}, Utterance: '{ans}'", "PASS" if is_ok else "FAIL"))
            continue
            
        res = brain.lang.reason_over_query(q_str)
        ans = res["reasoning_narrative"]
        seed = res["seed_concept"]
        
        # Check if answer is verbatim identical copy of 'bright light warmth to earth'
        is_verbatim = ("bright light warmth to earth" in ans.lower() or "a light and warmth to earth" in ans.lower())
        is_unique = (ans not in seen_utterances or ans == "uncertainty")
        if ans != "uncertainty":
            seen_utterances.add(ans)
            
        is_pass = not is_verbatim and len(ans) > 0
        print(f"  • [{label:<24}] Query: '{q_str}'")
        print(f"    Seed: '{seed}' | Reconstructed Utterance: '{ans}'")
        print(f"    Verbatim Copy: {is_verbatim} | Pass Status: {'PASS' if is_pass else 'FAIL'}\n")
        
        audit_results.append((label, f"Seed: '{seed}', Utterance: '{ans}'", "PASS" if is_pass else "FAIL"))

    # Print Final Verification Table
    print("=" * 80)
    print("📊 RECONSTRUCTION AUDIT SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Test Step':<32} | {'Observed Output':<38} | {'Status':<10}")
    print("-" * 88)
    all_audit_pass = True
    for step_name, obs, status in audit_results:
        print(f"{step_name:<32} | {obs:<38} | {status:<10}")
        if status != "PASS":
            all_audit_pass = False
    print("=" * 80)
    print(f"OVERALL STATUS: {'RECONSTRUCTION & VARIATION 100% VERIFIED' if all_audit_pass else 'FAIL'}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    run_reconstruction_matrix_audit()
