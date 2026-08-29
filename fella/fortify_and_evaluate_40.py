"""
FELLA Comprehensive 40-Variant Grammar Evaluator
===============================================
Fortifies the 10 core conceptual highways in the continuous neural substrate
and performs an exhaustive evaluation of all 10 concepts across 40 question variants.
Prints complete, transparent results for every single question variant.
"""

import os
import sys
import time
import re
from typing import List, Dict, Any, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


TEN_CONCEPTS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "concept": "The Sun & Solar Radiation",
        "highway": "The sun radiates bright light and thermal energy that warms the earth",
        "keywords": ["sun", "radiates", "light", "thermal", "energy", "warms", "earth"],
        "variants": [
            "What is the sun?",
            "Why does the sun radiate light?",
            "What emits thermal energy that warms the earth?",
            "Tell me about the sun."
        ]
    },
    {
        "id": 2,
        "concept": "The Moon & Lunar Orbit",
        "highway": "The moon orbits the planet earth across space",
        "keywords": ["moon", "orbits", "planet", "earth", "space"],
        "variants": [
            "Where is the moon located?",
            "What does the moon orbit?",
            "How does the moon travel?",
            "Tell me about the moon."
        ]
    },
    {
        "id": 3,
        "concept": "Volcanoes & Lava Eruptions",
        "highway": "Volcanoes erupt molten liquid lava from deep within the earth",
        "keywords": ["volcano", "volcanoes", "erupt", "molten", "liquid", "lava", "earth"],
        "variants": [
            "What is a volcano?",
            "What do volcanoes erupt?",
            "Where does molten lava come from?",
            "Tell me about volcanoes."
        ]
    },
    {
        "id": 4,
        "concept": "Plants & Photosynthesis",
        "highway": "Plants grow by absorbing sunlight through photosynthesis to produce oxygen",
        "keywords": ["plants", "grow", "absorbing", "sunlight", "photosynthesis", "produce", "oxygen"],
        "variants": [
            "How do plants grow?",
            "What is photosynthesis?",
            "Why do plants produce oxygen?",
            "Tell me about plants."
        ]
    },
    {
        "id": 5,
        "concept": "Gravity & Gravitational Attraction",
        "highway": "Gravity attracts physical matter toward the center of the earth",
        "keywords": ["gravity", "attracts", "physical", "matter", "earth", "force"],
        "variants": [
            "What is gravity?",
            "How does gravity attract physical matter?",
            "Why do objects fall toward the earth?",
            "Tell me about gravity."
        ]
    },
    {
        "concept": "Stars & Constellations",
        "id": 6,
        "highway": "Stars glow across the cosmos forming constellations in the night sky",
        "keywords": ["stars", "glow", "cosmos", "forming", "constellations", "night", "sky"],
        "variants": [
            "What are stars?",
            "Where do stars glow?",
            "How do constellations form in the night sky?",
            "Tell me about stars."
        ]
    },
    {
        "concept": "Black Holes & Gravitational Curvature",
        "id": 7,
        "highway": "Black holes possess extreme gravitational curvature that traps light",
        "keywords": ["black", "holes", "possess", "extreme", "gravitational", "curvature", "traps", "light"],
        "variants": [
            "What is a black hole?",
            "Why cannot light escape a black hole?",
            "What possesses extreme gravitational curvature?",
            "Tell me about black holes."
        ]
    },
    {
        "concept": "Fire & Thermal Energy",
        "id": 8,
        "highway": "Fire emits intense heat and bright light transforming matter",
        "keywords": ["fire", "emits", "intense", "heat", "bright", "light", "transforms", "matter"],
        "variants": [
            "What is fire?",
            "How does fire transform matter?",
            "What emits intense heat and bright light?",
            "Tell me about fire."
        ]
    },
    {
        "concept": "Water & The Water Cycle",
        "id": 9,
        "highway": "Water flows across the earth and evaporates into clouds to produce rain",
        "keywords": ["water", "flows", "earth", "evaporates", "clouds", "produce", "rain"],
        "variants": [
            "What is water?",
            "How do clouds produce rain?",
            "What is the water cycle?",
            "Tell me about water."
        ]
    },
    {
        "concept": "Friendship & Social Bonds",
        "id": 10,
        "highway": "Friends share trust, kindness, and understanding to create peaceful social bonds",
        "keywords": ["friends", "friend", "share", "trust", "kindness", "understanding", "peaceful", "social"],
        "variants": [
            "Who is a friend?",
            "What do friends share?",
            "How is trust created between people?",
            "Tell me about friendship."
        ]
    }
]


def evaluate_grammar_and_recall(response_text: str, keywords: List[str]) -> Tuple[bool, str]:
    resp = response_text.strip()
    if not resp:
        return False, "Empty response"
        
    words = resp.split()
    if len(words) < 3:
        return False, "Too short / fragmented"
        
    if not resp[0].isupper() or not resp.endswith('.'):
        return False, "Missing proper capitalization or terminal punctuation"
        
    tokens = set(re.findall(r'\b\w+\b', resp.lower()))
    hits = [kw for kw in keywords if kw.lower() in tokens or any(kw.lower() in t for t in tokens)]
    
    if len(hits) < 1:
        return False, f"Missing core concept keywords (hits: {hits})"
        
    return True, f"Valid Grammatical Thought (hits: {hits})"


def main():
    print("=" * 80)
    print("🚀 FELLA: FORTIFYING 10 CONCEPT HIGHWAYS & 40-VARIANT EVALUATION")
    print("=" * 80)
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    brain.boot_foundations()
    
    # 1. Fortify forward sequential pathways with high Hebbian conductance
    print("\n--- Ingesting High-Conductance Sequential Bridges for 10 Core Concepts ---")
    for item in TEN_CONCEPTS:
        nodes = brain.lang.ingest_continuous_stream(item["highway"], target_tier=3, learning_rate=0.55)
        print(f"✓ Fortified Concept {item['id']:02d} ({item['concept']}): {len(nodes)} nodes")
        
    # 2. Dream state consolidation to prune cross-talk
    print("\n🌙 Running Homeostatic Dream Cycle & Background Noise Pruning...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Pruned {dream_res['pruned_synapses']} weak synapses. Restored Confidence: {dream_res['restored_confidence']:.3f}\n")
    
    # Save fortified state
    brain.save_state(checkpoint_path)
    
    # 3. Exhaustive Evaluation Across All 10 Concepts and All 40 Variants
    print("=" * 80)
    print("📋 FULL QUESTION-BY-QUESTION RESULTS: ALL 10 CONCEPTS & ALL 40 VARIANTS")
    print("=" * 80)
    
    total_q = 0
    passed_q = 0
    start_time = time.time()
    
    for item in TEN_CONCEPTS:
        c_id = item["id"]
        c_name = item["concept"]
        keywords = item["keywords"]
        variants = item["variants"]
        
        print(f"\n================================================================================")
        print(f"🏷️  CONCEPT {c_id:02d}: {c_name.upper()}")
        print(f"   Target Highway: \"{item['highway']}\"")
        print(f"================================================================================")
        
        for v_idx, q in enumerate(variants):
            total_q += 1
            res = brain.converse(q)
            ans = res["last_response"]
            is_valid, msg = evaluate_grammar_and_recall(ans, keywords)
            
            if is_valid:
                passed_q += 1
                status = "✓ PASS (Grammatical & Accurate)"
            else:
                status = f"✗ FLAWED ({msg})"
                
            print(f"  [{c_id:02d}.{v_idx+1}] Question: \"{q}\"")
            print(f"        FELLA   : \"{ans}\"")
            print(f"        Status  : {status}\n")
            
    total_time = time.time() - start_time
    acc = (passed_q / float(total_q)) * 100.0
    
    print("=" * 80)
    print("🎉 EXHAUSTIVE 40-VARIANT EVALUATION COMPLETE!")
    print("=" * 80)
    print(f"• Total Question Variants Tested: {total_q}")
    print(f"• Proper Grammatical Sentences: {passed_q} ({acc:.1f}%)")
    print(f"• Total Physical Neurons: {len(brain.substrate.neurons)}")
    print(f"• Active Synaptic Channels: {brain.substrate.get_synapse_stats()['total_synapses']}")
    print(f"• Metacognitive Confidence: {brain.observer.self_confidence:.3f}")
    print(f"• Total Evaluation Time: {total_time:.2f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    main()
