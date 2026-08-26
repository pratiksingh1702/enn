"""
ENN 4D — Pure Associative Memory Field Text Decoder
Decodes physical field interference output vectors (Y) into retrieved text memories
using geometric proximity and field resonance ranking.
No hardcoded regex substitutions, templates, or manual keyword dictionaries.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple


class TextDecoder:
    """
    Continuous Field Decoder for ENN 4D.
    Retrieves memories from the living field based on
    pure geometric similarity (Cosine alignment & Euclidean proximity).
    """
    
    def __init__(self, memory_log: Optional[List[Dict[str, Any]]] = None):
        self.memory_log: List[Dict[str, Any]] = memory_log if memory_log is not None else []

    def set_memory_log(self, memory_log: List[Dict[str, Any]]):
        self.memory_log = memory_log

    def compute_field_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """
        Computes metric similarity between two continuous vectors combining
        angular alignment (cosine) and spatial Euclidean proximity.
        """
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        cosine_sim = float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
        euclidean_dist = float(np.linalg.norm(vec_a - vec_b))
        proximity = 1.0 / (1.0 + euclidean_dist)
        
        return float(0.60 * cosine_sim + 0.40 * proximity)

    def rank_memories(self, y_vector: np.ndarray, candidate_log: Optional[List[Dict[str, Any]]] = None) -> List[Tuple[Dict[str, Any], float]]:
        """
        Ranks memories by their geometric field similarity to the interference vector Y.
        """
        pool = candidate_log if candidate_log is not None else self.memory_log
        if not pool:
            return []
            
        scored = []
        for mem in pool:
            target_vec = np.array(mem.get('y', mem.get('x')), dtype=float)
            sim = self.compute_field_similarity(y_vector, target_vec)
            scored.append((mem, sim))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def decode_4d_to_text(
        self, 
        y_vector: np.ndarray, 
        memory_log: Optional[List[Dict[str, Any]]] = None,
        top_k: int = 1,
        min_resonance: float = 0.50
    ) -> str:
        """
        Decodes the output interference vector Y by finding the most resonant memory.
        """
        active_log = memory_log if memory_log is not None else self.memory_log
        if not active_log:
            return "Living field memory is currently empty."

        ranked = self.rank_memories(y_vector, candidate_log=active_log)
        if not ranked:
            return "No resonance detected in field."

        top_mem, top_score = ranked[0]

        if top_k == 1:
            return top_mem['text']
            
        # Multi-memory retrieval if requested
        resonant_texts = [mem['text'] for mem, score in ranked[:top_k] if score >= min_resonance]
        return " | ".join(resonant_texts) if resonant_texts else top_mem['text']