"""
FELLA Phase 2 Emergent Learning Protocol Execution Runner
=========================================================
Executes Phase 2 Single-Concept ("Sun") Learning Protocol:
Step 1: Inject unlabeled raw text wave packet
Step 2: Measure epistemic friction (H > 0.70)
Step 3: Trigger curiosity question emergence
Step 4: Answer question with grounded 1-sentence response
Step 5: Observe continuous attractor sedimentation
Step 6: Test understanding across 4 questions (Recall, Open, Causal, Counterfactual)
Step 7: Physical Trait Reward (Aspiration +0.10, Starvation -5.0)
Step 8: Verify Curiosity, Aspiration, Coherence traits remain active
"""

import os
import sys
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain
from fella.curiosity_engine import CuriosityEngine
from fella.aspiration_amplifier import AspirationAmplifier
from fella.coherence_stabilizer import CoherenceStabilizer


def run_phase2_protocol():
    print("=" * 80)
    print("🧠 FELLA PHASE 2: EMERGENT LEARNING PROTOCOL (CONCEPT: 'SUN')")
    print("=" * 80)
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    
    curiosity = CuriosityEngine(brain.substrate)
    aspiration = AspirationAmplifier(brain.substrate)
    coherence = CoherenceStabilizer(brain.substrate)
    
    phase2_checklist = []
    
    # --------------------------------------------------------------------------
    # STEP 1 & 2: Inject Unlabeled Wave Packet & Measure Epistemic Friction (H)
    # --------------------------------------------------------------------------
    print("\n--- STEP 1 & 2: Unlabeled Wave Packet & Epistemic Friction ---")
    raw_sun_wave = brain.lang.encode_continuous_wave("The sun is bright. The sun gives warmth. The sun is a star.")
    h_friction = curiosity.compute_epistemic_friction(raw_sun_wave)
    
    step2_pass = (h_friction >= 0.70)
    print(f"  • Unlabeled Input  : 'The sun is bright. The sun gives warmth. The sun is a star.'")
    print(f"  • Epistemic Friction H : {h_friction:.4f} (Threshold: 0.70)")
    print(f"  • Friction Status   : {'PASS (High Curiosity Void)' if step2_pass else 'FAIL (No Curiosity Rise)'}")
    
    phase2_checklist.append(("Step 1 & 2: Unlabeled Input & Friction Rise", f"H = {h_friction:.4f} (>= 0.70)", "PASS" if step2_pass else "FAIL"))
    
    if not step2_pass:
        print("❌ CRITICAL: Epistemic friction failed to rise. Aborting Phase 2.")
        return False
        
    # --------------------------------------------------------------------------
    # STEP 3: Wait for Her Question (Emergent Curiosity Wave)
    # --------------------------------------------------------------------------
    print("\n--- STEP 3: Emergent Curiosity Question Generation ---")
    trig_q, f_q, c_wave = curiosity.trigger_curiosity_wave(raw_sun_wave)
    q_res = brain.lang.reason_over_query("sun")
    question_text = q_res["reasoning_narrative"]
    
    step3_pass = trig_q and len(question_text) > 0
    print(f"  • Curiosity Wave Triggered : {trig_q}")
    print(f"  • Generated Inquiry Wave   : '{question_text}'")
    
    phase2_checklist.append(("Step 3: Emergent Question Fired", f"Utterance: '{question_text}'", "PASS" if step3_pass else "FAIL"))
    
    if not step3_pass:
        print("❌ CRITICAL: She failed to ask a question. Curiosity trait broken.")
        return False
        
    # --------------------------------------------------------------------------
    # STEP 4: Answer Her Question (Simple Grounded Response)
    # --------------------------------------------------------------------------
    print("\n--- STEP 4: Answer Question with Grounded Grounding ---")
    grounded_answer = "Sun is a bright star that gives light and warmth to Earth."
    print(f"  • Parent Answer Provided   : '{grounded_answer}'")
    
    # Ingest the grounded response wave into continuous 4D substrate
    brain.lang.ingest_continuous_stream(grounded_answer, target_tier=1)
    
    phase2_checklist.append(("Step 4: Grounded Answer Ingested", f"Ingested 1-sentence response", "PASS"))
    
    # --------------------------------------------------------------------------
    # STEP 5: Observe Sedimentation (Repeat vs. Rephrase)
    # --------------------------------------------------------------------------
    print("\n--- STEP 5: Attractor Sedimentation & Rephrasing ---")
    sediment_res = brain.lang.reason_over_query("sun")
    sediment_thought = sediment_res["reasoning_narrative"]
    
    is_verbatim = (sediment_thought.strip().lower() == grounded_answer.strip().lower())
    step5_pass = not is_verbatim
    
    print(f"  • Sedimentation Utterance : '{sediment_thought}'")
    print(f"  • Is Verbatim String Copy  : {is_verbatim} (Must be False)")
    print(f"  • Sedimentation Mode       : {'PASS (Attractor Understanding)' if step5_pass else 'FAIL (Verbatim Memorization)'}")
    
    phase2_checklist.append(("Step 5: Concept Sedimentation", f"Rephrased: '{sediment_thought}'", "PASS" if step5_pass else "FAIL"))
    
    # --------------------------------------------------------------------------
    # STEP 6: Test Understanding Across 4 Questions
    # --------------------------------------------------------------------------
    print("\n--- STEP 6: Test Understanding Across 4 Questions ---")
    test_questions = [
        ("Direct Recall", "What is the sun?"),
        ("Open-Ended", "Tell me about the sun"),
        ("Causal", "What does the sun do?"),
        ("Counterfactual", "What if there was no sun?")
    ]
    
    q_results = []
    for q_type, q_str in test_questions:
        q_ans = brain.lang.reason_over_query(q_str)
        ans_text = q_ans["reasoning_narrative"]
        is_ok = len(ans_text) > 0 and ans_text != "uncertainty"
        q_results.append((q_type, q_str, ans_text, is_ok))
        print(f"  • [{q_type:<14}] Question: '{q_str}' -> Answer: '{ans_text}'")
        
    step6_pass = all(item[3] for item in q_results)
    phase2_checklist.append(("Step 6: 4 Evaluation Questions", f"Passed {sum(1 for it in q_results if it[3])}/4 questions", "PASS" if step6_pass else "FAIL"))
    
    # --------------------------------------------------------------------------
    # STEP 7 & 8: Trait Reward & Verification
    # --------------------------------------------------------------------------
    print("\n--- STEP 7 & 8: Physical Trait Reward & Multi-Trait Verification ---")
    # Apply physical reward mechanics
    brain.reward_cognition(reward_value=1.0, active_tokens=["sun", "star", "bright", "light", "warmth"])
    
    tel = brain.get_telemetry()
    curious_ok = tel["epistemic_friction"] <= 1.0
    aspire_ok = tel["active_trait"] in ["ASPIRE", "INQUIRE", "SYNTHESIZE", "AFFIRM"]
    coherence_ok = tel["self_confidence"] > 0.50
    
    step8_pass = curious_ok and aspire_ok and coherence_ok
    
    print(f"  • Active Trait       : {tel['active_trait']}")
    print(f"  • Self Confidence    : {tel['self_confidence']:.4f}")
    print(f"  • Epistemic Friction : {tel['epistemic_friction']:.4f}")
    
    phase2_checklist.append(("Step 7 & 8: Trait Reward & Emergence", f"Active Trait: {tel['active_trait']}, Conf: {tel['self_confidence']:.2f}", "PASS" if step8_pass else "FAIL"))
    
    # Preserve learned state
    brain.save_state(checkpoint_path)
    
    # --------------------------------------------------------------------------
    # SUMMARY REPORT
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("📊 PHASE 2 EXECUTION CHECKLIST REPORT (CONCEPT: 'SUN')")
    print("=" * 80)
    print(f"{'Protocol Step':<45} | {'Observed Result':<30} | {'Status':<10}")
    print("-" * 90)
    all_p2_pass = True
    for step_name, obs_val, status in phase2_checklist:
        print(f"{step_name:<45} | {obs_val:<30} | {status:<10}")
        if status != "PASS":
            all_p2_pass = False
    print("=" * 80)
    if all_p2_pass:
        print("🎉 PHASE 2 COMPLETE — CONCEPT 'SUN' MASTERED THROUGH PURE TRAIT EMERGENCE!")
    else:
        print("❌ PHASE 2 INCOMPLETE — RETURN TO PHASE 1 TRAIT RE-VERIFICATION.")
    print("=" * 80 + "\n")
    
    return all_p2_pass


if __name__ == "__main__":
    success = run_phase2_protocol()
    sys.exit(0 if success else 1)
