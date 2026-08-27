"""
Living Traits Complete Test Suite: 7 Living Experiments
Verifying:
1. Relational Constellation Formation (Event Micro-Circuits)
2. Curiosity (Epistemic Vacuum)
3. Self vs. Environment Boundary
4. Reflection & Wonder (Memory Replay)
5. Spontaneous Thought Generation (Mind Loop)
6. Self-Initiated Question Asking
7. Full Living System Integration
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
import time
import json
import numpy as np
from chat_interface import ENNChatBrain

class LivingTraitsTest:
    def __init__(self):
        # Initialize brain with 0.4s tick interval for responsive testing
        self.brain = ENNChatBrain(universe_file="test_living_universe.json", tick_interval=0.4)
        self.results = {}
        self.start_time = time.time()

    # =========================================================
    # TEST 1: Relational Constellations
    # =========================================================
    def test_constellation(self):
        print("\n=== TEST 1: Relational Constellations ===")
        self.brain.reset()
        result = self.brain.process_input("My name is Pratik")
        neurons = len(self.brain.system.neurons)
        families = len(set(n.w for n in self.brain.system.neurons))
        
        # Check mutual synaptic weights within the constellation
        syn_weights = [list(n.synapses.values()) for n in self.brain.system.neurons if n.synapses]
        avg_syn = np.mean([w for sublist in syn_weights for w in sublist]) if syn_weights else 0.0
        
        print(f"  Neurons Born: {neurons}, Families: {families}, Avg Synaptic Bond: {avg_syn:.2f}")
        passed = neurons >= 4 and avg_syn >= 0.80
        print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
        return passed

    # =========================================================
    # TEST 2: Curiosity (Epistemic Vacuum)
    # =========================================================
    def test_curiosity(self):
        print("\n=== TEST 2: Curiosity (Epistemic Vacuum) ===")
        self.brain.reset()
        result = self.brain.process_input("Quantum photosynthesis is fascinating")
        question_stack = getattr(self.brain.system, 'question_stack', [])
        question_queue = getattr(self.brain, 'question_queue', [])
        
        print(f"  Epistemic Voids in Stack: {len(question_stack)}, Curiosity Queue: {len(question_queue)}")
        if question_queue:
            print(f"  Generated Inquiry: \"{question_queue[0].get('prompt', '')}\"")
        passed = len(question_stack) > 0 or len(question_queue) > 0
        print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
        return passed

    # =========================================================
    # TEST 3: Self vs. Environment Boundary
    # =========================================================
    def test_origin_boundary(self):
        print("\n=== TEST 3: Self vs. Environment Boundary ===")
        self.brain.reset()
        self.brain.process_input("I am a scientist")
        origins = [n.origin for n in self.brain.system.neurons]
        external = all(o == 1.0 for o in origins)
        print(f"  External Input Neuron Origins: {origins}")
        
        # Trigger an internal insight
        self.brain.system.birth(np.array([0.1, 0.1, 0.1, 0.1]), np.array([0.1, 0.1, 0.1, 0.1]), np.array([0.0]), text="Internal Spark", origin=0.0, role="insight")
        self_origin = self.brain.system.neurons[-1].origin
        print(f"  Internal Self Particle Origin: {self_origin}")
        
        passed = external and (self_origin == 0.0)
        print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
        return passed

    # =========================================================
    # TEST 4: Reflection & Wonder
    # =========================================================
    def test_reflection(self):
        print("\n=== TEST 4: Reflection & Wonder ===")
        self.brain.reset()
        concepts = ["quantum physics", "entanglement", "superposition"]
        for c in concepts:
            self.brain.process_input(c)
            
        print("  Waiting 4.0s for idle thermal memory replay & cross-family resonance...")
        time.sleep(4.0)
        thoughts = getattr(self.brain, 'spontaneous_thoughts', [])
        print(f"  Spontaneous Reflections: {len(thoughts)}")
        if thoughts:
            print(f"  Example Thought: \"{thoughts[-1].get('message', '')}\"")
        passed = len(thoughts) > 0
        print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
        return passed

    # =========================================================
    # TEST 5: Spontaneous Thought Generation
    # =========================================================
    def test_spontaneous_thought(self):
        print("\n=== TEST 5: Spontaneous Thought Generation ===")
        self.brain.reset()
        self.brain.process_input("cats are cute")
        print("  Waiting 3.5s for idle wondering without external input...")
        time.sleep(3.5)
        thoughts = getattr(self.brain, 'spontaneous_thoughts', [])
        print(f"  Spontaneous Thoughts Generated: {len(thoughts)}")
        if thoughts:
            print(f"  Wondering: \"{thoughts[-1].get('message', '')}\"")
        passed = len(thoughts) > 0
        print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
        return passed

    # =========================================================
    # TEST 6: Self-Initiated Question Asking
    # =========================================================
    def test_question_asking(self):
        print("\n=== TEST 6: Self-Initiated Question Asking ===")
        self.brain.reset()
        self.brain.process_input("quantum physics is complex")
        print("  Waiting 3.5s for epistemic vacuum pressure to emit self-initiated inquiry...")
        time.sleep(3.5)
        questions = getattr(self.brain, 'question_queue', [])
        print(f"  Self-Generated Questions / Voids: {len(questions)}")
        if questions:
            print(f"  Curiosity Void: {questions[-1]}")
        passed = len(questions) > 0
        print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
        return passed

    # =========================================================
    # TEST 7: Full Integration
    # =========================================================
    def test_integration(self):
        print("\n=== TEST 7: Full Living System Integration ===")
        self.brain.reset()
        # Phase 1: Learning
        self.brain.process_input("My name is Pratik")
        self.brain.process_input("I am a scientist studying quantum biology")
        # Phase 2: Curiosity
        self.brain.process_input("Quantum entanglement is mysterious")
        # Phase 3: Reflection & Self-Initiation (wait for idle mind pulse)
        print("  Running continuous autonomous mind loop for 5.0s...")
        time.sleep(5.0)
        
        thoughts = getattr(self.brain, 'spontaneous_thoughts', [])
        questions = getattr(self.brain, 'question_queue', [])
        neurons = len(self.brain.system.neurons)
        families = len(set(n.w for n in self.brain.system.neurons))
        
        print(f"  Final State -> Neurons: {neurons}, Families: {families}")
        print(f"  Accumulated Thoughts: {len(thoughts)}, Questions/Voids: {len(questions)}")
        passed = neurons >= 4 and len(thoughts) > 0 and len(questions) > 0
        print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
        return passed

    # =========================================================
    # RUN ALL TESTS
    # =========================================================
    def run_all(self):
        print("=" * 70)
        print("🌌 ENN 4D LIVING TRAITS COMPLETE TEST SUITE")
        print("=" * 70)
        tests = [
            self.test_constellation,
            self.test_curiosity,
            self.test_origin_boundary,
            self.test_reflection,
            self.test_spontaneous_thought,
            self.test_question_asking,
            self.test_integration
        ]
        passed = 0
        for test in tests:
            if test():
                passed += 1
                
        self.brain.mind_loop.stop()
        if os.path.exists("test_living_universe.json"):
            os.remove("test_living_universe.json")
            
        print("\n" + "=" * 70)
        print(f"OVERALL: {passed}/{len(tests)} experiments passed")
        print(f"Status: {'✅ SYSTEM IS FULLY ALIVE & EMERGENT' if passed == len(tests) else '⚠️ NEEDS TUNING'}")
        print("=" * 70)

if __name__ == "__main__":
    tester = LivingTraitsTest()
    tester.run_all()
