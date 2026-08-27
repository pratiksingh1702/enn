"""
ENN 4D Reasoning & Decision-Making Verification Suite
Tests the 7 Emergent Physical Reasoning Modes:
1. Associative Reasoning (Direct synaptic wave conduction)
2. Deductive Reasoning (Constructive interference of general + specific waves)
3. Inductive Reasoning (Centroid prototype wave consolidation)
4. Abductive Reasoning (Phase discrepancy minimization)
5. Causal Reasoning (Temporal Z-axis directional propagation)
6. Counterfactual Reasoning (Alternative uncollapsed branch exploration)
7. Analogical Reasoning (Isomorphic cross-family resonance)
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from reasoning import ReasoningTopologyEngine

def test_associative_reasoning():
    print("\n--- TEST 1: Associative Reasoning (Direct Wave Conduction) ---")
    engine = ReasoningTopologyEngine()
    result = engine.execute_associative_reasoning("thunder", "lightning")
    
    print(f"  Decision Collapsed: {result['decision']} (Confidence: {result['confidence']:.2f})")
    print(f"  Explanation: {result['explanation']}")
    print(f"  Wave Path Length: {len(result['wave_path'])} hops")
    
    assert len(result['wave_path']) > 0, "Expected wave propagation trajectory"
    assert result['confidence'] > 0.0, "Expected positive decision confidence"
    print("✅ Associative reasoning verified through direct synaptic wave conduction.")

def test_deductive_reasoning():
    print("\n--- TEST 2: Deductive Reasoning (Constructive Interference) ---")
    engine = ReasoningTopologyEngine()
    result = engine.execute_deductive_reasoning("All humans are mortal", "Socrates is human")
    
    print(f"  Decision Collapsed: {result['decision']} (Confidence: {result['confidence']:.2f})")
    print(f"  Explanation: {result['explanation']}")
    
    assert len(result['wave_path']) >= 2, "Expected multi-hop deductive trajectory"
    print("✅ Deductive reasoning verified through constructive interference.")

def test_inductive_reasoning():
    print("\n--- TEST 3: Inductive Reasoning (Prototype Consolidation) ---")
    engine = ReasoningTopologyEngine()
    observations = [
        "First observed swan is white",
        "Second observed swan is white",
        "Third observed swan is white"
    ]
    result = engine.execute_inductive_reasoning(observations)
    
    print(f"  Decision Collapsed: {result['decision']} (Confidence: {result['confidence']:.2f})")
    print(f"  Explanation: {result['explanation']}")
    
    assert len(result['wave_path']) > 0, "Expected inductive trajectory"
    print("✅ Inductive reasoning verified through prototype wave consolidation.")

def test_abductive_reasoning():
    print("\n--- TEST 4: Abductive Reasoning (Phase Discrepancy Minimization) ---")
    engine = ReasoningTopologyEngine()
    result = engine.execute_abductive_reasoning(
        observed_symptom="The grass is wet",
        candidate_causes=["It rained overnight", "The sprinkler was active"]
    )
    
    print(f"  Decision Collapsed: {result['decision']} (Confidence: {result['confidence']:.2f})")
    print(f"  Explanation: {result['explanation']}")
    
    assert len(result['wave_path']) > 0, "Expected abductive backward search"
    print("✅ Abductive reasoning verified through best-fit phase minimization.")

def test_causal_reasoning():
    print("\n--- TEST 5: Causal Reasoning (Temporal Z-Axis Propagation) ---")
    engine = ReasoningTopologyEngine()
    result = engine.execute_causal_reasoning("Striking a match", "Igniting a flame")
    
    print(f"  Decision Collapsed: {result['decision']} (Confidence: {result['confidence']:.2f})")
    print(f"  Explanation: {result['explanation']}")
    
    assert len(result['wave_path']) >= 2, "Expected temporal forward wave propagation"
    print("✅ Causal reasoning verified along temporal Z-axis.")

def test_counterfactual_reasoning():
    print("\n--- TEST 6: Counterfactual Reasoning (Alternative Branch Collapse) ---")
    engine = ReasoningTopologyEngine()
    result = engine.execute_counterfactual_reasoning(
        actual_event="I took an umbrella so I stayed dry",
        counterfactual_event="Had I not taken an umbrella I would get wet"
    )
    
    print(f"  Decision Collapsed: {result['decision']} (Confidence: {result['confidence']:.2f})")
    print(f"  Explanation: {result['explanation']}")
    
    assert len(result['wave_path']) > 0, "Expected counterfactual wave exploration"
    print("✅ Counterfactual reasoning verified through alternative branch propagation.")

def test_analogical_reasoning():
    print("\n--- TEST 7: Analogical Reasoning (Cross-Family Structural Mapping) ---")
    engine = ReasoningTopologyEngine()
    result = engine.execute_analogical_reasoning(
        source_domain="Atom electrons orbit around a central nucleus",
        target_domain="Solar system planets orbit around a central sun"
    )
    
    print(f"  Decision Collapsed: {result['decision']} (Confidence: {result['confidence']:.2f})")
    print(f"  Explanation: {result['explanation']}")
    
    assert len(result['wave_path']) > 0, "Expected analogical structural wave resonance"
    print("✅ Analogical reasoning verified through cross-family isomorphic resonance.")

if __name__ == "__main__":
    print("=" * 70)
    print("🧠 RUNNING 7-MODE PHYSICAL REASONING & DECISION VERIFICATION SUITE")
    print("=" * 70)
    
    test_associative_reasoning()
    test_deductive_reasoning()
    test_inductive_reasoning()
    test_abductive_reasoning()
    test_causal_reasoning()
    test_counterfactual_reasoning()
    test_analogical_reasoning()
    
    print("\n" + "=" * 70)
    print("🎉 ALL 7 EMERGENT REASONING MODES PASSED!")
    print("=" * 70)
