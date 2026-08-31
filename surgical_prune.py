from fella.fella_brain import FellaBrain
from collections import defaultdict

def run():
    print("Loading brain for surgical topological pruning based on IN-DEGREE...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    # Calculate in-degree (how many words point TO this word)
    in_degree = defaultdict(int)
    for n_id, n in brain.substrate.neurons.items():
        for peer_id in n.synapses.keys():
            in_degree[peer_id] += 1
            
    stop_words_identified = 0
    synapses_destroyed = 0
    
    # Identify meaningless gravity wells
    dead_nodes = set()
    for n_id, n in brain.substrate.neurons.items():
        degree = in_degree[n_id]
        if degree > 30:
            dead_nodes.add(n_id)
            stop_words_identified += 1
            print(f"Gravity Well Identified: '{n.text}' (In-Degree: {degree})")
            
    print(f"\nIdentified {stop_words_identified} massive gravity wells.")
    print("Initiating physical pruning...")
    
    for n_id, n in brain.substrate.neurons.items():
        dead_peers = [peer for peer in n.synapses if peer in dead_nodes]
        for peer in dead_peers:
            del n.synapses[peer]
            synapses_destroyed += 1
            
    print(f"Surgically obliterated {synapses_destroyed} meaningless synapses.")
    
    brain.save_state('fella_checkpoint.json')
    print("Perfected brain structure saved.")

if __name__ == '__main__':
    run()
