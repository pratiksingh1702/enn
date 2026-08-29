"""
FELLA Metacognition: Inward Self Observer & Epistemic Vacuums
============================================================
Evaluates internal cognitive consistency:
- Epistemic Friction: Discrepancy between internal cognitive expectation and external stimuli
- Self-Confidence Index: Metacognitive certainty score in [0.0, 1.0]
- Epistemic Vacuums: Active knowledge voids that trigger autonomous inquiries to Ollama
- Dynamic Learning Plasticity: eta(t) modulated by epistemic tension and flow state
"""

import numpy as np
import time
from typing import Dict, Any, List, Optional, Tuple


class EpistemicVacuum:
    """Represents a specific unresolved knowledge void / inquiry trigger."""
    def __init__(
        self,
        vacuum_id: str,
        concept_query: str,
        context_z: float,
        source_neuron_ids: List[int],
        tension: float = 1.0,
        context_prompt: str = ""
    ):
        self.vacuum_id = str(vacuum_id)
        self.concept_query = str(concept_query)
        self.context_z = float(context_z)
        self.source_neuron_ids = list(source_neuron_ids)
        self.tension = float(tension)
        self.context_prompt = str(context_prompt)
        self.created_at = time.time()
        self.resolved: bool = False
        self.resolution_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vacuum_id": self.vacuum_id,
            "concept_query": self.concept_query,
            "context_z": self.context_z,
            "source_neuron_ids": self.source_neuron_ids,
            "tension": self.tension,
            "context_prompt": self.context_prompt,
            "created_at": self.created_at,
            "resolved": self.resolved,
            "resolution_text": self.resolution_text
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EpistemicVacuum':
        v = cls(
            vacuum_id=str(data["vacuum_id"]),
            concept_query=str(data["concept_query"]),
            context_z=float(data.get("context_z", 0.0)),
            source_neuron_ids=list(data.get("source_neuron_ids", [])),
            tension=float(data.get("tension", 1.0)),
            context_prompt=str(data.get("context_prompt", ""))
        )
        v.created_at = float(data.get("created_at", time.time()))
        v.resolved = bool(data.get("resolved", False))
        v.resolution_text = str(data.get("resolution_text", ""))
        return v


class InwardObserver:
    """
    Internal Metacognitive Mirror.
    Observes cognitive flow, detects friction, tracks self-confidence, and maintains the queue of inquiries.
    """
    def __init__(self, base_plasticity: float = 0.15):
        self.base_plasticity = float(base_plasticity)
        self.epistemic_friction: float = 0.05
        self.self_confidence: float = 0.90
        self.plasticity: float = self.base_plasticity
        self.flow_state: bool = False
        
        # Knowledge voids queue
        self.vacuums: Dict[str, EpistemicVacuum] = {}
        self.next_vacuum_seq: int = 1

    def observe(self, expected_vector: Optional[np.ndarray], actual_vector: np.ndarray) -> Dict[str, float]:
        """
        Evaluates cognitive prediction consistency against actual input vector.
        Computes friction, confidence, and current plasticity.
        """
        if expected_vector is not None and len(expected_vector) == len(actual_vector):
            diff = actual_vector - expected_vector
            raw_friction = float(np.linalg.norm(diff))
            self.epistemic_friction = float(np.clip(0.7 * self.epistemic_friction + 0.3 * raw_friction, 0.0, 1.0))
        else:
            # Gentle baseline decay
            self.epistemic_friction = float(np.clip(self.epistemic_friction * 0.95, 0.02, 1.0))
            
        # Compute Self-Confidence Index
        self.self_confidence = float(np.clip(1.0 - 2.2 * self.epistemic_friction, 0.05, 0.999))
        self.flow_state = bool(self.epistemic_friction < 0.08 and self.self_confidence > 0.85)
        
        # Dynamic Meta-Learning Plasticity
        self.plasticity = float(self.base_plasticity * (1.0 + 1.5 * self.epistemic_friction - 0.4 * self.self_confidence))
        
        return {
            "epistemic_friction": self.epistemic_friction,
            "self_confidence": self.self_confidence,
            "plasticity": self.plasticity,
            "flow_state": float(1.0 if self.flow_state else 0.0)
        }

    def register_vacuum(
        self,
        concept_query: str,
        context_z: float,
        source_neuron_ids: Optional[List[int]] = None,
        tension: float = 1.0,
        context_prompt: str = ""
    ) -> EpistemicVacuum:
        """Registers an unresolved curiosity/knowledge void."""
        v_id = f"vac_{self.next_vacuum_seq:04d}_{int(context_z)}"
        self.next_vacuum_seq += 1
        
        vacuum = EpistemicVacuum(
            vacuum_id=v_id,
            concept_query=concept_query,
            context_z=context_z,
            source_neuron_ids=source_neuron_ids or [],
            tension=tension,
            context_prompt=context_prompt
        )
        self.vacuums[v_id] = vacuum
        # Spike epistemic friction slightly to reflect genuine inquiry interest
        self.epistemic_friction = min(1.0, self.epistemic_friction + 0.15 * tension)
        return vacuum

    def get_highest_priority_vacuum(self) -> Optional[EpistemicVacuum]:
        """Returns the most urgent unresolved epistemic vacuum."""
        unresolved = [v for v in self.vacuums.values() if not v.resolved]
        if not unresolved:
            return None
        return max(unresolved, key=lambda v: v.tension)

    def resolve_vacuum(self, vacuum_id: str, explanation_summary: str):
        """Marks a vacuum as resolved after learning from Ollama or experience."""
        if vacuum_id in self.vacuums:
            v = self.vacuums[vacuum_id]
            v.resolved = True
            v.resolution_text = str(explanation_summary)
            # Relieve friction upon satisfying curiosity
            self.epistemic_friction = max(0.02, self.epistemic_friction - 0.2 * v.tension)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_plasticity": self.base_plasticity,
            "epistemic_friction": self.epistemic_friction,
            "self_confidence": self.self_confidence,
            "plasticity": self.plasticity,
            "flow_state": self.flow_state,
            "vacuums": {k: v.to_dict() for k, v in self.vacuums.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InwardObserver':
        obs = cls(base_plasticity=float(data.get("base_plasticity", 0.15)))
        obs.epistemic_friction = float(data.get("epistemic_friction", 0.05))
        obs.self_confidence = float(data.get("self_confidence", 0.90))
        obs.plasticity = float(data.get("plasticity", 0.15))
        obs.flow_state = bool(data.get("flow_state", False))
        
        vacs = data.get("vacuums", {})
        for k, v_data in vacs.items():
            obs.vacuums[k] = EpistemicVacuum.from_dict(v_data)
            
        return obs
