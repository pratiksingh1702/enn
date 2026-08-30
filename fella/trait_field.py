"""
FELLA Trait Field: Psychological Attractor Basins & Intrinsic Drives
===================================================================
Governs autonomous intrinsic motivations:
- INQUIRE: Epistemic curiosity & exploration of unfamiliar knowledge
- ASPIRE: Drive for cognitive mastery, elegance, and higher-order synthesis
- SYNTHESIZE: Associative bridging across distant concept clusters & Z-planes
- SELF_IDENTITY: Self-reflection, agency, and social attachment to mentor/parent
- CAUTION: Uncertainty management, conflict avoidance, and truth verification
- AFFIRM: Reinforcement, contentment, and consolidation of successful learning
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple


class TraitAttractor:
    """An analytical potential energy basin in the trait manifold."""
    def __init__(self, name: str, centroid: np.ndarray, weight: float = 1.0, width: float = 0.45):
        self.name = str(name)
        self.centroid = np.array(centroid, dtype=float)
        self.weight = float(weight)
        self.width = float(width)

    def potential(self, x: np.ndarray) -> float:
        """Evaluates Gaussian potential energy well at position x."""
        diff = x - self.centroid
        dist_sq = float(np.sum(diff ** 2))
        return -self.weight * float(np.exp(-dist_sq / (2.0 * (self.width ** 2))))

    def gradient(self, x: np.ndarray) -> np.ndarray:
        """Evaluates gradient force attracting x toward centroid."""
        diff = x - self.centroid
        dist_sq = float(np.sum(diff ** 2))
        coeff = (self.weight / (self.width ** 2)) * np.exp(-dist_sq / (2.0 * (self.width ** 2)))
        return -coeff * diff


class TraitField:
    """
    Continuous Trait Drive Field for FELLA.
    Modulates internal emotional posture, learning motivation, and question formulation.
    """
    def __init__(self, dim: int = 4):
        self.dim = int(dim)
        self.state = np.array([0.5, 0.5, 0.5, 0.5], dtype=float)
        self.velocity = np.zeros(self.dim, dtype=float)
        self.active_trait: str = "INQUIRE"
        self.trait_energy: Dict[str, float] = {}
        
        # Initialize canonical trait attractor basins
        self.basins: Dict[str, TraitAttractor] = {
            "INQUIRE": TraitAttractor("INQUIRE", np.array([0.9, 0.2, 0.8, 0.3]), weight=1.2, width=0.4),
            "ASPIRE": TraitAttractor("ASPIRE", np.array([0.8, 0.8, 0.9, 0.7]), weight=1.3, width=0.45),
            "SYNTHESIZE": TraitAttractor("SYNTHESIZE", np.array([0.3, 0.9, 0.6, 0.8]), weight=1.1, width=0.4),
            "PATTERN": TraitAttractor("PATTERN", np.array([0.5, 0.5, 0.5, 0.5]), weight=1.25, width=0.42),
            "SELF_IDENTITY": TraitAttractor("SELF_IDENTITY", np.array([0.2, 0.3, 0.2, 0.9]), weight=1.0, width=0.35),
            "CAUTION": TraitAttractor("CAUTION", np.array([0.1, 0.1, 0.2, 0.2]), weight=1.0, width=0.35),
            "AFFIRM": TraitAttractor("AFFIRM", np.array([0.5, 0.95, 0.4, 0.6]), weight=1.1, width=0.4),
            "UNCERTAINTY": TraitAttractor("UNCERTAINTY", np.array([0.05, 0.05, 0.05, 0.05]), weight=1.3, width=0.35)
        }

    def step(self, external_drive: Optional[np.ndarray] = None, dt: float = 0.1) -> str:
        """
        Advances trait field dynamics under potential gradients + external sensory drive.
        Returns the dominant active trait.
        """
        # External drive force directly guides the trait state
        if external_drive is not None:
            drive_vec = np.array(external_drive, dtype=float)[:self.dim]
            if len(drive_vec) < self.dim:
                drive_vec = np.pad(drive_vec, (0, self.dim - len(drive_vec)))
            # Strong sensory drive coupling
            self.state = 0.4 * self.state + 0.6 * drive_vec
            
        # Sum attractor gradient forces
        grad_sum = np.zeros(self.dim, dtype=float)
        for name, basin in self.basins.items():
            grad_sum += basin.gradient(self.state)
            
        # Kinematic update with damping
        self.velocity = self.velocity * 0.7 + grad_sum * dt
        self.state = np.clip(self.state + self.velocity * dt, 0.0, 1.0)
        
        # Evaluate energies at new state
        energies: Dict[str, float] = {}
        for name, basin in self.basins.items():
            pot = basin.potential(self.state)
            energies[name] = float(-pot)  # Depth of well = affinity
            
        self.trait_energy = energies
        
        # Determine dominant collapsed trait
        self.active_trait = max(self.trait_energy.items(), key=lambda item: item[1])[0]
        return self.active_trait

    def inject_aspiration(self, intensity: float = 0.5):
        """Boosts the ASPIRE drive to encourage higher-order concept mastering."""
        aspire_centroid = self.basins["ASPIRE"].centroid
        self.state = self.state * (1.0 - intensity) + aspire_centroid * intensity

    def inject_curiosity(self, intensity: float = 0.6):
        """Boosts the INQUIRE drive upon encountering unknown facts or novel words."""
        inquire_centroid = self.basins["INQUIRE"].centroid
        self.state = self.state * (1.0 - intensity) + inquire_centroid * intensity

    def inject_uncertainty(self, intensity: float = 0.7):
        """Boosts the UNCERTAINTY drive upon high epistemic friction or weak resonance."""
        unc_centroid = self.basins["UNCERTAINTY"].centroid
        self.state = self.state * (1.0 - intensity) + unc_centroid * intensity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dim": self.dim,
            "state": self.state.tolist(),
            "active_trait": self.active_trait,
            "trait_energy": self.trait_energy
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TraitField':
        tf = cls(dim=int(data.get("dim", 4)))
        tf.state = np.array(data.get("state", [0.5, 0.5, 0.5, 0.5]), dtype=float)
        tf.active_trait = str(data.get("active_trait", "INQUIRE"))
        tf.trait_energy = data.get("trait_energy", {})
        return tf
