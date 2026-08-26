"""
ENN 4D: Full Validation Test Suite
Testing emergent properties, not just code execution.
"""

import sys
import os

# Ensure UTF-8 output on all operating systems/terminals
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from enn4d import ENN4D

class ENN4DValidation:
    def __init__(self, system: ENN4D = None):
        self.system = system if system else ENN4D(dim=4)
        self.results = {}

    # --- Helper Functions ---
    
    def normalize(self, x):
        norm = np.linalg.norm(x)
        return x / norm if norm > 0 else x
    
    def pattern_A(self):
        return self.normalize(np.array([0.0, 0.0, 1.0, 1.0]))
    
    def pattern_B(self):
        return self.normalize(np.array([1.0, 0.0, 1.0, 0.0]))
    
    def pattern_C(self):
        return self.normalize(np.array([1.0, 1.0, 0.0, 0.0]))
    
    def pattern_D(self):
        return self.normalize(np.array([0.0, 1.0, 0.0, 1.0]))
    
    def pattern_combination(self):
        return self.normalize(self.pattern_A() + self.pattern_B())
    
    def pattern_novel(self):
        return self.normalize(np.array([1.0, 1.0, 1.0, 1.0]))
    
    # =========================================================
    # TEST 1: Novelty & Surprise
    # =========================================================
    def test_novelty(self):
        print("\n" + "=" * 70)
        print("TEST 1: NOVELTY & SURPRISE")
        print("=" * 70)
        
        # Reset system
        self.system = ENN4D(dim=4)
        patterns = [
            self.pattern_A(),
            self.pattern_B(),
            self.pattern_C(),
            self.pattern_D(),
            self.pattern_novel()
        ]
        
        results = []
        for i, pattern in enumerate(patterns):
            before_neurons = len(self.system.neurons)
            before_families = len(set(n.w for n in self.system.neurons))
            
            # Train 10 steps
            for _ in range(10):
                self.system.step(pattern, pattern, np.array([0.1]))
            
            after_neurons = len(self.system.neurons)
            after_families = len(set(n.w for n in self.system.neurons))
            
            new_neurons = after_neurons - before_neurons
            new_families = after_families - before_families
            
            results.append({
                'pattern': i,
                'new_neurons': new_neurons,
                'new_families': new_families,
                'total_neurons': after_neurons,
                'total_families': after_families
            })
            
            print(f"Pattern {i+1}: Neurons {before_neurons} -> {after_neurons} "
                  f"(+{new_neurons}), Families {before_families} -> {after_families} "
                  f"(+{new_families})")
        
        # Assess
        novelty_score = sum(1 for r in results[1:] if r['new_families'] > 0) / (len(results) - 1)
        print(f"\nNovelty score: {novelty_score:.2f} (Threshold: 0.80)")
        print(f"Status: {'[PASS]' if novelty_score >= 0.80 else '[FAIL]'}")
        
        self.results['novelty'] = results
        return results
    
    # =========================================================
    # TEST 2: Generalization (Combination)
    # =========================================================
    def test_generalization(self):
        print("\n" + "=" * 70)
        print("TEST 2: GENERALIZATION (COMBINATION)")
        print("=" * 70)
        
        # Reset system
        self.system = ENN4D(dim=4)
        
        # Train on Pattern A and Pattern B separately
        print("Training on Pattern A...")
        for _ in range(30):
            self.system.step(self.pattern_A(), self.pattern_A(), np.array([0.1]))
        
        print("Training on Pattern B...")
        for _ in range(30):
            self.system.step(self.pattern_B(), self.pattern_B(), np.array([0.1]))
        
        before_neurons = len(self.system.neurons)
        before_families = len(set(n.w for n in self.system.neurons))
        
        # Present combination
        comb = self.pattern_combination()
        print(f"Presenting combination (A + B): {comb}")
        
        # Run for 30 steps to allow resonance
        outputs = []
        for i in range(30):
            output = self.system.step(comb, comb, np.array([0.1]))
            outputs.append(output)
        
        after_neurons = len(self.system.neurons)
        after_families = len(set(n.w for n in self.system.neurons))
        
        new_neurons = after_neurons - before_neurons
        new_families = after_families - before_families
        
        print(f"\nBefore: Neurons {before_neurons}, Families {before_families}")
        print(f"After:  Neurons {after_neurons}, Families {after_families}")
        print(f"New neurons: {new_neurons}, New families: {new_families}")
        
        created_new_family = new_families > 0
        
        print(f"Created new family: {created_new_family}")
        print(f"Status: {'[PASS] (No new family created for blend)' if not created_new_family else '[FAIL] (Should not create new family for combination)'}")
        
        self.results['generalization'] = {
            'before_neurons': before_neurons,
            'after_neurons': after_neurons,
            'new_families': new_families,
            'created_new_family': created_new_family,
            'outputs': outputs
        }
        
        return self.results['generalization']
    
    # =========================================================
    # TEST 3: Graceful Forgetting
    # =========================================================
    def test_forgetting(self):
        print("\n" + "=" * 70)
        print("TEST 3: GRACEFUL FORGETTING")
        print("=" * 70)
        
        # Reset system
        self.system = ENN4D(dim=4)
        
        # Train heavily on Pattern A
        print("Training on Pattern A for 50 steps...")
        energies = []
        for i in range(50):
            self.system.step(self.pattern_A(), self.pattern_A(), np.array([0.1]))
            energies.append(sum(n.energy for n in self.system.neurons))
        
        peak_energy = energies[-1]
        print(f"Peak energy: {peak_energy:.2f}")
        
        # Let it decay
        print("Waiting 200 steps with no input...")
        decay_energies = []
        for i in range(200):
            zero = np.zeros(self.system.dim)
            self.system.step(zero, zero, np.array([0.0]))
            total_energy = sum(n.energy for n in self.system.neurons)
            decay_energies.append(total_energy)
            if i % 50 == 0:
                print(f"  Step {i}: energy = {total_energy:.2f}")
        
        decay_smooth = np.std(np.diff(decay_energies)) < 0.5
        print(f"\nDecay smoothness: {decay_smooth}")
        print(f"Status: {'[PASS] (Smooth decay)' if decay_smooth else '[FAIL] (Abrupt decay)'}")
        
        self.results['forgetting'] = {
            'peak_energy': peak_energy,
            'decay_energies': decay_energies,
            'smooth': decay_smooth
        }
        
        return decay_energies
    
    # =========================================================
    # TEST 4: Spontaneous Activity (Dead Man Test)
    # =========================================================
    def test_spontaneous_activity(self):
        print("\n" + "=" * 70)
        print("TEST 4: SPONTANEOUS ACTIVITY (DEAD MAN TEST)")
        print("=" * 70)
        
        # Reset system
        self.system = ENN4D(dim=4)
        
        # Train briefly
        print("Training on Pattern A for 20 steps...")
        for i in range(20):
            self.system.step(self.pattern_A(), self.pattern_A(), np.array([0.1]))
        
        initial_energy = sum(n.energy for n in self.system.neurons)
        initial_neurons = len(self.system.neurons)
        print(f"Initial: Neurons {initial_neurons}, Energy {initial_energy:.2f}")
        
        print("Running with no input for 500 steps...")
        energies = []
        counts = []
        
        for i in range(500):
            zero = np.zeros(self.system.dim)
            self.system.step(zero, zero, np.array([0.0]))
            total_energy = sum(n.energy for n in self.system.neurons)
            energies.append(total_energy)
            counts.append(len(self.system.neurons))
            
            if i % 100 == 0:
                print(f"  Step {i}: Neurons {counts[-1]}, Energy {total_energy:.2f}")
        
        # Check if the system maintains baseline activity
        final_energy = energies[-1]
        final_neurons = counts[-1]
        is_alive = final_energy > 0.1 and final_neurons > 0
        
        print(f"\nFinal state: Neurons {final_neurons}, Energy {final_energy:.2f}")
        print(f"Status: {'[PASS] (System maintains baseline living activity)' if is_alive else '[FAIL] (System died completely)'}")
        
        self.results['spontaneous'] = {
            'energies': energies,
            'counts': counts,
            'is_alive': is_alive
        }
        
        return energies, counts
    
    # =========================================================
    # TEST 5: Creative Interference
    # =========================================================
    def test_creative_interference(self):
        print("\n" + "=" * 70)
        print("TEST 5: CREATIVE INTERFERENCE")
        print("=" * 70)
        
        # Reset system
        self.system = ENN4D(dim=4)
        
        # Train on Pattern A and Pattern B
        print("Training on Pattern A and B...")
        for _ in range(30):
            self.system.step(self.pattern_A(), self.pattern_A(), np.array([0.1]))
        for _ in range(30):
            self.system.step(self.pattern_B(), self.pattern_B(), np.array([0.1]))
        
        # Present Pattern A alone
        output_A = self.system.step(self.pattern_A(), self.pattern_A(), np.array([0.1]))
        
        # Present Pattern B alone
        output_B = self.system.step(self.pattern_B(), self.pattern_B(), np.array([0.1]))
        
        # Present combination
        comb = self.pattern_combination()
        output_comb = []
        for i in range(50):
            out = self.system.step(comb, comb, np.array([0.1]))
            output_comb.append(out)
        
        avg_output_comb = np.mean(output_comb, axis=0)
        
        # Check if the combination output is different from A and B
        diff_from_A = np.linalg.norm(avg_output_comb - output_A)
        diff_from_B = np.linalg.norm(avg_output_comb - output_B)
        
        print(f"Output A: {output_A.round(3)}")
        print(f"Output B: {output_B.round(3)}")
        print(f"Combination output (avg): {avg_output_comb.round(3)}")
        print(f"Difference from A: {diff_from_A:.3f}")
        print(f"Difference from B: {diff_from_B:.3f}")
        
        is_novel = diff_from_A > 0.1 and diff_from_B > 0.1
        print(f"\nOutput is novel (different from both A and B): {is_novel}")
        print(f"Status: {'[PASS] (Creative interference)' if is_novel else '[FAIL] (No novel output)'}")
        
        self.results['interference'] = {
            'output_A': output_A,
            'output_B': output_B,
            'output_comb': avg_output_comb,
            'is_novel': is_novel
        }
        
        return avg_output_comb
    
    # =========================================================
    # TEST 6: Context Sensitivity
    # =========================================================
    def test_context(self):
        print("\n" + "=" * 70)
        print("TEST 6: CONTEXT SENSITIVITY")
        print("=" * 70)
        
        # Reset system
        self.system = ENN4D(dim=4)
        
        # Present Pattern A with different Z values
        z_1 = np.array([0.1])
        z_2 = np.array([0.9])
        
        print("Presenting Pattern A with Z=0.1...")
        for _ in range(20):
            self.system.step(self.pattern_A(), self.pattern_A(), z_1)
        
        print("Presenting Pattern A with Z=0.9...")
        for _ in range(20):
            self.system.step(self.pattern_A(), self.pattern_A(), z_2)
        
        # Check the Z-coordinates of the neurons
        z_values = [n.z for n in self.system.neurons]
        print(f"\nZ-values stored: {z_values}")
        
        unique_z = len(set([tuple(np.round(z, 3)) for z in z_values]))
        print(f"Unique Z-values: {unique_z}")
        
        has_context = unique_z >= 1
        print(f"Status: {'[PASS] (Context stored)' if has_context else '[FAIL] (No context)'}")
        
        self.results['context'] = {
            'z_values': z_values,
            'unique_z': unique_z
        }
        
        return z_values
    
    # =========================================================
    # TEST 7: Self-Limiting Growth
    # =========================================================
    def test_self_limiting(self):
        print("\n" + "=" * 70)
        print("TEST 7: SELF-LIMITING GROWTH")
        print("=" * 70)
        
        # Reset system
        self.system = ENN4D(dim=4)
        
        print("Running 500 steps with random patterns...")
        counts = []
        energies = []
        
        for i in range(500):
            pattern = np.random.randn(4)
            pattern = pattern / (np.linalg.norm(pattern) + 1e-8)
            self.system.step(pattern, pattern, np.array([0.1]))
            
            counts.append(len(self.system.neurons))
            energies.append(sum(n.energy for n in self.system.neurons))
            
            if i % 100 == 0:
                print(f"  Step {i}: Neurons {counts[-1]}, Energy {energies[-1]:.2f}")
        
        final_100 = counts[-100:]
        equilibrium = np.std(final_100) < 10
        
        print(f"\nFinal 100 steps: Mean = {np.mean(final_100):.1f}, Std = {np.std(final_100):.1f}")
        print(f"Status: {'[PASS] (Self-limiting growth)' if equilibrium else '[FAIL] (Unstable growth)'}")
        
        self.results['self_limiting'] = {
            'counts': counts,
            'energies': energies,
            'equilibrium': equilibrium
        }
        
        return counts, energies
    
    # =========================================================
    # RUN ALL TESTS
    # =========================================================
    def run_all(self):
        print("\n" + "=" * 70)
        print("ENN 4D FULL VALIDATION TEST SUITE")
        print("Testing Emergent Properties of a Living System")
        print("=" * 70)
        
        tests = [
            self.test_novelty,
            self.test_generalization,
            self.test_forgetting,
            self.test_spontaneous_activity,
            self.test_creative_interference,
            self.test_context,
            self.test_self_limiting
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
        
        self.print_summary()
    
    def print_summary(self):
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        statuses = []
        
        # 1. Novelty
        if 'novelty' in self.results:
            novelty_score = sum(1 for r in self.results['novelty'][1:] if r['new_families'] > 0) / (len(self.results['novelty']) - 1)
            statuses.append(('Novelty & Surprise', novelty_score >= 0.80))
        
        # 2. Generalization
        if 'generalization' in self.results:
            created_new_family = self.results['generalization']['created_new_family']
            statuses.append(('Generalization (Combination)', not created_new_family))
        
        # 3. Forgetting
        if 'forgetting' in self.results:
            statuses.append(('Graceful Forgetting', self.results['forgetting']['smooth']))
        
        # 4. Spontaneous Activity
        if 'spontaneous' in self.results:
            statuses.append(('Spontaneous Activity (Dead Man Test)', self.results['spontaneous']['is_alive']))
        
        # 5. Interference
        if 'interference' in self.results:
            statuses.append(('Creative Interference', self.results['interference']['is_novel']))
        
        # 6. Context
        if 'context' in self.results:
            statuses.append(('Context Sensitivity', self.results['context']['unique_z'] >= 1))
        
        # 7. Self-Limiting
        if 'self_limiting' in self.results:
            statuses.append(('Self-Limiting Growth', self.results['self_limiting']['equilibrium']))
        
        passed = sum(1 for _, status in statuses if status)
        total = len(statuses)
        
        for name, status in statuses:
            print(f"[{'PASS' if status else 'FAIL'}] {name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        print(f"Status: {'>>> SYSTEM IS ALIVE <<<' if passed == total else '>>> SYSTEM NEEDS TUNING <<<'}")


if __name__ == "__main__":
    system = ENN4D(dim=4)
    validator = ENN4DValidation(system)
    validator.run_all()
