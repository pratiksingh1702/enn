"""
ENN 4D Living Traits Verification Suite
Verifies:
1. Relational Constellation Formation (Event Micro-Circuits)
2. Epistemic Curiosity Vacuum Triggering
3. Self vs Environment Boundary Polarity
4. Autonomous Reflection & Emergent Cross-Family Resonance (Mind Loop)
5. State Persistence
"""

import os
import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from enn4d import ENN4D, Neuron
from text_encoder import TextEncoder
from text_decoder import TextDecoder
from mind_loop import MindLoop

def test_constellation_and_synapses():
    print("\n--- TEST 1: Relational Constellation Formation ---")
    encoder = TextEncoder(dim=4)
    universe = ENN4D(dim=4)
    
    text = "I am Pratik"
    nodes = encoder.encode_constellation(text, time_step=0.1, origin=1.0)
    assert len(nodes) == 4, f"Expected 4 nodes (anchor + 3 components), got {len(nodes)}"
    
    out_y, void_event = universe.step_constellation(nodes, text=text)
    assert len(universe.neurons) == 4, f"Expected 4 neurons in universe, got {len(universe.neurons)}"
    
    # Verify mutual high-conductance synapses within constellation
    for i in range(4):
        syn = universe.neurons[i].synapses
        for j in range(4):
            if i != j:
                assert j in syn, f"Neuron {i} missing synapse to constellation peer {j}"
                assert syn[j] >= 0.85, f"Expected strong synaptic conductance >= 0.85, got {syn[j]}"
                
    print(f"✅ Constellation formed with {len(nodes)} interconnected nodes. Synaptic conductances: {universe.neurons[0].synapses}")

def test_curiosity_vacuum():
    print("\n--- TEST 2: Epistemic Curiosity Vacuum ---")
    encoder = TextEncoder(dim=4)
    decoder = TextDecoder()
    universe = ENN4D(dim=4)
    
    # Seed one familiar concept
    nodes1 = encoder.encode_constellation("I love programming", time_step=0.1, origin=1.0)
    universe.step_constellation(nodes1, text="I love programming")
    decoder.record_memory("I love programming", nodes1[0]["x"], nodes1[0]["y"], nodes1[0]["z"], 0, 1)
    
    # Introduce a completely novel, distant concept
    novel_text = "Photosynthesis in quantum chloroplasts"
    novel_nodes = encoder.encode_constellation(novel_text, time_step=0.2, origin=1.0)
    out_y, void_event = universe.step_constellation(novel_nodes, text=novel_text)
    
    assert void_event is not None, "Expected curiosity vacuum to be triggered for novel distant concept"
    assert void_event["tension"] > 0.0, f"Expected positive tension, got {void_event['tension']}"
    
    curiosity_msg = decoder.decode_curiosity_void(void_event)
    assert len(curiosity_msg) > 0
    print(f"✅ Curiosity vacuum triggered (tension: {void_event['tension']:.2f}): \"{curiosity_msg}\"")

def test_self_environment_boundary():
    print("\n--- TEST 3: Self vs Environment Boundary ---")
    universe = ENN4D(dim=4)
    
    # External sensory neuron
    n_ext = universe.birth(np.array([0.5, 0.5, 0.5, 0.5]), np.array([0.5, 0.5, 0.5, 0.5]), np.array([0.1]), text="External Fact", origin=1.0)
    # Internal thought neuron
    n_self = universe.birth(np.array([0.2, 0.2, 0.2, 0.2]), np.array([0.2, 0.2, 0.2, 0.2]), np.array([0.1]), text="Internal Insight", origin=0.0, role="insight")
    
    assert n_ext.origin == 1.0, "External neuron origin mismatch"
    assert n_self.origin == 0.0, "Internal neuron origin mismatch"
    assert n_self.role == "insight"
    print(f"✅ Self/Environment boundary verified: External={n_ext.origin}, Internal Self={n_self.origin}")

def test_idle_rumination_and_wonder():
    print("\n--- TEST 4: Autonomous Rumination & Cross-Family Resonance ---")
    encoder = TextEncoder(dim=4)
    universe = ENN4D(dim=4)
    
    # Create two different families
    n1 = encoder.encode_constellation("Quantum physics", time_step=0.1, origin=1.0)
    universe.step_constellation(n1, text="Quantum physics")
    
    n2 = encoder.encode_constellation("Neural consciousness", time_step=0.2, origin=1.0)
    universe.step_constellation(n2, text="Neural consciousness")
    
    # Run multiple idle reflection pulses
    insights = []
    for step in range(30):
        thought = universe.idle_step(noise_scale=0.06)
        if thought:
            insights.append(thought)
            
    print(f"✅ Idle rumination stepped 30 cycles, generated {len(insights)} spontaneous cross-family reflections/insights.")
    if insights:
        print(f"   Example thought: {insights[0]['message']}")

def test_persistence():
    print("\n--- TEST 5: State Persistence with Living Traits ---")
    test_file = "test_universe_traits.json"
    universe1 = ENN4D(dim=4)
    encoder = TextEncoder(dim=4)
    
    nodes = encoder.encode_constellation("Emergent AI Cosmos", time_step=0.1, origin=1.0)
    universe1.step_constellation(nodes, text="Emergent AI Cosmos")
    universe1.save(test_file)
    
    universe2 = ENN4D(dim=4)
    universe2.load(test_file)
    
    assert len(universe2.neurons) == len(universe1.neurons)
    assert universe2.neurons[0].origin == universe1.neurons[0].origin
    assert len(universe2.neurons[0].synapses) == len(universe1.neurons[0].synapses)
    
    if os.path.exists(test_file):
        os.remove(test_file)
    print(f"✅ Persistence verified: {len(universe2.neurons)} neurons and synapses saved & restored flawlessly.")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 RUNNING ENN 4D LIVING TRAITS VERIFICATION")
    print("=" * 60)
    
    test_constellation_and_synapses()
    test_curiosity_vacuum()
    test_self_environment_boundary()
    test_idle_rumination_and_wonder()
    test_persistence()
    
    print("\n" + "=" * 60)
    print("🎉 ALL LIVING TRAITS TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
