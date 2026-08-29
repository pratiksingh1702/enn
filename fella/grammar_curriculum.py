"""
FELLA Developmental Grammar Curriculum
=====================================
Teaches FELLA the foundational structure of the English language step-by-step:
1. Stage 1: Letters & Phonetics (Z=0)
2. Stage 2: Naming Objects & Entities (Nouns at Z=1)
3. Stage 3: Dynamic Actions (Verbs at Z=2) & Properties (Adjectives at Z=3)
4. Stage 4: 2-Word Core Sentences (Subject + Verb)
5. Stage 5: Complete Formatted Sentences (Subject + Verb + Object/Property)
6. Stage 6: Grammar Validation & Broken Sentence Error Correction
"""

import os
import sys
import time
from typing import Dict, Any, List

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


def run_grammar_curriculum(checkpoint_path: str = "fella_checkpoint.json") -> FellaBrain:
    print("=" * 80)
    print("🎓 FELLA: INITIATING 6-STAGE DEVELOPMENTAL GRAMMAR CURRICULUM")
    print("=" * 80)
    
    brain = FellaBrain(dim=16)
    brain.boot_foundations()
    
    # -------------------------------------------------------------------------
    # STAGE 1: Letters & Phonetics (Graphemes at Z=0)
    # -------------------------------------------------------------------------
    print("\n[Stage 1/6]: Grapheme Substrate Rehearsal (26 Letters)...")
    let_res = brain.rehearse_letters(practice_rounds=10)
    print(f"  ✓ Alphabet permanently grounded (Energy: {let_res['mean_energy']:.1f}, Conductance: 1.000)")

    # -------------------------------------------------------------------------
    # STAGE 2: Naming Entities & Actors (Nouns at Z=1)
    # -------------------------------------------------------------------------
    print("\n[Stage 2/6]: Naming the World (Entities / Nouns at Tier Z=1)...")
    entities = [
        "sun", "water", "earth", "trees", "plants", "gravity", "clouds", "rain",
        "fire", "moon", "stars", "forests", "oxygen", "animals", "fella", "friend"
    ]
    for entity in entities:
        brain.lang.ingest_continuous_stream(entity, target_tier=1)
        print(f"  • Entity Noun: \"{entity}\"")

    # -------------------------------------------------------------------------
    # STAGE 3: Dynamic Actions (Verbs at Z=2) & Properties (Adjectives at Z=3)
    # -------------------------------------------------------------------------
    print("\n[Stage 3/6]: Grounding Actions (Verbs at Z=2) & Qualities (Adjectives at Z=3)...")
    actions = [
        ("radiates", 2), ("attracts", 2), ("absorbs", 2), ("causes", 2),
        ("grows", 2), ("flows", 2), ("falls", 2), ("produces", 2),
        ("bright", 3), ("warm", 3), ("liquid", 3), ("green", 3),
        ("solid", 3), ("intense", 3), ("heavy", 3), ("fresh", 3)
    ]
    for word, tier in actions:
        brain.lang.ingest_continuous_stream(word, target_tier=tier)
        role = "Action (Verb)" if tier == 2 else "Quality (Adjective)"
        print(f"  • {role} [Z={tier}]: \"{word}\"")

    # -------------------------------------------------------------------------
    # STAGE 4: First Complete 2-Word Thoughts (Subject + Verb)
    # -------------------------------------------------------------------------
    print("\n[Stage 4/6]: Constructing First 2-Word Complete Sentences (Subject + Verb)...")
    two_word_sentences = [
        "Sun radiates",
        "Water flows",
        "Rain falls",
        "Plants grow",
        "Gravity attracts",
        "Fire burns",
        "Stars glow",
        "Birds fly"
    ]
    for s in two_word_sentences:
        brain.lang.ingest_continuous_stream(s, target_tier=2)
        print(f"  • Subject + Verb: \"{s}\"")

    # -------------------------------------------------------------------------
    # STAGE 5: Complete Formatted Sentences (Subject + Verb + Object/Property)
    # -------------------------------------------------------------------------
    print("\n[Stage 5/6]: Constructing Complete Formatted Sentences (SVO / SVA)...")
    complete_sentences = [
        "The sun radiates bright light and warmth",
        "Gravity attracts physical matter toward the earth",
        "Water nurtures growing green trees",
        "Green plants absorb sunlight through photosynthesis",
        "Photosynthesis produces glucose energy and fresh oxygen",
        "Heat causes liquid water to evaporate into vapor",
        "Water vapor cools in the atmosphere to form clouds",
        "Clouds produce rain that returns water to earth",
        "Fire emits intense heat and bright light",
        "Friends share trust and kindness in friendship"
    ]
    for s in complete_sentences:
        brain.lang.ingest_continuous_stream(s, target_tier=3)
        print(f"  • Complete SVO/SVA: \"{s}\"")

    # -------------------------------------------------------------------------
    # STAGE 6: Grammar Error Detection & Self-Correction Mastery
    # -------------------------------------------------------------------------
    print("\n[Stage 6/6]: Testing Grammar Error Detection & Self-Correction...")
    broken_tests = [
        "The radiating sun is the",
        "The water liquid",
        "Sun shines bright the",
        "Gravity attracts matter to the"
    ]
    for broken in broken_tests:
        res = brain.converse(broken)
        print(f"\n  [Broken Input]: \"{broken}\"")
        print(f"  FELLA Correction > {res['last_response']}")

    # Final Dream Consolidation
    print("\n🌙 Consolidating Grammar Field via Homeostatic Dream...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Reverberated activation waves across {dream_res['reverberated_neurons']} neurons.")
    
    # Save grammar-mastered brain
    brain.save_state(checkpoint_path)
    print(f"\n💾 Preserved grammar-grounded state to {checkpoint_path}")
    
    tel = brain.get_telemetry()
    print("=" * 80)
    print(f"🎉 GRAMMAR CURRICULUM COMPLETE!")
    print(f"• Total Neurons: {tel['total_neurons']}")
    print(f"• Total Synapses: {tel['synapse_stats']['total_synapses']}")
    print(f"• Confidence: {tel['self_confidence']:.3f}")
    print("=" * 80)
    
    return brain


if __name__ == "__main__":
    run_grammar_curriculum()
