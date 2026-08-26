"""
Text Encoder for ENN 4D Living Universe
Transforms human text into 4D sensory event vectors (X, Y, Z, W) with semantic consistency.
"""

import re
import numpy as np
from typing import Dict, Any, List, Optional


class TextEncoder:
    """
    Encodes text into 4D coordinate vectors (X, Y, Z, W).
    Provides dense semantic projection with deterministic semantic manifold mapping,
    supporting sentence-transformers if installed.
    """
    
    def __init__(self, dim: int = 4):
        self.dim = dim
        self.step_counter = 0
        self.memory_log: List[Dict[str, Any]] = []
        self._st_model = None
        
        # Try loading sentence-transformers if available
        try:
            from sentence_transformers import SentenceTransformer
            self._st_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            self._st_model = None
            
        # Deterministic projection matrix for 4D embedding
        np.random.seed(42)
        proj = np.random.randn(64, self.dim)
        q, _ = np.linalg.qr(proj)
        self._proj_matrix = q[:, :self.dim]

        # Topic categories for semantic family assignment (W coordinate)
        self.family_topics = {
            0: ["name", "who", "i am", "called", "identity", "alex", "smith", "person", "professor"],
            1: ["like", "love", "hate", "prefer", "favorite", "hobby", "cat", "dog", "apple", "food"],
            2: ["work", "job", "profession", "scientist", "engineer", "doctor", "teacher", "research"],
            3: ["where", "live", "place", "city", "location", "from", "world", "country"],
            4: ["feeling", "happy", "sad", "tired", "excited", "mood", "good", "great"],
            5: ["time", "today", "yesterday", "tomorrow", "now", "when", "year", "date"]
        }

    def _clean_text(self, text: str) -> str:
        return text.strip().lower()

    def is_query(self, text: str) -> bool:
        """Determines whether the input is an inquiry/question."""
        cleaned = self._clean_text(text)
        query_words = ["what", "who", "where", "when", "why", "how", "tell", "do you", "is my", "are you"]
        return any(q in cleaned for q in query_words) or cleaned.endswith("?")

    def extract_semantic_embedding(self, text: str) -> np.ndarray:
        """
        Extracts a dense semantic embedding in [0.05, 0.95]^dim.
        """
        cleaned = self._clean_text(text)
        
        if self._st_model is not None:
            try:
                emb = self._st_model.encode(cleaned, show_progress_bar=False)
                if len(emb) != self.dim:
                    chunk = emb[:64] if len(emb) >= 64 else np.pad(emb, (0, 64 - len(emb)))
                    proj = np.dot(chunk, self._proj_matrix)
                    vec = (proj - np.min(proj)) / (np.max(proj) - np.min(proj) + 1e-8)
                    return np.clip(vec * 0.8 + 0.1, 0.05, 0.95)
            except Exception:
                pass
                
        # High-order subword and semantic hashing
        feature_vec = np.zeros(64, dtype=float)
        words = re.findall(r'\b\w+\b', cleaned)
        
        for idx, word in enumerate(words):
            h_word = abs(hash(word)) % 64
            feature_vec[h_word] += 1.5 / ((idx + 1) ** 0.4)
            for k in range(len(word) - 2):
                gram = word[k:k+3]
                h_gram = abs(hash(gram)) % 64
                feature_vec[h_gram] += 0.4
                
        # Semantic topic affinity
        for fam_id, keywords in self.family_topics.items():
            for kw in keywords:
                if kw in cleaned:
                    feature_vec[fam_id * 8:(fam_id + 1) * 8] += 2.2
                    
        norm = np.linalg.norm(feature_vec)
        if norm > 0:
            feature_vec /= norm
            
        proj_4d = np.dot(feature_vec, self._proj_matrix)
        norm_4d = (proj_4d - np.min(proj_4d)) / (np.max(proj_4d) - np.min(proj_4d) + 1e-8)
        norm_4d = norm_4d * 0.8 + 0.1
        return np.round(norm_4d, 4)

    def assign_family(self, text: str, x_vector: np.ndarray) -> int:
        """Assigns semantic family ID (W)."""
        cleaned = self._clean_text(text)
        for fam_id, keywords in self.family_topics.items():
            if any(kw in cleaned for kw in keywords):
                return fam_id
        return int(np.argmax(x_vector) % len(self.family_topics))

    def encode_text_to_4d(self, text: str, temporal_step: Optional[int] = None) -> Dict[str, Any]:
        """
        Converts any sentence into a 4D sensory event vector.
        """
        self.step_counter += 1
        step_idx = temporal_step if temporal_step is not None else self.step_counter
        
        x_vec = self.extract_semantic_embedding(text)
        y_vec = x_vec.copy()
        
        z_val = float((step_idx % 100) / 100.0)
        z_vec = np.array([z_val], dtype=float)
        
        family_w = self.assign_family(text, x_vec)
        query_flag = self.is_query(text)
        
        event = {
            'text': text.strip(),
            'x': x_vec,
            'y': y_vec,
            'z': z_vec,
            'w': int(family_w),
            'is_query': query_flag,
            'step': step_idx
        }
        
        self.memory_log.append(event)
        return event

    def get_memory_log(self) -> List[Dict[str, Any]]:
        return self.memory_log

    def set_memory_log(self, memories: List[Dict[str, Any]]):
        self.memory_log = memories
        if memories:
            self.step_counter = max(m.get('step', 0) for m in memories)