import numpy as np

class CausalCortex:
    def __init__(self, initial_capacity=2000):
        """
        Phase 6: The Temporal Causal Cortex (Deep Reasoning).
        Tracks the asymmetric flow of time and causality. 
        Unlike spatial gravity (where A and B share geometry), 
        Causal Gravity is directional: A causes B (A -> B).
        
        Dynamically expands its T_matrix so it can run continuously for hours or days.
        """
        self.capacity = initial_capacity
        # T_matrix[i, j] represents the gravitational pull from Concept i forward in time to Concept j
        self.T_matrix = np.zeros((self.capacity, self.capacity), dtype=np.float32)
        
        # Short-term memory buffer to track what just happened (for temporal binding)
        self.active_concepts = []

    def _ensure_capacity(self, max_needed_idx: int):
        """Dynamically expands the T_matrix capacity when new concepts emerge."""
        if max_needed_idx >= self.capacity:
            new_capacity = max(max_needed_idx + 1000, int(self.capacity * 1.5))
            pad_rows = new_capacity - self.T_matrix.shape[0]
            pad_cols = new_capacity - self.T_matrix.shape[1]
            self.T_matrix = np.pad(self.T_matrix, ((0, pad_rows), (0, pad_cols)), mode='constant')
            self.capacity = new_capacity

    def bind_time(self, new_concept_indices: list):
        """
        Takes the indices of concepts that were just activated and binds them 
        to the concepts that were active a moment ago (Cause -> Effect).
        """
        if not new_concept_indices:
            return

        # Ensure matrix has room for both past and present concept indices
        all_indices = self.active_concepts + new_concept_indices
        if all_indices:
            self._ensure_capacity(max(all_indices))

        if not self.active_concepts:
            self.active_concepts = new_concept_indices
            return
            
        # Draw Temporal Vectors (Causal Tethers) from past concepts to present concepts
        for past_idx in self.active_concepts:
            for present_idx in new_concept_indices:
                if past_idx != present_idx:
                    # Strengthen the forward causal tether (Hebbian thermodynamic flow)
                    self.T_matrix[past_idx, present_idx] += 1.0
                    
        # Update short-term memory (Time moves forward)
        self.active_concepts = new_concept_indices

    def simulate_future(self, start_indices: list, steps: int = 1) -> np.ndarray:
        """
        Multi-step deep reasoning. 
        Injects thermodynamic energy into the start concepts and propagates it 
        forward through time across the T_matrix to predict the future state.
        """
        if start_indices:
            self._ensure_capacity(max(start_indices))

        # Initial energy state
        state = np.zeros(self.capacity, dtype=np.float32)
        for idx in start_indices:
            if idx < self.capacity:
                state[idx] = 1.0
                
        # Normalize T_matrix rows to prevent infinite energy explosions (Conservation of Energy)
        row_sums = self.T_matrix.sum(axis=1, keepdims=True)
        safe_T = np.divide(self.T_matrix, row_sums, out=np.zeros_like(self.T_matrix), where=row_sums!=0)
        
        # Propagate the energy wave forward through time
        for _ in range(steps):
            state = np.dot(state, safe_T)
            
        return state
