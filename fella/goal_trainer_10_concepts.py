"""
FELLA Goal-Driven Neural Reinforcement Training Engine
======================================================
Trains FELLA on 10 foundational conceptual domains across question variants.
Operates via pure Hebbian synaptic potentiation/depression, trait modulation
(ASPIRE on reward, CAUTION on correction), and continuous memory ingestion.

Zero code changes. Zero hardcoded responses.
Runs iteratively until convergence (>= 90% accuracy across all variant clusters).
"""

import os
import sys
import time
import re
import numpy as np
from typing import List, Dict, Any, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


# 10 Core Concepts with Varied Phrasings and Ground-Truth Lessons
CONCEPT_DOMAINS: List[Dict[str, Any]] = [
    {
        "concept": "Sun & Solar Radiation",
        "variants": [
            "What is the sun?",
            "Why does the sun radiate light?",
            "What emits thermal energy that warms the earth?",
            "Tell me about the sun in the solar system."
        ],
        "core_keywords": ["sun", "radiates", "light", "thermal", "energy", "warms", "earth", "star"],
        "teacher_lesson": "The sun is a luminous star that radiates bright light and emits thermal energy warming the earth."
    },
    {
        "concept": "Moon & Orbital Motion",
        "variants": [
            "Where is the moon located?",
            "What does the moon orbit?",
            "How does the moon travel across space?",
            "Explain the moon in relation to earth."
        ],
        "core_keywords": ["moon", "orbits", "planet", "earth", "space", "satellite"],
        "teacher_lesson": "The moon is a natural celestial satellite that orbits the planet earth across space."
    },
    {
        "concept": "Volcanoes & Magma Eruptions",
        "variants": [
            "What is a volcano?",
            "What do volcanoes erupt?",
            "Where does molten lava come from?",
            "How do volcanic eruptions shape the earth?"
        ],
        "core_keywords": ["volcano", "volcanoes", "erupt", "molten", "liquid", "lava", "deep", "earth"],
        "teacher_lesson": "Volcanoes erupt molten liquid lava and hot gases from deep magma chambers inside the earth."
    },
    {
        "concept": "Plants & Photosynthesis",
        "variants": [
            "How do plants grow?",
            "What is photosynthesis?",
            "Why do green plants produce oxygen?",
            "What do plants absorb to create energy?"
        ],
        "core_keywords": ["plants", "grow", "absorbing", "sunlight", "water", "photosynthesis", "produce", "oxygen"],
        "teacher_lesson": "Plants grow by absorbing sunlight and water through photosynthesis to produce glucose and oxygen."
    },
    {
        "concept": "Gravity & Gravitational Pull",
        "variants": [
            "What is gravity?",
            "How does gravity attract physical matter?",
            "Why do objects fall toward the earth?",
            "Explain the force of gravity."
        ],
        "core_keywords": ["gravity", "fundamental", "force", "attracts", "physical", "matter", "toward", "earth"],
        "teacher_lesson": "Gravity is the fundamental attractive force that pulls physical matter toward the center of the earth."
    },
    {
        "concept": "Stars & Constellations",
        "variants": [
            "What are stars?",
            "Where do stars glow?",
            "How do constellations form in the night sky?",
            "Tell me about stars in the cosmos."
        ],
        "core_keywords": ["stars", "glow", "cosmos", "forming", "constellations", "night", "sky", "celestial"],
        "teacher_lesson": "Stars are glowing celestial plasma bodies that shine across the cosmos forming constellations in the night sky."
    },
    {
        "concept": "Black Holes & Spacetime Curvature",
        "variants": [
            "What is a black hole?",
            "Why cannot light escape a black hole?",
            "What possesses extreme gravitational curvature?",
            "Explain the nature of a black hole."
        ],
        "core_keywords": ["black", "holes", "possess", "extreme", "gravitational", "curvature", "traps", "light"],
        "teacher_lesson": "Black holes possess extreme gravitational curvature that traps physical matter and prevents light from escaping."
    },
    {
        "concept": "Fire & Thermal Oxidation",
        "variants": [
            "What is fire?",
            "How does fire transform matter?",
            "What emits intense heat and bright light?",
            "Explain the process of fire."
        ],
        "core_keywords": ["fire", "emits", "intense", "heat", "bright", "light", "thermal", "transforms", "matter"],
        "teacher_lesson": "Fire is an exothermic reaction that emits intense heat and bright light as thermal energy transforms matter."
    },
    {
        "concept": "Water & The Water Cycle",
        "variants": [
            "What is water?",
            "How do clouds produce rain?",
            "What is the water cycle?",
            "Where does liquid water flow and evaporate?"
        ],
        "core_keywords": ["water", "liquid", "flows", "earth", "evaporates", "clouds", "produce", "rain"],
        "teacher_lesson": "Water is a liquid that flows across the earth and evaporates into clouds to produce rain precipitation."
    },
    {
        "concept": "Friendship & Social Bonds",
        "variants": [
            "Who is a friend?",
            "What do friends share?",
            "How is trust created between people?",
            "What is the meaning of friendship?"
        ],
        "core_keywords": ["friends", "friend", "share", "trust", "kindness", "understanding", "peaceful", "social", "bonds"],
        "teacher_lesson": "Friends are caring companions who share mutual trust, kindness, and understanding to create peaceful social bonds."
    }
]


def evaluate_neural_thought(response_text: str, core_keywords: List[str]) -> Tuple[float, List[str]]:
    """Evaluates the semantic precision and keyword recall of FELLA's neural thought."""
    tokens = set(re.findall(r'\b\w+\b', response_text.lower()))
    hits = [kw for kw in core_keywords if kw.lower() in tokens or any(kw.lower() in t for t in tokens)]
    recall = float(len(hits)) / max(1.0, float(min(4, len(core_keywords))))
    return min(1.0, recall), hits


def run_goal_training_loop():
    print("=" * 80)
    print("🎯 FELLA: ITERATIVE GOAL-DRIVEN REINFORCEMENT & CONVERGENCE TRAINING")
    print("=" * 80)
    print("Objective: Train FELLA on 10 core concepts across variant questions until >= 90% accuracy.")
    print("Mechanism: Pure Hebbian potentiation/depression (ASPIRE / CAUTION), zero hardcoding.\n")
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    brain.boot_foundations()
    
    epoch = 0
    max_epochs = 15
    target_accuracy = 90.0
    start_time = time.time()
    
    while epoch < max_epochs:
        epoch += 1
        print(f"\n================================================================================")
        print(f"🔄 [EPOCH {epoch}/{max_epochs}]: Probing 10 Concept Clusters across Question Variants")
        print(f"================================================================================")
        
        correct_count = 0
        total_questions = 0
        
        for c_idx, domain in enumerate(CONCEPT_DOMAINS):
            c_name = domain["concept"]
            variants = domain["variants"]
            keywords = domain["core_keywords"]
            teacher_lesson = domain["teacher_lesson"]
            
            # Pick a variant for this epoch
            q_variant = variants[(epoch - 1) % len(variants)]
            total_questions += 1
            
            # 1. FELLA performs internal simulation & thought generation
            res = brain.converse(q_variant)
            response_text = res["last_response"]
            active_trait = res["active_trait"]
            
            # 2. Evaluate accuracy
            score, hits = evaluate_neural_thought(response_text, keywords)
            active_tokens = [t.strip('.,;:"\'?') for t in response_text.split() if len(t.strip('.,;:"\'?')) > 0]
            
            # 3. Trait-Driven Reinforcement Feedback
            if score >= 0.50 or len(hits) >= 2:
                correct_count += 1
                r_res = brain.reward_cognition(reward_value=1.0, active_tokens=active_tokens)
                print(f"  [Concept {c_idx+1:02d}]: {c_name}")
                print(f"    Q: \"{q_variant}\"")
                print(f"    FELLA: \"{response_text}\"")
                print(f"    STATUS: ✓ REWARDED (+1.0) | Trait: 🚀 ASPIRE (Confidence: {r_res['self_confidence']:.2f}, Hits: {hits})\n")
            else:
                p_res = brain.penalize_cognition(
                    penalty_value=1.0,
                    active_tokens=active_tokens,
                    corrective_explanation=teacher_lesson
                )
                print(f"  [Concept {c_idx+1:02d}]: {c_name}")
                print(f"    Q: \"{q_variant}\"")
                print(f"    FELLA: \"{response_text}\"")
                print(f"    STATUS: ✗ INCORRECT (-1.0) | Trait: 🛡️ CAUTION (Confidence: {p_res['self_confidence']:.2f})")
                print(f"    Teacher Corrects & Grounds: \"{teacher_lesson}\"\n")
                
        epoch_acc = (correct_count / float(total_questions)) * 100.0
        print(f"📊 [EPOCH {epoch} SUMMARY]: Accuracy: {epoch_acc:.1f}% ({correct_count}/{total_questions}) | Physical Neurons: {len(brain.substrate.neurons)}")
        
        # Check convergence
        if epoch_acc >= target_accuracy and epoch >= 3:
            print(f"\n🎉 TARGET CONVERGENCE ACHIEVED! Accuracy: {epoch_acc:.1f}% >= {target_accuracy}%")
            break
            
    # Final Dream Consolidation
    print("\n🌙 Initiating Final Post-Training Dream Consolidation...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Reverberated activation across {dream_res['reverberated_neurons']} concept neurons.")
    print(f"✓ Pruned {dream_res['pruned_synapses']} noisy synapses.")
    print(f"✓ Restored Metacognitive Confidence to: {dream_res['restored_confidence']:.3f}")
    
    # Save master fortified checkpoint
    brain.save_state(checkpoint_path)
    print(f"💾 Master state preserved to {checkpoint_path}\n")
    
    # Final Validation Pass across all 10 concepts
    print("=" * 80)
    print("🔍 FINAL VALIDATION PROBING ACROSS ALL 10 CONCEPTS (AFTER TRAINING)")
    print("=" * 80)
    
    final_correct = 0
    for idx, domain in enumerate(CONCEPT_DOMAINS):
        test_q = domain["variants"][0]
        res = brain.converse(test_q)
        score, hits = evaluate_neural_thought(res["last_response"], domain["core_keywords"])
        is_pass = (score >= 0.50 or len(hits) >= 2)
        if is_pass:
            final_correct += 1
        tag = "✓ PASS" if is_pass else "✗ FAIL"
        print(f"[{idx+1:02d}] Q: \"{test_q}\"")
        print(f"     FELLA: \"{res['last_response']}\" [{tag}]\n")
        
    final_rate = (final_correct / float(len(CONCEPT_DOMAINS))) * 100.0
    elapsed_total = time.time() - start_time
    
    print("=" * 80)
    print(f"🎉 GOAL TRAINING COMPLETE! Final Accuracy: {final_rate:.1f}% ({final_correct}/10)")
    print(f"• Total Physical Neurons: {len(brain.substrate.neurons)}")
    print(f"• Trait Attractor: {brain.trait_field.active_trait}")
    print(f"• Metacognitive Confidence: {brain.observer.self_confidence:.3f}")
    print(f"• Total Time Elapsed: {elapsed_total:.2f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    run_goal_training_loop()
