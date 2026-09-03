import re

with open('fella/frontier_manifold.py', 'r') as f:
    text = f.read()
    
pattern = r'def _calculate_bond_fitness.*?return fitness'
replacement = '''def _calculate_bond_fitness(self, molecule: List[FellaNeuron], candidate: FellaNeuron, plan_vector: np.ndarray, original_plan: np.ndarray = None) -> float:
        """
        Calculates how well the candidate bonds to the active context wave AND how well it 
        resonates with the global plan vector. Also performs a Metacognitive Gist Check.
        """
        if not molecule:
            left_dent_dist = 0.0
            if candidate.left_context_clusters:
                actual_left_x = np.zeros_like(candidate.x)
                left_dent_dist = min(np.linalg.norm(c['mean'] - actual_left_x) for c in candidate.left_context_clusters)
            right_dent_dist = 0.0
        else:
            # Construct active context wave (Decaying memory of last 3 words)
            actual_left_x = np.zeros_like(candidate.x)
            weight = 1.0
            total_weight = 0.0
            for j in range(1, 4):
                idx = len(molecule) - j
                if idx >= 0:
                    damp = 1.0 / (max(1, len(molecule[idx].synapses)) ** 0.5)
                    actual_left_x += (molecule[idx].x * damp) * weight
                    total_weight += weight
                    weight *= 0.4
            if total_weight > 0:
                actual_left_x /= total_weight
                
            left_dent_dist = 1.0
            if candidate.left_context_clusters:
                left_dent_dist = min(np.linalg.norm(c['mean'] - actual_left_x) for c in candidate.left_context_clusters)
                
            right_dent_dist = 1.0
            left_word = molecule[-1]
            if left_word.right_context_clusters:
                right_dent_dist = min(np.linalg.norm(c['mean'] - candidate.x) for c in left_word.right_context_clusters)
            
        valence_bond = 1.0 / (1.0 + left_dent_dist + right_dent_dist)
        
        max_exp = max((n.exposure_count for n in self.brain.substrate.neurons.values()), default=1)
        is_catalyst = candidate.exposure_count > (max_exp * 0.20)
        
        if is_catalyst:
            semantic_resonance = 0.0
            fitness = valence_bond * 0.95 
        else:
            semantic_dist = np.linalg.norm(candidate.x - plan_vector)
            
            # Metacognitive Gist Check: Is the running sentence wave still pointing at the original plan?
            if original_plan is not None and len(molecule) > 0:
                running_wave = np.zeros_like(original_plan)
                for w in molecule:
                    running_wave += w.x
                running_wave += candidate.x
                r_norm = np.linalg.norm(running_wave)
                if r_norm > 0:
                    running_wave /= r_norm
                gist_alignment = np.dot(running_wave, original_plan)
                
                # If adding this word pulls the sentence backwards, heavily penalize
                if gist_alignment < 0.2:
                    semantic_dist += 2.0 # Massive penalty
                    
            semantic_resonance = 1.0 / (1.0 + semantic_dist)
            fitness = (0.7 * valence_bond) + (0.3 * semantic_resonance)
        
        return fitness'''

text = re.sub(pattern, replacement, text, flags=re.DOTALL)

text = text.replace('def crystallize_incremental(self, plan_vector: np.ndarray, max_length: int = 10, stop_threshold: float = 0.35) -> List[FellaNeuron]:', 
                    'def crystallize_incremental(self, plan_vector: np.ndarray, max_length: int = 10, stop_threshold: float = 0.35, original_plan: np.ndarray = None) -> List[FellaNeuron]:')

text = text.replace('fitness = penalty * self._calculate_bond_fitness(left_word, candidate, plan_vector)',
                    'fitness = penalty * self._calculate_bond_fitness(molecule, candidate, plan_vector, original_plan)')

text = text.replace('molecule = self.crystallize_incremental(plan_vector, max_length=max_length, stop_threshold=stop_threshold)',
                    'molecule = self.crystallize_incremental(plan_vector, max_length=max_length, stop_threshold=stop_threshold, original_plan=plan_vector)')

with open('fella/frontier_manifold.py', 'w') as f:
    f.write(text)
