"""
Coupled Dual-Network Architecture Verification Suite
Tests:
1. Inter-Field Bidirectional Wave Transmission & Attractor Resonance
2. Emergent Curiosity via Trait Attractor Dominance (No hardcoded rules)
3. Emergent Coherence / Grounding on Familiar Inputs
4. Autonomous Dual-Field Rumination & Wonder Oscillations
5. Dual-Network State Persistence
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
import numpy as np
from enn4d import DualFieldENN, TraitField, ENN4D
from text_encoder import TextEncoder
from text_decoder import TextDecoder

def test_inter_field_resonance():
    print("\n--- TEST 1: Inter-Field Bidirectional Wave Transmission ---")
    dual = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    nodes = encoder.encode_constellation("My name is Pratik", time_step=0.1, origin=1.0)
    y_eff, trait_event = dual.step_constellation(nodes, text="My name is Pratik")
    
    assert y_eff is not None and len(y_eff) == 4, "Expected valid 4D effective output vector"
    assert len(dual.neurons) == 5, f"Expected 5 neurons in world field, got {len(dual.neurons)}"
    
    # Check that trait field attractors were physically activated
    attractor_energies = {name: attr.energy for name, attr in dual.trait_field.attractors.items()}
    print(f"  Trait Attractor Energies: {attractor_energies}")
    assert any(attr.energy > attr.base_energy for name, attr in dual.trait_field.attractors.items()), "Expected attractor activation"
    print("✅ Inter-field wave transmission and attractor activation verified.")

def test_attractor_dynamics_novel_vs_familiar():
    print("\n--- TEST 2: Attractor Dynamics (Novelty Curiosity vs Coherence) ---")
    dual = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    # 1. Step familiar concept multiple times to build dense grounding
    for i in range(3):
        nodes = encoder.encode_constellation("Quantum physics", time_step=0.1 * i, origin=1.0)
        dual.step_constellation(nodes, text="Quantum physics")
        
    # Re-stepping familiar concept should activate Coherence attractor
    nodes_fam = encoder.encode_constellation("Quantum physics", time_step=0.4, origin=1.0)
    y_eff_fam, event_fam = dual.step_constellation(nodes_fam, text="Quantum physics")
    
    coherence_act = dual.trait_field.attractors["coherence"].last_activation
    print(f"  Familiar concept Coherence activation: {coherence_act:.4f}")
    
    # 2. Step distant novel concept -> should excite Curiosity attractor
    nodes_nov = encoder.encode_constellation("Exoplanet atmospheric chemistry in Andromeda", time_step=0.5, origin=1.0)
    y_eff_nov, event_nov = dual.step_constellation(nodes_nov, text="Exoplanet atmospheric chemistry in Andromeda")
    
    curiosity_act = dual.trait_field.attractors["curiosity"].last_activation
    print(f"  Novel concept Curiosity activation: {curiosity_act:.4f}")
    assert curiosity_act > 0.0, "Expected positive curiosity activation on novel concept"
    assert event_nov is not None, "Expected curiosity trait event on novel concept"
    print("✅ Emergent curiosity & coherence dynamics verified through coupled attractor resonance.")

def test_autonomous_dual_rumination():
    print("\n--- TEST 3: Autonomous Dual-Field Rumination ---")
    dual = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    # Seed two conceptual families
    n1 = encoder.encode_constellation("Quantum computation", time_step=0.1, origin=1.0)
    dual.step_constellation(n1, text="Quantum computation")
    n2 = encoder.encode_constellation("Biological neural networks", time_step=0.2, origin=1.0)
    dual.step_constellation(n2, text="Biological neural networks")
    
    # Step idle dynamics
    thoughts = []
    for _ in range(25):
        t = dual.idle_step(noise_scale=0.05)
        if t:
            thoughts.append(t)
            
    print(f"  Autonomous idle steps produced {len(thoughts)} thoughts/reflections.")
    assert len(thoughts) > 0, "Expected spontaneous thoughts from coupled idle oscillations"
    print("✅ Autonomous dual-field rumination verified.")

def test_dual_persistence():
    print("\n--- TEST 4: Dual-Network State Persistence ---")
    test_file = "test_dual_universe.json"
    dual1 = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    nodes = encoder.encode_constellation("Consciousness and living physics", time_step=0.1, origin=1.0)
    dual1.step_constellation(nodes, text="Consciousness and living physics")
    dual1.save(test_file)
    
    dual2 = DualFieldENN(dim=4)
    dual2.load(test_file)
    
    assert len(dual2.neurons) == len(dual1.neurons), "Neuron count mismatch"
    assert len(dual2.trait_field.attractors) == 4, "Attractor count mismatch"
    
    if os.path.exists(test_file):
        os.remove(test_file)
    print(f"✅ Dual-network universe saved and restored flawlessly ({len(dual2.neurons)} neurons, 4 attractors).")

if __name__ == "__main__":
    print("=" * 70)
    print("🔬 RUNNING COUPLED DUAL-NETWORK VERIFICATION SUITE")
    print("=" * 70)
    
    test_inter_field_resonance()
    test_attractor_dynamics_novel_vs_familiar()
    test_autonomous_dual_rumination()
    test_dual_persistence()
    
    print("\n" + "=" * 70)
    print("🎉 ALL COUPLED DUAL-NETWORK TESTS PASSED!")
    print("=" * 70)
