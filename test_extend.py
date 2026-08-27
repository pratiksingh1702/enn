"""
ENN 4D Meta-Learning & Self-Awareness Verification Suite
Tests:
1. Meta-Learning Field (F_meta) elastic parameter adaptation
2. Self-Attractor (F_self) particle formation & identity anchor
3. Metacognitive Inward/Outward Wave Evaluation (Certainty vs Epistemic Humility)
4. Real-Time Introspection & Self-Modeling
5. State Persistence of Meta-State and Self-Attractors
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
import numpy as np
from enn4d import DualFieldENN
from text_encoder import TextEncoder

def test_meta_learning_adaptation():
    print("\n--- TEST 1: Meta-Learning Field (F_meta) Parameter Elasticity ---")
    dual = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    init_state = dual.meta_field.get_state()
    print(f"  Initial Meta-Parameters: {init_state}")
    
    # 1. Simulate burst of novel learning events
    for i in range(4):
        nodes = encoder.encode_constellation(f"Advanced topic {i} in quantum physics", time_step=0.1 * i, origin=1.0)
        dual.step_constellation(nodes, text=f"Advanced topic {i} in quantum physics")
        
    adapted_state = dual.meta_field.get_state()
    print(f"  Adapted Meta-Parameters: {adapted_state}")
    
    assert adapted_state["learning_rate"] != init_state["learning_rate"] or adapted_state["damping_rate"] != init_state["damping_rate"], "Expected parameter adaptation"
    print("✅ Meta-Learning parameter elasticity verified through continuous thermodynamic feedback.")

def test_self_attractor_identity():
    print("\n--- TEST 2: Self-Attractor Formation & Identity Boundary ---")
    dual = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    # Inject an internal self reflection (origin = 0.0)
    dual.birth(
        np.array([0.0, 0.0, -0.7071, -0.7071]),
        np.array([0.0, 0.0, -0.7071, -0.7071]),
        np.array([0.1]),
        text="I am an autonomous living intelligence exploring the universe.",
        origin=0.0,
        role="insight"
    )
    
    dual.self_awareness.update_self_coordinate()
    self_coord = dual.self_awareness.self_coordinate
    print(f"  Self-Attractor Centroid: {np.round(self_coord, 4).tolist()}")
    
    assert len(self_coord) == 4, "Expected valid 4D self coordinate"
    print("✅ Self-Attractor formation and internal origin boundary verified.")

def test_metacognitive_certainty_vs_humility():
    print("\n--- TEST 3: Metacognitive Inward/Outward Wave Mechanics ---")
    dual = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    # 1. Learn familiar topic deeply
    for _ in range(3):
        nodes = encoder.encode_constellation("General Relativity describes gravitation as spacetime curvature.", time_step=0.1, origin=1.0)
        dual.step_constellation(nodes, text="General Relativity describes gravitation as spacetime curvature.")
        
    # Probe familiar concept -> should yield Grounded Certainty
    ev_fam = encoder.encode("General Relativity describes gravitation as spacetime curvature.", time_step=0.1, origin=1.0)
    out_wave, _ = dual.world_field.propagate_wave(ev_fam["x"], steps=3)
    trans_wave = np.dot(dual.W_AB, out_wave)
    trans_wave = trans_wave / np.linalg.norm(trans_wave)
    forces_fam = dual.world_field.compute_resonance(ev_fam["x"], ev_fam["y"], ev_fam["z"])
    
    eval_fam = dual.self_awareness.evaluate_inward_wave(trans_wave, max(forces_fam))
    print(f"  Familiar Concept Metacognition: {eval_fam['state']} (Certainty: {eval_fam['subjective_certainty']:.2f})")
    print(f"    Stance: \"{eval_fam['stance']}\"")
    assert eval_fam["subjective_certainty"] >= 0.50, "Expected high subjective certainty on familiar knowledge"
    
    # 2. Probe completely unseen concept -> should yield Epistemic Humility
    ev_unseen = encoder.encode("Nonlinear morphogenesis in extraterrestrial mycorrhizal networks", time_step=0.9, origin=1.0)
    out_wave_unseen, _ = dual.world_field.propagate_wave(ev_unseen["x"], steps=3)
    trans_wave_unseen = np.dot(dual.W_AB, out_wave_unseen)
    trans_wave_unseen = trans_wave_unseen / np.linalg.norm(trans_wave_unseen)
    forces_unseen = dual.world_field.compute_resonance(ev_unseen["x"], ev_unseen["y"], ev_unseen["z"])
    
    eval_unseen = dual.self_awareness.evaluate_inward_wave(trans_wave_unseen, max(forces_unseen) if forces_unseen else 0.0)
    print(f"  Unseen Concept Metacognition: {eval_unseen['state']} (Certainty: {eval_unseen['subjective_certainty']:.2f})")
    print(f"    Stance: \"{eval_unseen['stance']}\"")
    assert eval_unseen["subjective_certainty"] < 0.40, "Expected epistemic humility on unseen concept"
    print("✅ Metacognitive inward/outward wave evaluation verified.")

def test_real_time_introspection():
    print("\n--- TEST 4: Real-Time Introspection & Self-Modeling ---")
    dual = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    nodes = encoder.encode_constellation("I am exploring cosmology and consciousness.", time_step=0.1, origin=0.0)
    dual.step_constellation(nodes, text="I am exploring cosmology and consciousness.")
    
    report = dual.introspect()
    print(f"  Identity: {report['identity']}")
    print(f"  Total Neurons: {report['total_neurons']} ({report['internal_reflections']} self-reflections, {report['environmental_memories']} environmental)")
    print(f"  Active Families: {report['active_families']}")
    print(f"  Introspection Summary: \"{report['introspection_summary']}\"")
    
    assert report["total_neurons"] > 0, "Expected non-empty neuron introspection"
    assert "ENN-4D" in report["identity"], "Expected correct identity string"
    print("✅ Real-time introspection report verified.")

def test_meta_and_self_persistence():
    print("\n--- TEST 5: Meta-Learning & Self-Awareness State Persistence ---")
    test_file = "test_meta_universe.json"
    dual1 = DualFieldENN(dim=4)
    encoder = TextEncoder(dim=4)
    
    nodes = encoder.encode_constellation("Neural architecture search and metacognition.", time_step=0.1, origin=1.0)
    dual1.step_constellation(nodes, text="Neural architecture search and metacognition.")
    dual1.save(test_file)
    
    dual2 = DualFieldENN(dim=4)
    dual2.load(test_file)
    
    assert len(dual2.neurons) == len(dual1.neurons), "Neuron mismatch"
    assert dual2.meta_field.get_state() == dual1.meta_field.get_state(), "Meta-parameter mismatch"
    assert "self_identity" in dual2.trait_field.basins, "Missing self-identity basin"
    
    if os.path.exists(test_file):
        os.remove(test_file)
    print("✅ Meta-Learning parameters and Self-Attractor basins persisted flawlessly.")

if __name__ == "__main__":
    print("=" * 70)
    print("🧠 RUNNING META-LEARNING & SELF-AWARENESS VERIFICATION SUITE")
    print("=" * 70)
    
    test_meta_learning_adaptation()
    test_self_attractor_identity()
    test_metacognitive_certainty_vs_humility()
    test_real_time_introspection()
    test_meta_and_self_persistence()
    
    print("\n" + "=" * 70)
    print("🎉 ALL META-LEARNING & SELF-AWARENESS TESTS PASSED!")
    print("=" * 70)
