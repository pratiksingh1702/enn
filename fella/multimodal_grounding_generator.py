"""
FELLA Real 536D Multimodal Grounding Curriculum Generator
=========================================================
Generates 1,000 paired multimodal exposures:
Sentence Stream + 536D Continuous Perceptual State (512D Visual + 16D Physics + 4D VAD + 4D Temporal).
"""

import random
import numpy as np
from typing import List, Tuple, Dict, Any
from fella.real_physics_engine import DeterministicPhysicsEngine, GROUNDED_PHYSICAL_ARCHETYPES
from fella.real_perceptual_encoders import (
    RealVisualEncoder,
    RealEmotionEncoder,
    RealTemporalEncoder,
    UnifiedPerceptualState
)


class RealMultimodalCurriculumGenerator:
    """Generates paired linguistic and deterministic 536D continuous perceptual vectors."""
    def __init__(self, seed: int = 42):
        random.seed(seed)
        
        self.phys_engine = DeterministicPhysicsEngine()
        self.vis_encoder = RealVisualEncoder(dim=512)
        self.emo_encoder = RealEmotionEncoder()
        self.temp_encoder = RealTemporalEncoder()
        
        # Grounded Real Archetypes across 6 Core Domains with Real CLIP Visual Prompts
        self.domains = {
            "sun": {
                "sentences": [
                    "The sun is a radiant star that generates immense heat through nuclear fusion and emits bright light across space.",
                    "Solar photons illuminate planetary orbits and warm the earth through continuous radiant thermal energy.",
                    "A massive star radiates immense electromagnetic flux to sustain planetary warmth."
                ],
                "clip_prompt": "a photo of the bright yellow radiant sun glowing in outer space with solar flares and intense heat",
                "physics_key": "sun",
                "emotion": {"valence": 0.90, "arousal": 0.90, "safety": 0.85, "social_warmth": 0.80},
                "temporal": {"frequency_hz": 0.001, "tempo": 0.30, "periodicity": 0.95, "persistence": 0.99}
            },
            "water": {
                "sentences": [
                    "Water is a clear liquid compound that flows through river networks, evaporates into vapor, and falls as rain.",
                    "Liquid water circulates through planetary hydrological cycles to nourish living organisms.",
                    "A vast liquid ocean balances climate and sustains marine life across the globe."
                ],
                "clip_prompt": "a photo of clear transparent blue liquid water flowing through a natural river with ripples and reflections",
                "physics_key": "water",
                "emotion": {"valence": 0.92, "arousal": 0.50, "safety": 0.95, "social_warmth": 0.70},
                "temporal": {"frequency_hz": 0.05, "tempo": 0.60, "periodicity": 0.85, "persistence": 0.90}
            },
            "air": {
                "sentences": [
                    "Air is an invisible mixture of atmospheric gases that surrounds the planet and enables biological respiration.",
                    "Atmospheric air provides essential oxygen for cellular respiration and shields living ecosystems.",
                    "An invisible gaseous atmosphere envelops planetary terrain and balances surface temperature."
                ],
                "clip_prompt": "a photo of clear blue sky with gentle clouds and transparent atmospheric breeze over the horizon",
                "physics_key": "air",
                "emotion": {"valence": 0.95, "arousal": 0.35, "safety": 0.95, "social_warmth": 0.60},
                "temporal": {"frequency_hz": 0.20, "tempo": 0.50, "periodicity": 0.70, "persistence": 0.95}
            },
            "plants": {
                "sentences": [
                    "Plants are living green autotrophs that capture radiant sunlight through photosynthesis to produce oxygen.",
                    "Forest trees and vegetation convert solar photons into organic nutrients and breathable air.",
                    "Chloroplasts in green leaves synthesize glucose to support planetary life webs."
                ],
                "clip_prompt": "a photo of vibrant green leaves in a lush forest with sunlight shining through tree branches",
                "physics_key": "plants",
                "emotion": {"valence": 0.95, "arousal": 0.30, "safety": 0.95, "social_warmth": 0.85},
                "temporal": {"frequency_hz": 0.0001, "tempo": 0.20, "periodicity": 0.90, "persistence": 0.85}
            },
            "gravity": {
                "sentences": [
                    "Gravity is the invisible geometric curvature of spacetime that attracts mass and holds orbits together.",
                    "Massive celestial objects warp surrounding spacetime fabric to govern orbital mechanics.",
                    "A black hole is an extreme gravitational sink where spacetime curvature traps light and matter."
                ],
                "clip_prompt": "a photo of deep dark outer space with warped spacetime, celestial planetary orbits, and a black hole accretion disk",
                "physics_key": "gravity",
                "emotion": {"valence": 0.80, "arousal": 0.75, "safety": 0.80, "social_warmth": 0.30},
                "temporal": {"frequency_hz": 1e-5, "tempo": 0.10, "periodicity": 0.99, "persistence": 1.0}
            },
            "friendship": {
                "sentences": [
                    "Friendship is an empathetic interpersonal bond founded upon mutual trust, compassionate care, and shared understanding.",
                    "Mutual respect and open communication build lasting emotional safety and social harmony.",
                    "True friends practice empathy to support each other and cultivate deep trust."
                ],
                "clip_prompt": "a photo of two close friends smiling warmly together with empathy, mutual trust, and joyful connection",
                "physics_key": "friendship",
                "emotion": {"valence": 0.98, "arousal": 0.70, "safety": 0.98, "social_warmth": 0.98},
                "temporal": {"frequency_hz": 0.10, "tempo": 0.50, "periodicity": 0.80, "persistence": 0.95}
            },
            "quantum_computing": {
                "sentences": [
                    "Quantum computing uses quantum bits in superposition and entanglement to calculate complex mathematical states simultaneously.",
                    "Superconducting quantum circuits manipulate quantum superposition to perform parallel computation.",
                    "Quantum entanglement enables qubits to process vast states and solve complex mathematical challenges."
                ],
                "clip_prompt": "a photo of a superconducting quantum computer processor circuit with quantum qubits, superposition pathways, and golden dilution cryostat",
                "physics_key": "quantum_computing",
                "emotion": {"valence": 0.85, "arousal": 0.80, "safety": 0.85, "social_warmth": 0.40},
                "temporal": {"frequency_hz": 5e9, "tempo": 0.95, "periodicity": 0.90, "persistence": 0.70}
            }
        }

    def generate_paired_curriculum(self, total_count: int = 1000) -> List[Tuple[str, UnifiedPerceptualState]]:
        """Generates 1,000 paired (Sentence, 536D Real CLIP Perceptual State) training exposures."""
        dataset = []
        domain_keys = list(self.domains.keys())
        
        while len(dataset) < total_count:
            d_key = random.choice(domain_keys)
            d = self.domains[d_key]
            sent = random.choice(d["sentences"])
            
            # 1. Real 512D CLIP Visual Vector
            v_vec = self.vis_encoder.encode_visual_prompt(d["clip_prompt"])
            
            # 2. Deterministic 16D Physics Vector
            p_spec = GROUNDED_PHYSICAL_ARCHETYPES[d["physics_key"]]
            p_vec = self.phys_engine.calculate_physical_state(
                temp_k=p_spec["temp_k"],
                mass_kg=p_spec["mass_kg"],
                radius_m=p_spec["radius_m"],
                density_g_cm3=p_spec["density_g_cm3"],
                velocity_m_s=p_spec["velocity_m_s"],
                pressure_pa=p_spec["pressure_pa"],
                matter_phase=p_spec["matter_phase"]
            )
            
            # 3. Real 4D Emotion Vector
            e_spec = d["emotion"]
            e_vec = self.emo_encoder.encode_somatic_state(
                valence=e_spec["valence"],
                arousal=e_spec["arousal"],
                safety=e_spec["safety"],
                social_warmth=e_spec["social_warmth"]
            )
            
            # 4. Real 4D Temporal Vector
            t_spec = d["temporal"]
            t_vec = self.temp_encoder.encode_temporal_dynamics(
                frequency_hz=t_spec["frequency_hz"],
                tempo=t_spec["tempo"],
                periodicity=t_spec["periodicity"],
                persistence=t_spec["persistence"]
            )
            
            state = UnifiedPerceptualState(
                visual_512=v_vec,
                physics_16=p_vec,
                emotion_4=e_vec,
                temporal_4=t_vec
            )
            dataset.append((sent, state))
            
        random.shuffle(dataset)
        return dataset


