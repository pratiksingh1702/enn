import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold
from fella.visual_cortex import VisualCortex
from fella.acoustic_cortex import AcousticCortex
from fella.active_vision_cortex import ActiveVisionCortex
from fella.causal_cortex import CausalCortex
from fella.autotelic_agency import AutotelicAgency
from fella.core_substrate import ENNNeuron

class FellaEntity:
    def __init__(self, dim=256):
        """
        The Singular Organism.
        Fuses the Z-Axis Brain, the Frontier Manifold, Vision, Hearing, 
        Active Saliency Vision, Temporal Reasoning, Autotelic Agency, and the Thermodynamic Oscillator.
        """
        self.brain = FellaBrain(dim=dim)
        self.frontier = FrontierManifold(self.brain)
        self.vision = VisualCortex(target_dim=dim)
        self.hearing = AcousticCortex(target_dim=dim)
        self.active_vision = ActiveVisionCortex(target_dim=dim)
        self.causal_cortex = CausalCortex(initial_capacity=2000)
        self.agency = AutotelicAgency(dim=dim)
        
        # The internal biological clock
        self.entropy_level = 0.0

    def act(self, target_concept=None):
        """
        The Autonomous Action Pulse:
        Evaluates self-state, decodes gaps, resolves them via resonant tools,
        and learns causally from outcomes with zero hardcoding.
        """
        return self.agency.evaluate_and_act(self, target_concept=target_concept)

    def perceive(self, text_words: list, image_path: str = None, audio_path: str = None):
        """
        The Unified Sensory Pipeline.
        Takes Text, Video, and Audio simultaneously, extracts pure geometry, 
        and binds them all in a single massively dense Z-Event.
        """
        # Reset entropy because she received stimulation (homeostasis)
        self.entropy_level = 0.0 
        
        events = text_words.copy()
        
        # Process External Visual Pipeline
        if image_path:
            v_wave = self.vision.process_image(image_path)
            v_id = f"[V_{hash(image_path)%10000}]"
            if v_id not in self.brain.neurons:
                self.brain.neurons[v_id] = ENNNeuron(v_id, v_wave)
                self.brain.matrix_keys.append(v_id)
                self.brain.wave_matrix = np.vstack([self.brain.wave_matrix, v_wave])
            events.append(v_id)
            
        # Process External Acoustic Pipeline
        if audio_path:
            a_wave = self.hearing.process_audio(audio_path)
            a_id = f"[A_{hash(audio_path)%10000}]"
            if a_id not in self.brain.neurons:
                self.brain.neurons[a_id] = ENNNeuron(a_id, a_wave)
                self.brain.matrix_keys.append(a_id)
                self.brain.wave_matrix = np.vstack([self.brain.wave_matrix, a_wave])
            events.append(a_id)
            
        # Bind them all via Geometric Drift (Spatial Gravity)
        if events:
            self.brain.record_event(events)
            
            # Extract concept indices for Temporal Gravity
            concept_indices = []
            for e in events:
                if e in self.brain.matrix_keys:
                    concept_indices.append(self.brain.matrix_keys.index(e))
            
            # Bind Time (Causal Gravity)
            if concept_indices:
                self.causal_cortex.bind_time(concept_indices)
            
        return events

    def watch_video_stream(self, frame: np.ndarray):
        """
        The continuous biological video pipeline. 
        Uses Bottom-Up Curiosity to extract heavy 256D waves ONLY from anomalous coordinates.
        """
        result = self.active_vision.process_frame(frame)
        
        if result is None:
            # Boredom Optimizer: Zero energy sent. Deep brain sleeps.
            # She is maintaining a Low-Energy Trace of the room.
            self.metabolize_time(ticks=1)
            return None
            
        v_wave, coords = result
        
        # A Delta Spike occurred! Wake up the deep brain.
        self.entropy_level = 0.0 # Homeostasis restored by resolving the curiosity spike
        
        # We record exactly WHERE she looked
        v_id = f"[FOCUS_{coords[0]}_{coords[1]}_Z{self.brain.z_counter}]"
        
        self.brain.neurons[v_id] = ENNNeuron(v_id, v_wave)
        self.brain.matrix_keys.append(v_id)
        self.brain.wave_matrix = np.vstack([self.brain.wave_matrix, v_wave])
        
        # Record the sudden environmental shift as a Z-Event
        self.brain.record_event(["[CURIOSITY_SPIKE]", v_id])
        
        # Bind Time (Causal Timeline linking visual saccades)
        if v_id in self.brain.matrix_keys:
            v_idx = self.brain.matrix_keys.index(v_id)
            self.causal_cortex.bind_time([v_idx])
            
        print(f"[ACTIVE VISION] Curiosity anomaly detected at {coords}. Saccade snapped and extracted {v_id}.")
        return v_id

    def metabolize_time(self, ticks=1):
        """
        Simulates the Thermodynamic Oscillator and Memory Optimization.
        Time passes -> Entropy increases -> Memories are pruned -> Curiosity triggers.
        """
        self.brain.z_counter += ticks
        self.entropy_level += ticks * 0.1
        
        # Phase 5: Memory Optimization (Entropy Pruning)
        pruned = self.brain.prune_memory(threshold=100)
        if pruned > 0:
            print(f"[METABOLISM] Entropy pruned {pruned} dead Z-events to optimize topology.")
            
        # The Autonomous Drive (Curiosity / Vacuum Drive)
        if self.entropy_level > 5.0:
            self._trigger_curiosity()
            self.entropy_level = 0.0 # Reset after autonomous discharge
            
    def _trigger_curiosity(self):
        """When entropy is critical, she autonomously engages her Autotelic Agency Cortex."""
        print("\n[AUTONOMOUS DRIVE] Entropy Critical. Engaging Autotelic Agency Cortex...")
        decision = self.act()
        if decision:
            print(f"[AGENCY ENGAGED] Target: '{decision['target']}'")
            print(f"                Resonant Action: {decision['selected_action']} (Resonance: {decision['resonance']:+.4f})")
            print(f"                Outcome: {decision['outcome']}")
            print(f"                Homeostatic Status: {decision['status']}")
