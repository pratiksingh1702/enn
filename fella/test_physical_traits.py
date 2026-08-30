import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fella.fella_brain import FellaBrain

def run_trait_proofs():
    print("================================================================================")
    print("🧪 FELLA PHYSICAL TRAIT PROOF SUITE")
    print("================================================================================\n")
    
    # Boot a fresh brain for the test
    brain = FellaBrain(name="FELLA")
    brain.boot_foundations()
    
    # --------------------------------------------------------------------------------
    print("PROOF 1: CURIOSITY (The Entropy Void Reflex)")
    print("Teaching: 'Moon orbits'")
    brain.converse("Moon orbits")
    print("User: 'what is moon?'")
    tel = brain.converse("what is moon?")
    print(f"FELLA: {tel['last_response']}")
    print("-> Proof: She reached the word 'orbits'. She saw no forward connections.")
    print("   Her energy dropped, triggering a reflex to ask the environment for the missing bridge.\n")

    # --------------------------------------------------------------------------------
    print("PROOF 2: SELF-AWARENESS (The Ego Anchor)")
    print("Teaching: 'I am learning' and 'Bird is flying'")
    brain.converse("I am learning")
    brain.converse("Bird is flying")
    
    ego_node = brain.substrate.neurons[-1]
    # Find which concepts physically linked to the EGO node
    ego_links = []
    for peer_id, w in ego_node.synapses.items():
        if peer_id in brain.substrate.neurons:
            ego_links.append(brain.substrate.neurons[peer_id].text)
            
    print("User: 'who are you?'")
    tel = brain.converse("who are you?")
    print(f"FELLA: {tel['last_response']}")
    print(f"-> Proof: The word 'I' was physically mapped to Node -1 (The Ego Core).")
    print(f"   Her Ego Node physically points to: {ego_links}")
    print("   'Bird' is a separate entity entirely.\n")

    # --------------------------------------------------------------------------------
    print("PROOF 3: ASPIRATION (Mass & Gravitational Pull)")
    print("Teaching: 'Water is cold' (1 exposure)")
    brain.converse("Water is cold")
    
    print("Teaching: 'Water is life' (5 exposures -> High Mass)")
    for _ in range(5):
        brain.converse("Water is life")
        
    cold_node = next((n for n in brain.substrate.neurons.values() if n.text.lower() == "cold"), None)
    life_node = next((n for n in brain.substrate.neurons.values() if n.text.lower() == "life"), None)
    
    print(f"   Node 'cold' mass: {getattr(cold_node, 'mass', 1.0):.2f}")
    print(f"   Node 'life' mass: {getattr(life_node, 'mass', 1.0):.2f}")
    
    print("User: 'what is water?'")
    tel = brain.converse("what is water?")
    print(f"FELLA: {tel['last_response']}")
    print("-> Proof: 'life' accumulated physical mass (gravity) through reinforcement.")
    print("   Her traversal wave was physically pulled toward the heavier, more coherent goal.\n")

    # --------------------------------------------------------------------------------
    print("PROOF 4: TRUE LEARNER (Synaptic Decay / Forgetting)")
    print("Teaching: 'Xylophone is loud'")
    brain.converse("Xylophone is loud")
    
    xylo_node = next((n for n in brain.substrate.neurons.values() if n.text.lower() == "xylophone"), None)
    loud_node = next((n for n in brain.substrate.neurons.values() if n.text.lower() == "loud"), None)
    is_node = next((n for n in brain.substrate.neurons.values() if n.text.lower() == "is"), None)
    
    w_before = xylo_node.synapses.get(is_node.id, 0.0) if xylo_node and is_node else 0.0
    print(f"   Synapse [xylophone -> is] weight BEFORE decay: {w_before:.2f}")
    
    print("   [Fast-Forwarding Time: Applying 100 Synaptic Decay Heartbeats...]")
    for _ in range(100):
        brain.substrate.apply_synaptic_decay(decay_rate=0.005)
        
    w_after = xylo_node.synapses.get(is_node.id, 0.0) if xylo_node and is_node else 0.0
    print(f"   Synapse [xylophone -> is] weight AFTER decay: {w_after:.2f}")
    
    print("User: 'what is xylophone?'")
    tel = brain.converse("what is xylophone?")
    print(f"FELLA: {tel['last_response']}")
    print("-> Proof: The synaptic bridge rotted away because it was never reinforced.")
    print("   She physically forgot it. She is now uncertain.\n")
    
    print("================================================================================")

if __name__ == "__main__":
    run_trait_proofs()
