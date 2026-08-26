"""
ENN 4D — Pure Mathematical Semantic Text Encoder
Continuous vector space projection using subword hashing, inverse-frequency weighting,
and orthonormal 4D manifold projection.
No hardcoded rules or manual topic dictionaries.
"""

import hashlib
import re
import numpy as np
from typing import Dict, Any, List, Optional


class TextEncoder:
    """
    Deterministic Continuous Vector Encoder for ENN 4D.
    Maps arbitrary text into normalized continuous 4D sensory vectors [0.05, 0.95]^4.
    """
    
    def __init__(self, dim: int = 4, feature_dim: int = 256):
        self.dim = dim
        self.feature_dim = feature_dim
        self.step_counter = 0
        self.memory_log: List[Dict[str, Any]] = []
        
        # Deterministic Orthonormal Projection Matrix (feature_dim -> dim)
        rng = np.random.RandomState(42)
        rand_mat = rng.randn(self.feature_dim, self.dim)
        q, _ = np.linalg.qr(rand_mat)
        self._proj_matrix = q[:, :self.dim]

        # Common functional particles receive diminished frequency weight
        self._functional_tokens = {
            "a", "an", "the", "is", "am", "are", "was", "were", "be", "been",
            "and", "or", "in", "on", "at", "to", "for", "of", "with", "by",
            "it", "this", "that", "do", "does", "did"
        }

    def _hash_token(self, token: str, seed: int = 0) -> int:
        """Deterministic integer hash for token."""
        h = hashlib.sha256(f"{seed}:{token}".encode('utf-8')).hexdigest()
        return int(h[:8], 16) % self.feature_dim

    def _text_to_feature_vector(self, text: str) -> np.ndarray:
        """
        Converts text to a high-dimensional continuous feature vector using
        word tokens, character n-grams, and inverse frequency weighting.
        """
        cleaned = text.strip().lower()
        words = re.findall(r'\b\w+\b', cleaned)
        
        vec = np.zeros(self.feature_dim, dtype=float)
        if not words:
            return vec

        for pos, word in enumerate(words):
            # Functional vs Content token weighting
            is_func = word in self._functional_tokens or len(word) <= 2
            base_weight = 0.25 if is_func else 2.5
            pos_factor = 1.0 / np.sqrt(pos + 1.0)
            token_weight = base_weight * pos_factor
            
            # 1. Whole-word feature
            w_idx = self._hash_token(word, seed=1)
            vec[w_idx] += token_weight
            
            # 2. Subword character n-grams (3, 4, 5) for root & morphological semantics
            if not is_func:
                for n in (3, 4, 5):
                    if len(word) >= n:
                        for i in range(len(word) - n + 1):
                            ngram = word[i:i+n]
                            ng_idx = self._hash_token(ngram, seed=n)
                            vec[ng_idx] += 1.0 * pos_factor

            # 3. Word-pair bi-grams for context phrase semantics
            if pos < len(words) - 1:
                next_w = words[pos + 1]
                bigram = f"{word}_{next_w}"
                bg_idx = self._hash_token(bigram, seed=2)
                vec[bg_idx] += 1.5 * pos_factor

        # L2 Normalization
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def extract_vector(self, text: str) -> np.ndarray:
        """
        Projects high-dimensional text feature vector onto the 4D field coordinate box [0.05, 0.95].
        """
        features = self._text_to_feature_vector(text)
        projected = np.dot(features, self._proj_matrix)
        
        # Min-max scaling onto [0.05, 0.95]
        min_v = np.min(projected)
        max_v = np.max(projected)
        if max_v - min_v > 1e-8:
            normalized = (projected - min_v) / (max_v - min_v)
        else:
            normalized = np.full_like(projected, 0.5)
            
        scaled = normalized * 0.9 + 0.05
        return np.round(scaled, 4)

    def encode_text_to_4d(self, text: str, temporal_step: Optional[int] = None) -> Dict[str, Any]:
        """
        Encodes text into a 4D sensory event vector:
        - X: Continuous semantic position in 4D space
        - Y: Target associative memory vector
        - Z: Normalized temporal step
        - W: Dynamic family placeholder (assigned organically by ENN4D spatial clustering)
        """
        self.step_counter += 1
        step_idx = temporal_step if temporal_step is not None else self.step_counter
        
        x_vec = self.extract_vector(text)
        y_vec = x_vec.copy()
        
        # Normalized temporal coordinate
        z_val = float((step_idx % 1000) / 1000.0)
        z_vec = np.array([z_val], dtype=float)
        
        event = {
            'text': text.strip(),
            'x': x_vec,
            'y': y_vec,
            'z': z_vec,
            'w': None,
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