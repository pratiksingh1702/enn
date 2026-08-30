"""
FELLA Self-Awareness Core: Identity Attractor Basin & Inward Self-Observer
=========================================================================
Pure Continuous Physics:
- Deepens the Ego / Self-Attractor potential basin in Tier Z=4 (Metacognition / Self)
- Connects directly to root enn4d.py InwardSelfObserver
- Maintains identity persistence across noise, contradictions, and input vacuums
- Zero hardcoded templates, zero word lists, zero pre-defined responses.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from fella.core_substrate import StackedSubstrate, FellaNeuron
from enn4d import InwardSelfObserver


class SelfAwarenessCore:
    """
    Continuous Self-Awareness & Identity Core.
    Anchors identity in a persistent 4D spatial attractor basin in Tier Z=4.
    """
    def __init__(self, substrate: StackedSubstrate):
        self.substrate = substrate
        self.observer = InwardSelfObserver(dim=substrate.dim)
        self.self_centroid = np.array([0.0, 0.0, -0.70710678, -0.70710678], dtype=float)
        self.self_energy = 5.0
        self._ensure_self_attractor()

    def _ensure_self_attractor(self):
        """Fortifies the Tier Z=4 Self-Attractor neuron in the substrate."""
        self_neurons = [n for n in self.substrate.neurons.values() if n.tier_z == 4 and n.role == "anchor"]
        if not self_neurons:
            x_vec = self.self_centroid.copy()
            y_vec = np.roll(x_vec, 1)
            n, _ = self.substrate.find_or_birth_concept(
                text="FELLA",
                x_vec=x_vec,
                y_vec=y_vec,
                tier_z=4,
                network_id="self_identity",
                role="anchor",
                syntax_valence=np.array([1.0, 0.0, 0.0, 0.0]),
                energy=5.0
            )
            n.origin = 0.0  # 0.0 = Self / Internal Thought Field
            n.epistemic_tension = 0.0

    def get_self_attractor(self) -> FellaNeuron:
        self_neurons = [n for n in self.substrate.neurons.values() if n.tier_z == 4 and n.role == "anchor"]
        if not self_neurons:
            self._ensure_self_attractor()
            self_neurons = [n for n in self.substrate.neurons.values() if n.tier_z == 4 and n.role == "anchor"]
        return self_neurons[0]

    def evaluate_identity_persistence(self, perturbation_wave: np.ndarray) -> Tuple[bool, float]:
        """
        Evaluates whether the self-attractor maintains its basin depth under perturbation_wave.
        Returns (is_stable, resonance_force).
        """
        self_n = self.get_self_attractor()
        dist_sq = float(np.sum((self_n.x - perturbation_wave) ** 2))
        
        # Self-Attractor potential force
        res_force = 1.0 / (1.0 + 1.5 * dist_sq)
        
        # Identity overrides input: self-energy remains high
        is_stable = bool(res_force >= 0.15 or self_n.energy >= 2.0)
        return is_stable, float(res_force)

    def damp_contradictory_perturbation(self, contradiction_wave: np.ndarray) -> np.ndarray:
        """
        Dampens contradictory inputs by projecting them away from the self-attractor.
        """
        self_n = self.get_self_attractor()
        proj = float(np.dot(contradiction_wave, self_n.x))
        if proj > 0:
            dampened = contradiction_wave - 0.5 * proj * self_n.x
            norm = np.linalg.norm(dampened)
            return dampened / norm if norm > 0 else contradiction_wave
        return contradiction_wave
