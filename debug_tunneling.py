import numpy as np
import scipy.linalg
from fella.fella_brain import FellaBrain

def debug_tunneling():
    print("Loading Brain...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    # Check if 'dispersal' exists and what its properties are
    dispersal_node = None
    for n in brain.substrate.neurons.values():
        if 'dispersal' in n.text.lower():
            dispersal_node = n
            break
            
    if dispersal_node:
        print(f"\n[DEBUG] Found 'dispersal' node! Degree: {len(dispersal_node.synapses)}")
    else:
        print("\n[DEBUG] 'dispersal' node not found in graph.")

    # Recreate the exact tunneling condition
    # Using the first 150 nodes as we did in the patch
    subgraph_nodes = list(brain.substrate.neurons.keys())[:150]
    
    # Let's pick a random start node from these 150 to simulate the jump
    start_idx = 10  
    
    print(f"\n[DEBUG] Running Quantum Tunneling on 150-node subgraph...")
    print(f"Start Node: {brain.substrate.neurons[subgraph_nodes[start_idx]].text}")
    
    N = len(subgraph_nodes)
    adj = np.zeros((N, N))
    node_to_idx = {nid: i for i, nid in enumerate(subgraph_nodes)}
    
    for i, nid in enumerate(subgraph_nodes):
        for tgt, w in brain.substrate.neurons[nid].synapses.items():
            if tgt in node_to_idx:
                adj[i, node_to_idx[tgt]] = float(w)
                
    degrees = np.sum(adj, axis=1)
    D = np.diag(degrees)
    L = D - adj
    
    # Check Laplacian properties
    print(f"Laplacian Max Value: {np.max(L)}, Min Value: {np.min(L)}")
    
    U = scipy.linalg.expm(-1j * L * 1.0)
    
    psi_0 = np.zeros(N, dtype=np.complex128)
    psi_0[start_idx] = 1.0
    
    psi_t = np.dot(U, psi_0)
    probabilities = np.abs(psi_t)**2
    
    # Zero out connected nodes
    for idx in range(N):
        if adj[start_idx, idx] > 0 or idx == start_idx:
            probabilities[idx] = 0.0
            
    # Print Top 5
    print("\n[TOP 5 TUNNELING CANDIDATES]")
    top_5_indices = np.argsort(probabilities)[-5:][::-1]
    
    for rank, idx in enumerate(top_5_indices):
        prob = probabilities[idx]
        text = brain.substrate.neurons[subgraph_nodes[idx]].text
        print(f"#{rank+1} | Node: '{text}' | Probability: {prob:.6f}")

if __name__ == '__main__':
    debug_tunneling()
