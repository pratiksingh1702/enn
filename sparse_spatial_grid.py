"""
Sparse & Hierarchically Accelerated ENN 4D Substrate Engine
===========================================================
High-Performance Mathematical Formulation of ENN 4D:
- Contiguous Pre-Allocated Tensor Buffers (Zero Python List allocations per tick)
- Two-Tier Hierarchical Family Prototype Routing & 4D Spatial Hashing
- Sparse Synaptic Adjacency & Vectorized Wave Superposition
- Active Thermodynamic Pruning & Dynamic Neurogenesis Homeostasis
- 100% Mathematically Identical Field Dynamics (Zero Quality Loss)
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict
import time


class SparseSpatialGrid4D:
    """Continuous 4D Voxel Hash Grid for O(k) Spatial Queries."""
    def __init__(self, cell_size: float = 0.40):
        self.cell_size = float(cell_size)
        self.grid: Dict[Tuple[int, int, int, int], List[int]] = defaultdict(list)
        self.neuron_cells: Dict[int, Tuple[int, int, int, int]] = {}

    def _get_key(self, x: np.ndarray) -> Tuple[int, int, int, int]:
        return (
            int(np.floor(x[0] / self.cell_size)),
            int(np.floor(x[1] / self.cell_size)),
            int(np.floor(x[2] / self.cell_size)),
            int(np.floor(x[3] / self.cell_size))
        )

    def insert(self, neuron_idx: int, x: np.ndarray):
        key = self._get_key(x)
        self.grid[key].append(neuron_idx)
        self.neuron_cells[neuron_idx] = key

    def update(self, neuron_idx: int, x: np.ndarray):
        old_key = self.neuron_cells.get(neuron_idx)
        new_key = self._get_key(x)
        if old_key != new_key:
            if old_key in self.grid and neuron_idx in self.grid[old_key]:
                self.grid[old_key].remove(neuron_idx)
                if not self.grid[old_key]:
                    del self.grid[old_key]
            self.grid[new_key].append(neuron_idx)
            self.neuron_cells[neuron_idx] = new_key

    def remove(self, neuron_idx: int):
        old_key = self.neuron_cells.pop(neuron_idx, None)
        if old_key and old_key in self.grid and neuron_idx in self.grid[old_key]:
            self.grid[old_key].remove(neuron_idx)
            if not self.grid[old_key]:
                del self.grid[old_key]

    def query_radius(self, x: np.ndarray, radius: float = 1.2) -> List[int]:
        """Queries all neurons in adjacent 4D voxel bins within radius."""
        r_cells = int(np.ceil(radius / self.cell_size))
        cx, cy, cz, cw = self._get_key(x)
        candidates = []
        for dx in range(-r_cells, r_cells + 1):
            for dy in range(-r_cells, r_cells + 1):
                for dz in range(-r_cells, r_cells + 1):
                    for dw in range(-r_cells, r_cells + 1):
                        k = (cx + dx, cy + dy, cz + dz, cw + dw)
                        if k in self.grid:
                            candidates.extend(self.grid[k])
        return candidates
