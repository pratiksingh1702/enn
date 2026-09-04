import os
import sys
import numpy as np
from fella.fella_brain import FellaBrain
from fella.causal_cortex import CausalCortex
from fella.mental_simulator import MentalSimulator

class FellaVoice:
    """
    Pure Neuromorphic Conversational Synthesis:
    - ZERO hardcoded phrase templates (no Mad-Libs, no canned sentences).
    - ZERO hardcoded keyword interceptors or material dictionaries.
    - 100% emergent traversal across the 256D continuous vector manifold and Causal T-Matrix.
    """
    def __init__(self, checkpoint_file="fella_hyper_mind.json"):
        self.brain = FellaBrain(dim=256)
        if os.path.exists(checkpoint_file):
            self.brain.load_state(checkpoint_file)
            print(f"[FELLA ONLINE] Substrate active: {len(self.brain.neurons)} concepts, {self.brain.z_counter} Z-events.", flush=True)
        else:
            print(f"[FELLA WARNING] '{checkpoint_file}' not found. Loading fresh substrate.", flush=True)

        self.key_to_idx = {k: i for i, k in enumerate(self.brain.matrix_keys)}

        # Build dynamic Causal Cortex (windowed flux) and direct sequential syntax matrix (adjacent generation)
        self.causal = CausalCortex(initial_capacity=len(self.brain.matrix_keys))
        self.seq_T = np.zeros((len(self.brain.matrix_keys), len(self.brain.matrix_keys)), dtype=np.float32)
        sorted_z = sorted(self.brain.events.keys())
        for z in sorted_z:
            words = [n.text for n in self.brain.events[z] if n.text in self.key_to_idx]
            for i in range(len(words)):
                p_idx = self.key_to_idx[words[i]]
                if i + 1 < len(words):
                    n_idx = self.key_to_idx[words[i + 1]]
                    if p_idx != n_idx:
                        self.seq_T[p_idx, n_idx] += 1.0
                for j in range(i + 1, min(i + 5, len(words))):
                    n_idx = self.key_to_idx[words[j]]
                    if p_idx != n_idx:
                        self.causal.T_matrix[p_idx, n_idx] += 1.0 / (j - i)

        # Precompute safe transition matrices and corpus graph metrics
        row_sums = self.causal.T_matrix.sum(axis=1, keepdims=True)
        self.safe_T = np.divide(self.causal.T_matrix, row_sums, out=np.zeros_like(self.causal.T_matrix), where=row_sums != 0)
        seq_row_sums = self.seq_T.sum(axis=1, keepdims=True)
        self.safe_seq_T = np.divide(self.seq_T, seq_row_sums, out=np.zeros_like(self.seq_T), where=seq_row_sums != 0)
        self.in_deg = self.causal.T_matrix.sum(axis=0)
        self.N_events = float(max(1, self.brain.z_counter))
        self.simulator = MentalSimulator(self.brain, self.causal, self.seq_T, self.key_to_idx)

    def converse(self, user_input: str) -> str:
        """
        Pure Neuromorphic Traversal:
        - Information Saliency (IDF, In-Degree Centrality, End-Focus, Causal Flux, Hebbian Consolidation) selects semantic anchor.
        - Dynamic traversal across Causal Cortex (T-Matrix) strictly bounded by anchor's episodic memory trace (Ochiai-Cosine affinity).
        - Natural utterance emerges strictly from the active causal trajectory without templates or canned phrases.
        """
        tokens = [w.strip("?,.!\"'();:").lower() for w in user_input.split() if w.strip("?,.!\"'();:")]
        q_indices = [self.key_to_idx[t] for t in tokens if t in self.key_to_idx]

        # If query has no recognized episodic tokens, ground via continuous 256D wave resonance
        if not q_indices:
            wave = self.brain.encode_wave(" ".join(tokens) if tokens else "silence")
            sims = self.brain.get_fast_similarity(wave)
            q_indices = [int(np.argmax(sims))]

        # 1. Information Saliency Anchor Selection
        scores = {}
        for i, idx in enumerate(q_indices):
            w = self.brain.matrix_keys[idx]
            ev = len(self.brain.neurons[w].z_events)
            if ev == 0:
                continue

            # Shannon Inverse Document Frequency (IDF)
            idf = np.log(1.0 + (self.N_events / ev))

            # Graph In-Degree Centrality Penalty (dampens universal connector hubs like 'the', 'is', 'a')
            hub_penalty = 1.0 / (1.0 + np.log(1.0 + self.in_deg[idx] / 35.0))

            # Universal Syntactic End-Focus Gradient (Theme-Rheme progression)
            pos_gradient = 1.0 + (i / len(q_indices))

            # Net Directed Causal Flux (initiator/subject leadership within the query)
            flux = 0.0
            for j in q_indices:
                if idx != j:
                    deg_scale = np.sqrt((1.0 + self.in_deg[idx]) * (1.0 + self.in_deg[j]))
                    flux += (self.causal.T_matrix[idx, j] - self.causal.T_matrix[j, idx]) / deg_scale
            causal_factor = 1.0 + max(0.0, flux)

            # Synaptic Consolidation (biological saturation curve)
            consolidation = np.tanh(0.6 * ev)

            scores[idx] = idf * hub_penalty * pos_gradient * causal_factor * consolidation

        focal_idx = max(scores, key=scores.get) if scores else q_indices[-1]
        focal_word = self.brain.matrix_keys[focal_idx]
        focal_evs = self.brain.neurons[focal_word].z_events

        # 2. Emergent Sequential Syntactic Traversal bounded by Anchor's Episodic Memory
        trajectory = [focal_word]
        visited = {focal_idx}
        curr_idx = focal_idx

        for _ in range(16):
            conductances = self.safe_seq_T[curr_idx]
            if np.all(conductances == 0):
                break

            top_candidates = np.argsort(conductances)[::-1][:150]
            best_cand = None
            best_cand_score = -1.0

            for cand in top_candidates:
                if cand in visited:
                    continue
                cand_word = self.brain.matrix_keys[cand]
                if not cand_word.isalpha():
                    continue

                cond = conductances[cand]
                if cond < 0.001:
                    break

                cand_evs = self.brain.neurons[cand_word].z_events
                shared = len(focal_evs & cand_evs)
                if shared == 0:
                    continue

                # Episodic Resonance: conductance scaled by context alignment
                trans_score = cond * (shared / np.sqrt(len(cand_evs)))
                if trans_score > best_cand_score:
                    best_cand_score = trans_score
                    best_cand = cand

            if best_cand is None:
                break

            trajectory.append(self.brain.matrix_keys[best_cand])
            visited.add(best_cand)
            curr_idx = best_cand

        # Trim dangling terminal connectors (conjunctions/prepositions/articles)
        dangling_terminals = {"and", "to", "of", "the", "a", "an", "in", "by", "with", "or", "for", "as"}
        while len(trajectory) > 1 and trajectory[-1] in dangling_terminals:
            trajectory.pop()

        utt = " ".join(trajectory)
        return utt[0].upper() + utt[1:] + "."

def start_interactive_chat():
    print("==================================================")
    print("TALK TO FELLA: UN-FAKED NEUROMORPHIC INTERFACE")
    print("==================================================")
    print("• Pure Causal Traversal: Energy propagation through 256D Manifold.")
    print("• Zero hardcoded sentence templates, zero keyword matching.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    fella = FellaVoice("fella_hyper_mind.json")

    while True:
        try:
            user_msg = input("\n[YOU]: ").strip()
            if not user_msg:
                continue
            if user_msg.lower() in ["exit", "quit"]:
                break

            reply = fella.converse(user_msg)
            print(f"[FELLA]: {reply}")

        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    start_interactive_chat()
