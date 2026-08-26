"""
ENN 4D: High-Performance Vectorized Living Physics Engine
With Robust Synaptic Wiring, Hebbian Plasticity, and Stable Topology Tracking.
"""

import sys
import json
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from collections import defaultdict

class Neuron:
    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: int, text: str = "", features: Optional[np.ndarray] = None):
        self.x = np.array(x, dtype=float).copy()           # Input coordinates (X)
        self.y = np.array(y, dtype=float).copy()           # Output coordinates (Y)
        self.z = np.array(z, dtype=float).copy()           # Temporal coordinate (Z)
        self.w = int(w)                                    # Family ID (W)
        self.text = str(text)                              # Natural language semantic concept
        self.features = np.array(features, dtype=float).copy() if features is not None else None
        
        # Physical properties
        self.energy = 1.0                                  # Mass / activation potential
        self.velocity_x = np.zeros_like(self.x)            # Momentum in X
        self.velocity_y = np.zeros_like(self.y)            # Momentum in Y
        self.velocity_z = np.zeros_like(self.z)            # Momentum in Z
        self.age = 0                                       # Time steps since birth
        self.connections: List[int] = []                   # Synaptic links (max 16)
        self.last_active = 0                               # Last activated step

    def clone(self) -> 'Neuron':
        daughter = Neuron(
            x=self.x + np.random.randn(*self.x.shape) * 0.04,
            y=self.y + np.random.randn(*self.y.shape) * 0.04,
            z=self.z.copy(),
            w=self.w,
            text=self.text,
            features=self.features
        )
        daughter.connections = list(self.connections)
        daughter.last_active = self.last_active
        return daughter


class ENN4D:
    def __init__(self, dim: int = 4):
        self.dim = dim
        self.neurons: List[Neuron] = []
        self.next_family_id = 0
        self.history = []
        self.energy_history = []
        self.event_count = 0
        
        # Physical & Family parameters
        self.epsilon = 0.40         # Novelty threshold for birth
        self.family_resonance_threshold = 0.55  # If prototype force > this, join family
        self.family_capacity = 16   # Max neurons in a family before sub-family mitosis
        self.merge_distance = 0.15  # Spatial merge threshold
        self.split_energy = 4.0     # Energy mitosis threshold
        self.decay_rate = 0.015     # Thermodynamic decay
        self.momentum = 0.4         # Spatial momentum
        self.baseline_energy = 0.15 # Basal metabolic floor
        self.min_energy = 0.05      # Pruning floor
        self.max_connections = 16   # Synaptic capacity per neuron

    # --- VECTORIZED MATRICES ---
    def _get_x_matrix(self) -> np.ndarray:
        if not self.neurons:
            return np.empty((0, self.dim))
        return np.array([n.x for n in self.neurons])

    def _get_y_matrix(self) -> np.ndarray:
        if not self.neurons:
            return np.empty((0, self.dim))
        return np.array([n.y for n in self.neurons])

    def _get_energy_vector(self) -> np.ndarray:
        if not self.neurons:
            return np.empty((0,))
        return np.array([n.energy for n in self.neurons])

    # --- FAMILY PROTOTYPES ---
    def get_all_family_prototypes(self) -> Dict[int, np.ndarray]:
        """Compute energy-weighted centroids for all active families."""
        families = defaultdict(list)
        for n in self.neurons:
            families[n.w].append(n)
            
        prototypes = {}
        for w, members in families.items():
            energies = np.array([m.energy for m in members])
            xs = np.array([m.x for m in members])
            total_e = np.sum(energies)
            prototypes[w] = (np.sum(xs * energies[:, None], axis=0) / total_e) if total_e > 0 else np.mean(xs, axis=0)
        return prototypes

    def find_best_family(self, event_x: np.ndarray) -> Tuple[Optional[int], float]:
        """Fast vectorized prototype search."""
        prototypes = self.get_all_family_prototypes()
        if not prototypes:
            return None, 0.0
            
        fam_ids = list(prototypes.keys())
        proto_mat = np.array([prototypes[w] for w in fam_ids])
        
        dist_sq = np.sum((proto_mat - event_x) ** 2, axis=1)
        forces = 1.0 / (1.0 + 3.0 * dist_sq)
        
        best_idx = np.argmax(forces)
        return fam_ids[best_idx], float(forces[best_idx])

    # --- 1. VECTORIZED RESONANCE ---
    def compute_resonance(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray) -> List[float]:
        """Vectorized field resonance force calculation."""
        if not self.neurons:
            return []
        x_mat = self._get_x_matrix()
        y_mat = self._get_y_matrix()
        
        dx_sq = np.sum((x_mat - event_x) ** 2, axis=1)
        dy_sq = np.sum((y_mat - event_y) ** 2, axis=1)
        forces = 1.0 / (1.0 + 3.0 * (dx_sq + dy_sq))
        return forces.tolist()

    # --- 2. VECTORIZED INTERFERENCE ---
    def interfere(self, event_x: np.ndarray, forces: List[float], event_y: Optional[np.ndarray] = None) -> np.ndarray:
        if not self.neurons:
            return event_y.copy() if event_y is not None else np.zeros(self.dim)
            
        f_arr = np.array(forces)
        e_arr = self._get_energy_vector()
        weights = f_arr * e_arr
        
        mask = f_arr > 0.05
        total_w = np.sum(weights[mask])
        if total_w > 0:
            y_mat = self._get_y_matrix()
            return np.sum(y_mat[mask] * weights[mask, None], axis=0) / total_w
        return event_y.copy() if event_y is not None else np.zeros(self.dim)

    # --- 3. HEBBIAN AMPLIFICATION & SYNAPSE WIRING ---
    def amplify(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, forces: List[float], signal_magnitude: float):
        if signal_magnitude < 1e-4 or not self.neurons:
            return
            
        f_arr = np.array(forces)
        active_indices = np.where(f_arr > 0.1)[0]
        
        for i in active_indices:
            force = f_arr[i]
            n = self.neurons[i]
            n.energy += force * signal_magnitude * 0.20
            n.last_active = self.event_count
            
            shift_x = (event_x - n.x) * force * 0.08
            shift_y = (event_y - n.y) * force * 0.08
            
            n.velocity_x = (n.velocity_x + shift_x) * self.momentum
            n.velocity_y = (n.velocity_y + shift_y) * self.momentum
            n.x += n.velocity_x
            n.y += n.velocity_y
            n.z = 0.9 * n.z + 0.1 * event_z
            n.age += 1

        # Hebbian synaptic wiring: Active neurons wiring together, sorted by resonance force!
        if len(active_indices) > 1:
            sorted_active = active_indices[np.argsort(f_arr[active_indices])[::-1]][:6]
            for i in sorted_active:
                for j in sorted_active:
                    if i != j:
                        if j not in self.neurons[i].connections and len(self.neurons[i].connections) < self.max_connections:
                            self.neurons[i].connections.append(int(j))
                        if i not in self.neurons[j].connections and len(self.neurons[j].connections) < self.max_connections:
                            self.neurons[j].connections.append(int(i))

    # --- 4. DAMPING & HOMEOSTASIS ---
    def dampen(self):
        for n in self.neurons:
            inactivity = max(0, self.event_count - n.last_active)
            decay = self.decay_rate * (1.0 + inactivity * 0.01)
            
            if n.energy > self.baseline_energy:
                n.energy = max(self.baseline_energy, n.energy - decay)
            else:
                n.energy = min(self.baseline_energy, n.energy + np.random.uniform(0.0005, 0.002))
            
            n.x += np.random.randn(*n.x.shape) * 0.0005
            n.y += np.random.randn(*n.y.shape) * 0.0005

    # --- 5. PHASE TRANSITIONS ---
    def phase_transition(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, signal_magnitude: float, text: str = "", features: Optional[np.ndarray] = None):
        if signal_magnitude > 1e-4:
            if not self.neurons:
                self.birth(event_x, event_y, event_z, None, text=text, features=features)
            else:
                best_family, proto_force = self.find_best_family(event_x)
                forces = self.compute_resonance(event_x, event_y, event_z)
                max_force = max(forces) if forces else 0.0
                
                if max_force < self.epsilon and proto_force < self.family_resonance_threshold:
                    self.birth(event_x, event_y, event_z, None, text=text, features=features)
                else:
                    target_fam = best_family if best_family is not None else 0
                    self.birth(event_x, event_y, event_z, target_fam, text=text, features=features)

        # Periodic maintenance
        if self.event_count % 15 == 0:
            self.check_family_capacities()
            self.merge_neurons()
            self.clean_connections()

    def birth(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, family: Optional[int] = None, text: str = "", features: Optional[np.ndarray] = None) -> Neuron:
        """Birth a new neuron and construct synaptic bridges to nearest neighbors."""
        if family is None:
            family = self.next_family_id
            self.next_family_id += 1
            
        new_neuron = Neuron(x, y, z, family, text=text, features=features)
        new_neuron.last_active = self.event_count
        new_neuron.energy = 2.0
        
        new_idx = len(self.neurons)
        if self.neurons:
            x_mat = self._get_x_matrix()
            dists = np.linalg.norm(x_mat - x, axis=1)
            
            # Wire to top 4 spatially closest neighbors in 4D space
            nearest_indices = np.argsort(dists)[:4]
            for peer_idx in nearest_indices:
                peer_idx = int(peer_idx)
                new_neuron.connections.append(peer_idx)
                if new_idx not in self.neurons[peer_idx].connections and len(self.neurons[peer_idx].connections) < self.max_connections:
                    self.neurons[peer_idx].connections.append(new_idx)
                
        self.neurons.append(new_neuron)
        return new_neuron

    def check_family_capacities(self):
        family_members = defaultdict(list)
        for i, n in enumerate(self.neurons):
            family_members[n.w].append(i)
            
        for w, indices in list(family_members.items()):
            if len(indices) > self.family_capacity:
                self.split_family(w, indices)

    def split_family(self, family_id: int, member_indices: List[int]):
        pts = np.array([self.neurons[i].x for i in member_indices])
        mean_pt = np.mean(pts, axis=0)
        
        u, s, vt = np.linalg.svd(pts - mean_pt)
        v0 = vt[0] if len(vt) > 0 else np.ones(self.dim)
        
        new_fam_id = self.next_family_id
        self.next_family_id += 1
        
        for idx in member_indices:
            if np.dot(self.neurons[idx].x - mean_pt, v0) > 0:
                self.neurons[idx].w = new_fam_id

    def clean_connections(self):
        """Sanitize and deduplicate connections within valid bounds."""
        n_count = len(self.neurons)
        for i, n in enumerate(self.neurons):
            valid_conns = []
            for c in n.connections:
                if 0 <= c < n_count and c != i and c not in valid_conns:
                    valid_conns.append(c)
            n.connections = valid_conns[:self.max_connections]

    def merge_neurons(self):
        if len(self.neurons) < 2:
            return
        x_mat = self._get_x_matrix()
        families = np.array([n.w for n in self.neurons])
        
        merged = set()
        for i in range(len(self.neurons)):
            if i in merged: continue
            same_fam = np.where((families == families[i]) & (np.arange(len(self.neurons)) > i))[0]
            if len(same_fam) == 0: continue
            
            dists = np.linalg.norm(x_mat[same_fam] - x_mat[i], axis=1)
            close_idx = same_fam[np.where(dists < self.merge_distance)[0]]
            
            for j in close_idx:
                if j in merged: continue
                n1, n2 = self.neurons[i], self.neurons[j]
                total_e = n1.energy + n2.energy
                n1.x = (n1.x * n1.energy + n2.x * n2.energy) / total_e
                n1.y = (n1.y * n1.energy + n2.y * n2.energy) / total_e
                n1.energy = total_e * 0.85
                if not n1.text and n2.text: n1.text = n2.text
                
                # Merge connection sets
                n1.connections = list(set(n1.connections + n2.connections))
                merged.add(j)
                
        if merged:
            surviving = [n for idx, n in enumerate(self.neurons) if idx not in merged]
            old_to_new = {old: new for new, old in enumerate([i for i in range(len(self.neurons)) if i not in merged])}
            for n in surviving:
                n.connections = [old_to_new[c] for c in n.connections if c in old_to_new and old_to_new[c] != surviving.index(n)]
            self.neurons = surviving
            self.clean_connections()

    # --- PHYSICAL STEP ---
    def step(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, text: str = "", features: Optional[np.ndarray] = None) -> np.ndarray:
        self.event_count += 1
        signal_magnitude = float(np.linalg.norm(event_x) + np.linalg.norm(event_y)) / 2.0
        
        forces = self.compute_resonance(event_x, event_y, event_z)
        output_y = self.interfere(event_x, forces, event_y)
        self.amplify(event_x, event_y, event_z, forces, signal_magnitude)
        self.dampen()
        self.phase_transition(event_x, event_y, event_z, signal_magnitude, text=text, features=features)
        
        self.history.append(len(self.neurons))
        self.energy_history.append(sum(n.energy for n in self.neurons))
        return output_y

    # --- HIERARCHICAL RESONANCE PROBE ---
    def probe_resonance(self, query_x: np.ndarray, query_features: Optional[np.ndarray] = None, top_k: int = 3) -> List[Tuple[Neuron, float]]:
        if not self.neurons:
            return []

        prototypes = self.get_all_family_prototypes()
        if not prototypes:
            return []

        # Tier 1: Rank families by prototype resonance
        fam_ids = list(prototypes.keys())
        proto_mat = np.array([prototypes[w] for w in fam_ids])
        dist_sq = np.sum((proto_mat - query_x) ** 2, axis=1)
        f_forces = 1.0 / (1.0 + 3.0 * dist_sq)
        
        top_fam_indices = np.argsort(f_forces)[::-1][:max(3, len(fam_ids) // 3)]
        top_families = set(fam_ids[idx] for idx in top_fam_indices)
        
        # Tier 2: Score candidate neurons
        candidates = [n for n in self.neurons if n.w in top_families and n.text]
        if not candidates:
            candidates = [n for n in self.neurons if n.text]

        scored = []
        for n in candidates:
            norm_qx, norm_nx = np.linalg.norm(query_x), np.linalg.norm(n.x)
            sim_4d = float(np.dot(query_x / norm_qx, n.x / norm_nx)) if norm_qx > 0 and norm_nx > 0 else 0.0
            
            sim_feat = 0.0
            if query_features is not None and n.features is not None:
                norm_qf, norm_nf = np.linalg.norm(query_features), np.linalg.norm(n.features)
                if norm_qf > 0 and norm_nf > 0:
                    sim_feat = float(np.dot(query_features / norm_qf, n.features / norm_nf))
                    
            dist_sq = np.sum((query_x - n.x) ** 2)
            force = 1.0 / (1.0 + 3.0 * dist_sq)
            
            semantic_score = (0.6 * sim_feat + 0.4 * max(0.0, sim_4d)) if query_features is not None else max(0.0, sim_4d)
            activation = force * n.energy * (1.0 + 3.0 * semantic_score)
            scored.append((n, float(activation)))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    # --- PERSISTENCE ---
    def save(self, filepath: str = "universe.json"):
        self.clean_connections()
        data = {
            "event_count": self.event_count,
            "next_family_id": self.next_family_id,
            "total_energy": float(sum(n.energy for n in self.neurons)),
            "total_neurons": len(self.neurons),
            "num_families": len(set(n.w for n in self.neurons)),
            "total_connections": sum(len(n.connections) for n in self.neurons),
            "neurons": [
                {
                    "id": i,
                    "x": np.round(n.x, 4).tolist(),
                    "y": np.round(n.y, 4).tolist(),
                    "z": np.round(n.z, 4).tolist(),
                    "w": int(n.w),
                    "text": n.text,
                    "energy": float(np.round(n.energy, 4)),
                    "age": int(n.age),
                    "connections": [int(c) for c in n.connections if c < len(self.neurons) and c != i],
                    "last_active": int(n.last_active)
                }
                for i, n in enumerate(self.neurons)
            ]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, filepath: str = "universe.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.event_count = data["event_count"]
        self.next_family_id = data["next_family_id"]
        self.neurons = []
        for d in data["neurons"]:
            n = Neuron(
                np.array(d["x"]),
                np.array(d["y"]),
                np.array(d["z"]),
                d["w"],
                text=d.get("text", "")
            )
            n.energy = float(d["energy"])
            n.age = int(d["age"])
            n.connections = list(d.get("connections", []))
            n.last_active = int(d.get("last_active", 0))
            self.neurons.append(n)
