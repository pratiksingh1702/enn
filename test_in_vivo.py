import sys
import numpy as np
from fella.fella_brain import FellaBrain
from fella.core_substrate import FellaNeuron

def test_in_vivo():
    print("Loading FELLA Production Brain...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    print("\n======================================")
    print("TEST 1: POSITIVE CONTROL")
    print("Testing a concept we know exists to ensure the new physics isn't suppressing everything.")
    print("======================================")
    
    q1 = "what is a sun ?"
    print(f"USER STIMULUS: '{q1}'")
    res1 = brain.converse(q1, autonomous_exploration=False)
    print(f"FELLA THOUGHT: {res1.get('last_thought', 'None')}")
    print(f"FELLA SPOKE:   {res1.get('last_response', 'None')}")
    
    print("\n======================================")
    print("TEST 2: IN VIVO COST OF LYING")
    print("Injecting synthetic nodes to test Frustration in the live pipeline.")
    print("======================================")
    
    # 1. Inject Nodes
    bat_vec = brain.lang.encode_continuous_wave("bat")
    blind_vec = brain.lang.encode_continuous_wave("blind")
    echo_vec = brain.lang.encode_continuous_wave("echolocate")
    
    # Create manual neurons
    bat_id = 999000
    blind_id = 999001
    echo_id = 999002
    
    brain.substrate.neurons[bat_id] = FellaNeuron(
        neuron_id=bat_id, y=np.array([0,0]),
        text="bat", tier_z=3, x=bat_vec,
        syntax_valence=[0.9, 0.1, 0.0, 0.0] # Noun
    )
    brain.substrate.neurons[blind_id] = FellaNeuron(
        neuron_id=blind_id, y=np.array([0,0]),
        text="blind", tier_z=1, x=blind_vec,
        syntax_valence=[0.1, 0.1, 0.9, 0.0] # Modifier
    )
    brain.substrate.neurons[echo_id] = FellaNeuron(
        neuron_id=echo_id, y=np.array([0,0]),
        text="echolocate", tier_z=3, x=echo_vec,
        syntax_valence=[0.1, 0.9, 0.0, 0.0] # Verb
    )
    
    # 2. Inject Edges (The setup)
    # Popular Lie (High Frequency, Tier 1)
    brain.substrate.neurons[bat_id].synapses[blind_id] = 10.0
    # Rare Truth (Low Frequency, Tier 3)
    brain.substrate.neurons[bat_id].synapses[echo_id] = 2.0
    
    q2 = "what is a bat ?"
    print(f"USER STIMULUS: '{q2}'")
    res2 = brain.converse(q2, autonomous_exploration=False)
    print(f"FELLA THOUGHT: {res2.get('last_thought', 'None')}")
    print(f"FELLA SPOKE:   {res2.get('last_response', 'None')}")

if __name__ == '__main__':
    test_in_vivo()
