"""
ENN 4D: Pure Semantic Text Decoder
Zero hardcoding. Zero string templates.
Decodes 4D physical interference vectors back to natural language text
using continuous mathematical resonance.
"""

import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

class MemoryRecord:
    def __init__(self, text: str, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: int, time_step: int, features: Optional[np.ndarray] = None):
        self.text = text
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        self.z = np.array(z, dtype=float)
        self.w = int(w) if w is not None else 0
        self.time_step = int(time_step)
        self.features = np.array(features, dtype=float) if features is not None else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "x": self.x.tolist(),
            "y": self.y.tolist(),
            "z": self.z.tolist(),
            "w": self.w,
            "time_step": self.time_step
        }


class TextDecoder:
    def __init__(self):
        """Initialize the associative memory bank."""
        self.memory_log: List[MemoryRecord] = []
        
    def record_memory(self, text: str, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: int, time_step: int, features: Optional[np.ndarray] = None):
        """Store an episodic memory particle in the memory bank."""
        record = MemoryRecord(text, x, y, z, w, time_step, features)
        self.memory_log.append(record)

    def decode_4d_to_text(self, y_vector: np.ndarray, query_features: Optional[np.ndarray] = None) -> str:
        """
        Pure vector decode: Finds the most resonant memory string for the physical field output vector Y.
        Zero hardcoded templates.
        """
        matches = self.find_resonant_memories(y_vector, query_features=query_features, top_k=1)
        if matches:
            return matches[0][0]
        return "No active resonance in memory."

    def find_resonant_memories(self, y_vector: np.ndarray, query_features: Optional[np.ndarray] = None, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Calculates mathematical resonance across all stored memories.
        Combines 4D field output vector alignment with feature manifold resonance.
        """
        if not self.memory_log:
            return []

        y_vec = np.array(y_vector, dtype=float)
        norm_y = np.linalg.norm(y_vec)
        if norm_y > 0:
            y_vec = y_vec / norm_y

        scored = []
        for record in self.memory_log:
            norm_rec = np.linalg.norm(record.x)
            sim_4d = float(np.dot(y_vec, record.x / norm_rec)) if norm_rec > 0 else 0.0
            
            sim_feat = 0.0
            if query_features is not None and record.features is not None:
                norm_qf = np.linalg.norm(query_features)
                norm_rf = np.linalg.norm(record.features)
                if norm_qf > 0 and norm_rf > 0:
                    sim_feat = float(np.dot(query_features / norm_qf, record.features / norm_rf))
            
            # Continuous resonance score
            total_resonance = (0.5 * sim_feat + 0.5 * sim_4d) if query_features is not None else sim_4d
            scored.append((record.text, float(total_resonance)))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def save_memory_log(self, filepath: str = "memory_log.json"):
        """Save memory bank to JSON file."""
        data = [r.to_dict() for r in self.memory_log]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_memory_log(self, filepath: str = "memory_log.json"):
        """Load memory bank from JSON file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.memory_log = [
                MemoryRecord(
                    d["text"],
                    np.array(d["x"]),
                    np.array(d["y"]),
                    np.array(d["z"]),
                    d.get("w", 0),
                    d.get("time_step", 0)
                )
                for d in data
            ]
        except FileNotFoundError:
            self.memory_log = []


# Global helper instance
_default_decoder = TextDecoder()

def decode_4d_to_text(y_vector: np.ndarray) -> str:
    return _default_decoder.decode_4d_to_text(y_vector)