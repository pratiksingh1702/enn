"""
Clean Emergent Associative Memory Test for ENN 4D
"""

import os
import sys
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from enn4d import ENN4D
from text_encoder import TextEncoder
from text_decoder import TextDecoder

def test_clean_emergent_recall():
    print("=" * 60)
    print("TESTING PURE EMERGENT CONTINUOUS ENCODING & RECALL")
    print("=" * 60)
    
    system = ENN4D(dim=4)
    encoder = TextEncoder(dim=4)
    decoder = TextDecoder()
    
    # 1. Teach distinct knowledge concepts
    knowledge_base = [
        "My name is Professor Smith.",
        "I am a quantum physicist and scientist.",
        "I love cats, dogs, and biology.",
        "I live in London, United Kingdom."
    ]
    
    print("\n1. Feeding knowledge into the living field:")
    for text in knowledge_base:
        event = encoder.encode_text_to_4d(text)
        # Train / step into the physical field
        out_y = system.step(event['x'], event['y'], event['z'])
        print(f"  -> Imprinted: '{text}' | Family: {system.neurons[-1].w} | Position: {np.round(event['x'], 3)}")
        
    decoder.set_memory_log(encoder.get_memory_log())
    print(f"\nTotal neurons birthed: {len(system.neurons)} across {len(set(n.w for n in system.neurons))} families.")
    
    # 2. Query the field with paraphrased / unseen questions
    test_queries = [
        "Who am I?",
        "What is my job and field of research?",
        "Which pets and animals do I like?",
        "Where is my home city located?"
    ]
    
    print("\n2. Querying the living field (Pure Resonance & Interference):")
    for query in test_queries:
        # Encode query to sensory coordinates
        q_event = encoder.encode_text_to_4d(query)
        
        # Step through continuous wave dynamics
        out_y = system.step(q_event['x'], q_event['y'], q_event['z'])
        forces = system.compute_resonance(q_event['x'], q_event['y'], q_event['z'])
        
        # Decode associative output Y
        # Exclude query itself from target recall pool
        declarative_log = [m for m in encoder.get_memory_log() if m['text'] in knowledge_base]
        recalled = decoder.decode_4d_to_text(out_y, memory_log=declarative_log)
        
        print(f"\n[Query]: '{query}'")
        print(f"  -> Max Resonance Force: {max(forces):.4f}")
        print(f"  -> Living Field Recalled: '{recalled}'")

if __name__ == '__main__':
    test_clean_emergent_recall()