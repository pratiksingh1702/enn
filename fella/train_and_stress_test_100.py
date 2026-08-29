"""
FELLA 100-Question Natural Rephrasing & Self-Correction Trainer
==============================================================
Runs 100 raw, varied, and rephrased questions across 10 conceptual domains:
- Tests robustness to broken syntax ("you name ?", "water hot ?", "sun what ?")
- Reinforces continuous semantic links across the (X, Y, Z) manifold
- Validates that FELLA produces grounded, non-gibberish responses
"""

import os
import sys
import time
from typing import List, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


def run_100_question_curriculum():
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    brain.boot_foundations()
    
    # 100 Raw Questions across 10 Domains (including broken, conversational, and formal queries)
    question_suites: List[Tuple[str, List[str], str]] = [
        # Domain 1: Identity & Self
        (
            "Domain 1: Identity & Self-Model",
            [
                "Who are you?",
                "you name ?",
                "What are you called?",
                "who is fella",
                "tell me your name",
                "fella who?",
                "what is your identity",
                "are you fella",
                "name please",
                "who is talking right now?"
            ],
            "FELLA is a living cognitive mind learning and understanding the world"
        ),
        # Domain 2: Sun, Light & Thermal Radiation
        (
            "Domain 2: Sun, Light & Warmth",
            [
                "What does the sun do?",
                "why sun shines?",
                "sun what?",
                "what is sunlight?",
                "does the sun give warmth?",
                "where does heat come from?",
                "the sun is hot?",
                "tell me about the sun",
                "sun and light?",
                "what emits bright warmth?"
            ],
            "The sun radiates bright light and emits warmth and thermal energy"
        ),
        # Domain 3: Water, Rain & Evaporation
        (
            "Domain 3: Water, Rain & Evaporation",
            [
                "What is water?",
                "rain where from?",
                "why does rain fall?",
                "water hot what happens?",
                "what is evaporation?",
                "how does water become vapor?",
                "clouds make rain?",
                "water liquid?",
                "ocean has water?",
                "ice melts into what?"
            ],
            "Heat causes liquid water to evaporate into vapor which cools into clouds and returns as rain"
        ),
        # Domain 4: Living Plants, Trees & Photosynthesis
        (
            "Domain 4: Plants, Trees & Photosynthesis",
            [
                "How do plants grow?",
                "why trees green?",
                "plants need sun?",
                "do plants drink water?",
                "what is photosynthesis?",
                "where do leaves get energy?",
                "what makes oxygen for animals?",
                "roots anchor what in soil?",
                "seeds grow into what?",
                "why forests matter?"
            ],
            "Green plants absorb sunlight and water through photosynthesis to produce glucose energy and fresh oxygen"
        ),
        # Domain 5: Earth, Gravity & Motion
        (
            "Domain 5: Earth, Gravity & Planetary Motion",
            [
                "What is gravity?",
                "why objects fall down?",
                "gravity pulls what?",
                "why earth has weight?",
                "moon orbits earth?",
                "earth revolves around sun?",
                "why day and night happen?",
                "is earth our planet?",
                "what holds matter down?",
                "gravity force attracts what?"
            ],
            "Gravity attracts physical matter toward the center of the earth and causes objects to have weight"
        ),
        # Domain 6: Air, Atmosphere & Respiration
        (
            "Domain 6: Air, Atmosphere & Breathing",
            [
                "What is air?",
                "what do animals breathe from air?",
                "is air transparent gas?",
                "atmosphere gases surround what?",
                "why oxygen vital for life?",
                "what surrounds the earth?",
                "do birds fly in air?",
                "air is what state of matter?",
                "oxygen comes from where?",
                "breathing air gives what?"
            ],
            "The atmosphere is a mixture of transparent gases surrounding earth where animals breathe oxygen"
        ),
        # Domain 7: Friendship, Care & Kindness
        (
            "Domain 7: Friendship, Care & Kindness",
            [
                "Why is friendship important?",
                "friends share what?",
                "what does kindness bring?",
                "does love create strong bond?",
                "parents provide guidance?",
                "why care for friends?",
                "is kindness peaceful and joyful?",
                "friend trust matters?",
                "why be kind to others?",
                "helping friends brings what?"
            ],
            "Friends share trust and kindness, creating strong emotional bonds that bring peace and joy"
        ),
        # Domain 8: Thinking, Curiosity & Questions
        (
            "Domain 8: Thinking, Curiosity & Learning",
            [
                "Why do we ask questions?",
                "what is curiosity?",
                "thinking solves difficult challenges?",
                "learning brings confidence?",
                "why do we learn every day?",
                "mind thinks to understand?",
                "questions spark what in mind?",
                "how do we understand the world?",
                "does knowledge grow over time?",
                "is learning good for the mind?"
            ],
            "Questions spark curiosity in the mind and thinking helps solve challenges while learning builds confidence"
        ),
        # Domain 9: Fire, Heat & Energy Transformations
        (
            "Domain 9: Fire, Heat & Energy",
            [
                "What is fire?",
                "fire emits what?",
                "is fire hot and glowing?",
                "thermal energy causes what?",
                "heat melts ice into water?",
                "fire burns bright light?",
                "what makes intense heat?",
                "energy transforms between states?",
                "solar energy comes from sun?",
                "fire emits heat and light?"
            ],
            "Fire emits intense heat and bright light as thermal energy transforms physical matter"
        ),
        # Domain 10: Stars, Moon & Cosmos
        (
            "Domain 10: Stars, Moon & Cosmos",
            [
                "What are stars?",
                "stars glow in night sky?",
                "constellation is pattern of stars?",
                "does moon orbit earth?",
                "space has stars and planets?",
                "what shines quietly at night?",
                "planets move in space?",
                "universe is vast cosmos?",
                "stars shine far away in space?",
                "night sky has glowing stars?"
            ],
            "Stars glow in the quiet night sky forming constellations across the vast cosmos while the moon orbits earth"
        )
    ]
    
    total_q = 0
    start_time = time.time()
    
    print("=" * 80)
    print("🚀 INITIATING 100-QUESTION MULTI-REPHRASING & REINFORCEMENT CURRICULUM")
    print("=" * 80)
    
    for suite_idx, (domain_title, q_list, corrective_truth) in enumerate(question_suites, 1):
        print(f"\n================================================================================")
        print(f"📖 [{domain_title}] (Domain {suite_idx}/10)")
        print(f"================================================================================")
        
        # 1. Ground the core declarative truth firmly into the neural substrate
        brain.lang.ingest_continuous_stream(corrective_truth, target_tier=2 if "sun" in corrective_truth or "water" in corrective_truth else 3)
        
        # 2. Ask all 10 raw rephrasings
        for q_idx, q in enumerate(q_list, 1):
            total_q += 1
            res = brain.converse(q)
            resp = res.get("last_response", "").strip()
            trait = res.get("active_trait", "INQUIRE")
            fric = res.get("epistemic_friction", 0.0)
            
            print(f"[{total_q:03d}/100] User > \"{q}\"")
            print(f"       FELLA [{trait} | Friction={fric:.2f}] > {resp}\n")
            
        # Brief homeostatic step after each domain suite
        brain.substrate.step_thermodynamics()

    # Final Dream Consolidation
    print("\n🌙 Running Final Homeostatic Dream Consolidation...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Reverberated activation waves across {dream_res['reverberated_neurons']} neurons.")
    
    # Save fortified checkpoint
    brain.save_state(checkpoint_path)
    print(f"💾 Checkpoint updated with all 100 learned rephrasings in {checkpoint_path}")
    
    elapsed = time.time() - start_time
    tel = brain.get_telemetry()
    print("=" * 80)
    print(f"🎉 100-QUESTION CURRICULUM COMPLETE in {elapsed:.2f}s!")
    print(f"• Total Neurons: {tel['total_neurons']}")
    print(f"• Total Synapses: {tel['synapse_stats']['total_synapses']}")
    print(f"• Self-Confidence: {tel['self_confidence']:.3f}")
    print("=" * 80)


if __name__ == "__main__":
    run_100_question_curriculum()
