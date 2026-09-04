# Pure Neuromorphic Mental Simulator (Prefrontal Simulation & Inverse Abduction)
import numpy as np

class MentalSimulator:
    """
    Prefrontal Cortex Cognitive Simulation Engine:
    - Forward Causal Rollout: Simulates physical trajectories in 256D space across Causal Cortex (T-matrix).
    - Inverse Causal Abduction: Searches backward from goal state G using transposed conductance T^T.
    - Counterfactual Evaluation: Modulates initial boundary states (e.g. soft cushion vs rigid floor).
    - Homeostatic Metacognition: Monitors entropy to ensure thermodynamic consistency.
    """
    def __init__(self, brain, causal_cortex, seq_matrix, key_to_idx):
        self.brain = brain
        self.causal = causal_cortex
        self.seq_T = seq_matrix
        self.key_to_idx = key_to_idx
        self.idx_to_key = {i: k for k, i in key_to_idx.items()}
        self.dim = brain.dim
        self.N = len(brain.matrix_keys)

        # Precompute row-normalized forward and backward causal transition matrices
        row_sums = self.causal.T_matrix[:self.N, :self.N].sum(axis=1, keepdims=True)
        self.forward_T = np.divide(self.causal.T_matrix[:self.N, :self.N], row_sums, 
                                   out=np.zeros((self.N, self.N), dtype=np.float32), where=row_sums != 0)
        
        # Transposed backward causal matrix for inverse problem solving (Effect -> Cause)
        T_trans = self.causal.T_matrix[:self.N, :self.N].T
        col_sums = T_trans.sum(axis=1, keepdims=True)
        self.backward_T = np.divide(T_trans, col_sums, 
                                    out=np.zeros((self.N, self.N), dtype=np.float32), where=col_sums != 0)

        # Scale-free hub penalty to filter grammatical connector hubs during inverse abduction
        in_deg = self.seq_T.sum(axis=0)[:self.N]
        self.hub_penalty = 1.0 / (1.0 + np.log(1.0 + in_deg / 35.0))

        # Sequential syntax matrix for speech emission
        seq_sums = self.seq_T.sum(axis=1, keepdims=True)
        self.safe_seq_T = np.divide(self.seq_T, seq_sums, 
                                    out=np.zeros_like(self.seq_T), where=seq_sums != 0)

    def forward_rollout(self, initial_indices: list, steps: int = 6, counterfactual_damps: dict = None) -> list:
        """
        Runs forward dynamical mental simulation in 256D continuous vector manifold.
        Simulates: State(t+1) = T * State(t) + Wave_Resonance
        """
        if not initial_indices:
            return []

        state = np.zeros(self.N, dtype=np.float32)
        for idx in initial_indices:
            if idx < self.N:
                state[idx] = 1.0 / len(initial_indices)

        trajectory_indices = list(initial_indices)
        visited = set(initial_indices)

        for _ in range(steps):
            # Dynamic time propagation through Causal Cortex
            state = np.dot(state, self.forward_T)

            # Apply counterfactual physical modulations if present (e.g. damping rigid impact)
            if counterfactual_damps:
                for damp_idx, factor in counterfactual_damps.items():
                    if damp_idx < self.N:
                        state[damp_idx] *= factor

            if np.all(state == 0):
                break

            active_top = np.argsort(state)[::-1][:10]
            if len(active_top) == 0 or state[active_top[0]] < 1e-4:
                break

            # Select next emergent physical state
            for next_idx in active_top:
                if next_idx not in visited:
                    visited.add(next_idx)
                    trajectory_indices.append(next_idx)
                    break

        return [self.idx_to_key[i] for i in trajectory_indices if i in self.idx_to_key]

    def inverse_abduction(self, goal_concept: str, max_steps: int = 4) -> list:
        """
        High-IQ Problem Solving (Goal-Driven Abduction):
        Searches backwards from goal state G using transposed causal matrix T^T.
        Deduces what prerequisite actions or causal interventions lead to G.
        """
        if goal_concept not in self.key_to_idx:
            return []

        g_idx = self.key_to_idx[goal_concept]
        state = np.zeros(self.N, dtype=np.float32)
        state[g_idx] = 1.0

        causal_prereqs = [goal_concept]
        visited = {g_idx}

        for _ in range(max_steps):
            # Backtrack causes: state(t-1) = state(t) * T^T
            state = np.dot(state, self.backward_T)
            if np.all(state == 0):
                break

            # Saliency-weighted causal backtracking (filters universal connector hubs)
            salience = state * self.hub_penalty
            top_causes = np.argsort(salience)[::-1][:10]
            best_cause = None
            for c_idx in top_causes:
                if c_idx not in visited and self.idx_to_key[c_idx].isalpha():
                    best_cause = c_idx
                    break

            if best_cause is None or salience[best_cause] < 1e-5:
                break

            visited.add(best_cause)
            causal_prereqs.append(self.idx_to_key[best_cause])

        # Reverse so sequence flows Cause -> Effect -> Goal
        return causal_prereqs[::-1]

    def evaluate_entropy(self, concept_indices: list) -> float:
        """Homeostatic verification: Computes Shannon entropy of the active state distribution."""
        if not concept_indices:
            return 0.0
        vecs = [self.brain.neurons[self.idx_to_key[i]].x_wave for i in concept_indices if i in self.idx_to_key]
        if not vecs:
            return 0.0
        # Gram matrix of wave overlaps
        gram = np.dot(vecs, np.transpose(vecs))
        norm_gram = gram / (np.trace(gram) + 1e-9)
        eigenvals = np.linalg.eigvalsh(norm_gram)
        eigenvals = eigenvals[eigenvals > 1e-6]
        return -float(np.sum(eigenvals * np.log(eigenvals)))
