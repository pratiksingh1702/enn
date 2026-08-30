"""
FELLA Real Perceptual Encoders (536D Unified Manifold)
======================================================
Pure Continuous High-Dimensional Perceptual Physics:
1. Real Visual Manifold (512D): Real OpenAI CLIP (ViT-B/32) visual-semantic embeddings.
2. Deterministic Physics Manifold (16D): Thermodynamic flux, gravitational curvature, density, velocity, pressure.
3. Somatic/Emotional Manifold (4D): Continuous Valence, Arousal, Dominance/Safety, Social Warmth.
4. Temporal Dynamics Manifold (4D): Oscillation Frequency, Tempo, Periodicity, Persistence.
Total Dimensionality: 512 + 16 + 4 + 4 = 536 Dimensions.
"""

import os
import torch
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from transformers import CLIPTokenizer, CLIPTextModelWithProjection
from fella.real_physics_engine import DeterministicPhysicsEngine, GROUNDED_PHYSICAL_ARCHETYPES


class RealVisualEncoder:
    """Computes real 512-dimensional continuous visual-semantic embeddings using OpenAI CLIP (ViT-B/32)."""
    def __init__(self, model_id: str = "openai/clip-vit-base-patch32", *args, **kwargs):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dim = 512
        self.tokenizer = CLIPTokenizer.from_pretrained(model_id)
        self.text_model = CLIPTextModelWithProjection.from_pretrained(model_id).to(self.device)
        self.text_model.eval()
        self.cache: Dict[str, np.ndarray] = {}

    def encode_visual_prompt(self, visual_description: str) -> np.ndarray:
        """Extracts 512D real CLIP visual-semantic embedding from visual description."""
        if visual_description in self.cache:
            return self.cache[visual_description]
            
        inputs = self.tokenizer([visual_description], padding=True, truncation=True, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.text_model(**inputs)
            emb = outputs.text_embeds[0].cpu().numpy().astype(float)
            
        norm = np.linalg.norm(emb)
        normalized_emb = emb / norm if norm > 0 else emb
        self.cache[visual_description] = normalized_emb
        return normalized_emb

    def encode_visual_properties(
        self,
        luminance: float = 0.5,
        dominant_wavelength_nm: float = 550.0,
        spatial_scale: float = 0.5,
        motion_velocity: float = 0.5,
        transparency: float = 0.0
    ) -> np.ndarray:
        """Legacy compatibility wrapper routing to CLIP space."""
        desc = f"an optical visual field with luminance {luminance:.2f} wavelength {dominant_wavelength_nm:.0f}nm"
        return self.encode_visual_prompt(desc)


class RealEmotionEncoder:
    """Computes continuous 4D Valence-Arousal-Dominance (VAD) Somatic Manifold."""
    def encode_somatic_state(
        self,
        valence: float,      # -1.0 (Harm/Pain) -> +1.0 (Thriving/Joy)
        arousal: float,      # 0.0 (Quiescent) -> 1.0 (High Metabolic Energy)
        safety: float,       # 0.0 (Threat/Annihilation) -> 1.0 (Absolute Security)
        social_warmth: float # 0.0 (Isolated/Indifferent) -> 1.0 (Empathetic Union)
    ) -> np.ndarray:
        return np.array([
            np.clip(float(valence), -1.0, 1.0),
            np.clip(float(arousal), 0.0, 1.0),
            np.clip(float(safety), 0.0, 1.0),
            np.clip(float(social_warmth), 0.0, 1.0)
        ], dtype=float)


class RealTemporalEncoder:
    """Computes continuous 4D Temporal Dynamics Manifold."""
    def encode_temporal_dynamics(
        self,
        frequency_hz: float, # Oscillation rate
        tempo: float,        # 0.0 (Glacial/Slow) -> 1.0 (Rapid/Violent)
        periodicity: float,  # 0.0 (Chaotic/Stochastic) -> 1.0 (Strictly Harmonic)
        persistence: float   # 0.0 (Transient Flash) -> 1.0 (Cosmic Invariant)
    ) -> np.ndarray:
        return np.array([
            np.tanh(float(frequency_hz) / 10.0),
            np.clip(float(tempo), 0.0, 1.0),
            np.clip(float(periodicity), 0.0, 1.0),
            np.clip(float(persistence), 0.0, 1.0)
        ], dtype=float)


class UnifiedPerceptualState:
    """Encapsulates a unified 536-dimensional continuous multimodal perceptual state."""
    def __init__(
        self,
        visual_512: np.ndarray,
        physics_16: np.ndarray,
        emotion_4: np.ndarray,
        temporal_4: np.ndarray
    ):
        self.visual = np.array(visual_512, dtype=float)[:512]
        self.physics = np.array(physics_16, dtype=float)[:16]
        self.emotion = np.array(emotion_4, dtype=float)[:4]
        self.temporal = np.array(temporal_4, dtype=float)[:4]

    def to_536_vector(self) -> np.ndarray:
        """Concatenates all 4 real channels into a unified 536-dimensional vector."""
        v = np.pad(self.visual, (0, max(0, 512 - len(self.visual))))[:512]
        p = np.pad(self.physics, (0, max(0, 16 - len(self.physics))))[:16]
        e = np.pad(self.emotion, (0, max(0, 4 - len(self.emotion))))[:4]
        t = np.pad(self.temporal, (0, max(0, 4 - len(self.temporal))))[:4]
        return np.concatenate([v, p, e, t])

    @classmethod
    def from_536_vector(cls, vec: np.ndarray) -> "UnifiedPerceptualState":
        arr = np.pad(vec, (0, max(0, 536 - len(vec))))[:536]
        return cls(
            visual_512=arr[0:512],
            physics_16=arr[512:528],
            emotion_4=arr[528:532],
            temporal_4=arr[532:536]
        )

