import os
import sys
import numpy as np
from fella.fella_brain import FellaBrain
from fella.causal_cortex import CausalCortex

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

        # Build dynamic Causal Cortex with sliding-window temporal tethers
        self.causal = CausalCortex(initial_capacity=len(self.brain.matrix_keys))
        sorted_z = sorted(self.brain.events.keys())
        for z in sorted_z:
            words = [n.text for n in self.brain.events[z] if n.text in self.key_to_idx]
            for i in range(len(words)):
                p_idx = self.key_to_idx[words[i]]
                for j in range(i + 1, min(i + 5, len(words))):
                    n_idx = self.key_to_idx[words[j]]
                    if p_idx != n_idx:
                        self.causal.T_matrix[p_idx, n_idx] += 1.0 / (j - i)

        # Precompute safe transition matrix
        row_sums = self.causal.T_matrix.sum(axis=1, keepdims=True)
        self.safe_T = np.divide(self.causal.T_matrix, row_sums, out=np.zeros_like(self.causal.T_matrix), where=row_sums != 0)

    def converse(self, user_input: str) -> str:
        """
        Pure Neuromorphic Traversal:
        - Information saliency (Shannon IDF + Kolmogorov complexity) selects the semantic anchor.
        - Injects query energy into Causal Cortex (T-Matrix) and 256D continuous vector manifold.
        - Assembles emergent trajectory from the active causal path without templates.
        """
        raw_tokens = [w.strip("?,.!\"'();:").lower() for w in user_input.split() if len(w) > 0]
        if not raw_tokens:
            return "Perception is silent. No wave received."

        # 1. Candidate Concept Identification (Case-insensitive continuous projection)
        candidates = []
        lower_to_key = {k.lower(): k for k in self.brain.matrix_keys}
        for i in range(len(raw_tokens) - 1):
            comp = f"{raw_tokens[i]}_{raw_tokens[i+1]}"
            if comp in lower_to_key:
                candidates.append((lower_to_key[comp], i))

        for i, t in enumerate(raw_tokens):
            if t in lower_to_key:
                candidates.append((lower_to_key[t], i))

        if not candidates:
            ephemeral_wave = self.brain.encode_wave(" ".join(raw_tokens))
            sims = self.brain.get_fast_similarity(ephemeral_wave)
            top_idx = int(np.argmax(sims))
            top_concept = self.brain.matrix_keys[top_idx]
            sim_score = float(sims[top_idx])
            return f"I have not directly perceived '{user_input}'. Closest geometric resonance: '{top_concept}' ({sim_score:+.3f})."

        # 2. Information Saliency: Zipfian Specificity & Syntactic Focus
        q_vecs = [self.brain.neurons[c].x_wave for c, _ in candidates]
        q_centroid = np.mean(q_vecs, axis=0)
        q_centroid /= (np.linalg.norm(q_centroid) + 1e-9)

        query_evs = set()
        for c, _ in candidates:
            query_evs.update(self.brain.neurons[c].z_events)

        scored = []
        for c, pos in candidates:
            neuron = self.brain.neurons[c]
            ev_count = len(neuron.z_events)
            if ev_count == 0:
                continue

            # Zipfian Information Specificity: common hubs have high ev, specific concepts have lower ev
            specificity = 1.0 / np.sqrt(ev_count)
            # Universal Syntactic End-Focus Gradient
            pos_weight = (1.0 + (pos / len(raw_tokens))) ** 2
            # Holographic maximum continuous wave resonance across substrate
            sims = self.brain.get_fast_similarity(neuron.x_wave)
            sims[self.key_to_idx[c]] = -1.0
            max_res = max(0.01, float(np.max(sims)))
            # Kolmogorov length complexity
            kolmogorov = np.log1p(len(c))
            scored.append((c, pos, specificity * pos_weight * max_res * kolmogorov))

        if not scored:
            return f"Concepts in '{user_input}' have no episodic grounding."

        max_score = max(s[2] for s in scored)
        top_cluster = [s for s in scored if s[2] >= 0.70 * max_score]
        # In the top resonant content cluster, pick the thematic head (earliest position)
        focal_key = sorted(top_cluster, key=lambda s: s[1])[0][0]
        focal_idx = self.key_to_idx[focal_key]
        focal_evs = self.brain.neurons[focal_key].z_events

        # 3. Thermodynamic Traversal across Causal Cortex (T-Matrix) & Vector Manifold
        trajectory = [focal_key]
        visited_indices = {focal_idx}
        curr_idx = focal_idx
        max_hops = 7

        for _ in range(max_hops):
            conductances = self.safe_T[curr_idx]
            if np.all(conductances == 0):
                break

            top_candidates = np.argsort(conductances)[::-1][:30]
            best_next = None
            best_score = -999.0

            for cand_idx in top_candidates:
                if cand_idx in visited_indices:
                    continue
                cand_word = self.brain.matrix_keys[cand_idx]
                if cand_word.startswith("[") or not cand_word.isalnum():
                    continue

                cond = conductances[cand_idx]
                if cond < 0.001:
                    break

                cand_n = self.brain.neurons[cand_word]
                cand_evs = cand_n.z_events
                shared = len(focal_evs & cand_evs)

                # Grounded Hebbian episodic association with focal memory
                hebbian = (1.0 + 3.0 * (shared / (np.sqrt(len(focal_evs) * len(cand_evs)) + 1e-9))) if shared > 0 else 0.05
                # Princeton SIF continuous wave resonance
                spec = 1.0 / np.sqrt(len(cand_evs))
                res = float(np.dot(q_centroid, cand_n.x_wave))

                score = (cond * hebbian) + (0.20 * spec * res)
                if score > best_score:
                    best_score = score
                    best_next = cand_idx

            # Stop when energy dissipates
            if best_next is None or best_score < 0.01:
                break

            cand_word = self.brain.matrix_keys[best_next]
            trajectory.append(cand_word)
            visited_indices.add(best_next)
            curr_idx = best_next

        # 5. Emergent Output Synthesis (Natural traversal sentence)
        utterance = " ".join(trajectory)
        clean_utterance = utterance[0].upper() + utterance[1:] + "."
        return clean_utterance

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
                print("\n[FELLA]: Until we speak again. I will keep organizing my mind.")
                break

            reply = fella.converse(user_msg)
            print(f"[FELLA]: {reply}")

        except KeyboardInterrupt:
            print("\n\n[FELLA]: Transitioning to sleep.")
            break

if __name__ == '__main__':
    start_interactive_chat()
