"""
ENN 4D: A Living Physics Engine for Thought
Physics-based neural dynamics: Resonance, Interference, Amplification, Damping, and Phase Transitions.
Includes basal metabolic homeostasis, connections tracking, and universe JSON state serialization.
"""

import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from collections import defaultdict

# --- THE 4D NEURON (Particle) ---

class Neuron:
    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: int):
        self.x = np.array(x, dtype=float).copy()           # Input coordinates (X)
        self.y = np.array(y, dtype=float).copy()           # Output coordinates (Y)
        self.z = np.array(z, dtype=float).copy()           # Event / Temporal state (Z)
        self.w = int(w)                                    # Family ID (W)
        
        # Physical properties
        self.energy = 1.0                                  # Mass / activation potential
        self.velocity_x = np.zeros_like(self.x)            # Momentum in X
        self.velocity_y = np.zeros_like(self.y)            # Momentum in Y
        self.velocity_z = np.zeros_like(self.z)            # Momentum in Z
        self.age = 0                                       # Time steps since birth
        self.connections: List[int] = []                   # Connected neuron indices
        self.last_active = 0                               # Last activated step
        
    def distance_to(self, other: 'Neuron') -> float:
        """4D distance with family affinity."""
        dx = np.linalg.norm(self.x - other.x)
        dy = np.linalg.norm(self.y - other.y)
        dz = np.linalg.norm(self.z - other.z) * 0.1
        dw = 0.0 if self.w == other.w else 1.0
        return float(dx + dy + dz + dw)
    
    def clone(self) -> 'Neuron':
        """Create a slightly modified daughter copy."""
        noise = 0.05
        daughter = Neuron(
            x=self.x + np.random.randn(*self.x.shape) * noise,
            y=self.y + np.random.randn(*self.y.shape) * noise,
            z=self.z.copy(),
            w=self.w
        )
        daughter.connections = list(self.connections)
        return daughter
    
    def __repr__(self):
        return f"N(w={self.w}, e={self.energy:.2f}, age={self.age})"

# --- THE ENN 4D SYSTEM (The Universe) ---

class ENN4D:
    def __init__(self, dim: int = 4):
        self.dim = dim
        self.neurons: List[Neuron] = []
        self.next_family_id = 0
        self.history = []           # Track neuron count over time
        self.energy_history = []    # Track total system energy
        self.event_count = 0
        
        # Physical & Biological constants
        self.epsilon = 0.45         # Novelty threshold: max resonance force below this births a neuron
        self.merge_distance = 0.25  # Spatial threshold for merging close neurons
        self.split_energy = 3.5     # Energy threshold for splitting overactive neurons
        self.decay_rate = 0.015     # Natural damping rate
        self.momentum = 0.4         # Momentum factor for spatial attraction
        self.baseline_energy = 0.15 # Basal metabolic floor (Spontaneous life activity)
        self.min_energy = 0.05      # Pruning threshold: neurons below this die
        
    # --- RESONANCE: Compute the field force on each neuron ---
    def compute_resonance(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray) -> List[float]:
        """Compute the resonance force of the incoming event on each neuron."""
        forces = []
        for neuron in self.neurons:
            dx = np.linalg.norm(event_x - neuron.x)
            dy = np.linalg.norm(event_y - neuron.y)
            dist_sq = (dx * dx) + (dy * dy)
            force = 1.0 / (1.0 + 3.0 * dist_sq)
            forces.append(float(force))
        return forces
    
    # --- INTERFERENCE: Combine active neurons' outputs ---
    def interfere(self, event_x: np.ndarray, forces: List[float], event_y: Optional[np.ndarray] = None) -> np.ndarray:
        """Compute the interference output of active neurons."""
        if not self.neurons:
            return event_y.copy() if event_y is not None else np.zeros(self.dim)
        
        combined_y = np.zeros(self.dim)
        total_force = 0.0
        
        for neuron, force in zip(self.neurons, forces):
            if force > 0.05:
                combined_y += force * neuron.y
                total_force += force
        
        if total_force > 0:
            return combined_y / total_force
        else:
            return event_y.copy() if event_y is not None else np.zeros(self.dim)
    
    # --- AMPLIFICATION: Strengthen active neurons ---
    def amplify(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, forces: List[float], signal_magnitude: float):
        """Amplify neurons proportional to resonance force and input signal power."""
        if signal_magnitude < 1e-4:
            return
            
        active_indices = []
        for i, (neuron, force) in enumerate(zip(self.neurons, forces)):
            if force > 0.1:
                active_indices.append(i)
                energy_gain = force * signal_magnitude * 0.15
                neuron.energy += energy_gain
                neuron.last_active = self.event_count
                
                # Spatial convergence toward the resonant event
                shift_x = (event_x - neuron.x) * force * 0.08
                shift_y = (event_y - neuron.y) * force * 0.08
                
                neuron.velocity_x = (neuron.velocity_x + shift_x) * self.momentum
                neuron.velocity_y = (neuron.velocity_y + shift_y) * self.momentum
                
                neuron.x += neuron.velocity_x
                neuron.y += neuron.velocity_y
                neuron.z = 0.9 * neuron.z + 0.1 * event_z
                
            neuron.age += 1
            
        # Synaptic wire-together dynamics (Hebbian co-activation)
        for i in active_indices:
            for j in active_indices:
                if i != j and j not in self.neurons[i].connections:
                    self.neurons[i].connections.append(j)
    
    # --- DAMPING & HOMEOSTASIS: Thermodynamic decay with basal living floor ---
    def dampen(self):
        """Apply continuous thermodynamic damping with basal homeostasis."""
        for neuron in self.neurons:
            inactivity = max(0, self.event_count - neuron.last_active)
            decay = self.decay_rate * (1.0 + inactivity * 0.01)
            
            # Smoothly decay towards basal homeostasis floor
            if neuron.energy > self.baseline_energy:
                neuron.energy = max(self.baseline_energy, neuron.energy - decay)
            else:
                thermal_pulse = np.random.uniform(0.0005, 0.002)
                neuron.energy = min(self.baseline_energy, neuron.energy + thermal_pulse)
            
            # Small thermal noise
            noise = 0.001
            neuron.x += np.random.randn(*neuron.x.shape) * noise
            neuron.y += np.random.randn(*neuron.y.shape) * noise
    
    # --- PHASE TRANSITION: Birth, Merge, Split, Death ---
    def phase_transition(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray, signal_magnitude: float):
        """Apply phase transitions to the system."""
        # 1. Birth: If input has signal and no neuron resonates sufficiently
        if signal_magnitude > 1e-4:
            if not self.neurons:
                self.birth(event_x, event_y, event_z, None)
            else:
                forces = self.compute_resonance(event_x, event_y, event_z)
                max_force = max(forces) if forces else 0.0
                if max_force < self.epsilon:
                    self.birth(event_x, event_y, event_z, None)
        
        # 2. Merge: Merge neurons that are too close within same family
        self.merge_neurons()
        
        # 3. Split: Split over-amplified neurons
        self.split_neurons()
        
        # 4. Prune: Remove dead neurons
        self.prune_neurons()
    
    def find_matching_family(self, x: np.ndarray) -> Optional[int]:
        """Find if input belongs to an existing family cluster."""
        if not self.neurons:
            return None
            
        families = defaultdict(list)
        for neuron in self.neurons:
            families[neuron.w].append(neuron)
            
        best_family = None
        best_dist = float('inf')
        
        for family_id, members in families.items():
            mean_x = np.mean([n.x for n in members], axis=0)
            dist = np.linalg.norm(x - mean_x)
            if dist < best_dist:
                best_dist = dist
                best_family = family_id
                
        if best_dist < 0.5:
            return best_family
        return None
    
    def birth(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, family: Optional[int] = None) -> Neuron:
        """Birth a new neuron in a new or matching family."""
        if family is None:
            family = self.find_matching_family(x)
            
        if family is None:
            family = self.next_family_id
            self.next_family_id += 1
        
        new_neuron = Neuron(x, y, z, family)
        new_neuron.last_active = self.event_count
        
        # Connect to spatially close existing neurons
        new_idx = len(self.neurons)
        for idx, other in enumerate(self.neurons):
            if np.linalg.norm(new_neuron.x - other.x) < 0.8:
                new_neuron.connections.append(idx)
                other.connections.append(new_idx)
                
        self.neurons.append(new_neuron)
        return new_neuron
    
    def merge_neurons(self):
        """Merge neurons that are too close to each other in 4D space."""
        if len(self.neurons) < 2:
            return
            
        merged = set()
        for i in range(len(self.neurons)):
            if i in merged:
                continue
            for j in range(i + 1, len(self.neurons)):
                if j in merged:
                    continue
                n1 = self.neurons[i]
                n2 = self.neurons[j]
                
                dist = np.linalg.norm(n1.x - n2.x) + np.linalg.norm(n1.y - n2.y)
                if dist < self.merge_distance and n1.w == n2.w:
                    total_e = n1.energy + n2.energy
                    n1.x = (n1.x * n1.energy + n2.x * n2.energy) / total_e
                    n1.y = (n1.y * n1.energy + n2.y * n2.energy) / total_e
                    n1.energy = total_e * 0.85
                    
                    # Merge connections
                    n1.connections = list(set(n1.connections + n2.connections))
                    if i in n1.connections:
                        n1.connections.remove(i)
                    if j in n1.connections:
                        n1.connections.remove(j)
                        
                    merged.add(j)
        
        if merged:
            surviving = [n for idx, n in enumerate(self.neurons) if idx not in merged]
            # Remap connection indices
            old_to_new = {}
            new_idx = 0
            for idx in range(len(self.neurons)):
                if idx not in merged:
                    old_to_new[idx] = new_idx
                    new_idx += 1
            for n in surviving:
                n.connections = [old_to_new[c] for c in n.connections if c in old_to_new]
            self.neurons = surviving
    
    def split_neurons(self):
        """Split neurons whose energy exceeds the phase transition threshold."""
        new_neurons = []
        for neuron in self.neurons:
            if neuron.energy > self.split_energy:
                d1 = neuron.clone()
                d2 = neuron.clone()
                
                d1.energy = neuron.energy * 0.55
                d2.energy = neuron.energy * 0.45
                
                noise = 0.08
                d1.x += np.random.randn(*d1.x.shape) * noise
                d2.x -= np.random.randn(*d2.x.shape) * noise
                
                new_neurons.extend([d1, d2])
            else:
                new_neurons.append(neuron)
        
        self.neurons = new_neurons
    
    def prune_neurons(self):
        """Remove dead neurons whose energy dropped below the minimum threshold."""
        alive = [n for n in self.neurons if n.energy >= self.min_energy]
        if len(alive) != len(self.neurons):
            old_to_new = {old_idx: new_idx for new_idx, old_idx in enumerate(
                [i for i, n in enumerate(self.neurons) if n.energy >= self.min_energy]
            )}
            for n in alive:
                n.connections = [old_to_new[c] for c in n.connections if c in old_to_new]
            self.neurons = alive
    
    # --- STEP THE SYSTEM ---
    def step(self, event_x: np.ndarray, event_y: np.ndarray, event_z: np.ndarray) -> np.ndarray:
        """Process a single event through the 5 physical laws."""
        self.event_count += 1
        signal_magnitude = float(np.linalg.norm(event_x) + np.linalg.norm(event_y)) / 2.0
        
        # 1. Resonance
        forces = self.compute_resonance(event_x, event_y, event_z)
        
        # 2. Interference
        output_y = self.interfere(event_x, forces, event_y)
        
        # 3. Amplification
        self.amplify(event_x, event_y, event_z, forces, signal_magnitude)
        
        # 4. Damping & Homeostasis
        self.dampen()
        
        # 5. Phase transition
        self.phase_transition(event_x, event_y, event_z, signal_magnitude)
        
        # History tracking
        self.history.append(len(self.neurons))
        self.energy_history.append(sum(n.energy for n in self.neurons))
        
        return output_y
    
    # --- PERSISTENCE: Save & Load Universe ---
    def save(self, filepath: str = "universe.json"):
        """Save the full living universe state to a JSON file."""
        data = {
            "event_count": self.event_count,
            "next_family_id": self.next_family_id,
            "total_energy": float(sum(n.energy for n in self.neurons)),
            "total_neurons": len(self.neurons),
            "num_families": len(set(n.w for n in self.neurons)),
            "neurons": [
                {
                    "id": i,
                    "x": np.round(n.x, 4).tolist(),
                    "y": np.round(n.y, 4).tolist(),
                    "z": np.round(n.z, 4).tolist(),
                    "w": int(n.w),
                    "energy": float(np.round(n.energy, 4)),
                    "age": int(n.age),
                    "velocity_x": np.round(n.velocity_x, 4).tolist(),
                    "velocity_y": np.round(n.velocity_y, 4).tolist(),
                    "connections": [int(c) for c in n.connections if c < len(self.neurons) and c != i],
                    "last_active": int(n.last_active)
                }
                for i, n in enumerate(self.neurons)
            ]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Living universe state saved to {filepath} ({len(self.neurons)} neurons, {data['num_families']} families)")

    def load(self, filepath: str = "universe.json"):
        """Load a living universe state from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.event_count = data["event_count"]
        self.next_family_id = data["next_family_id"]
        self.neurons = []
        for d in data["neurons"]:
            n = Neuron(np.array(d["x"]), np.array(d["y"]), np.array(d["z"]), d["w"])
            n.energy = float(d["energy"])
            n.age = int(d["age"])
            n.velocity_x = np.array(d["velocity_x"])
            n.velocity_y = np.array(d["velocity_y"])
            n.connections = list(d.get("connections", []))
            n.last_active = int(d.get("last_active", 0))
            self.neurons.append(n)
        print(f"Loaded universe from {filepath}: {len(self.neurons)} neurons, {self.event_count} events.")

    # --- STATE INSPECTION ---
    def display(self):
        """Display summary of the system state."""
        print(f"\n--- ENN 4D System ---")
        print(f"Total Neurons: {len(self.neurons)}")
        print(f"Total Energy: {sum(n.energy for n in self.neurons):.2f}")
        print(f"Total Families: {len(set(n.w for n in self.neurons))}")
        print(f"Events Processed: {self.event_count}")
        
        families = defaultdict(list)
        for neuron in self.neurons:
            families[neuron.w].append(neuron)
        
        for family_id, members in sorted(families.items()):
            avg_energy = np.mean([n.energy for n in members])
            print(f"  Family {family_id}: {len(members)} neurons, avg energy {avg_energy:.2f}")


def run_demo():
    """Run a demonstration of the ENN 4D system and save state."""
    system = ENN4D(dim=4)
    
    pattern_A = np.array([0.0, 0.0, 1.0, 1.0]) / np.sqrt(2)
    pattern_B = np.array([1.0, 0.0, 1.0, 0.0]) / np.sqrt(2)
    pattern_C = np.array([1.0, 1.0, 0.0, 0.0]) / np.sqrt(2)
    pattern_D = np.array([0.0, 1.0, 0.0, 1.0]) / np.sqrt(2)
    pattern_E = np.array([0.5, 0.5, 0.5, 0.5])
    
    print("=" * 60)
    print("ENN 4D DEMONSTRATION & SNAPSHOT")
    print("=" * 60)
    
    print("\n--- Training across 5 distinct pattern domains ---")
    for i in range(40):
        system.step(pattern_A, pattern_A, np.array([0.1]))
    for i in range(40):
        system.step(pattern_B, pattern_B, np.array([0.2]))
    for i in range(40):
        system.step(pattern_C, pattern_C, np.array([0.3]))
    for i in range(40):
        system.step(pattern_D, pattern_D, np.array([0.4]))
    for i in range(40):
        system.step(pattern_E, pattern_E, np.array([0.5]))
    
    system.display()
    system.save("universe.json")
    return system


if __name__ == "__main__":
    system = run_demo()
