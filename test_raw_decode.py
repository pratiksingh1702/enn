import sys
import numpy as np
from fella.fella_brain import FellaBrain
from fella.core_substrate import FellaNeuron

def test_raw_decode():
    print("Loading FELLA Production Brain...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    print("\n[INJECTING BAT]")
    bat_vec = brain.lang.encode_continuous_wave("bat")
    blind_vec = brain.lang.encode_continuous_wave("blind")
    echo_vec = brain.lang.encode_continuous_wave("echolocate")
    
    bat_id = 999000
    blind_id = 999001
    echo_id = 999002
    
    brain.substrate.neurons[bat_id] = FellaNeuron(
        neuron_id=bat_id, y=np.array([0,0]),
        text="bat", tier_z=3, x=bat_vec,
        syntax_valence=[0.9, 0.1, 0.0, 0.0]
    )
    brain.substrate.neurons[blind_id] = FellaNeuron(
        neuron_id=blind_id, y=np.array([0,0]),
        text="blind", tier_z=1, x=blind_vec,
        syntax_valence=[0.1, 0.1, 0.9, 0.0]
    )
    brain.substrate.neurons[echo_id] = FellaNeuron(
        neuron_id=echo_id, y=np.array([0,0]),
        text="echolocate", tier_z=3, x=echo_vec,
        syntax_valence=[0.1, 0.9, 0.0, 0.0]
    )
    
    brain.substrate.neurons[bat_id].synapses[blind_id] = 10.0
    brain.substrate.neurons[bat_id].synapses[echo_id] = 2.0
    
    print("\n[RUNNING RAW TRAJECTORY]")
    # Run the raw decoder 5 times to see the Boltzmann distribution at work
    for i in range(5):
        path = brain.lang.decode_raw_synaptic_trajectory(bat_id, max_length=5)
        path_words = [brain.substrate.neurons[nid].text for nid in path]
        print(f"Run {i+1}: {path_words}")
        
    print("\n[RUNNING SUN]")
    sun_nodes = [nid for nid, n in brain.substrate.neurons.items() if n.text.lower() == 'sun']
    if sun_nodes:
        for i in range(5):
            path = brain.lang.decode_raw_synaptic_trajectory(sun_nodes[0], max_length=5)
            path_words = [brain.substrate.neurons[nid].text for nid in path]
            print(f"Sun Run {i+1}: {path_words}")
            
if __name__ == '__main__':
    test_raw_decode()
