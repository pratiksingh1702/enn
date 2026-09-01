import json
import math
from fella.fella_brain import FellaBrain

def test_questions():
    fella = FellaBrain.load_state("fella_checkpoint.json")

    hot_words = ["?", "what", "where", "who", "why", "how"]
    for word in hot_words:
        node = fella.wave_engine._get_or_create_neuron(word)
        node.phase = math.pi
        node.hot_potential = 100.0

    # Let's debug specifically "what is tub ?"
    q = "what is tub ?"
    print(f"\n[DEBUGGING]: {q}")
    
    # Simulate exactly what fella_brain.py does
    text_clean = q
    target_id = fella.wave_engine._get_or_create_neuron("what").id
    print(f"Target ID (what): {target_id}")
    
    found_answer = False
    if fella.wave_engine.determine_spectron_type(fella.substrate.neurons[target_id]) == "hot":
        words = text_clean.replace("?", "").split()
        for w in words:
            n = fella.wave_engine._get_or_create_neuron(w)
            print(f"  Word: '{w}', ID: {n.id}, Type: {fella.wave_engine.determine_spectron_type(n)}")
            if n.id != target_id and fella.wave_engine.determine_spectron_type(n) != "catalyst":
                resonant_nodes = []
                for syn_id, weight in n.synapses.items():
                    syn_n = fella.substrate.neurons[syn_id]
                    syn_type = fella.wave_engine.determine_spectron_type(syn_n)
                    print(f"    -> Synapse: '{syn_n.text}', Type: {syn_type}, Weight: {weight}")
                    if syn_type not in ["hot", "catalyst"] and syn_n.text != "user":
                        resonant_nodes.append((syn_n.text, weight))
                
                print(f"    Resonant Nodes for '{w}': {resonant_nodes}")
                if resonant_nodes:
                    resonant_nodes.sort(key=lambda x: x[1], reverse=True)
                    answer = resonant_nodes[0][0]
                    print(f"    FOUND ANSWER: {answer}")
                    found_answer = True
                    break

    print(f"Final found_answer: {found_answer}")

if __name__ == "__main__":
    test_questions()
