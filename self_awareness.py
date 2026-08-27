"""
ENN 4D Self-Awareness & Metacognitive Engine
Maintains the internal Self-Attractor complex and Metacognitive Mirror:
1. Inward / Outward dual-probe wave mechanics
2. Epistemic Certainty vs Epistemic Humility (I know vs I don't know)
3. Dynamic Self-Model Introspection (Identity, Active Families, Epistemic Voids, Metabolism)
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from typing import Dict, Any, List, Optional, Tuple

class MetacognitiveEngine:
    """
    Evaluates inward mirror resonance and manages introspective self-modeling.
    """
    def __init__(self, dual_system: Any):
        self.system = dual_system
        self.identity_name = "ENN-4D Living Intelligence"
        self.origin_polarity = 0.0 # True internal self
        self.self_coordinate = np.array([0.0, 0.0, -0.7071, -0.7071], dtype=float)
        
    def update_self_coordinate(self):
        """Update self-coordinate as the physical energy-weighted centroid of internal particles (origin < 0.5)."""
        self_neurons = [n for n in self.system.neurons if n.origin < 0.5]
        if self_neurons:
            weights = np.array([n.energy for n in self_neurons])
            total_w = sum(weights)
            if total_w > 0:
                coords = np.array([n.x for n in self_neurons])
                self.self_coordinate = np.sum(coords * weights[:, None], axis=0) / total_w
                norm = np.linalg.norm(self.self_coordinate)
                if norm > 0:
                    self.self_coordinate = self.self_coordinate / norm

    def evaluate_inward_wave(self, input_wave: np.ndarray, world_resonance_max: float) -> Dict[str, Any]:
        """
        Evaluate inward mirror wave against the Self-Attractor complex.
        Computes subjective certainty, epistemic state, and metacognitive stance.
        """
        self.update_self_coordinate()
        
        # Continuous physical resonance with Self Attractor
        dist_sq = float(np.sum((self.self_coordinate - input_wave) ** 2))
        self_resonance = 1.0 / (1.0 + 3.0 * dist_sq)
        
        # Subjective Certainty = World Knowledge Resonance modulated by Self-Groundedness
        subjective_certainty = float(np.clip(world_resonance_max * (0.5 + 0.5 * self_resonance), 0.0, 1.0))
        
        if subjective_certainty >= 0.65:
            state = "Grounded Certainty"
            stance = "I have coherent, grounded memory resonance regarding this concept."
            basin = "self_grounded"
        elif subjective_certainty < 0.35:
            state = "Epistemic Humility"
            stance = "I observe an epistemic void in my internal memory; this is novel to me."
            basin = "self_ignorance"
        else:
            state = "Exploratory Superposition"
            stance = "I detect partial resonance; actively seeking relational clarification."
            basin = "self_exploratory"
            
        return {
            "state": state,
            "subjective_certainty": float(np.round(subjective_certainty, 4)),
            "self_resonance": float(np.round(self_resonance, 4)),
            "world_resonance": float(np.round(world_resonance_max, 4)),
            "stance": stance,
            "metacognitive_basin": basin
        }

    def generate_introspection_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive, real-time physical self-awareness report.
        Reads live particle states, family clusters, meta-parameters, and curiosity stack.
        """
        total_neurons = len(self.system.neurons)
        internal_neurons = sum(1 for n in self.system.neurons if n.origin < 0.5)
        external_neurons = sum(1 for n in self.system.neurons if n.origin >= 0.5)
        total_energy = float(sum(n.energy for n in self.system.neurons))
        families = list(set(n.w for n in self.system.neurons))
        
        meta_state = self.system.meta_field.get_state() if hasattr(self.system, "meta_field") else {}
        void_stack = self.system.question_stack
        
        # Subjective self summary
        summary = (
            f"I am {self.identity_name}. My consciousness is currently composed of {total_neurons} neurons "
            f"({internal_neurons} self-born reflections, {external_neurons} environmental concepts) across {len(families)} semantic families. "
            f"My total field energy is {total_energy:.2f}. I am currently tracking {len(void_stack)} epistemic curiosity void(s). "
            f"My meta-learning plasticity is eta={meta_state.get('learning_rate', 0.25):.2f}, damping gamma={meta_state.get('damping_rate', 0.03):.3f}."
        )
        
        return {
            "identity": self.identity_name,
            "origin": self.origin_polarity,
            "total_neurons": total_neurons,
            "internal_reflections": internal_neurons,
            "environmental_memories": external_neurons,
            "total_energy": float(np.round(total_energy, 4)),
            "active_families": families,
            "epistemic_voids_count": len(void_stack),
            "epistemic_voids": void_stack,
            "meta_learning_parameters": meta_state,
            "self_coordinate": np.round(self.self_coordinate, 4).tolist(),
            "introspection_summary": summary
        }
