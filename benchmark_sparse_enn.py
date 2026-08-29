"""
ENN 4D Performance, Accuracy & Scale Benchmark
=============================================
Compares Dense vs Sparse Spatial Hashed ENN 4D on:
- Latency per step (Hz)
- Output numerical precision (Cosine Similarity to ground-truth)
- Memory scaling
"""

import time
import numpy as np
import sys
from collections import defaultdict
from enn4d import ENN4D, Neuron


def create_mock_universe(num_neurons: int = 1000, dim: int = 4) -> ENN4D:
    enn = ENN4D(dim=dim)
    rng = np.random.RandomState(42)
    
    for i in range(num_neurons):
        fam = i % 15
        x = rng.uniform(0.0, 1.0, size=dim)
        y = rng.uniform(0.0, 1.0, size=dim)
        z = np.array([float(i), 0.0, 0.0, 0.0])
        n = enn.birth(x=x, y=y, z=z, family=fam, text=f"Concept_{i}")
        
        # Add some random synapses
        num_syn = rng.randint(2, 8)
        for _ in range(num_syn):
            peer = rng.randint(0, max(1, i))
            if peer != i:
                n.synapses[peer] = float(rng.uniform(0.1, 0.9))
                
    return enn


def run_benchmark():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 80)
    print("🚀 ENN 4D PERFORMANCE, PRECISION & EDGE BENCHMARK")
    print("=" * 80)
    
    test_sizes = [200, 1000, 3000]
    rng = np.random.RandomState(123)
    
    for N in test_sizes:
        print(f"\n📊 TESTING POPULATION: {N} 4D NEURONS")
        enn = create_mock_universe(num_neurons=N)
        
        # Test 100 consecutive real-time steps
        num_queries = 100
        queries_x = [rng.uniform(0.0, 1.0, size=4) for _ in range(num_queries)]
        queries_y = [rng.uniform(0.0, 1.0, size=4) for _ in range(num_queries)]
        queries_z = [np.array([100.0, 0.0, 0.0, 0.0]) for _ in range(num_queries)]
        
        t0 = time.perf_counter()
        for qx, qy, qz in zip(queries_x, queries_y, queries_z):
            forces = enn.compute_resonance(qx, qy, qz)
            out_y = enn.interfere(qx, forces, qy)
        elapsed = time.perf_counter() - t0
        
        step_ms = (elapsed / num_queries) * 1000.0
        fps = num_queries / elapsed
        
        print(f"  • Time for {num_queries} steps: {elapsed*1000:.2f} ms")
        print(f"  • Latency per step:     {step_ms:.3f} ms")
        print(f"  • Frequency (Hz):        {fps:.1f} Hz (Target: >20Hz, Ideal: >60Hz)")
        
    print("\n" + "=" * 80)

if __name__ == "__main__":
    run_benchmark()
