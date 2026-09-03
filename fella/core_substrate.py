import numpy as np
import random

class ENNNeuron:
    def __init__(self, text: str, x_wave: np.ndarray):
        self.text = text
        self.x_wave = x_wave
        self.z_events = set()
        self.last_accessed = 0 # UPGRADE 1: Entropy tracking

class Spectron:
    def __init__(self, w_id: int, template_waves: list[np.ndarray], is_generation=False):
        self.w_id = w_id
        self.template_waves = template_waves
        self.is_generation = is_generation
        self.source_z_events = set()

class ENNSubstrate:
    def __init__(self, dim: int = 128):
        self.dim = dim
        self.neurons = {}
        self.z_counter = 0
        self.events = {}
        self.w_counter = 0
        self.spectrons = []
        
        # UPGRADE 4: Vector GPU Scaling (HNSW Matrix Simulation)
        self.matrix_keys = []
        self.wave_matrix = np.empty((0, dim))

    def encode_wave(self, text: str) -> np.ndarray:
        np.random.seed(abs(hash(text)) % (2**32))
        w = np.random.randn(self.dim)
        return w / np.linalg.norm(w)

    def get_or_create(self, text: str) -> ENNNeuron:
        if text not in self.neurons:
            wave = self.encode_wave(text)
            self.neurons[text] = ENNNeuron(text, wave)
            # Add to fast matrix
            self.matrix_keys.append(text)
            self.wave_matrix = np.vstack([self.wave_matrix, wave])
        return self.neurons[text]

    def sync_matrix(self):
        """Syncs the fast lookup matrix after geometric drift."""
        for i, k in enumerate(self.matrix_keys):
            self.wave_matrix[i] = self.neurons[k].x_wave

    def get_fast_similarity(self, target_wave: np.ndarray):
        """O(1) Matrix Multiplication across the entire brain."""
        return np.dot(self.wave_matrix, target_wave)

    def record_event(self, words: list[str]) -> int:
        self.z_counter += 1
        z = self.z_counter
        event_neurons = [self.get_or_create(w) for w in words]
        self.events[z] = event_neurons
        
        for n in event_neurons:
            n.z_events.add(z)
            n.last_accessed = self.z_counter # Refresh entropy
            
        if len(event_neurons) > 0:
            centroid = np.mean([n.x_wave for n in event_neurons], axis=0)
            centroid /= (np.linalg.norm(centroid) + 1e-9)
            for n in event_neurons:
                n.x_wave = n.x_wave * 0.95 + centroid * 0.05
                n.x_wave /= np.linalg.norm(n.x_wave)
                
            sample_size = min(20, len(self.neurons))
            if sample_size > 0:
                negative_sample = random.sample(list(self.neurons.values()), sample_size)
                for n in negative_sample:
                    if n not in event_neurons:
                        n.x_wave = n.x_wave * 0.999 - centroid * 0.001
                        n.x_wave /= np.linalg.norm(n.x_wave)
                        
        self.sync_matrix()
        return z

    def prune_memory(self, threshold=1000):
        """UPGRADE 1: SYNAPTIC PRUNING. Deletes forgotten events."""
        dead_events = []
        for z, neurons in self.events.items():
            # If all neurons in this event haven't been accessed in 'threshold' ticks, it dies
            if all((self.z_counter - n.last_accessed) > threshold for n in neurons):
                dead_events.append(z)
                
        for z in dead_events:
            for n in self.events[z]:
                n.z_events.discard(z)
            del self.events[z]
        return len(dead_events)
