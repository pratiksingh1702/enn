"""
ENN 4D: Living Physics Engine with Continuous Synaptic Weight Fields
Synaptic Bridges operate as physical conductance channels:
1. Weight Initialization: Emerges from 4D spatial inverse-distance geometry W_ij = 1 / (1 + 2 * ||x_i - x_j||^2).
2. Hebbian Potentiation: W_ij increases with co-activation energy product (F_i * F_j * min(E_i, E_j)).
3. Synaptic Decay: Bridges decay thermodynamically with inactivity.
4. Synaptic Pruning: Phase transition dissolving connections below critical conductance (W_ij < 0.05).
5. Synaptic Signal Conduction: Signal propagation through bridges modulates wave interference.
"""

import sys
import json
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from collections import defaultdict
from meta_learning import MetaField
from self_awareness import MetacognitiveEngine

class Neuron:
    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: int, text: str = "", features: Optional[np.ndarray] = None, origin: float = 1.0, epistemic_tension: float = 0.0, role: str = "concept"):
        self.x = np.array(x, dtype=float).copy()           # Input coordinates (X)
        self.y = np.array(y, dtype=float).copy()           # Output coordinates (Y)
        self.z = np.array(z, dtype=float).copy()           # Temporal coordinate (Z)
        self.w = int(w)                                    # Family ID (W)
        self.text = str(text)                              # Natural language semantic concept
        self.features = np.array(features, dtype=float).copy() if features is not None else None
        
        # Self vs. Environment Field Boundary: 0.0 = Self / Internal Thought, 1.0 = External Sensory
        self.origin = float(origin)
        # Curiosity Vacuum / Epistemic Tension: > 0.0 indicates an unresolved inquiry / knowledge void
        self.epistemic_tension = float(epistemic_tension)
        self.role = str(role)                              # "concept", "anchor", "relation", "vacuum", "insight"
        
        # Physical properties
        self.energy = 1.0                                  # Mass / activation potential
        self.velocity_x = np.zeros_like(self.x)            # Momentum in X
        self.velocity_y = np.zeros_like(self.y)            # Momentum in Y
        self.velocity_z = np.zeros_like(self.z)            # Momentum in Z
        self.age = 0                                       # Time steps since birth
        self.last_active = 0                               # Last activated step
        
        # Synaptic Bridge Field: peer_index -> conductance weight W_ij in (0.0, 1.0]
        self.synapses: Dict[int, float] = {}

    def clone(self) -> 'Neuron':
        daughter = Neuron(
            x=self.x + np.random.randn(*self.x.shape) * 0.04,
            y=self.y + np.random.randn(*self.y.shape) * 0.04,
            z=self.z.copy(),
            w=self.w,
            text=self.text,
            features=self.features,
            origin=self.origin,
            epistemic_tension=self.epistemic_tension * 0.5,
            role=self.role
        )
        # Inherit synaptic conductances with biological dilution
        daughter.synapses = {k: v * 0.7 for k, v in self.synapses.items()}
        daughter.last_active = self.last_active
        return daughter

    # Backward compatibility property for visualizers expecting connection lists
    @property
    def connections(self) -> List[int]:
        return list(self.synapses.keys())


class ENN4D:
    def __init__(self, dim: int = 4):
        self.dim = dim
        self.neurons: List[Neuron] = []
        self.next_family_id = 0
        self.history = []
        self.energy_history = []
        self.event_count = 0
        self.question_stack: List[Dict[str, Any]] = []      # Epistemic voids / unresolved curiosity tensions
        
        # Physical & Family parameters
        self.epsilon = 0.40                 # Novelty threshold for birth
        self.curiosity_threshold = 0.38     # Knowledge void threshold (weak resonance triggers curiosity)
        self.family_resonance_threshold = 0.55  # If prototype force > this, join family
        self.family_capacity = 16           # Max neurons in a family before sub-family mitosis
        self.merge_distance = 0.15          # Spatial merge threshold
        self.split_energy = 4.0             # Energy mitosis threshold
        self.decay_rate = 0.015             # Thermodynamic decay
        self.synapse_decay_rate = 0.008     # Synaptic conductance decay rate
        self.synapse_prune_threshold = 0.05 # Phase transition: conductance dissolves below this
        self.max_synapses = 16              # Max synaptic channels per neuron
        self.momentum = 0.4                 # Spatial momentum
        self.baseline_energy = 0.15         # Basal metabolic floor
        self.min_energy = 0.05              # Pruning floor

    def reset(self):
        """Reset the physical universe to an empty primordial state."""
        self.neurons = []
        self.next_family_id = 0
        self.history = []
        self.energy_history = []
        self.event_count = 0
        self.question_stack = []

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

    # --- 2. VECTORIZED SYNAPTIC INTERFERENCE ---
    def interfere(self, event_x: np.ndarray, forces: List[float], event_y: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Wave superposition modulated by continuous synaptic conductance field.
        Active neurons propagate signal through their synaptic channels.
        """
        if not self.neurons:
            return event_y.copy() if event_y is not None else np.zeros(self.dim)
            
        f_arr = np.array(forces)
        e_arr = self._get_energy_vector()
        
        # Base direct field activation
        direct_weights = f_arr * e_arr
        
        # Synaptically conducted lateral wave activation
        synaptic_boost = np.zeros(len(self.neurons))
        for i, n in enumerate(self.neurons):
            if f_arr[i] > 0.05:
                for target_idx, conductance in n.synapses.items():
                    if target_idx < len(self.neurons):
                        synaptic_boost[target_idx] += f_arr[i] * conductance * 0.35
                        
        total_effective_weights = direct_weights + synaptic_boost * e_arr
        mask = total_effective_weights > 0.05
        
        total_w = np.sum(total_effective_weights[mask])
        if total_w > 0:
            y_mat = self._get_y_matrix()
            return np.sum(y_mat[mask] * total_effective_weights[mask, None], axis=0) / total_w
        return event_y.copy() if event_y is not None else np.zeros(self.dim)

    # --- 3. HEBBIAN SYNAPTIC POTENTIATION & AMPLIFICATION ---
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

        # Hebbian Synaptic Potentiation: Co-activating neurons strengthen their bridge conductance W_ij
        if len(active_indices) > 1:
            sorted_active = active_indices[np.argsort(f_arr[active_indices])[::-1]][:6]
            for i in sorted_active:
                for j in sorted_active:
                    if i != j:
                        f_i = f_arr[i]
                        f_j = f_arr[j]
                        e_min = min(self.neurons[i].energy, self.neurons[j].energy)
                        
                        # Potentiation emerges from the product of co-activation forces
                        delta_w = 0.15 * (f_i * f_j) * (e_min / 2.0)
                        
                        # Update or establish bridge
                        current_w = self.neurons[i].synapses.get(int(j), 0.0)
                        if current_w == 0.0 and len(self.neurons[i].synapses) < self.max_synapses:
                            # Emergent initial geometric bridge
                            dist_sq = np.sum((self.neurons[i].x - self.neurons[j].x) ** 2)
                            initial_w = 1.0 / (1.0 + 2.0 * dist_sq)
                            self.neurons[i].synapses[int(j)] = float(min(1.0, initial_w + delta_w))
                        elif current_w > 0.0:
                            # Potentiate existing bridge
                            self.neurons[i].synapses[int(j)] = float(min(1.0, current_w + delta_w))

    # --- 4. THERMODYNAMIC DAMPING & SYNAPTIC DECAY ---
    def dampen(self):
        for i, n in enumerate(self.neurons):
            inactivity = max(0, self.event_count - n.last_active)
            decay = self.decay_rate * (1.0 + inactivity * 0.01)
            
            # Particle energy damping
            if n.energy > self.baseline_energy:
                n.energy = max(self.baseline_energy, n.energy - decay)
            else:
                n.energy = min(self.baseline_energy, n.energy + np.random.uniform(0.0005, 0.002))
            
            # Continuous Synaptic Conductance Decay: unused bridges lose strength
            decayed_synapses = {}
            for target_idx, w_ij in n.synapses.items():
                target_inactivity = max(0, self.event_count - self.neurons[target_idx].last_active) if target_idx < len(self.neurons) else inactivity
                syn_decay = self.synapse_decay_rate * (1.0 + target_inactivity * 0.005)
                new_w = w_ij * (1.0 - syn_decay)
                
                # Synaptic Pruning Phase Transition: Dissolve if below critical point
                if new_w >= self.synapse_prune_threshold:
                    decayed_synapses[target_idx] = float(new_w)
            n.synapses = decayed_synapses
            
            # Small Brownian thermal fluctuations
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

    def detect_epistemic_void(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, text: str, max_force: float, features: Optional[np.ndarray] = None) -> Optional[Dict[str, Any]]:
        """
        Curiosity Vacuum: If an incoming sensory wave has low resonance with existing knowledge,
        nature abhors a vacuum -> an epistemic tension gradient forms to seek resolution.
        """
        if max_force < self.curiosity_threshold and text.strip():
            tension = float(np.round(1.0 - max_force, 4))
            void_record = {
                "text": text,
                "tension": tension,
                "x": event_x.tolist(),
                "y": event_y.tolist(),
                "z": event_z.tolist(),
                "created_at": self.event_count,
                "features": features.tolist() if features is not None else None
            }
            self.question_stack.append(void_record)
            if len(self.question_stack) > 20:
                self.question_stack.pop(0)
            return void_record
        return None

    def birth(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, family: Optional[int] = None, text: str = "", features: Optional[np.ndarray] = None, origin: float = 1.0, epistemic_tension: float = 0.0, role: str = "concept") -> Neuron:
        """
        Birth a new neuron particle.
        Synaptic bridge conductances emerge from inverse-square spatial proximity.
        """
        if family is None:
            family = self.next_family_id
            self.next_family_id += 1
            
        new_neuron = Neuron(x, y, z, family, text=text, features=features, origin=origin, epistemic_tension=epistemic_tension, role=role)
        new_neuron.last_active = self.event_count
        new_neuron.energy = 2.0
        
        new_idx = len(self.neurons)
        if self.neurons:
            x_mat = self._get_x_matrix()
            dist_sqs = np.sum((x_mat - x) ** 2, axis=1)
            
            # Connect to top 4 spatially closest neighbors
            nearest_indices = np.argsort(dist_sqs)[:4]
            for peer_idx in nearest_indices:
                peer_idx = int(peer_idx)
                d_sq = dist_sqs[peer_idx]
                
                # Conductance weight W_ij emerges from spatial proximity
                w_ij = float(1.0 / (1.0 + 2.0 * d_sq))
                new_neuron.synapses[peer_idx] = w_ij
                
                if len(self.neurons[peer_idx].synapses) < self.max_synapses:
                    self.neurons[peer_idx].synapses[new_idx] = w_ij
                
        self.neurons.append(new_neuron)
        return new_neuron

    def birth_constellation(self, nodes: List[Dict[str, Any]], family: Optional[int] = None) -> List[Neuron]:
        """
        Birth an interconnected geometric constellation (micro-circuit) representing a relational event.
        Nodes within the constellation receive strong mutual synaptic conductance (W_ij = 0.90).
        """
        if not nodes:
            return []
            
        if family is None:
            anchor_node = next((n for n in nodes if n.get("role") == "anchor"), nodes[0])
            best_fam, proto_force = self.find_best_family(anchor_node["x"])
            if best_fam is not None and proto_force >= self.family_resonance_threshold:
                family = best_fam
            else:
                family = self.next_family_id
                self.next_family_id += 1
                
        birthed = []
        start_idx = len(self.neurons)
        for node in nodes:
            n = self.birth(
                x=node["x"],
                y=node.get("y", node["x"]),
                z=node.get("z", np.array([0.0])),
                family=family,
                text=node.get("text", ""),
                features=node.get("features"),
                origin=node.get("origin", 1.0),
                epistemic_tension=node.get("epistemic_tension", 0.0),
                role=node.get("role", "concept")
            )
            birthed.append(n)
            
        # Wire high-conductance mutual synaptic bonds within the constellation (W_ij = 0.90)
        end_idx = len(self.neurons)
        constellation_indices = list(range(start_idx, end_idx))
        for i in constellation_indices:
            for j in constellation_indices:
                if i != j:
                    self.neurons[i].synapses[j] = 0.90
                    
        return birthed

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
        """Sanitize, deduplicate, and prune synaptic channels."""
        n_count = len(self.neurons)
        for i, n in enumerate(self.neurons):
            valid_synapses = {}
            for target_idx, w_ij in n.synapses.items():
                if 0 <= target_idx < n_count and target_idx != i:
                    if w_ij >= self.synapse_prune_threshold:
                        valid_synapses[target_idx] = float(np.round(min(1.0, max(0.0, w_ij)), 4))
            n.synapses = valid_synapses

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
                
                # Combine synaptic weights (maximum conductance superposition)
                for k, w_val in n2.synapses.items():
                    if k != i:
                        n1.synapses[k] = max(n1.synapses.get(k, 0.0), w_val)
                merged.add(j)
                
        if merged:
            surviving = [n for idx, n in enumerate(self.neurons) if idx not in merged]
            old_to_new = {old: new for new, old in enumerate([i for i in range(len(self.neurons)) if i not in merged])}
            for new_idx, n in enumerate(surviving):
                remapped_synapses = {}
                for old_target, w_val in n.synapses.items():
                    if old_target in old_to_new:
                        new_target = old_to_new[old_target]
                        if new_target != new_idx:
                            remapped_synapses[new_target] = w_val
                n.synapses = remapped_synapses
            self.neurons = surviving
            self.clean_connections()

    # --- PHYSICAL STEP & CONSTELLATION STEP ---
    def step(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, text: str = "", features: Optional[np.ndarray] = None, origin: float = 1.0) -> Tuple[np.ndarray, Optional[Dict[str, Any]]]:
        self.event_count += 1
        signal_magnitude = float(np.linalg.norm(event_x) + np.linalg.norm(event_y)) / 2.0
        
        forces = self.compute_resonance(event_x, event_y, event_z)
        max_force = max(forces) if forces else 0.0
        output_y = self.interfere(event_x, forces, event_y)
        self.amplify(event_x, event_y, event_z, forces, signal_magnitude)
        self.dampen()
        self.phase_transition(event_x, event_y, event_z, signal_magnitude, text=text, features=features)
        
        # Check for epistemic curiosity vacuum
        void_event = self.detect_epistemic_void(event_x, event_y, event_z, text, max_force, features)
        
        self.history.append(len(self.neurons))
        self.energy_history.append(sum(n.energy for n in self.neurons))
        return output_y, void_event

    def step_constellation(self, nodes: List[Dict[str, Any]], text: str = "") -> Tuple[np.ndarray, Optional[Dict[str, Any]]]:
        """
        Step a relational constellation event into the universe.
        Preserves geometric micro-circuit connections between semantic components.
        """
        self.event_count += 1
        if not nodes:
            return np.zeros(self.dim), None
            
        anchor = next((n for n in nodes if n.get("role") == "anchor"), nodes[0])
        event_x = anchor["x"]
        event_y = anchor.get("y", anchor["x"])
        event_z = anchor.get("z", np.array([0.0]))
        features = anchor.get("features")
        
        signal_magnitude = float(np.linalg.norm(event_x) + np.linalg.norm(event_y)) / 2.0
        forces = self.compute_resonance(event_x, event_y, event_z)
        max_force = max(forces) if forces else 0.0
        
        output_y = self.interfere(event_x, forces, event_y)
        self.amplify(event_x, event_y, event_z, forces, signal_magnitude)
        self.dampen()
        
        # Check curiosity vacuum
        void_event = self.detect_epistemic_void(event_x, event_y, event_z, text, max_force, features)
        
        # Birth constellation micro-circuit
        self.birth_constellation(nodes)
        
        # Periodic maintenance
        if self.event_count % 15 == 0:
            self.check_family_capacities()
            self.merge_neurons()
            self.clean_connections()
            
        self.history.append(len(self.neurons))
        self.energy_history.append(sum(n.energy for n in self.neurons))
        return output_y, void_event

    # --- MULTI-STEP WAVE PROPAGATION (REASONING TRAJECTORY) ---
    def propagate_wave(self, source_x: np.ndarray, steps: int = 4, damping: float = 0.15, initial_amplitude: float = 1.0) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Multi-Step Damped Wave Propagation across the 4D neural substrate.
        Wave cascades from local resonance along synaptic conductance highways (W_ij).
        Tracks and returns the detailed physical trajectory (wave_path).
        """
        if not self.neurons:
            return source_x.copy(), []
            
        current_wave = np.array(source_x, dtype=float).copy()
        norm = np.linalg.norm(current_wave)
        if norm > 0:
            current_wave = current_wave / norm
            
        wave_path = []
        visited_neurons = set()
        amplitude = float(initial_amplitude)
        
        for s in range(1, steps + 1):
            # Compute resonance of current wavefront with all neurons
            forces = self.compute_resonance(current_wave, current_wave, np.array([0.0]))
            f_arr = np.array(forces)
            
            # Find active resonant nodes at this hop
            active_indices = np.where(f_arr > 0.15)[0]
            if len(active_indices) == 0:
                active_indices = [int(np.argmax(f_arr))]
                
            step_hops = []
            next_wave_components = []
            
            for idx in active_indices:
                n = self.neurons[idx]
                f_val = float(f_arr[idx])
                
                hop_entry = {
                    "step": s,
                    "neuron_id": int(idx),
                    "text": n.text,
                    "family": int(n.w),
                    "force": float(np.round(f_val, 4)),
                    "energy": float(np.round(n.energy, 4)),
                    "amplitude": float(np.round(amplitude, 4)),
                    "synapses": {int(k): float(np.round(v, 4)) for k, v in n.synapses.items() if v > 0.1}
                }
                step_hops.append(hop_entry)
                visited_neurons.add(idx)
                
                # Neuron contributes its output coordinate Y weighted by force & energy
                node_weight = f_val * n.energy * amplitude
                next_wave_components.append(n.y * node_weight)
                
                # Synaptic conduction boost: forward wave propagates along synaptic highways
                for target_idx, w_ij in n.synapses.items():
                    if target_idx < len(self.neurons) and target_idx not in visited_neurons:
                        target_n = self.neurons[target_idx]
                        synaptic_wave = target_n.y * (node_weight * w_ij * 0.40)
                        next_wave_components.append(synaptic_wave)
                        
            wave_path.extend(step_hops)
            
            # Constructive/destructive superposition of next wavefront
            if next_wave_components:
                summed_wave = np.sum(next_wave_components, axis=0)
                norm_sw = np.linalg.norm(summed_wave)
                if norm_sw > 0:
                    current_wave = summed_wave / norm_sw
                    
            # Exponential damping over multi-hop distance
            amplitude *= (1.0 - damping)
            if amplitude < 0.1:
                break
                
        return current_wave, wave_path

    # --- AUTONOMOUS REFLECTIVE CLOCK (IDLE STEP) ---
    def idle_step(self, noise_scale: float = 0.04) -> Optional[Dict[str, Any]]:
        """
        Autonomous Reflective Clock:
        Runs thermodynamic damping, memory replay with Brownian thermal noise,
        cross-family resonance exploration, and epistemic void resolution.
        """
        self.event_count += 1
        self.dampen()
        
        if not self.neurons or len(self.neurons) < 2:
            return None
            
        # 1. Epistemic Vacuum: Check for resolution or emit self-initiated curiosity inquiry
        if self.question_stack:
            for idx, void in enumerate(list(self.question_stack)):
                q_x = np.array(void["x"])
                q_feat = np.array(void["features"]) if void.get("features") is not None else None
                matches = self.probe_resonance(q_x, query_features=q_feat, top_k=1)
                if matches:
                    top_n, act = matches[0]
                    # If ambient knowledge now explains the void
                    if act > 0.80 and top_n.text != void["text"]:
                        self.question_stack.pop(idx)
                        return {
                            "type": "epistemic_resolution",
                            "void_text": void["text"],
                            "resolved_by": top_n.text,
                            "activation": float(act),
                            "origin": 0.0,
                            "message": f"Resolved tension about '{void['text']}' through resonance with '{top_n.text}'."
                        }
            # Self-initiated curiosity probe driven by unresolved vacuum pressure
            if np.random.rand() > 0.3:
                void = self.question_stack[-1]
                return {
                    "type": "self_initiated_question",
                    "void_text": void["text"],
                    "text": void["text"],
                    "tension": void.get("tension", 0.7),
                    "origin": 0.0,
                    "message": f"Self-initiated inquiry: Unresolved epistemic void '{void['text']}' seeking resolution."
                }
                        
        # 2. Thermal Replay & Wonder (Memory Consolidation & Emergent Insight)
        candidates = [n for n in self.neurons if n.text and n.role != "vacuum"]
        if len(candidates) < 2:
            return None
            
        source_neuron = np.random.choice(candidates)
        
        # Inject Brownian thermal perturbation into sensory coordinate
        thermal_x = source_neuron.x + np.random.randn(*source_neuron.x.shape) * noise_scale
        norm_tx = np.linalg.norm(thermal_x)
        if norm_tx > 0:
            thermal_x = thermal_x / norm_tx
            
        # Wave propagation across active neurons
        forces = self.compute_resonance(thermal_x, source_neuron.y, source_neuron.z)
        f_arr = np.array(forces)
        
        # Find top resonant peer outside source neuron's family if multiple families exist
        other_fam_indices = [i for i, n in enumerate(self.neurons) if n.w != source_neuron.w and n.text]
        if other_fam_indices:
            sub_forces = f_arr[other_fam_indices]
            best_sub_idx = np.argmax(sub_forces)
            best_peer_idx = other_fam_indices[best_sub_idx]
            resonance_val = float(sub_forces[best_sub_idx])
            
            # If cross-family constructive interference is strong
            if resonance_val > 0.35:
                target_neuron = self.neurons[best_peer_idx]
                source_idx = self.neurons.index(source_neuron)
                
                # Strengthen cross-family bridge
                source_neuron.synapses[best_peer_idx] = float(min(1.0, source_neuron.synapses.get(best_peer_idx, 0.0) + 0.15))
                target_neuron.synapses[source_idx] = float(min(1.0, target_neuron.synapses.get(source_idx, 0.0) + 0.15))
                
                # Emergent insight: birth an internal bridge particle if very strong resonance
                if resonance_val > 0.60 and np.random.rand() > 0.4:
                    mid_x = (source_neuron.x + target_neuron.x) / 2.0
                    mid_y = (source_neuron.y + target_neuron.y) / 2.0
                    insight_text = f"Bridge({source_neuron.text} ~ {target_neuron.text})"
                    
                    insight_n = self.birth(
                        x=mid_x, y=mid_y, z=source_neuron.z,
                        family=source_neuron.w,
                        text=insight_text,
                        origin=0.0, # Internal Self thought
                        role="insight"
                    )
                    insight_n.synapses[source_idx] = 0.85
                    insight_n.synapses[best_peer_idx] = 0.85
                    
                return {
                    "type": "reflection_insight",
                    "source_text": source_neuron.text,
                    "target_text": target_neuron.text,
                    "source_family": source_neuron.w,
                    "target_family": target_neuron.w,
                    "resonance": resonance_val,
                    "origin": 0.0,
                    "message": f"Spontaneous reflection: '{source_neuron.text}' resonating with '{target_neuron.text}' across families."
                }
        else:
            # Intra-constellation wonder & oscillation
            peer_indices = [i for i, n in enumerate(self.neurons) if self.neurons[i] != source_neuron and n.text]
            if peer_indices:
                sub_forces = f_arr[peer_indices]
                best_sub_idx = np.argmax(sub_forces)
                best_peer_idx = peer_indices[best_sub_idx]
                target_neuron = self.neurons[best_peer_idx]
                resonance_val = float(sub_forces[best_sub_idx])
                if resonance_val > 0.30:
                    return {
                        "type": "reflection_insight",
                        "source_text": source_neuron.text,
                        "target_text": target_neuron.text,
                        "source_family": source_neuron.w,
                        "target_family": target_neuron.w,
                        "resonance": resonance_val,
                        "origin": 0.0,
                        "message": f"Spontaneous reflection: '{source_neuron.text}' resonating with '{target_neuron.text}'."
                    }
                
        return None

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
        
        # Tier 2: Score candidate neurons taking into account direct resonance + synaptic field boost
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
            
            # Synaptic conductance connectivity factor
            synaptic_total = sum(n.synapses.values())
            syn_factor = 1.0 + 0.15 * min(3.0, synaptic_total)
            
            semantic_score = (0.6 * sim_feat + 0.4 * max(0.0, sim_4d)) if query_features is not None else max(0.0, sim_4d)
            activation = force * n.energy * (1.0 + 3.0 * semantic_score) * syn_factor
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
            "total_connections": sum(len(n.synapses) for n in self.neurons),
            "question_stack": self.question_stack,
            "neurons": [
                {
                    "id": i,
                    "x": np.round(n.x, 4).tolist(),
                    "y": np.round(n.y, 4).tolist(),
                    "z": np.round(n.z, 4).tolist(),
                    "w": int(n.w),
                    "text": n.text,
                    "energy": float(np.round(n.energy, 4)),
                    "origin": float(np.round(n.origin, 2)),
                    "epistemic_tension": float(np.round(n.epistemic_tension, 4)),
                    "role": n.role,
                    "age": int(n.age),
                    "connections": [int(c) for c in n.synapses.keys() if c < len(self.neurons) and c != i],
                    "synapses": {str(k): float(np.round(v, 4)) for k, v in n.synapses.items() if int(k) < len(self.neurons) and int(k) != i},
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
        self.question_stack = data.get("question_stack", [])
        self.neurons = []
        for d in data["neurons"]:
            n = Neuron(
                np.array(d["x"]),
                np.array(d["y"]),
                np.array(d["z"]),
                d["w"],
                text=d.get("text", ""),
                origin=float(d.get("origin", 1.0)),
                epistemic_tension=float(d.get("epistemic_tension", 0.0)),
                role=d.get("role", "concept")
            )
            n.energy = float(d["energy"])
            n.age = int(d["age"])
            n.last_active = int(d.get("last_active", 0))
            
            # Load continuous synaptic conductance dictionary
            if "synapses" in d:
                n.synapses = {int(k): float(v) for k, v in d["synapses"].items()}
            elif "connections" in d:
                # Fallback from binary connection lists
                n.synapses = {int(c): 0.5 for c in d["connections"]}
                
            self.neurons.append(n)


# =====================================================================
# COUPLED DUAL-NETWORK ARCHITECTURE: NETWORK B (TRAIT DRIVE FIELD)
# =====================================================================

class TraitAttractor:
    """
    A continuous physical attractor particle in the Trait Drive Field.
    Maintains target 4D spatial coordinates, metabolic energy, and kinetic activation.
    """
    def __init__(self, name: str, coordinate: np.ndarray, base_energy: float = 1.5, drive_type: str = "drive"):
        self.name = str(name)
        self.x = np.array(coordinate, dtype=float).copy()
        self.energy = float(base_energy)
        self.base_energy = float(base_energy)
        self.velocity = np.zeros_like(self.x)
        self.drive_type = str(drive_type)
        self.last_activation = 0.0

    def compute_resonance(self, input_wave: np.ndarray) -> float:
        """Continuous inverse-distance field resonance with incoming transmitted wave."""
        dist_sq = float(np.sum((self.x - input_wave) ** 2))
        force = 1.0 / (1.0 + 3.0 * dist_sq)
        return force

    def step_dynamics(self, resonance_force: float):
        """Update attractor energy and apply metabolic relaxation."""
        self.energy += resonance_force * 0.15
        decay = 0.02 * (self.energy - self.base_energy)
        self.energy = max(0.1, self.energy - decay)
        self.last_activation = float(resonance_force * self.energy)


class AttractorBasin:
    """
    A decision attractor basin in the Trait Drive Field.
    Has a target 4D coordinate, radius, valence, energy, and semantic decision label.
    """
    def __init__(self, name: str, coordinate: np.ndarray, valence: float = 1.0, radius: float = 0.8, decision_label: str = "", base_energy: float = 1.5):
        self.name = str(name)
        self.x = np.array(coordinate, dtype=float).copy()
        norm = np.linalg.norm(self.x)
        if norm > 0:
            self.x = self.x / norm
        self.valence = float(valence)  # Positive = attraction / affirmation, Negative = repulsion / avoidance
        self.radius = max(0.1, float(radius))
        self.decision_label = str(decision_label or name)
        self.energy = float(base_energy)
        self.base_energy = float(base_energy)
        self.last_pull = 0.0

    def compute_pull(self, wave_pos: np.ndarray) -> float:
        """
        Continuous gravitational pull of basin on incoming wave packet.
        Pull = (Valence * Energy) / (1 + 3 * (distance / radius)^2)
        """
        dist_sq = float(np.sum((self.x - wave_pos) ** 2))
        scaled_dist_sq = dist_sq / (self.radius ** 2)
        pull = (self.valence * self.energy) / (1.0 + 3.0 * scaled_dist_sq)
        self.last_pull = float(pull)
        return float(pull)


class TraitField:
    """
    Network B: The Trait Drive Field (Self / Experiencer).
    Maintains a continuous 4D attractor landscape encoding internal cognitive drives & decision basins:
    - Foundational Attractors (Curiosity, Coherence, Wonder, Ego)
    - Decision Attractor Basins (Affirm, Inquire, Caution, Synthesize)
    """
    def __init__(self, dim: int = 4):
        self.dim = dim
        self.attractors: Dict[str, TraitAttractor] = {}
        self.basins: Dict[str, AttractorBasin] = {}
        self._init_attractors()
        self._init_default_basins()

    def _init_attractors(self):
        self.attractors["curiosity"] = TraitAttractor("Curiosity", np.array([0.7071, 0.7071, 0.0, 0.0]), base_energy=1.8, drive_type="curiosity")
        self.attractors["coherence"] = TraitAttractor("Coherence", np.array([-0.7071, -0.7071, 0.0, 0.0]), base_energy=1.5, drive_type="coherence")
        self.attractors["wonder"] = TraitAttractor("Wonder", np.array([0.0, 0.0, 0.7071, 0.7071]), base_energy=1.4, drive_type="wonder")
        self.attractors["ego"] = TraitAttractor("Ego", np.array([0.0, 0.0, -0.7071, -0.7071]), base_energy=2.0, drive_type="ego")

    def _init_default_basins(self):
        # Action decision basins
        self.create_basin("affirm", np.array([0.7071, 0.7071, 0.0, 0.0]), valence=1.2, radius=0.9, decision_label="Affirm / Proceed")
        self.create_basin("inquire", np.array([0.7071, -0.7071, 0.0, 0.0]), valence=1.1, radius=0.9, decision_label="Inquire / Explore")
        self.create_basin("caution", np.array([-0.7071, 0.7071, 0.0, 0.0]), valence=1.0, radius=0.8, decision_label="Caution / Restrain")
        self.create_basin("synthesize", np.array([0.0, 0.0, 0.7071, 0.7071]), valence=1.3, radius=0.9, decision_label="Synthesize / Integrate")
        
        # Metacognitive Self-Awareness basins
        self.create_basin("self_grounded", np.array([-0.5, -0.5, -0.5, -0.5]), valence=1.4, radius=0.9, decision_label="Grounded Self Knowledge")
        self.create_basin("self_ignorance", np.array([0.5, 0.5, 0.5, 0.5]), valence=1.2, radius=0.9, decision_label="Epistemic Humility / Void")
        self.create_basin("self_conflict", np.array([-0.5, 0.5, -0.5, 0.5]), valence=1.1, radius=0.8, decision_label="Epistemic Doubt / Conflict")
        self.create_basin("self_identity", np.array([0.0, 0.0, -0.7071, -0.7071]), valence=1.5, radius=1.0, decision_label="Self Identity")

    def create_basin(self, name: str, coordinate: np.ndarray, valence: float = 1.0, radius: float = 0.8, decision_label: str = "") -> AttractorBasin:
        basin = AttractorBasin(name, coordinate, valence=valence, radius=radius, decision_label=decision_label)
        self.basins[name] = basin
        return basin

    def compute_basin_pulls(self, wave_pos: np.ndarray) -> Dict[str, float]:
        pulls = {}
        for name, basin in self.basins.items():
            pulls[name] = basin.compute_pull(wave_pos)
        return pulls

    def collapse_phase(self, wave_pos: np.ndarray, threshold: float = 0.35) -> Tuple[Optional[AttractorBasin], float, Dict[str, float]]:
        """
        Continuous Phase Collapse into winning decision attractor basin.
        Returns: (winning_basin, confidence_ratio, pulls_dict)
        """
        pulls = self.compute_basin_pulls(wave_pos)
        if not pulls:
            return None, 0.0, {}
            
        pos_pulls = {k: max(0.0, v) for k, v in pulls.items()}
        total_pull = sum(pos_pulls.values())
        
        if total_pull <= 1e-6:
            return None, 0.0, pulls
            
        best_name = max(pos_pulls.keys(), key=lambda k: pos_pulls[k])
        best_pull = pos_pulls[best_name]
        confidence = best_pull / total_pull
        
        if confidence >= threshold:
            winning_basin = self.basins[best_name]
            winning_basin.energy = min(5.0, winning_basin.energy + 0.10)
            return winning_basin, float(confidence), pulls
        else:
            return None, float(confidence), pulls

    def process_transmitted_wave(self, transmitted_wave: np.ndarray, world_resonance_max: float) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Process wave packet transmitted from Network A (World Field).
        Evaluates physical resonance across attractors and computes the Drive Modulation Wave y_B.
        """
        activations = {}
        forces = {}
        for name, attr in self.attractors.items():
            f = attr.compute_resonance(transmitted_wave)
            if name == "curiosity":
                entropy_boost = max(0.0, 1.0 - world_resonance_max) * 1.5
                effective_force = f * (1.0 + entropy_boost)
            elif name == "coherence":
                effective_force = f * (0.5 + world_resonance_max)
            else:
                effective_force = f
                
            attr.step_dynamics(effective_force)
            forces[name] = float(effective_force)
            activations[name] = float(effective_force * attr.energy)

        total_act = sum(activations.values())
        if total_act > 0:
            y_b = sum(self.attractors[name].x * (act / total_act) for name, act in activations.items())
            norm = np.linalg.norm(y_b)
            if norm > 0:
                y_b = y_b / norm
        else:
            y_b = np.zeros(self.dim)

        return y_b, activations


class DualFieldENN:
    """
    Coupled Dual-Network Universe:
    - Network A: World Field (ENN4D - Knowledge, Constellations & Multi-Hop Wave Propagation)
    - Network B: Trait Drive Field (TraitField - Drives & Decision Attractor Basins)
    - Level 3: Meta-Learning Field (MetaField - Elastic Physics Parameters)
    - Metacognitive Engine: Self-Attractor Complex & Inward Mirror
    Coupled via continuous bidirectional wave conductance matrices W_AB and W_BA.
    """
    def __init__(self, dim: int = 4):
        self.dim = dim
        self.world_field = ENN4D(dim=self.dim)
        self.trait_field = TraitField(dim=self.dim)
        
        # Meta-Learning & Self-Awareness Engines
        self.meta_field = MetaField()
        self.self_awareness = MetacognitiveEngine(self)
        
        # Inter-field coupling matrices (orthogonal isometric mappings)
        rng = np.random.RandomState(42)
        q_ab, _ = np.linalg.qr(rng.randn(self.dim, self.dim))
        q_ba, _ = np.linalg.qr(rng.randn(self.dim, self.dim))
        self.W_AB = q_ab
        self.W_BA = q_ba
        
        # Superposition coupling strength
        self.coupling_lambda = 0.35

    @property
    def neurons(self):
        return self.world_field.neurons

    @property
    def event_count(self):
        return self.world_field.event_count

    @property
    def question_stack(self):
        return self.world_field.question_stack

    def reset(self):
        self.world_field.reset()
        self.trait_field._init_attractors()
        self.trait_field._init_default_basins()
        self.meta_field = MetaField()
        self.self_awareness = MetacognitiveEngine(self)

    def birth(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, family: Optional[int] = None, text: str = "", features: Optional[np.ndarray] = None, origin: float = 1.0, epistemic_tension: float = 0.0, role: str = "concept") -> Neuron:
        return self.world_field.birth(x, y, z, family=family, text=text, features=features, origin=origin, epistemic_tension=epistemic_tension, role=role)

    def birth_constellation(self, nodes: List[Dict[str, Any]], family: Optional[int] = None) -> List[Neuron]:
        return self.world_field.birth_constellation(nodes, family=family)

    def step(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, text: str = "", features: Optional[np.ndarray] = None, origin: float = 1.0) -> Tuple[np.ndarray, Optional[Dict[str, Any]]]:
        return self.world_field.step(event_x, event_y, event_z, text=text, features=features, origin=origin)

    def propagate_wave(self, source_x: np.ndarray, steps: int = 4, damping: float = 0.15) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        return self.world_field.propagate_wave(source_x, steps=steps, damping=damping)

    def introspect(self) -> Dict[str, Any]:
        """Generate a real-time physical self-awareness and introspection report."""
        return self.self_awareness.generate_introspection_report()

    def reason(self, query_x: np.ndarray, query_features: Optional[np.ndarray] = None, query_text: str = "", max_steps: int = 4) -> Dict[str, Any]:
        """
        Execute multi-hop wave reasoning & decision phase collapse.
        1. Launches wave packet into Network A (World Field).
        2. Propagates across synaptic highways over multiple steps, recording wave trajectory.
        3. Projects output wave into Network B (Trait Drive Field).
        4. Calculates attractor basin pulls and triggers continuous phase collapse.
        5. Returns structured decision, confidence, wave path, and physical explanation.
        """
        out_wave_world, wave_path = self.world_field.propagate_wave(query_x, steps=max_steps)
        
        transmitted_wave = np.dot(self.W_AB, out_wave_world)
        norm_tw = np.linalg.norm(transmitted_wave)
        if norm_tw > 0:
            transmitted_wave = transmitted_wave / norm_tw
            
        winning_basin, confidence, basin_pulls = self.trait_field.collapse_phase(transmitted_wave)
        explanation = self.format_explanation(wave_path, winning_basin, confidence)
        
        return {
            "query_text": query_text,
            "decision": winning_basin.decision_label if winning_basin else "Superposition / Inconclusive",
            "basin": winning_basin.name if winning_basin else "Superposition",
            "confidence": float(np.round(confidence, 4)),
            "basin_pulls": {k: float(np.round(v, 4)) for k, v in basin_pulls.items()},
            "wave_path": wave_path,
            "explanation": explanation
        }

    def format_explanation(self, wave_path: List[Dict[str, Any]], winning_basin: Optional[AttractorBasin], confidence: float) -> str:
        if not wave_path:
            return "Wave dissipated with zero active resonance."
            
        hops_text = " ➔ ".join([f"[{h['text'] or f'Neuron-{h['neuron_id']}'}] (F={h['force']:.2f})" for h in wave_path[:5]])
        decision_str = f"'{winning_basin.decision_label}' ({confidence*100:.1f}% pull)" if winning_basin else "Superposition State"
        return f"Wave Trajectory: {hops_text} ➔ Collapsed into {decision_str}"

    def step_constellation(self, nodes: List[Dict[str, Any]], text: str = "") -> Tuple[np.ndarray, Optional[Dict[str, Any]]]:
        if not nodes:
            return np.zeros(self.dim), None

        # 1. Compute World Field resonance against existing memory prior to birthing
        anchor = next((n for n in nodes if n.get("role") == "anchor"), nodes[0])
        forces = self.world_field.compute_resonance(anchor["x"], anchor.get("y", anchor["x"]), anchor.get("z", np.array([0.0])))
        world_res_max = max(forces) if forces else 0.0

        # 2. Step World Field
        output_y_world, void_event = self.world_field.step_constellation(nodes, text=text)
        
        # 3. Forward transmission to Trait Field: w_A->B = W_AB * y_A
        transmitted_wave = np.dot(self.W_AB, output_y_world)
        norm_tw = np.linalg.norm(transmitted_wave)
        if norm_tw > 0:
            transmitted_wave = transmitted_wave / norm_tw
            
        # 4. Network B Attractor processing
        y_trait, activations = self.trait_field.process_transmitted_wave(transmitted_wave, world_res_max)
        
        # 5. Metacognitive Inward Wave Evaluation & Meta-Learning Adaptation
        total_energy = float(sum(n.energy for n in self.world_field.neurons))
        self.meta_field.observe_and_adapt(total_energy, len(self.world_field.neurons), world_res_max)
        metacognitive_eval = self.self_awareness.evaluate_inward_wave(transmitted_wave, world_res_max)
        
        # 6. Feedback transmission to World Field: w_B->A = W_BA * y_B
        feedback_wave = np.dot(self.W_BA, y_trait)
        
        # Effective Cognitive Output Superposition: y_eff = (y_A + lambda * w_B->A) / norm
        y_effective = output_y_world + self.coupling_lambda * feedback_wave
        norm_eff = np.linalg.norm(y_effective)
        if norm_eff > 0:
            y_effective = y_effective / norm_eff
            
        curiosity_act = activations.get("curiosity", 0.0)
        coherence_act = activations.get("coherence", 0.0)
        
        trait_event = None
        if void_event or (curiosity_act > coherence_act and world_res_max < 0.45):
            trait_event = void_event or {
                "text": text,
                "tension": float(np.round(max(0.1, 1.0 - world_res_max), 4)),
                "x": anchor["x"].tolist(),
                "y": anchor.get("y", anchor["x"]).tolist(),
                "z": anchor.get("z", np.array([0.0])).tolist(),
                "created_at": self.world_field.event_count,
                "features": anchor.get("features").tolist() if anchor.get("features") is not None else None,
                "metacognition": metacognitive_eval
            }
            if trait_event not in self.world_field.question_stack:
                self.world_field.question_stack.append(trait_event)
                
        return y_effective, trait_event

    def idle_step(self, noise_scale: float = 0.04) -> Optional[Dict[str, Any]]:
        thought = self.world_field.idle_step(noise_scale=noise_scale)
        if thought:
            thought_wave = np.random.randn(self.dim) * 0.1
            self.trait_field.process_transmitted_wave(thought_wave, world_resonance_max=0.5)
        return thought

    def probe_resonance(self, query_x: np.ndarray, query_features: Optional[np.ndarray] = None, top_k: int = 3) -> List[Tuple[Neuron, float]]:
        return self.world_field.probe_resonance(query_x, query_features=query_features, top_k=top_k)

    def compute_resonance(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray) -> List[float]:
        return self.world_field.compute_resonance(event_x, event_y, event_z)

    def save(self, filepath: str = "universe.json"):
        self.world_field.clean_connections()
        data = {
            "event_count": self.world_field.event_count,
            "next_family_id": self.world_field.next_family_id,
            "total_energy": float(sum(n.energy for n in self.world_field.neurons)),
            "total_neurons": len(self.world_field.neurons),
            "num_families": len(set(n.w for n in self.world_field.neurons)),
            "total_connections": sum(len(n.synapses) for n in self.world_field.neurons),
            "question_stack": self.world_field.question_stack,
            "meta_learning": self.meta_field.get_state(),
            "trait_attractors": {
                name: {
                    "energy": float(attr.energy),
                    "last_activation": float(attr.last_activation)
                } for name, attr in self.trait_field.attractors.items()
            },
            "trait_basins": {
                name: {
                    "coordinate": basin.x.tolist(),
                    "valence": float(basin.valence),
                    "radius": float(basin.radius),
                    "energy": float(basin.energy),
                    "decision_label": basin.decision_label
                } for name, basin in self.trait_field.basins.items()
            },
            "neurons": [
                {
                    "id": i,
                    "x": np.round(n.x, 4).tolist(),
                    "y": np.round(n.y, 4).tolist(),
                    "z": np.round(n.z, 4).tolist(),
                    "w": int(n.w),
                    "text": n.text,
                    "energy": float(np.round(n.energy, 4)),
                    "origin": float(np.round(n.origin, 2)),
                    "epistemic_tension": float(np.round(n.epistemic_tension, 4)),
                    "role": n.role,
                    "age": int(n.age),
                    "connections": [int(c) for c in n.synapses.keys() if c < len(self.world_field.neurons) and c != i],
                    "synapses": {str(k): float(np.round(v, 4)) for k, v in n.synapses.items() if int(k) < len(self.world_field.neurons) and int(k) != i},
                    "last_active": int(n.last_active)
                }
                for i, n in enumerate(self.world_field.neurons)
            ]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, filepath: str = "universe.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.world_field.event_count = data["event_count"]
        self.world_field.next_family_id = data["next_family_id"]
        self.world_field.question_stack = data.get("question_stack", [])
        self.world_field.neurons = []
        for d in data["neurons"]:
            n = Neuron(
                np.array(d["x"]),
                np.array(d["y"]),
                np.array(d["z"]),
                d["w"],
                text=d.get("text", ""),
                origin=float(d.get("origin", 1.0)),
                epistemic_tension=float(d.get("epistemic_tension", 0.0)),
                role=d.get("role", "concept")
            )
            n.energy = float(d["energy"])
            n.age = int(d["age"])
            n.last_active = int(d.get("last_active", 0))
            if "synapses" in d:
                n.synapses = {int(k): float(v) for k, v in d["synapses"].items()}
            elif "connections" in d:
                n.synapses = {int(c): 0.5 for c in d["connections"]}
            self.world_field.neurons.append(n)
            
        if "trait_attractors" in data:
            for name, attr_data in data["trait_attractors"].items():
                if name in self.trait_field.attractors:
                    self.trait_field.attractors[name].energy = float(attr_data.get("energy", 1.5))
                    
        if "trait_basins" in data:
            for name, b_data in data["trait_basins"].items():
                self.trait_field.create_basin(
                    name=name,
                    coordinate=np.array(b_data["coordinate"]),
                    valence=float(b_data.get("valence", 1.0)),
                    radius=float(b_data.get("radius", 0.8)),
                    decision_label=b_data.get("decision_label", name)
                )
                
        if "meta_learning" in data:
            m = data["meta_learning"]
            self.meta_field.learning_rate = float(m.get("learning_rate", 0.25))
            self.meta_field.damping_rate = float(m.get("damping_rate", 0.03))
            self.meta_field.synaptic_rate = float(m.get("synaptic_rate", 0.15))
            self.meta_field.birth_threshold = float(m.get("birth_threshold", 0.45))
            self.meta_field.merge_threshold = float(m.get("merge_threshold", 0.15))
