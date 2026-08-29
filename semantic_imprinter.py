"""
High-Bandwidth 4D Semantic Imprinter
====================================
Rapidly ingests structured text, documentation, code, or conceptual graphs,
decomposes them into relational 4D semantic constellations, and injects them
directly into ENN 4D Network A with mutual Hebbian synaptic conductance channels.
"""

import re
import time
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from enn4d import ENN4D, Neuron


class SemanticImprinter:
    """
    Deconstructs knowledge streams into 4D space-time coordinate constellations:
    - X-axis (Input Receptive Vector): [Subject/Entity Axis, Relation/Action Axis, Domain Axis, Complexity Axis]
    - Y-axis (Output Action Vector): [Effect Vector, Valence, Synthesis Priority, Motor Target]
    - Z-axis (Space-Time Coordinate): [Creation Timestamp, Depth Level, Hierarchy Level, Temporal Order]
    - W-axis (Family Prototype ID): Deterministic domain cluster ID (Physics, Biology, Architecture, Philosophy, Code)
    """
    def __init__(self):
        # Domain keyword hash map for assigning W family prototype IDs
        self.domain_family_map = {
            "physics": 0,
            "architecture": 1,
            "biology": 2,
            "metabolism": 2,
            "philosophy": 3,
            "cognition": 3,
            "technology": 4,
            "code": 4,
            "cosmology": 5,
            "society": 6,
            "social": 6
        }

    def _determine_domain_family(self, text: str) -> int:
        t_low = text.lower()
        for domain, fam_id in self.domain_family_map.items():
            if domain in t_low:
                return fam_id
        # Fallback hash
        return abs(hash(text[:10])) % 8

    def _text_to_4d_vector(self, text: str, domain_id: int, depth: int = 0) -> np.ndarray:
        """Projects a concept string into normalized 4D continuous coordinates."""
        seed = abs(hash(text.strip().lower())) % (2**32 - 1)
        rng = np.random.RandomState(seed)
        
        # Dim 0: Domain / Category coordinate
        d0 = (domain_id + 1.0) / 10.0
        # Dim 1: Word length / Structural density
        d1 = float(np.clip(len(text) / 40.0, 0.1, 0.9))
        # Dim 2: Semantic Hash Axis
        d2 = float(rng.uniform(0.15, 0.85))
        # Dim 3: Hierarchy depth
        d3 = float(np.clip(0.2 + depth * 0.15, 0.1, 0.95))
        
        vec = np.array([d0, d1, d2, d3], dtype=np.float32)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else np.array([0.5, 0.5, 0.5, 0.5], dtype=np.float32)

    def extract_concept_constellations(self, raw_text: str, topic_hint: str = "General") -> List[Dict[str, Any]]:
        """
        Parses raw text into interconnected concept nodes with 4D coordinates.
        """
        # Split into sentences / paragraphs
        sentences = [s.strip() for s in re.split(r'[.\n;]+', raw_text) if len(s.strip()) > 8]
        if not sentences:
            sentences = [raw_text.strip()]

        domain_id = self._determine_domain_family(topic_hint + " " + raw_text)
        nodes = []
        timestamp = float(time.time())

        # Anchor Node (Topic Root)
        root_x = self._text_to_4d_vector(topic_hint, domain_id, depth=0)
        root_y = np.array([1.0, 0.5, 0.5, 1.0], dtype=np.float32)
        root_z = np.array([timestamp, 0.0, 0.0, 0.0], dtype=np.float32)
        
        nodes.append({
            "text": f"Topic: {topic_hint.title()}",
            "x": root_x,
            "y": root_y,
            "z": root_z,
            "role": "anchor",
            "family": domain_id,
            "origin": 1.0,
            "epistemic_tension": 0.0
        })

        # Concept Nodes
        for idx, sent in enumerate(sentences[:15]): # Limit to top 15 nodes per burst
            # Extract key concept phrases
            words = re.findall(r'\b[a-zA-Z]{3,20}\b', sent)
            interesting = [w.title() for w in words if w.lower() not in ["the", "and", "that", "this", "with", "have", "you", "are", "for", "from", "into"]]
            concept_label = " ".join(interesting[:3]) if interesting else sent[:25]
            
            node_x = self._text_to_4d_vector(concept_label, domain_id, depth=idx+1)
            node_y = np.array([0.8, float(idx)/15.0, 0.5, 1.0], dtype=np.float32)
            node_z = np.array([timestamp + (idx * 0.1), float(idx), 0.0, 0.0], dtype=np.float32)
            
            nodes.append({
                "text": concept_label,
                "x": node_x,
                "y": node_y,
                "z": node_z,
                "role": "concept",
                "family": domain_id,
                "origin": 1.0,
                "epistemic_tension": 0.05
            })

        return nodes

    def imprint_into_enn(self, enn: ENN4D, raw_text: str, topic_hint: str = "General") -> Dict[str, Any]:
        """
        Rapidly imprints concept constellations and establishes mutual synaptic bridges.
        """
        nodes = self.extract_concept_constellations(raw_text, topic_hint)
        domain_id = nodes[0]["family"] if nodes else 0
        
        # Birth constellation in Network A
        birthed_neurons = enn.birth_constellation(nodes, family=domain_id)
        
        return {
            "status": "imprinted",
            "topic": topic_hint,
            "family_id": domain_id,
            "nodes_created": len(birthed_neurons),
            "total_brain_neurons": len(enn.neurons),
            "total_brain_synapses": sum(len(n.synapses) for n in enn.neurons)
        }
