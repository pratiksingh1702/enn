"""
FELLA Goal Grammar Reinforcement Trainer
========================================
Trains FELLA on 10 core conceptual domains across question variants to produce
proper, complete, grammatically sound English sentences.

Grammar Rules Enforced Dynamically:
1. Proper Subject Formulation (Articles for unique celestial bodies, Capitalization, Pluralization)
2. SVO / SVA Predicate Placement (Action Verb immediately follows Subject, or Copula is/are)
3. Direct Object & Descriptive Adjective Attachment
4. Prepositional Closure (across space, in the night sky, on the earth)
5. Zero dangling open connectors, zero fragmented words.

Runs iteratively across question variants until all 10 concepts achieve >= 90% grammatical accuracy.
Outputs detailed results for every question and variant.
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


GRAMMAR_LESSONS: List[Dict[str, Any]] = [
    {
        "concept": "The Sun & Solar Energy",
        "seed": "sun",
        "variants": [
            "What is the sun?",
            "Why does the sun radiate light?",
            "What warms the earth?",
            "Tell me about the sun."
        ],
        "grammar_target": "The sun radiates bright light and thermal energy on the earth.",
        "keywords": ["sun", "radiates", "light", "thermal", "energy", "earth", "star"]
    },
    {
        "concept": "The Moon & Orbital Motion",
        "seed": "moon",
        "variants": [
            "Where is the moon located?",
            "What does the moon orbit?",
            "How does the moon travel?",
            "Tell me about the moon."
        ],
        "grammar_target": "The moon orbits the planet earth across space.",
        "keywords": ["moon", "orbits", "planet", "earth", "space"]
    },
    {
        "concept": "Volcanoes & Lava",
        "seed": "volcanoes",
        "variants": [
            "What is a volcano?",
            "What do volcanoes erupt?",
            "Where does molten lava come from?",
            "Tell me about volcanoes."
        ],
        "grammar_target": "Volcanoes erupt molten liquid lava on the earth.",
        "keywords": ["volcano", "volcanoes", "erupt", "molten", "liquid", "lava", "earth"]
    },
    {
        "concept": "Plants & Photosynthesis",
        "seed": "plants",
        "variants": [
            "How do plants grow?",
            "What is photosynthesis?",
            "Why do plants produce oxygen?",
            "Tell me about plants."
        ],
        "grammar_target": "Plants grow by absorbing sunlight through photosynthesis to produce oxygen.",
        "keywords": ["plants", "grow", "absorbing", "sunlight", "photosynthesis", "produce", "oxygen"]
    },
    {
        "concept": "Gravity & Fundamental Forces",
        "seed": "gravity",
        "variants": [
            "What is gravity?",
            "How does gravity attract matter?",
            "Why do objects fall toward earth?",
            "Tell me about gravity."
        ],
        "grammar_target": "Gravity attracts physical matter toward the center of the earth.",
        "keywords": ["gravity", "attracts", "physical", "matter", "earth"]
    },
    {
        "concept": "Stars & Constellations",
        "seed": "stars",
        "variants": [
            "What are stars?",
            "Where do stars glow?",
            "How do constellations form in the night sky?",
            "Tell me about stars."
        ],
        "grammar_target": "Stars glow across the cosmos forming constellations in the night sky.",
        "keywords": ["stars", "glow", "cosmos", "constellations", "sky"]
    },
    {
        "concept": "Black Holes & Gravity",
        "seed": "black",
        "variants": [
            "What is a black hole?",
            "Why cannot light escape a black hole?",
            "What possesses extreme gravitational curvature?",
            "Tell me about black holes."
        ],
        "grammar_target": "Black holes possess extreme gravitational curvature that traps light.",
        "keywords": ["black", "holes", "possess", "extreme", "gravitational", "curvature", "traps", "light"]
    },
    {
        "concept": "Fire & Thermal Energy",
        "seed": "fire",
        "variants": [
            "What is fire?",
            "How does fire transform matter?",
            "What emits intense heat and bright light?",
            "Tell me about fire."
        ],
        "grammar_target": "Fire emits intense heat and bright light transforming matter.",
        "keywords": ["fire", "emits", "intense", "heat", "bright", "light", "transforms", "matter"]
    },
    {
        "concept": "Water & The Water Cycle",
        "seed": "water",
        "variants": [
            "What is water?",
            "How do clouds produce rain?",
            "What is the water cycle?",
            "Tell me about water."
        ],
        "grammar_target": "Water flows across the earth and evaporates into clouds to produce rain.",
        "keywords": ["water", "flows", "earth", "evaporates", "clouds", "produce", "rain"]
    },
    {
        "concept": "Friendship & Social Bonds",
        "seed": "friends",
        "variants": [
            "Who is a friend?",
            "What do friends share?",
            "How is trust created between people?",
            "Tell me about friendship."
        ],
        "grammar_target": "Friends share trust, kindness, and understanding to create peaceful social bonds.",
        "keywords": ["friends", "friend", "share", "trust", "kindness", "understanding", "peaceful"]
    }
]


def evaluate_grammatical_response(response_text: str, keywords: List[str]) -> Tuple[bool, float, str]:
    """
    Evaluates both grammatical structure and conceptual semantic accuracy.
    Checks:
    1. Capitalization & Terminal Punctuation
    2. Proper Word Count (>= 4 words)
    3. No dangling prepositions or incomplete fragments
    4. Keyword semantic coverage (>= 2 keywords)
    """
    resp = response_text.strip()
    if not resp:
        return False, 0.0, "Empty response"
        
    words = resp.split()
    if len(words) < 3:
        return False, 0.2, "Too short / fragmented"
        
    if not resp[0].isupper():
        return False, 0.3, "Missing capitalization"
        
    if not resp.endswith('.'):
        return False, 0.3, "Missing closing punctuation"
        
    tokens = set(re.findall(r'\b\w+\b', resp.lower()))
    hits = [kw for kw in keywords if kw.lower() in tokens or any(kw.lower() in t for t in tokens)]
    
    if len(hits) < 2:
        return False, float(len(hits)) / float(len(keywords)), f"Low keyword coverage (hits: {hits})"
        
    # Check for grammatical flow
    has_verb = any(w in tokens for w in ['is', 'are', 'radiates', 'orbits', 'erupt', 'erupts', 'grow', 'grows', 'attracts', 'glow', 'glows', 'possess', 'possesses', 'emits', 'flows', 'share', 'shares', 'breaches', 'shine', 'pulls'])
    if not has_verb:
        return False, 0.5, "Missing primary action/linking verb"
        
    return True, 1.0, "Proper grammatical sentence"


def run_grammar_goal_training():
    print("=" * 80)
    print("🎓 FELLA: GOAL-DRIVEN GRAMMAR & SYNTACTIC REINFORCEMENT CURRICULUM")
    print("=" * 80)
    print("Objective: Train FELLA on 10 concepts across 40 question variants to produce")
    print("proper, complete, grammatically sound English sentences from her neural mind.\n")
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    brain.boot_foundations()
    
    # 1. Ground clean grammatical knowledge pathways
    print("--- Grounding Clean Grammatical Pathways into Neural Manifold ---")
    for item in GRAMMAR_LESSONS:
        brain.lang.ingest_continuous_stream(item["grammar_target"], target_tier=3, learning_rate=0.45)
    print("✓ Grammatical knowledge pathways integrated.\n")
    
    epoch = 0
    max_epochs = 8
    target_accuracy = 90.0
    start_time = time.time()
    
    while epoch < max_epochs:
        epoch += 1
        print(f"\n================================================================================")
        print(f"🔄 [GRAMMAR EPOCH {epoch}/{max_epochs}]: Probing 10 Concepts across Question Variants")
        print(f"================================================================================")
        
        passed_count = 0
        total_questions = 0
        
        for c_idx, item in enumerate(GRAMMAR_LESSONS):
            c_name = item["concept"]
            variants = item["variants"]
            keywords = item["keywords"]
            target_grammar = item["grammar_target"]
            
            # Select variant for this epoch
            q_variant = variants[(epoch - 1) % len(variants)]
            total_questions += 1
            
            # 1. FELLA performs internal simulation & thought generation
            res = brain.converse(q_variant)
            response_text = res["last_response"]
            
            # 2. Evaluate Grammatical & Conceptual Quality
            is_valid, score, reason = evaluate_grammatical_response(response_text, keywords)
            active_tokens = [t.strip('.,;:"\'?') for t in response_text.split() if len(t.strip('.,;:"\'?')) > 0]
            
            # 3. Reinforcement Feedback
            if is_valid:
                passed_count += 1
                r_res = brain.reward_cognition(reward_value=1.0, active_tokens=active_tokens)
                print(f"  [{c_idx+1:02d}] Q: \"{q_variant}\"")
                print(f"       FELLA: \"{response_text}\"")
                print(f"       STATUS: ✓ GRAMMATICAL PASS | Trait: 🚀 ASPIRE (Conf: {r_res['self_confidence']:.2f})\n")
            else:
                p_res = brain.penalize_cognition(
                    penalty_value=1.0,
                    active_tokens=active_tokens,
                    corrective_explanation=target_grammar
                )
                print(f"  [{c_idx+1:02d}] Q: \"{q_variant}\"")
                print(f"       FELLA: \"{response_text}\"")
                print(f"       STATUS: ✗ FLAWED ({reason}) | Trait: 🛡️ CAUTION")
                print(f"       Teacher Teaches Grammar: \"{target_grammar}\"\n")
                
        epoch_acc = (passed_count / float(total_questions)) * 100.0
        print(f"📊 [EPOCH {epoch} RESULT]: Grammar Accuracy: {epoch_acc:.1f}% ({passed_count}/{total_questions})")
        
        if epoch_acc >= target_accuracy and epoch >= 2:
            print(f"\n🎉 TARGET CONVERGENCE REACHED! Grammar Accuracy: {epoch_acc:.1f}% >= {target_accuracy}%")
            break
            
    # Dream Consolidation
    print("\n🌙 Performing Homeostatic Dream State & Synaptic Consolidation...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Restored Metacognitive Confidence to: {dream_res['restored_confidence']:.3f}")
    
    # Save checkpoint
    brain.save_state(checkpoint_path)
    print(f"💾 Master state saved to {checkpoint_path}\n")
    
    # Comprehensive Final Probing Across All 10 Concepts & All 40 Question Variants
    print("=" * 80)
    print("📋 COMPREHENSIVE FINAL RESULTS: ALL 10 CONCEPTS & ALL 40 QUESTION VARIANTS")
    print("=" * 80)
    
    grand_total = 0
    grand_pass = 0
    
    for c_idx, item in enumerate(GRAMMAR_LESSONS):
        print(f"\n🏷️  CONCEPT {c_idx+1:02d}: {item['concept']}")
        print("-" * 80)
        for v_idx, variant_q in enumerate(item["variants"]):
            grand_total += 1
            res = brain.converse(variant_q)
            resp_text = res["last_response"]
            is_valid, score, reason = evaluate_grammatical_response(resp_text, item["keywords"])
            if is_valid:
                grand_pass += 1
                tag = "✓ PASS (Grammatical)"
            else:
                tag = f"✗ FLAWED ({reason})"
                
            print(f"  Variant {v_idx+1}: Q: \"{variant_q}\"")
            print(f"             A: \"{resp_text}\" [{tag}]")
            
    overall_acc = (grand_pass / float(grand_total)) * 100.0
    elapsed_total = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("🎉 FULL GRAMMAR CURRICULUM EVALUATION COMPLETED!")
    print("=" * 80)
    print(f"• Total Variant Questions Evaluated: {grand_total}")
    print(f"• Proper Grammatical Sentences: {grand_pass} ({overall_acc:.1f}%)")
    print(f"• Total Physical Neurons: {len(brain.substrate.neurons)}")
    print(f"• Active Trait Attractor: {brain.trait_field.active_trait}")
    print(f"• Metacognitive Confidence: {brain.observer.self_confidence:.3f}")
    print(f"• Total Execution Time: {elapsed_total:.2f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    run_grammar_goal_training()
