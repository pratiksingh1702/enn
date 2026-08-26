"""
ENN 4D Test Suite
Observing emergent behavior: Birth, Resonance/Clustering, Amplification, Damping, Novelty, Phase Transitions, and Stability.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import List, Dict, Optional
from enn4d import ENN4D

class ENN4DTest:
    def __init__(self, system: Optional[ENN4D] = None):
        self.system = system if system is not None else ENN4D(dim=4)
        self.results = {}
    
    def generate_patterns(self, num_patterns: int, dim: int = 4) -> List[np.ndarray]:
        """Generate normalized random distinct patterns."""
        patterns = []
        for _ in range(num_patterns):
            pattern = np.random.randn(dim)
            norm = np.linalg.norm(pattern)
            if norm > 0:
                pattern = pattern / norm
            patterns.append(pattern)
        return patterns
    
    def measure_clustering(self) -> dict:
        """Measure clustering by family and spatial dispersion."""
        families = defaultdict(list)
        for neuron in self.system.neurons:
            families[neuron.w].append(neuron)
        
        intra_distances = []
        inter_distances = []
        
        for family_id, members in families.items():
            if len(members) > 1:
                for i in range(len(members)):
                    for j in range(i + 1, len(members)):
                        d = np.linalg.norm(members[i].x - members[j].x)
                        intra_distances.append(d)
        
        family_ids = list(families.keys())
        for i in range(len(family_ids)):
            for j in range(i + 1, len(family_ids)):
                members_i = families[family_ids[i]]
                members_j = families[family_ids[j]]
                avg_d = np.mean([np.linalg.norm(n1.x - n2.x) for n1 in members_i for n2 in members_j])
                inter_distances.append(avg_d)
        
        intra_mean = float(np.mean(intra_distances)) if intra_distances else 0.0
        inter_mean = float(np.mean(inter_distances)) if inter_distances else 0.0
        
        return {
            'intra_mean': intra_mean,
            'intra_std': float(np.std(intra_distances)) if intra_distances else 0.0,
            'inter_mean': inter_mean,
            'inter_std': float(np.std(inter_distances)) if inter_distances else 0.0,
            'num_families': len(families)
        }
    
    # --- EXPERIMENTS ---
    
    def run_birth_experiment(self, num_patterns: int = 10):
        """Experiment 1: Birth and Growth."""
        print("\n=== EXPERIMENT 1: Birth and Growth ===")
        print(f"Presenting {num_patterns} distinct novel patterns...")
        
        patterns = self.generate_patterns(num_patterns, dim=self.system.dim)
        neuron_counts = []
        
        for i, pattern in enumerate(patterns):
            self.system.step(pattern, pattern, np.array([0.1]))
            neuron_counts.append(len(self.system.neurons))
            print(f"  Pattern {i+1}: {len(self.system.neurons)} neurons (Families: {len(set(n.w for n in self.system.neurons))})")
        
        self.results['birth'] = neuron_counts
        
        # Assessment
        print(f"\nAssessment:")
        print(f"  Initial neurons: {neuron_counts[0] if neuron_counts else 0}")
        print(f"  Final neurons: {neuron_counts[-1] if neuron_counts else 0}")
        growth_rate = (neuron_counts[-1] - neuron_counts[0]) / (num_patterns - 1) if num_patterns > 1 else 0
        print(f"  Growth rate: {growth_rate:.2f} neurons/pattern")
        
        return neuron_counts
    
    def run_clustering_experiment(self):
        """Experiment 2: Resonance and Clustering."""
        print("\n=== EXPERIMENT 2: Resonance and Clustering ===")
        
        pattern_A = np.array([0.0, 0.0, 1.0, 1.0]) / np.sqrt(2)
        pattern_B = np.array([1.0, 0.0, 1.0, 0.0]) / np.sqrt(2)
        pattern_C = np.array([1.0, 1.0, 0.0, 0.0]) / np.sqrt(2)
        pattern_D = np.array([0.0, 1.0, 0.0, 1.0]) / np.sqrt(2)
        
        patterns = [pattern_A, pattern_B, pattern_C, pattern_D]
        labels = ['A', 'B', 'C', 'D']
        
        print("Training on 4 distinct patterns A, B, C, D (30 steps each)...")
        for label, pattern in zip(labels, patterns):
            for i in range(30):
                self.system.step(pattern, pattern, np.array([0.1]))
            print(f"  Trained on pattern {label} (Current Families: {len(set(n.w for n in self.system.neurons))})")
        
        clustering = self.measure_clustering()
        print(f"\nClustering:")
        print(f"  Families: {clustering['num_families']}")
        print(f"  Intra-family spatial distance: {clustering['intra_mean']:.3f}")
        print(f"  Inter-family spatial distance: {clustering['inter_mean']:.3f}")
        ratio = (clustering['inter_mean'] / clustering['intra_mean']) if clustering['intra_mean'] > 0 else clustering['inter_mean']
        print(f"  Clustering separation score: {ratio:.2f}")
        
        self.results['clustering'] = clustering
        return clustering
    
    def run_amplification_experiment(self, steps: int = 100):
        """Experiment 3: Amplification and Strength."""
        print("\n=== EXPERIMENT 3: Amplification ===")
        
        pattern = np.array([0.0, 0.0, 1.0, 1.0]) / np.sqrt(2)
        energies = []
        
        print(f"Presenting resonant pattern for {steps} steps...")
        
        initial_e = sum(n.energy for n in self.system.neurons)
        for i in range(steps):
            self.system.step(pattern, pattern, np.array([0.1]))
            total_energy = sum(n.energy for n in self.system.neurons)
            energies.append(total_energy)
            if i % 25 == 0 or i == steps - 1:
                print(f"  Step {i}: total energy = {total_energy:.2f}")
        
        self.results['amplification'] = energies
        
        print(f"\nAssessment:")
        print(f"  Initial energy: {energies[0]:.2f}")
        print(f"  Final energy: {energies[-1]:.2f}")
        print(f"  Energy growth: {energies[-1] - energies[0]:.2f}")
        
        return energies
    
    def run_damping_experiment(self, train_steps: int = 40, wait_steps: int = 150):
        """Experiment 4: Damping and Forgetting."""
        print("\n=== EXPERIMENT 4: Damping ===")
        
        pattern = np.array([0.0, 0.0, 1.0, 1.0]) / np.sqrt(2)
        
        print(f"Injecting energy for {train_steps} steps...")
        for i in range(train_steps):
            self.system.step(pattern, pattern, np.array([0.1]))
        
        initial_neurons = len(self.system.neurons)
        initial_energy = sum(n.energy for n in self.system.neurons)
        print(f"  State before rest: {initial_neurons} neurons, total energy = {initial_energy:.2f}")
        
        print(f"Observing system during {wait_steps} rest steps (zero input signal)...")
        energies = []
        counts = []
        
        for i in range(wait_steps):
            zero = np.zeros(self.system.dim)
            self.system.step(zero, zero, np.array([0.0]))
            
            total_energy = sum(n.energy for n in self.system.neurons)
            energies.append(total_energy)
            counts.append(len(self.system.neurons))
            
            if i % 50 == 0 or i == wait_steps - 1:
                print(f"  Step {i}: {len(self.system.neurons)} neurons, energy = {total_energy:.2f}")
        
        self.results['damping'] = {'energies': energies, 'counts': counts}
        
        print(f"\nAssessment:")
        print(f"  Initial energy: {initial_energy:.2f} -> Final energy: {energies[-1]:.2f}")
        print(f"  Energy decay: {initial_energy - energies[-1]:.2f}")
        print(f"  Neurons: {initial_neurons} -> {counts[-1]} (Pruned: {initial_neurons - counts[-1]})")
        
        return energies, counts
    
    def run_novelty_experiment(self):
        """Experiment 5: Interference and Novelty."""
        print("\n=== EXPERIMENT 5: Novelty Detection ===")
        
        pattern_A = np.array([0.0, 0.0, 1.0, 1.0]) / np.sqrt(2)
        pattern_B = np.array([1.0, 0.0, 1.0, 0.0]) / np.sqrt(2)
        
        print("Establishing base memory on Pattern A and Pattern B...")
        for i in range(30):
            self.system.step(pattern_A, pattern_A, np.array([0.1]))
        for i in range(30):
            self.system.step(pattern_B, pattern_B, np.array([0.1]))
        
        base_count = len(self.system.neurons)
        print(f"  Base neurons: {base_count}")
        
        novel_patterns = [
            np.array([0.0, 0.0, 1.0, 0.9]) / np.linalg.norm([0.0, 0.0, 1.0, 0.9]), # Familiar (close to A)
            np.array([0.0, 1.0, 0.0, 0.0]),                                        # Completely Novel
            np.array([1.0, 1.0, 0.0, 0.0]) / np.sqrt(2),                          # Completely Novel
        ]
        
        created = 0
        for i, pattern in enumerate(novel_patterns):
            before = len(self.system.neurons)
            self.system.step(pattern, pattern, np.array([0.1]))
            after = len(self.system.neurons)
            diff = after - before
            created += max(0, diff)
            desc = "Familiar" if i == 0 else "Novel"
            print(f"  Pattern {i+1} ({desc}): Neurons {before} -> {after} (Delta: {diff:+d})")
        
        self.results['novelty'] = created
        return created
    
    def run_phase_transition_experiment(self, steps: int = 150):
        """Experiment 6: Phase Transition (Splitting & Reorganization)."""
        print("\n=== EXPERIMENT 6: Phase Transition ===")
        
        pattern = np.array([0.0, 0.0, 1.0, 1.0]) / np.sqrt(2)
        counts = []
        energies = []
        
        print(f"Pumping high energy for {steps} steps to trigger mitosis (splitting)...")
        
        initial_neurons = len(self.system.neurons)
        for i in range(steps):
            self.system.step(pattern, pattern, np.array([0.1]))
            counts.append(len(self.system.neurons))
            energies.append(sum(n.energy for n in self.system.neurons))
            
            if i % 50 == 0 or i == steps - 1:
                print(f"  Step {i}: {counts[-1]} neurons, total energy = {energies[-1]:.2f}")
        
        self.results['phase_transition'] = {'counts': counts, 'energies': energies}
        print(f"  Phase transition result: {initial_neurons} -> {counts[-1]} neurons (mitosis events triggered)")
        return counts, energies
    
    def run_stability_experiment(self, steps: int = 300):
        """Experiment 7: Long-Term Stability & Dynamic Equilibrium."""
        print("\n=== EXPERIMENT 7: Long-Term Stability ===")
        
        patterns = self.generate_patterns(5, dim=self.system.dim)
        counts = []
        energies = []
        
        print(f"Running continuous dynamic stream for {steps} steps...")
        
        for i in range(steps):
            pattern = patterns[i % len(patterns)]
            self.system.step(pattern, pattern, np.array([0.1]))
            counts.append(len(self.system.neurons))
            energies.append(sum(n.energy for n in self.system.neurons))
        
        self.results['stability'] = {'counts': counts, 'energies': energies}
        
        avg_count = np.mean(counts[-100:])
        std_count = np.std(counts[-100:])
        avg_energy = np.mean(energies[-100:])
        std_energy = np.std(energies[-100:])
        
        print(f"\nAssessment:")
        print(f"  Equilibrium neurons: {avg_count:.1f} ± {std_count:.1f}")
        print(f"  Equilibrium energy: {avg_energy:.2f} ± {std_energy:.2f}")
        
        return counts, energies
    
    # --- RUN ALL EXPERIMENTS ---
    
    def run_all(self):
        """Run all experiments in sequence."""
        print("=" * 70)
        print("ENN 4D TEST SUITE")
        print("=" * 70)
        
        experiments = [
            self.run_birth_experiment,
            self.run_clustering_experiment,
            self.run_amplification_experiment,
            self.run_damping_experiment,
            self.run_novelty_experiment,
            self.run_phase_transition_experiment,
            self.run_stability_experiment
        ]
        
        for experiment in experiments:
            try:
                experiment()
            except Exception as e:
                print(f"  ERROR: {e}")
                continue
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        summary = []
        
        if 'birth' in self.results:
            data = self.results['birth']
            summary.append(f"Birth rate: {(data[-1] - data[0]) / (len(data) - 1):.2f} neurons/event")
        
        if 'clustering' in self.results:
            data = self.results['clustering']
            summary.append(f"Number of families: {data['num_families']}")
            summary.append(f"Inter-family distance: {data['inter_mean']:.3f}")
        
        if 'amplification' in self.results:
            data = self.results['amplification']
            summary.append(f"Energy growth: {data[-1] - data[0]:.2f}")
        
        if 'damping' in self.results:
            data = self.results['damping']
            decay = data['energies'][0] - data['energies'][-1]
            summary.append(f"Energy decay: {decay:.2f} (Damping active)")
        
        if 'novelty' in self.results:
            summary.append(f"Novelty response: {self.results['novelty']} new neurons birthed")
        
        if 'phase_transition' in self.results:
            data = self.results['phase_transition']
            summary.append(f"Phase transition amplitude: {max(data['counts']) - min(data['counts'])} neurons")
        
        if 'stability' in self.results:
            data = self.results['stability']
            avg_count = np.mean(data['counts'][-100:])
            std_count = np.std(data['counts'][-100:])
            summary.append(f"Equilibrium stability: {avg_count:.1f} ± {std_count:.1f} neurons")
        
        for item in summary:
            print(f"  {item}")


if __name__ == "__main__":
    system = ENN4D(dim=4)
    tester = ENN4DTest(system)
    tester.run_all()
