import re

file_path = r'c:\Users\Dell\Downloads\enn\fella\language_grounding.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add the import
if 'from fella.true_physics_engine import TruePhysicsEngine' not in content:
    content = content.replace(
        'import numpy as np\n',
        'import numpy as np\nfrom fella.true_physics_engine import TruePhysicsEngine\n'
    )

# 2. Replace the scoring logic and sorting with the TruePhysicsEngine logic
old_logic = """                # Apply the final thermodynamic equation
                score = (float(conductance) ** 1.8) * flow_bonus * cluster_bonus * tier_boost * cond_boost * wave_boost * inhibition * gravity_penalty
                candidates.append((target_id, score, float(conductance)))
                
            if not candidates:
                # Phase 8: Quantum Semantic Bridging (Overcoming Graph Fragmentation)
                # If physical electrical paths are severed or missing, we do NOT default to uncertainty.
                # Instead, we use the `momentum_wave` (the true geometric meaning of the current thought)
                # to instantly jump across the brain to the closest semantic concept in 512D space.
                best_quantum_jump = None
                best_cosine = -1.0
                m_norm = np.linalg.norm(momentum_wave)
                
                if m_norm > 0:
                    for n_id, n in self.substrate.neurons.items():
                        if n_id in visited or n.tier_z == 0:
                            continue
                        t_norm = np.linalg.norm(n.x)
                        if t_norm > 0:
                            cosine = float(np.dot(momentum_wave, n.x) / (m_norm * t_norm))
                            # Enforce a strict semantic threshold so she doesn't jump to random noise
                            if cosine > 0.65 and cosine > best_cosine:
                                best_cosine = cosine
                                best_quantum_jump = n_id
                                
                if best_quantum_jump is not None:
                    # We found a pure semantic match! Force the jump.
                    candidates.append((best_quantum_jump, 999.0, 1.0))
                else:
                    break
                
            candidates.sort(key=lambda item: item[1], reverse=True)
            next_id, _, w_trans = candidates[0]"""

new_logic = """                # TRUE PHYSICS: Hamiltonian Potential Well
                # All bonuses (syntax, clustering, query attraction) are treated as potential wells.
                # The deeper the well (higher bonus), the lower the energetic cost of the state.
                potential_well = 1.0 / (flow_bonus * cluster_bonus * tier_boost * cond_boost * wave_boost * inhibition * gravity_penalty + 1e-9)
                candidates.append((target_id, float(conductance), target_n.x, potential_well))
                
            physics = TruePhysicsEngine(temperature=0.5)  # Simulated Annealing T
            next_id = None
            w_trans = 1.0
            
            if candidates:
                # Phase 1: True Thermodynamics (Boltzmann Distribution over Hamiltonian)
                cand_ids = [c[0] for c in candidates]
                conductances = [c[1] for c in candidates]
                vectors = np.array([c[2] for c in candidates])
                wells = np.array([c[3] for c in candidates])
                
                energies = []
                momentum_norm = momentum_wave / (np.linalg.norm(momentum_wave) + 1e-9)
                for i, c in enumerate(conductances):
                    resistance = 1.0 / (c + 1e-9)
                    v_norm = vectors[i] / (np.linalg.norm(vectors[i]) + 1e-9)
                    frustration = 1.0 - np.dot(momentum_norm, v_norm)
                    # H = Resistance + Semantic Frustration + Syntax Potential
                    H = resistance + (2.5 * frustration) + wells[i]
                    energies.append(H)
                
                energies = np.array(energies)
                boltzmann = np.exp(-energies / physics.temperature)
                probs = boltzmann / np.sum(boltzmann)
                
                next_id = np.random.choice(cand_ids, p=probs)
                # Find original conductance for dissipation
                for c in candidates:
                    if c[0] == next_id:
                        w_trans = c[1]
                        break
            else:
                # Phase 2: Quantum Structural Tunneling (Schrödinger Graph Laplacian)
                # We extract the local active subgraph to run the Unitary Evolution
                subgraph_nodes = list(self.substrate.neurons.keys())[:150] # Fast subset
                if curr_id not in subgraph_nodes:
                    subgraph_nodes.append(curr_id)
                
                N = len(subgraph_nodes)
                adj = np.zeros((N, N))
                node_to_idx = {nid: i for i, nid in enumerate(subgraph_nodes)}
                
                for i, nid in enumerate(subgraph_nodes):
                    for tgt, w in self.substrate.neurons[nid].synapses.items():
                        if tgt in node_to_idx:
                            adj[i, node_to_idx[tgt]] = float(w)
                            
                tunnel_res = physics.quantum_structural_tunneling(subgraph_nodes, adj, node_to_idx[curr_id], time_t=1.0)
                if tunnel_res is not None and tunnel_res not in visited:
                    next_id = tunnel_res
                    w_trans = 1.0 # Quantum tunneling uses zero local energy loss
                else:
                    break
                    
            if next_id is None:
                break"""

content = content.replace(old_logic, new_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Language Grounding Patched with True Physics!")
