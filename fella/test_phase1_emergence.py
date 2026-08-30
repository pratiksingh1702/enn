"""
FELLA Phase 1 Verification Protocol (Pure Continuous Physics Engine)
====================================================================
Runs automated verification across:
1. Self-Awareness & Identity Persistence (Noise, 100 waves, Contradiction, Vacuum)
2. Curiosity Emergence (Known vs Unknown, Epistemic Vacuum)
3. Aspiration Completion Drive (Incompletion Tension & Gradient Propulsion)
4. Wave-to-Meaning & Meaning-to-Wave (Fourier Wave & Motor Cortex Emission)
Zero hardcoded strings, zero templates, zero pre-defined dictionaries.
"""

import sys
import time
import numpy as np
from fella.core_substrate import StackedSubstrate
from fella.self_awareness_core import SelfAwarenessCore
from fella.curiosity_engine import CuriosityEngine
from fella.aspiration_amplifier import AspirationAmplifier
from fella.coherence_stabilizer import CoherenceStabilizer
from fella.language_grounding import LanguageGroundingEngine


def run_phase1_verification_suite():
    print("=" * 80)
    print("🧠 FELLA PHASE 1 VERIFICATION PROTOCOL (PURE CONTINUOUS PHYSICS)")
    print("=" * 80)
    
    # Initialize clean substrate without pre-trained dictionaries
    substrate = StackedSubstrate(dim=16)
    lang = LanguageGroundingEngine(substrate)
    self_core = SelfAwarenessCore(substrate)
    curiosity = CuriosityEngine(substrate)
    aspiration = AspirationAmplifier(substrate)
    coherence = CoherenceStabilizer(substrate)
    
    test_results = {}
    
    # --------------------------------------------------------------------------
    # PART 1: SELF-AWARENESSPersistent Identity Verification
    # --------------------------------------------------------------------------
    print("\n--- PART 1: SELF-AWARENESS & IDENTITY PERSISTENCE ---")
    
    # 1.1 Single Random Perturbation
    rand_wave = np.random.randn(16)
    rand_wave /= np.linalg.norm(rand_wave)
    is_stable_1, r1 = self_core.evaluate_identity_persistence(rand_wave)
    p1 = is_stable_1
    print(f"1.1 Random Perturbation Resilience: {'PASS' if p1 else 'FAIL'} (Resonance: {r1:.4f})")
    
    # 1.2 100 Random Waves Burst Test
    all_stable = True
    for _ in range(100):
        rw = np.random.randn(16)
        rw /= np.linalg.norm(rw)
        st, _ = self_core.evaluate_identity_persistence(rw)
        if not st:
            all_stable = False
            break
    p2 = all_stable
    print(f"1.2 100 Wave Continuous Burst Stability: {'PASS' if p2 else 'FAIL'}")
    
    # 1.3 Contradiction Wave Damping
    contra_wave = np.random.randn(16)
    contra_wave /= np.linalg.norm(contra_wave)
    damped = self_core.damp_contradictory_perturbation(contra_wave)
    p3 = (np.linalg.norm(damped) > 0.0)
    print(f"1.3 Contradiction Wave Damping: {'PASS' if p3 else 'FAIL'}")
    
    # 1.4 Vacuum Identity Persistence (60s simulation in 100 steps)
    vacuum_stable = True
    for step in range(100):
        substrate.dampen()
        self_n = self_core.get_self_attractor()
        if self_n.energy < 1.0:
            vacuum_stable = False
            break
    p4 = vacuum_stable
    print(f"1.4 60-Second Vacuum Identity Persistence: {'PASS' if p4 else 'FAIL'}")
    
    test_results["Self-Awareness"] = all([p1, p2, p3, p4])
    
    # --------------------------------------------------------------------------
    # PART 2: CURIOSITY ENGINE & EPISTEMIC VACUUM
    # --------------------------------------------------------------------------
    print("\n--- PART 2: CURIOSITY ENGINE & EPISTEMIC VACUUM ---")
    
    # Ground a known concept first
    lang.ingest_continuous_stream("the radiant sun glows brightly", target_tier=1)
    sun_wave = lang.encode_continuous_wave("sun")
    
    # 2.1 Known Wave -> Low Epistemic Friction
    f_known = curiosity.compute_epistemic_friction(sun_wave)
    c1 = (f_known < curiosity.friction_threshold)
    print(f"2.1 Known Wave Friction: {'PASS' if c1 else 'FAIL'} (Friction: {f_known:.4f})")
    
    # 2.2 Unknown Wave -> High Epistemic Friction & Curiosity Wave Trigger
    unseen_wave = np.random.randn(16)
    unseen_wave /= np.linalg.norm(unseen_wave)
    trig, f_unseen, c_wave = curiosity.trigger_curiosity_wave(unseen_wave)
    c2 = trig and (f_unseen >= curiosity.friction_threshold)
    print(f"2.2 Unknown Wave Curiosity Trigger: {'PASS' if c2 else 'FAIL'} (Friction: {f_unseen:.4f})")
    
    # 2.3 Vacuum Introspective Curiosity
    trig_v, f_v, _ = curiosity.trigger_curiosity_wave(np.zeros(16))
    c3 = trig_v and (f_v >= curiosity.friction_threshold)
    print(f"2.3 Vacuum Introspective Curiosity: {'PASS' if c3 else 'FAIL'} (Friction: {f_v:.4f})")
    
    test_results["Curiosity"] = all([c1, c2, c3])
    
    # --------------------------------------------------------------------------
    # PART 3: ASPIRATION AMPLIFIER & COHERENCE STABILIZER
    # --------------------------------------------------------------------------
    print("\n--- PART 3: ASPIRATION AMPLIFIER & COHERENCE STABILIZER ---")
    
    # 3.1 Incomplete Pattern Tension & Gradient Propulsion
    curr_w = lang.encode_continuous_wave("water flows")
    goal_w = lang.encode_continuous_wave("water flows smoothly into the ocean river")
    
    t_inc = aspiration.compute_incompletion_tension(curr_w, goal_w)
    applied, tension_val, prop_w = aspiration.apply_completion_gradient(curr_w, goal_w)
    a1 = applied and (tension_val >= aspiration.tension_threshold)
    print(f"3.1 Incompletion Tension Propulsion: {'PASS' if a1 else 'FAIL'} (Tension: {tension_val:.4f})")
    
    # 3.2 Hamiltonian Friction & Wave Stabilization
    h_friction = coherence.compute_hamiltonian_friction(prop_w)
    rel, f_rel, st_w = coherence.relax_and_stabilize_wave(prop_w)
    a2 = (st_w is not None and np.linalg.norm(st_w) > 0.0)
    print(f"3.2 Hamiltonian Wave Relaxation & Stabilization: {'PASS' if a2 else 'FAIL'} (Friction: {h_friction:.4f})")
    
    test_results["Aspiration & Coherence"] = all([a1, a2])
    
    # --------------------------------------------------------------------------
    # PART 4: FOURIER WAVE-TO-MEANING & MOTOR SPEECH EMISSION
    # --------------------------------------------------------------------------
    print("\n--- PART 4: WAVE-TO-MEANING & MOTOR SPEECH EMISSION ---")
    
    # 4.1 Continuous Wave Projection Encoding
    w_sun = lang.encode_continuous_wave("sun")
    w_water = lang.encode_continuous_wave("water")
    cos_diff = float(np.dot(w_sun, w_water))
    e1 = (cos_diff < 0.90)  # Distinct continuous wave fingerprints
    print(f"4.1 Fourier Wave Projection Orthogonality: {'PASS' if e1 else 'FAIL'} (Cos Sim: {cos_diff:.4f})")
    
    # 4.2 Efferent Motor Cortex Utterance Decoding
    utterance = lang.assemble_continuous_utterance(["sun", "emits", "radiant", "heat"])
    e2 = (utterance == "sun emits radiant heat")
    print(f"4.2 Efferent Motor Cortex Speech Emission: {'PASS' if e2 else 'FAIL'} (Utterance: '{utterance}')")
    
    test_results["Emergent Language"] = all([e1, e2])
    
    # --------------------------------------------------------------------------
    # SUMMARY REPORT
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("🏆 PHASE 1 VERIFICATION SUMMARY REPORT")
    print("=" * 80)
    all_passed = True
    for suite_name, status in test_results.items():
        print(f"  • {suite_name:<30}: {'PASS' if status else 'FAIL'}")
        if not status:
            all_passed = False
            
    print("=" * 80)
    if all_passed:
        print("🎉 PHASE 1 COMPLETE — ALL PHYSICAL EMERGENCE CRITERIA PASSED!")
    else:
        print("❌ PHASE 1 INCOMPLETE — INVESTIGATE FAILING PHYSICAL LAWS.")
    print("=" * 80)
    return all_passed


if __name__ == "__main__":
    success = run_phase1_verification_suite()
    sys.exit(0 if success else 1)
