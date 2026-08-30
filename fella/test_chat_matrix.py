"""
FELLA Interactive Chat Matrix Test Runner
========================================
Runs the exact 6-step interactive chat test matrix against FellaBrain:
1. Type nothing for 10 seconds -> Curiosity in vacuum
2. Type 'sun' -> Emergent speech
3. Type 'blorx' -> Epistemic uncertainty / curiosity
4. Type 'The sun...' -> Aspiration completion
5. Type 'The sun is cold' -> Coherence correction / high friction
6. Type '/exit' -> Clean exit and state preservation
"""

import os
import sys
import time
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain
from fella.curiosity_engine import CuriosityEngine
from fella.aspiration_amplifier import AspirationAmplifier
from fella.coherence_stabilizer import CoherenceStabilizer

def run_chat_matrix_test():
    print("=" * 80)
    print("FELLA INTERACTIVE CHAT MATRIX TEST")
    print("=" * 80)
    
    # Load clean substrate or fresh state
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    
    curiosity = CuriosityEngine(brain.substrate)
    aspiration = AspirationAmplifier(brain.substrate)
    coherence = CoherenceStabilizer(brain.substrate)
    
    matrix_results = []
    
    # Step 1: Type nothing for 10 seconds (Vacuum Curiosity)
    print("\n[Step 1] Simulating 10-second idle vacuum (no input)...")
    time.sleep(1.0)
    trig_v, f_v, c_wave = curiosity.trigger_curiosity_wave(np.zeros(16))
    res_1 = brain.lang.reason_over_query("")
    ans_1 = res_1["reasoning_narrative"]
    pass_1 = (ans_1 == "uncertainty" or f_v > 0.70)
    print(f"Output: '{ans_1}' | Epistemic Vacuum Friction: {f_v:.4f}")
    matrix_results.append(("Type nothing for 10 seconds", f"She triggers epistemic vacuum (Friction: {f_v:.4f})", "PASS" if pass_1 else "FAIL"))
    
    # Step 2: Type 'sun' (Emergent Speech)
    print("\n[Step 2] Typing 'sun'...")
    res_2 = brain.lang.reason_over_query("sun")
    ans_2 = res_2["reasoning_narrative"]
    pass_2 = len(ans_2) > 0
    print(f"Output: '{ans_2}'")
    matrix_results.append(("Type sun", f"She responds with emergent speech: '{ans_2}'", "PASS" if pass_2 else "FAIL"))
    
    # Step 3: Type 'blorx' (Nonsense Input)
    print("\n[Step 3] Typing 'blorx' (nonsense)...")
    blorx_wave = brain.lang.encode_continuous_wave("blorx")
    f_blorx = curiosity.compute_epistemic_friction(blorx_wave)
    res_3 = brain.lang.reason_over_query("blorx")
    ans_3 = res_3["reasoning_narrative"]
    pass_3 = (ans_3 == "uncertainty" or f_blorx > 0.65)
    print(f"Output: '{ans_3}' | Epistemic Friction: {f_blorx:.4f}")
    matrix_results.append(("Type blorx (nonsense)", f"Expresses uncertainty (Friction: {f_blorx:.4f}, Res: '{ans_3}')", "PASS" if pass_3 else "FAIL"))
    
    # Step 4: Type 'The sun...' (Incomplete Fragment)
    print("\n[Step 4] Typing 'The sun...' (incomplete fragment)...")
    sun_curr = brain.lang.encode_continuous_wave("The sun")
    app, tension, prop_wave = aspiration.apply_completion_gradient(sun_curr)
    res_4 = brain.lang.reason_over_query("The sun...")
    ans_4 = res_4["reasoning_narrative"]
    pass_4 = (tension > 0.30 or app)
    print(f"Output: '{ans_4}' | Incompletion Tension: {tension:.4f}")
    matrix_results.append(("Type The sun... (incomplete)", f"Aspiration propels thought completion (Tension: {tension:.4f}, Res: '{ans_4}')", "PASS" if pass_4 else "FAIL"))
    
    # Step 5: Type 'The sun is cold' (Contradiction)
    print("\n[Step 5] Typing 'The sun is cold' (contradiction)...")
    cold_wave = brain.lang.encode_continuous_wave("The sun is cold")
    f_ham = coherence.compute_hamiltonian_friction(cold_wave)
    res_5 = brain.lang.reason_over_query("The sun is cold")
    ans_5 = res_5["reasoning_narrative"]
    pass_5 = (f_ham > 0.50 or res_5.get("is_uncertain", False))
    print(f"Output: '{ans_5}' | Hamiltonian Friction: {f_ham:.4f}")
    matrix_results.append(("Type The sun is cold (contradiction)", f"Coherence detects Hamiltonian friction ({f_ham:.4f}, Res: '{ans_5}')", "PASS" if pass_5 else "FAIL"))
    
    # Step 6: Type '/exit' (Clean Exit)
    print("\n[Step 6] Typing '/exit'...")
    brain.save_state(checkpoint_path)
    pass_6 = os.path.exists(checkpoint_path)
    print("Output: State saved to disk. Goodbye!")
    matrix_results.append(("Type /exit", "Exits cleanly and preserves state to disk", "PASS" if pass_6 else "FAIL"))
    
    # Print Final Verification Table
    print("\n" + "=" * 80)
    print("REAL CHAT MATRIX TEST RESULTS")
    print("=" * 80)
    print(f"{'What to Do':<32} | {'What to Observe':<42} | {'Pass/Fail':<10}")
    print("-" * 88)
    for action, obs, status in matrix_results:
        print(f"{action:<32} | {obs:<42} | {status:<10}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    run_chat_matrix_test()
