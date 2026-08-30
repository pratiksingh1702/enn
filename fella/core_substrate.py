"""
FELLA Core Substrate: Multi-Network Tiered (X, Y, Z) Cognitive Substrate
========================================================================
Implements the continuous Embodied Neural Network (ENN) physics across
discrete abstraction tiers (Z=0, 1, 2, 3, 4) with 4D Continuous Syntactic Valences:
- Z = 0: Graphemic & Phonetic Foundation (26 letters, 650 fortified bridges)
- Z = 1: Concrete Entities & Nouns (Actors / Subjects / Objects)
- Z = 2: Dynamic Actions & Transformations (Verbs / Predicates)
- Z = 3: Properties, States & Qualities (Adjectives / Descriptors)
- Z = 4: Metacognitive & Social Synthesis (Self-Model / Relations)
"""

import numpy as np
import time
import json
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import defaultdict, deque


class FellaNeuron:
    """A living continuous neuron with semantic coordinates and 4D syntactic valence."""
    def __init__(
        self,
        neuron_id: int,
        x: np.ndarray,
        y: np.ndarray,
        z: float = 0.0,
        tier_z: int = 0,
        network_id: str = "general",
        w: int = 0,
        text: str = "",
        role: str = "concept",
        grammatical_role: str = "noun",
        syntax_valence: Optional[np.ndarray] = None,
        origin: float = 1.0,
        epistemic_tension: float = 0.0,
        energy: float = 1.0,
        features: Optional[np.ndarray] = None
    ):
        self.id = int(neuron_id)
        self.x = np.array(x, dtype=float).copy()           # Input coordinates (X in R^D)
        self.y = np.array(y, dtype=float).copy()           # Output coordinates (Y in R^D)
        self.z = float(z)                                  # Continuous / Tier Z coordinate
        self.tier_z = int(tier_z if tier_z is not None else int(round(z)))
        self.network_id = str(network_id)                  # Specific modular concept network
        self.w = int(w)                                    # Family / Cluster identifier
        self.text = str(text)                              # Concept label
        self.role = str(role)                              # "letter", "entity", "action", "property", "anchor"
        self.grammatical_role = str(grammatical_role)      # "noun", "verb", "adj", "pointer"
        
        # 4D Syntactic Valence Vector: [v_noun, v_verb, v_adj, v_pointer]
        if syntax_valence is not None:
            self.syntax_valence = np.array(syntax_valence, dtype=float).copy()
        else:
            self.syntax_valence = np.zeros(4, dtype=float)
            if self.grammatical_role == "noun":
                self.syntax_valence[0] = 1.0
            elif self.grammatical_role == "verb":
                self.syntax_valence[1] = 1.0
            elif self.grammatical_role == "adj":
                self.syntax_valence[2] = 1.0
            elif self.grammatical_role == "pointer":
                self.syntax_valence[3] = -1.0
                
        self.origin = float(origin)
        self.epistemic_tension = float(epistemic_tension)
        self.energy = float(energy)
        self.features = np.array(features, dtype=float).copy() if features is not None else None
        
        # Momentum & Lifecycle
        self.velocity_x = np.zeros_like(self.x)
        self.velocity_y = np.zeros_like(self.y)
        self.age = 0
        self.last_active = 0
        
        # Synaptic Bridge Field: target_id -> conductance weight W_ij in (0.0, 1.0]
        self.synapses: Dict[int, float] = {}
        # Relational Bridge Tags
        self.synapse_relations: Dict[int, str] = {}

    def clone(self, new_id: int) -> 'FellaNeuron':
        daughter = FellaNeuron(
            neuron_id=new_id,
            x=self.x + np.random.randn(*self.x.shape) * 0.03,
            y=self.y + np.random.randn(*self.y.shape) * 0.03,
            z=self.z,
            tier_z=self.tier_z,
            network_id=self.network_id,
            w=self.w,
            text=self.text,
            role=self.role,
            grammatical_role=self.grammatical_role,
            syntax_valence=self.syntax_valence,
            origin=self.origin,
            epistemic_tension=self.epistemic_tension * 0.5,
            energy=self.energy * 0.5,
            features=self.features
        )
        daughter.synapses = {k: v * 0.75 for k, v in self.synapses.items()}
        daughter.synapse_relations = dict(self.synapse_relations)
        daughter.last_active = self.last_active
        return daughter

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": self.x.tolist(),
            "y": self.y.tolist(),
            "z": float(self.z),
            "tier_z": int(self.tier_z),
            "network_id": str(self.network_id),
            "w": int(self.w),
            "text": str(self.text),
            "role": str(self.role),
            "grammatical_role": str(self.grammatical_role),
            "syntax_valence": self.syntax_valence.tolist(),
            "origin": float(self.origin),
            "epistemic_tension": float(self.epistemic_tension),
            "energy": float(self.energy),
            "age": int(self.age),
            "last_active": int(self.last_active),
            "features": self.features.tolist() if self.features is not None else None,
            "synapses": {str(k): float(v) for k, v in self.synapses.items()},
            "synapse_relations": {str(k): str(v) for k, v in self.synapse_relations.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FellaNeuron':
        n = cls(
            neuron_id=int(data["id"]),
            x=np.array(data["x"], dtype=float),
            y=np.array(data["y"], dtype=float),
            z=float(data.get("z", 0.0)),
            tier_z=int(data.get("tier_z", int(round(data.get("z", 0.0))))),
            network_id=str(data.get("network_id", "general")),
            w=int(data.get("w", 0)),
            text=str(data.get("text", "")),
            role=str(data.get("role", "concept")),
            grammatical_role=str(data.get("grammatical_role", "noun")),
            syntax_valence=np.array(data.get("syntax_valence", [1, 0, 0, 0]), dtype=float),
            origin=float(data.get("origin", 1.0)),
            epistemic_tension=float(data.get("epistemic_tension", 0.0)),
            energy=float(data.get("energy", 1.0)),
            features=np.array(data["features"], dtype=float) if data.get("features") is not None else None
        )
        n.age = int(data.get("age", 0))
        n.last_active = int(data.get("last_active", 0))
        n.synapses = {int(k): float(v) for k, v in data.get("synapses", {}).items()}
        n.synapse_relations = {int(k): str(v) for k, v in data.get("synapse_relations", {}).items()}
        return n


class StackedSubstrate:
    """
    Tiered (X, Y, Z) Cognitive Substrate with Continuous Grammar Physics.
    """
    def __init__(self, dim: int = 16, decay_rate: float = 0.008, pruning_threshold: float = 0.05):
        self.dim = int(dim)
        self.decay_rate = float(decay_rate)
        self.pruning_threshold = float(pruning_threshold)
        
        self.neurons: Dict[int, FellaNeuron] = {}
        self.next_neuron_id: int = 1
        self.current_step: int = 0
        self.current_event_z: float = 0.0
        
        self.ego_id = -1
        ego_node = FellaNeuron(
            neuron_id=self.ego_id,
            x=np.zeros(self.dim),
            y=np.zeros(self.dim),
            z=-1.0,
            tier_z=-1,
            text="<EGO>",
            role="ego_core"
        )
        ego_node.mass = 50.0
        self.neurons[self.ego_id] = ego_node
        
        # Fast Spatial Indexing Cache
        self._dirty_tensors: bool = True
        self._cached_ids: np.ndarray = np.array([], dtype=int)
        self._cached_X: np.ndarray = np.zeros((0, self.dim), dtype=float)
        self._cached_Y: np.ndarray = np.zeros((0, self.dim), dtype=float)
        self._cached_Z: np.ndarray = np.zeros((0,), dtype=float)
        self._cached_tiers: np.ndarray = np.zeros((0,), dtype=int)

    def _sync_tensors(self):
        if not self._dirty_tensors:
            return
        if not self.neurons:
            self._cached_ids = np.array([], dtype=int)
            self._cached_X = np.zeros((0, self.dim), dtype=float)
            self._cached_Y = np.zeros((0, self.dim), dtype=float)
            self._cached_Z = np.zeros((0,), dtype=float)
            self._cached_tiers = np.zeros((0,), dtype=int)
            self._dirty_tensors = False
            return
        
        ids, x_list, y_list, z_list, tier_list = [], [], [], [], []
        for n_id, n in self.neurons.items():
            ids.append(n_id)
            x_list.append(n.x)
            y_list.append(n.y)
            z_list.append(n.z)
            tier_list.append(n.tier_z)
            
        self._cached_ids = np.array(ids, dtype=int)
        self._cached_X = np.array(x_list, dtype=float)
        self._cached_Y = np.array(y_list, dtype=float)
        self._cached_Z = np.array(z_list, dtype=float)
        self._cached_tiers = np.array(tier_list, dtype=int)
        self._dirty_tensors = False

    def birth_neuron(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: Optional[float] = None,
        tier_z: Optional[int] = None,
        network_id: str = "general",
        w: int = 0,
        text: str = "",
        role: str = "concept",
        grammatical_role: str = "noun",
        syntax_valence: Optional[np.ndarray] = None,
        origin: float = 1.0,
        epistemic_tension: float = 0.0,
        energy: float = 1.0
    ) -> FellaNeuron:
        """Spawns a new living neuron with continuous coordinates and syntax valence."""
        n_id = self.next_neuron_id
        self.next_neuron_id += 1
        
        target_z = float(self.current_event_z if z is None else z)
        target_tier = int(tier_z if tier_z is not None else int(round(target_z)))
        
        x_vec = np.array(x, dtype=float)
        y_vec = np.array(y, dtype=float)
        if x_vec.shape[0] != self.dim:
            x_vec = np.pad(x_vec, (0, max(0, self.dim - x_vec.shape[0])))[:self.dim]
        if y_vec.shape[0] != self.dim:
            y_vec = np.pad(y_vec, (0, max(0, self.dim - y_vec.shape[0])))[:self.dim]
            
        neuron = FellaNeuron(
            neuron_id=n_id,
            x=x_vec,
            y=y_vec,
            z=target_z,
            tier_z=target_tier,
            network_id=network_id,
            w=w,
            text=text,
            role=role,
            grammatical_role=grammatical_role,
            syntax_valence=syntax_valence,
            origin=origin,
            epistemic_tension=epistemic_tension,
            energy=energy
        )
        neuron.last_active = self.current_step
        self.neurons[n_id] = neuron
        self._dirty_tensors = True
        return neuron

    def find_or_birth_concept(
        self,
        text: str,
        x_vec: np.ndarray,
        y_vec: Optional[np.ndarray] = None,
        tier_z: int = 1,
        network_id: str = "general",
        role: str = "concept",
        grammatical_role: str = "noun",
        syntax_valence: Optional[np.ndarray] = None,
        energy: float = 2.0
    ) -> Tuple[FellaNeuron, bool]:
        """Strict concept deduplication in continuous (X, Y, Z) space."""
        text_clean = text.strip().lower()
        if y_vec is None:
            y_vec = np.roll(x_vec, 1) * 0.85 + np.roll(x_vec, -1) * 0.15
            norm_y = np.linalg.norm(y_vec)
            if norm_y > 0:
                y_vec = y_vec / norm_y
                
        # 1. Exact text match on this tier
        for n in self.neurons.values():
            if n.tier_z == tier_z and n.text.lower() == text_clean:
                n.energy = min(5.0, n.energy + 0.35)
                n.last_active = self.current_step
                return n, False
                
        # 2. Continuous field resonance check
        forces = self.compute_field_resonance(x_vec, y_target=y_vec, tier_filter=tier_z)
        if forces:
            best_id = max(forces.items(), key=lambda it: it[1])[0]
            if forces[best_id] > 0.85:
                existing = self.neurons[best_id]
                existing.energy = min(5.0, existing.energy + 0.35)
                existing.last_active = self.current_step
                return existing, False
                
        # 3. Birth new unique concept hub
        new_neuron = self.birth_neuron(
            x=x_vec,
            y=y_vec,
            z=float(tier_z),
            tier_z=tier_z,
            network_id=network_id,
            w=tier_z,
            text=text_clean,
            role=role,
            grammatical_role=grammatical_role,
            syntax_valence=syntax_valence,
            origin=1.0,
            energy=energy
        )
        return new_neuron, True

    def compute_field_resonance(
        self,
        x_sensory: np.ndarray,
        y_target: Optional[np.ndarray] = None,
        z_event: Optional[float] = None,
        tier_filter: Optional[int] = None,
        z_weight: float = 0.5
    ) -> Dict[int, float]:
        self._sync_tensors()
        if len(self._cached_ids) == 0:
            return {}
            
        x_vec = np.array(x_sensory, dtype=float)
        if x_vec.shape[0] != self.dim:
            x_vec = np.pad(x_vec, (0, max(0, self.dim - x_vec.shape[0])))[:self.dim]
            
        dx2 = np.sum((self._cached_X - x_vec) ** 2, axis=1)
        
        if y_target is not None:
            y_vec = np.array(y_target, dtype=float)
            if y_vec.shape[0] != self.dim:
                y_vec = np.pad(y_vec, (0, max(0, self.dim - y_vec.shape[0])))[:self.dim]
            dy2 = np.sum((self._cached_Y - y_vec) ** 2, axis=1)
        else:
            dy2 = 0.0
            
        if z_event is not None:
            dz2 = z_weight * ((self._cached_Z - float(z_event)) ** 2)
        else:
            dz2 = 0.0
            
        forces = 1.0 / (1.0 + 3.0 * (dx2 + dy2 + dz2))
        
        result: Dict[int, float] = {}
        for idx, n_id in enumerate(self._cached_ids):
            if tier_filter is not None and self._cached_tiers[idx] != tier_filter:
                continue
            result[int(n_id)] = float(forces[idx])
            
        return result

    def build_synaptic_bridge(
        self,
        src_id: int,
        dst_id: int,
        initial_conductance: Optional[float] = None,
        relation_type: str = "associated_with"
    ) -> float:
        if src_id not in self.neurons or dst_id not in self.neurons or src_id == dst_id:
            return 0.0
            
        n_src = self.neurons[src_id]
        n_dst = self.neurons[dst_id]
        
        if initial_conductance is None:
            dist_sq = (
                np.sum((n_src.x - n_dst.x) ** 2) +
                np.sum((n_src.y - n_dst.y) ** 2) +
                0.25 * ((n_src.z - n_dst.z) ** 2)
            )
            initial_conductance = float(np.clip(1.0 / (1.0 + 2.0 * dist_sq), 0.1, 1.0))
            
        conductance = float(np.clip(initial_conductance, 0.0, 1.0))
        n_src.synapses[dst_id] = conductance
        n_src.synapse_relations[dst_id] = str(relation_type)
        
        # Aspire trait physics: Mass increases slightly when a node forms a new structural connection
        if hasattr(n_src, 'mass'):
            n_src.mass = min(10.0, getattr(n_src, 'mass', 1.0) + 0.05)
            
        return conductance

    def potentiate_hebbian(self, active_forces: Dict[int, float], learning_rate: float = 0.15):
        active_ids = [n_id for n_id, f in active_forces.items() if f > 0.12]
        n_active = len(active_ids)
        
        for i in range(n_active):
            id_i = active_ids[i]
            n_i = self.neurons.get(id_i)
            if not n_i:
                continue
            f_i = active_forces[id_i]
            n_i.last_active = self.current_step
            n_i.energy = min(5.0, n_i.energy + f_i * 0.15)
            
            for j in range(i + 1, n_active):
                id_j = active_ids[j]
                n_j = self.neurons.get(id_j)
                if not n_j:
                    continue
                f_j = active_forces[id_j]
                
                # Semantic Cosine Resonance Gating: Only potentiate if concepts are semantically aligned
                sim = float(np.dot(n_i.x, n_j.x))
                if sim > -0.2:
                    co_act = f_i * f_j * min(n_i.energy, n_j.energy) * max(0.2, (sim + 1.0) / 2.0)
                    delta_w = learning_rate * co_act
                    
                    curr_ij = n_i.synapses.get(id_j, 0.0)
                    if curr_ij == 0.0 and co_act > 0.20:
                        self.build_synaptic_bridge(id_i, id_j, initial_conductance=delta_w)
                    elif curr_ij > 0.0:
                        n_i.synapses[id_j] = float(min(1.0, curr_ij + delta_w))
                        
                    curr_ji = n_j.synapses.get(id_i, 0.0)
                    if curr_ji == 0.0 and co_act > 0.20:
                        self.build_synaptic_bridge(id_j, id_i, initial_conductance=delta_w)
                    elif curr_ji > 0.0:
                        n_j.synapses[id_i] = float(min(1.0, curr_ji + delta_w))
                else:
                    # Lateral Anti-Hebbian Inhibition: Depress spurious cross-talk between opposing concepts
                    if id_j in n_i.synapses:
                        n_i.synapses[id_j] = float(max(0.0, n_i.synapses[id_j] - 0.08 * learning_rate))
                    if id_i in n_j.synapses:
                        n_j.synapses[id_i] = float(max(0.0, n_j.synapses[id_i] - 0.08 * learning_rate))

    def dampen(self, decay_rate: float = 0.015):
        """Thermodynamic damping & metabolic relaxation step across all substrate neurons."""
        self.current_step += 1
        for n in self.neurons.values():
            if n.role == "anchor":
                n.energy = 5.0
                continue
            inactivity = max(0, self.current_step - n.last_active)
            decay = decay_rate * (1.0 + inactivity * 0.01)
            n.energy = max(0.1, n.energy - decay)

    def prune_cross_talk_synapses(self, threshold: float = 0.40, max_fanout: int = 12) -> int:
        """
        Anti-Hebbian Topological Pruning:
        Dissolves weak spurious cross-talk connections that cause semantic bleed,
        preserving focused high-conductance relational highways.
        """
        pruned = 0
        for n in self.neurons.values():
            if n.tier_z == 0 and n.role == "letter":
                continue  # Preserve alphabet layer
                
            peers = list(n.synapses.items())
            # Remove any synapse below threshold
            for peer_id, weight in peers:
                if weight < threshold:
                    del n.synapses[peer_id]
                    if peer_id in n.synapse_relations:
                        del n.synapse_relations[peer_id]
                    pruned += 1
                    
            # If fanout exceeds max_fanout, retain only the top conductance bridges
            if len(n.synapses) > max_fanout:
                sorted_syn = sorted(n.synapses.items(), key=lambda it: it[1], reverse=True)
                keep_syn = dict(sorted_syn[:max_fanout])
                for peer_id in list(n.synapses.keys()):
                    if peer_id not in keep_syn:
                        del n.synapses[peer_id]
                        if peer_id in n.synapse_relations:
                            del n.synapse_relations[peer_id]
                        pruned += 1
                        
        return pruned

    def step_thermodynamics(self) -> Dict[str, int]:
        self.current_step += 1
        pruned_synapses = 0
        
        for n_id, n in self.neurons.items():
            n.age += 1
            if n.role != "letter" and self.current_step - n.last_active > 15:
                n.energy = max(0.2, n.energy * 0.995)
                
        for n in self.neurons.values():
            dead_peers = []
            for peer_id, weight in list(n.synapses.items()):
                decayed_w = weight * 0.985
                if decayed_w < self.pruning_threshold or peer_id not in self.neurons:
                    dead_peers.append(peer_id)
                else:
                    n.synapses[peer_id] = float(decayed_w)
                    
            for dead in dead_peers:
                del n.synapses[dead]
                if dead in n.synapse_relations:
                    del n.synapse_relations[dead]
                pruned_synapses += 1
                
        return {
            "pruned_synapses": pruned_synapses,
            "total_neurons": len(self.neurons)
        }

    def propagate_wave(
        self,
        seed_neuron_ids: List[int],
        max_hops: int = 3,
        damping: float = 0.65
    ) -> Dict[int, float]:
        wave_energy: Dict[int, float] = defaultdict(float)
        queue: deque = deque()
        
        for s_id in seed_neuron_ids:
            if s_id in self.neurons:
                wave_energy[s_id] = 1.0
                queue.append((s_id, 1.0, 0))
                
        visited = set(seed_neuron_ids)
        
        while queue:
            curr_id, curr_pot, hop = queue.popleft()
            if hop >= max_hops or curr_pot < 0.05:
                continue
                
            curr_neuron = self.neurons.get(curr_id)
            if not curr_neuron:
                continue
                
            for neighbor_id, conductance in curr_neuron.synapses.items():
                if neighbor_id not in self.neurons:
                    continue
                transferred = curr_pot * conductance * damping
                if transferred > wave_energy[neighbor_id]:
                    wave_energy[neighbor_id] = transferred
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        queue.append((neighbor_id, transferred, hop + 1))
                        
        return dict(wave_energy)

    def get_tier_and_network_stats(self) -> Dict[str, Any]:
        tier_counts = defaultdict(int)
        network_counts = defaultdict(int)
        intra_network_syn = 0
        intra_plane_syn = 0
        cross_tier_syn = 0
        
        for n_id, n in self.neurons.items():
            tier_counts[n.tier_z] += 1
            network_counts[f"Z{n.tier_z}:{n.network_id}"] += 1
            
            for dst_id, w in n.synapses.items():
                n_dst = self.neurons.get(dst_id)
                if not n_dst:
                    continue
                if n.tier_z != n_dst.tier_z:
                    cross_tier_syn += 1
                elif n.network_id == n_dst.network_id:
                    intra_network_syn += 1
                else:
                    intra_plane_syn += 1
                    
        total = intra_network_syn + intra_plane_syn + cross_tier_syn
        return {
            "total_neurons": len(self.neurons),
            "tier_distribution": dict(tier_counts),
            "network_distribution": dict(network_counts),
            "total_synapses": total,
            "intra_network_synapses": intra_network_syn,
            "intra_plane_synapses": intra_plane_syn,
            "cross_tier_synapses": cross_tier_syn
        }

    def get_synapse_stats(self) -> Dict[str, Any]:
        stats = self.get_tier_and_network_stats()
        return {
            "total_synapses": stats["total_synapses"],
            "intra_plane_synapses": stats["intra_network_synapses"] + stats["intra_plane_synapses"],
            "cross_z_inter_plane_synapses": stats["cross_tier_synapses"],
            "tier_distribution": stats["tier_distribution"],
            "network_distribution": stats["network_distribution"]
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dim": self.dim,
            "current_step": self.current_step,
            "current_event_z": float(self.current_event_z),
            "next_neuron_id": self.next_neuron_id,
            "decay_rate": self.decay_rate,
            "pruning_threshold": self.pruning_threshold,
            "neurons": [n.to_dict() for n in self.neurons.values()]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StackedSubstrate':
        sub = cls(
            dim=int(data.get("dim", 16)),
            decay_rate=float(data.get("decay_rate", 0.008)),
            pruning_threshold=float(data.get("pruning_threshold", 0.05))
        )
        sub.current_step = int(data.get("current_step", 0))
        sub.current_event_z = float(data.get("current_event_z", 0.0))
        sub.next_neuron_id = int(data.get("next_neuron_id", 1))
        
        for n_data in data.get("neurons", []):
            n = FellaNeuron.from_dict(n_data)
            sub.neurons[n.id] = n
            
        sub._dirty_tensors = True
        return sub

    def apply_synaptic_decay(self, decay_rate: float = 0.005):
        """Applies global synaptic forgetting across the entire topology."""
        for n in self.neurons.values():
            for peer_id in list(n.synapses.keys()):
                n.synapses[peer_id] *= (1.0 - decay_rate)
                if n.synapses[peer_id] < self.pruning_threshold:
                    del n.synapses[peer_id]
