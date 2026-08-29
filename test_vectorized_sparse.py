"""
True High-Speed Vectorized & Sparse Synaptic ENN 4D
===================================================
Uses pure NumPy vectorized force computations and sparse adjacency lookups.
"""

import time
import numpy as np
import sys
from typing import Optional, Dict, List, Tuple, Any
from enn4d import ENN4D, Neuron


class ENN4DVectorized(ENN4D):
    """
    Pure NumPy Vectorized Engine:
    - Never converts forces to Python lists in inner loop
    - Vectorized synaptic wave propagation
    - Cached array buffers
    """
    def __init__(self, dim: int = 4):
        super().__init__(dim=dim)
        self._cached_x = np.empty((0, dim), dtype=np.float32)
        self._cached_y = np.empty((0, dim), dtype=np.float32)
        self._cached_e = np.empty((0,), dtype=np.float32)
        self._is_dirty = True

    def _sync(self):
        if self._is_dirty:
            if not self.neurons:
                self._cached_x = np.empty((0, self.dim), dtype=np.float32)
                self._cached_y = np.empty((0, self.dim), dtype=np.float32)
                self._cached_e = np.empty((0,), dtype=np.float32)
            else:
                self._cached_x = np.array([n.x for n in self.neurons], dtype=np.float32)
                self._cached_y = np.array([n.y for n in self.neurons], dtype=np.float32)
                self._cached_e = np.array([n.energy for n in self.neurons], dtype=np.float32)
            self._is_dirty = False

    def birth(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, family: Optional[int] = None, text: str = "", role: str = "concept", features: Optional[np.ndarray] = None) -> Neuron:
        n = super().birth(x=x, y=y, z=z, family=family, text=text, role=role, features=features)
        self._is_dirty = True
        return n

    def compute_resonance_np(self, event_x: np.ndarray, event_y: np.ndarray) -> np.ndarray:
        """Computes force vector directly as float32 NumPy array (0 conversions)."""
        self._sync()
        if len(self.neurons) == 0:
            return np.empty((0,), dtype=np.float32)
            
        dx_sq = np.sum((self._cached_x - event_x) ** 2, axis=1)
        dy_sq = np.sum((self._cached_y - event_y) ** 2, axis=1)
        return 1.0 / (1.0 + 3.0 * (dx_sq + dy_sq))

    def interfere_np(self, forces_np: np.ndarray, event_y: Optional[np.ndarray] = None) -> np.ndarray:
        """Vectorized wave superposition."""
        n_count = len(self.neurons)
        if n_count == 0:
            return event_y.copy() if event_y is not None else np.zeros(self.dim, dtype=np.float32)
            
        direct_weights = forces_np * self._cached_e
        
        # Sparse synaptic propagation
        active_idx = np.where(forces_np > 0.08)[0]
        if len(active_idx) > 0:
            synaptic_boost = np.zeros(n_count, dtype=np.float32)
            for i in active_idx:
                f_val = forces_np[i]
                for target_idx, cond in self.neurons[i].synapses.items():
                    if target_idx < n_count:
                        synaptic_boost[target_idx] += f_val * cond * 0.35
            total_effective = direct_weights + synaptic_boost * self._cached_e
        else:
            total_effective = direct_weights

        mask = total_effective > 0.05
        tot_w = np.sum(total_effective[mask])
        if tot_w > 0:
            return np.sum(self._cached_y[mask] * total_effective[mask, None], axis=0) / tot_w
        return event_y.copy() if event_y is not None else np.zeros(self.dim, dtype=np.float32)


def benchmark_pure_vectorized():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 80)
    print("⚡ PURE NUMPY VECTORIZED ENN 4D BENCHMARK")
    print("=" * 80)
    
    rng = np.random.RandomState(42)
    test_sizes = [200, 1000, 3000, 10000]
    
    for N in test_sizes:
        enn = ENN4DVectorized(dim=4)
        for i in range(N):
            fam = i % 15
            x = rng.uniform(0.0, 1.0, size=4)
            y = rng.uniform(0.0, 1.0, size=4)
            z = np.array([float(i), 0.0, 0.0, 0.0])
            n = enn.birth(x=x, y=y, z=z, family=fam, text=f"Concept_{i}")
            
            num_syn = rng.randint(2, 6)
            for _ in range(num_syn):
                p = rng.randint(0, max(1, i))
                if p != i:
                    n.synapses[p] = float(rng.uniform(0.1, 0.8))
                    
        enn._sync()
        num_queries = 200
        queries_x = [rng.uniform(0.0, 1.0, size=4).astype(np.float32) for _ in range(num_queries)]
        queries_y = [rng.uniform(0.0, 1.0, size=4).astype(np.float32) for _ in range(num_queries)]
        
        t0 = time.perf_counter()
        for qx, qy in zip(queries_x, queries_y):
            f_np = enn.compute_resonance_np(qx, qy)
            out_y = enn.interfere_np(f_np, qy)
        elapsed = (time.perf_counter() - t0) * 1000.0
        
        step_ms = elapsed / num_queries
        fps = 1000.0 / step_ms
        
        print(f"📊 Scale: {N:>5} Neurons | Step Latency: {step_ms:>6.3f} ms | Frequency: {fps:>7.1f} Hz", flush=True)

    print("=" * 80, flush=True)

if __name__ == "__main__":
    benchmark_pure_vectorized()
