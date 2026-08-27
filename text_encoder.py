"""
ENN 4D: Neural Text Encoder (with Batching Support)
Zero hardcoding. Zero rule dictionaries. Zero templates.
Uses continuous deep semantic embeddings from local HuggingFace cache (BAAI/bge-small-en-v1.5)
with batching support for high-throughput streaming.
"""

import os
import glob
import hashlib
import numpy as np
from typing import Dict, Any, Optional, List

class TextEncoder:
    def __init__(self, dim: int = 4, seed: int = 42):
        self.dim = dim
        self.seed = seed
        self._hf_model = None
        self._hf_tokenizer = None
        self._use_hf = False
        self._proj = None
        
        self._init_model()

    def _init_model(self):
        cache_pattern = os.path.expanduser(r'~/.cache/huggingface/hub/models--BAAI--bge-small-en-v1.5/snapshots/*')
        snapshots = glob.glob(cache_pattern)
        
        if snapshots and os.path.isdir(snapshots[0]):
            try:
                import torch
                from transformers import AutoTokenizer, AutoModel
                snapshot_dir = snapshots[0]
                self._hf_tokenizer = AutoTokenizer.from_pretrained(snapshot_dir)
                self._hf_model = AutoModel.from_pretrained(snapshot_dir)
                self._hf_model.eval()
                self._use_hf = True
                
                rng = np.random.RandomState(self.seed)
                mat = rng.randn(384, self.dim)
                q, _ = np.linalg.qr(mat)
                self._proj = q[:, :self.dim]
                return
            except Exception:
                self._use_hf = False
                
        self.vocab_dim = 2048
        rng = np.random.RandomState(self.seed)
        mat = rng.randn(self.vocab_dim, self.dim)
        q, _ = np.linalg.qr(mat)
        self._proj = q[:, :self.dim]

    def encode_batch(self, texts: List[str], time_steps: Optional[List[float]] = None) -> List[Dict[str, Any]]:
        """Encode a batch of texts simultaneously for high speed."""
        if time_steps is None:
            time_steps = [(i * 0.001) % 1.0 for i in range(len(texts))]
            
        results = []
        if self._use_hf:
            import torch
            batch_size = 64
            all_embeddings = []
            for i in range(0, len(texts), batch_size):
                chunk = texts[i:i+batch_size]
                formatted = [f"Represent this sentence: {t}" if t.endswith('?') else t for t in chunk]
                inputs = self._hf_tokenizer(formatted, padding=True, truncation=True, max_length=128, return_tensors='pt')
                with torch.no_grad():
                    out = self._hf_model(**inputs)
                    emb = out[0][:, 0]
                    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
                    all_embeddings.append(emb.cpu().numpy())
                    
            embs = np.vstack(all_embeddings)
            dense_4d = np.dot(embs, self._proj)
            norms = np.linalg.norm(dense_4d, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            dense_4d = dense_4d / norms
            
            for idx, text in enumerate(texts):
                x_vec = np.round(dense_4d[idx], 4).astype(float)
                results.append({
                    "text": text,
                    "x": x_vec,
                    "y": x_vec.copy(),
                    "z": np.array([float(np.round(time_steps[idx] % 1.0, 4))]),
                    "w": None,
                    "features": embs[idx]
                })
        else:
            for idx, text in enumerate(texts):
                results.append(self.encode(text, time_step=time_steps[idx]))
                
        return results

    def _embed_text(self, text: str) -> np.ndarray:
        if self._use_hf:
            import torch
            formatted = f"Represent this sentence: {text}" if text.endswith('?') else text
            inputs = self._hf_tokenizer([formatted], padding=True, truncation=True, max_length=128, return_tensors='pt')
            with torch.no_grad():
                out = self._hf_model(**inputs)
                emb = out[0][:, 0]
                emb = torch.nn.functional.normalize(emb, p=2, dim=1)
                return emb[0].cpu().numpy()
        else:
            normalized = " " + text.lower().strip() + " "
            vec = np.zeros(self.vocab_dim, dtype=float)
            for n in (2, 3, 4):
                for i in range(len(normalized) - n + 1):
                    h = int(hashlib.md5(normalized[i:i+n].encode('utf-8')).hexdigest(), 16) % self.vocab_dim
                    vec[h] += 1.0 / np.sqrt(n)
            for word in text.lower().split():
                h = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16) % self.vocab_dim
                vec[h] += 2.0
            norm = np.linalg.norm(vec)
            return vec / norm if norm > 0 else vec

    def encode(self, text: str, time_step: float = 0.1, family: Optional[int] = None, origin: float = 1.0) -> Dict[str, Any]:
        features = self._embed_text(text)
        dense_4d = np.dot(features, self._proj)
        norm_4d = np.linalg.norm(dense_4d)
        dense_4d = (dense_4d / norm_4d) if norm_4d > 0 else np.array([0.5, 0.5, 0.5, 0.5])
            
        x_vec = np.round(dense_4d, 4).astype(float)
        y_vec = x_vec.copy()
        z_vec = np.array([float(np.round(time_step % 1.0, 4))])
        
        return {
            "text": text,
            "x": x_vec,
            "y": y_vec,
            "z": z_vec,
            "w": family,
            "origin": float(origin),
            "features": features
        }

    def encode_constellation(self, text: str, time_step: float = 0.1, family: Optional[int] = None, origin: float = 1.0) -> List[Dict[str, Any]]:
        """
        Decomposes an utterance into a relational micro-circuit (geometric constellation).
        Returns a list of node dicts with anchor, component, and relational vectors.
        """
        words = [w.strip() for w in text.strip().split() if w.strip()]
        if len(words) <= 1:
            # Single token -> single neuron
            base = self.encode(text, time_step=time_step, family=family, origin=origin)
            base["role"] = "anchor"
            return [base]

        # 1. Global Anchor
        anchor = self.encode(text, time_step=time_step, family=family, origin=origin)
        anchor["role"] = "anchor"
        nodes = [anchor]

        # 2. Sub-components: entities / relations / objects
        # For short sentences (e.g. "I am Pratik"), individual tokens form constellation nodes.
        # For longer sentences, small 2-3 word phrases form nodes.
        chunks = []
        if len(words) <= 4:
            chunks = words
        else:
            # Group into 2-word sliding phrases
            for i in range(0, len(words), 2):
                chunks.append(" ".join(words[i:i+2]))

        for idx, chunk in enumerate(chunks):
            chunk_enc = self.encode(chunk, time_step=time_step, family=family, origin=origin)
            # Offset slightly relative to anchor coordinate to create a coherent geometric orbit
            offset = 0.05 * (chunk_enc["x"] - anchor["x"])
            node_x = anchor["x"] + offset
            norm = np.linalg.norm(node_x)
            if norm > 0:
                node_x = node_x / norm
                
            chunk_enc["x"] = np.round(node_x, 4)
            chunk_enc["y"] = chunk_enc["x"].copy()
            chunk_enc["role"] = "relation" if idx == 1 and len(chunks) >= 3 else ("subject" if idx == 0 else "object")
            nodes.append(chunk_enc)

        return nodes


_default_encoder = TextEncoder(dim=4)

def encode_text_to_4d(text: str, time_step: float = 0.1) -> Dict[str, Any]:
    return _default_encoder.encode(text, time_step=time_step)

def encode_constellation(text: str, time_step: float = 0.1, origin: float = 1.0) -> List[Dict[str, Any]]:
    return _default_encoder.encode_constellation(text, time_step=time_step, origin=origin)