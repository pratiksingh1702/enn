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
