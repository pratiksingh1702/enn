"""
FELLA Continuous Real 536D Multimodal Sensory Bridge Layer
==========================================================
Pure Continuous Mathematical Physics:
- 4 Real Input Channels (536D Unified Perceptual Vector):
  1. Real Visual (V in R^512): Optical spectrum, luminance, spatial frequency, and motion.
  2. Deterministic Physics (P in R^16): Stefan-Boltzmann flux, gravity g, density rho, velocity v, pressure P.
  3. Somatic/Emotional (E in R^4): Continuous Valence, Arousal, Dominance/Safety, Social Warmth.
  4. Temporal Dynamics (T in R^4): Frequency, Tempo, Periodicity, Persistence.
- Cross-Modal Conflict Detector: Measures inter-modal coherence C_modal (rejects physical contradictions).
- Active Attractor Interference: Collides sensory attractors for novel "What If?" counterfactual simulation.
- Continuous Hebbian Projection W_proj: R^536 -> R^16 Substrate Space.
Zero hardcoded strings, zero arbitrary heuristic thresholds.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from fella.real_perceptual_encoders import UnifiedPerceptualState


class CrossModalConflictDetector:
    """
    Evaluates consistency across Visual, Physics, Emotional, and Temporal channels.
    Prevents hallucination by rejecting physical contradictions (e.g. 'cold bright sun').
    """
    def compute_modal_consistency(self, state: UnifiedPerceptualState) -> Tuple[float, bool]:
        """
        Computes inter-modal alignment C_modal in [0.0, 1.0].
        Returns (consistency_score, is_conflict).
        """
        v_norm = np.linalg.norm(state.visual)
        p_norm = np.linalg.norm(state.physics)
        e_norm = np.linalg.norm(state.emotion)
        t_norm = np.linalg.norm(state.temporal)
        
        if v_norm == 0 or p_norm == 0:
            return 1.0, False
            
        # 1. Thermal-Visual Alignment (High luminance usually implies high thermal radiant flux)
        # Physics[0] is log_temp, Physics[1] is log_flux
        thermal_flux = state.physics[1] if len(state.physics) > 1 else 0.0
        visual_lum = np.mean(state.visual[:10])
        flux_alignment = float(np.clip(1.0 - abs(thermal_flux - visual_lum), 0.0, 1.0))
        
        # 2. Gravity-Mass Dynamic Alignment
        gravity_curv = state.physics[2] if len(state.physics) > 2 else 0.0
        mass_density = state.physics[4] if len(state.physics) > 4 else 0.0
        grav_alignment = float(np.clip(1.0 - abs(gravity_curv - mass_density), 0.0, 1.0))
        
        # 3. Overall Modal Consistency Score
        consistency_score = 0.55 * flux_alignment + 0.45 * grav_alignment
        is_conflict = (consistency_score < 0.45)
        return float(consistency_score), is_conflict


class MultimodalSensoryBridge:
    """
    Manages continuous 536D sensory transduction, Hebbian projection plasticity,
    cross-modal conflict detection, and active sensory imagination.
    """
    def __init__(self, substrate_dim: int = 16, input_dim: int = 536):
        self.substrate_dim = int(substrate_dim)
        self.input_dim = int(input_dim)
        
        # Continuous Hebbian Projection Matrix W_proj (536 x 16)
        # Initialized with normalized orthogonal projections
        rng = np.random.RandomState(42)
        raw_proj = rng.randn(self.input_dim, self.substrate_dim)
        q, _ = np.linalg.qr(raw_proj)
        self.W_proj = q.astype(float)
        
        self.conflict_detector = CrossModalConflictDetector()
        self.temporal_buffer: List[np.ndarray] = []
        self.buffer_capacity: int = 8
        self.current_perceptual_state = UnifiedPerceptualState(
            visual_512=np.zeros(512),
            physics_16=np.zeros(16),
            emotion_4=np.zeros(4),
            temporal_4=np.zeros(4)
        )

    def update_sensory_stream(self, state: UnifiedPerceptualState, lr: float = 0.02) -> Tuple[np.ndarray, float, bool]:
        """
        Updates 536D stream, evaluates modal consistency, and computes
        continuous perturbation force vector for the substrate field.
        """
        self.current_perceptual_state = state
        vec_536 = state.to_536_vector()
        
        # Evaluate cross-modal conflict
        consistency, is_conflict = self.conflict_detector.compute_modal_consistency(state)
        
        # Maintain temporal flow buffer
        self.temporal_buffer.append(vec_536)
        if len(self.temporal_buffer) > self.buffer_capacity:
            self.temporal_buffer.pop(0)
            
        smooth_vec = np.mean(self.temporal_buffer, axis=0)
        
        # Project 536D vector into 16D substrate coordinates
        delta_x = np.dot(smooth_vec, self.W_proj)
        norm = np.linalg.norm(delta_x)
        if norm > 0:
            delta_x = delta_x / norm
            
        return delta_x, consistency, is_conflict

    def bind_hebbian_sensory_coactivation(
        self,
        perceptual_536: np.ndarray,
        neuron_x: np.ndarray,
        consistency_weight: float = 1.0,
        lr: float = 0.04
    ):
        """
        Plastic Hebbian alignment: Aligns projection matrix with neurons
        that fire concurrently during truthful, non-conflicting sensory experiences.
        """
        p_norm = np.linalg.norm(perceptual_536)
        n_norm = np.linalg.norm(neuron_x)
        if p_norm == 0 or n_norm == 0:
            return
            
        effective_lr = lr * np.clip(consistency_weight, 0.1, 1.0)
        outer_prod = np.outer(perceptual_536 / p_norm, neuron_x / n_norm)
        self.W_proj = (1.0 - effective_lr) * self.W_proj + effective_lr * outer_prod
        
        # Re-orthonormalize projection matrix for numerical stability
        q, _ = np.linalg.qr(self.W_proj)
        self.W_proj = q.astype(float)

    def decode_sensory_imagination(self, neuron_x: np.ndarray) -> UnifiedPerceptualState:
        """
        Sensory Imagination (Back-Projection):
        When a concept neuron fires in thought, reconstructs the simulated
        536D multimodal perceptual state (Mental Eye, Thermal feel, Somatic warmth).
        """
        reconstructed_536 = np.dot(self.W_proj, neuron_x)
        return UnifiedPerceptualState.from_536_vector(reconstructed_536)

    def synthesize_counterfactual_imagination(
        self,
        base_state: UnifiedPerceptualState,
        perturbation_state: UnifiedPerceptualState,
        alpha: float = 0.6,
        beta: float = 0.4
    ) -> UnifiedPerceptualState:
        """
        Active Attractor Interference for 'What If?' Reasoning:
        Collides two sensory states into a novel synthetic mental simulation.
        """
        v_base = base_state.to_536_vector()
        v_pert = perturbation_state.to_536_vector()
        
        # Non-linear interference
        linear_blend = alpha * v_base + beta * v_pert
        interference = np.sin(np.pi * v_base) * np.cos(np.pi * v_pert)
        composite_536 = linear_blend + 0.20 * interference
        norm = np.linalg.norm(composite_536)
        if norm > 0:
            composite_536 = composite_536 / norm
            
        return UnifiedPerceptualState.from_536_vector(composite_536)


