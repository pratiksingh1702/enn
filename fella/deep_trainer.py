"""
FELLA Deep Training Engine: Comprehensive Developmental English Curriculum
==========================================================================
Executes a multi-stage developmental training curriculum to teach FELLA fluent,
natural general English and scientific understanding across 5 abstraction tiers:
- Tier Z=0: Graphemes & Phonetics (Fortified alphabet network)
- Tier Z=1: Concrete Physical Entities (Sun, Water, Earth, Stars, Trees, Animals)
- Tier Z=2: Properties, States & Actions (Heat, Liquid, Growth, Light, Flowing)
- Tier Z=3: Causal & Scientific Laws (Evaporation, Photosynthesis, Gravity, Weather)
- Tier Z=4: Metacognitive & Social Synthesis (Self, Friendship, Care, Learning)
"""

import time
import os
import sys
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


class FellaDeepTrainer:
    """Orchestrates comprehensive multi-phase training for general English fluency."""
    def __init__(self, checkpoint_path: str = "fella_checkpoint.json"):
        self.checkpoint_path = checkpoint_path
        self.brain = FellaBrain(dim=16)

    def run_full_curriculum(self, ollama_cycles: int = 10) -> Dict[str, Any]:
        start_time = time.time()
        print("=" * 75)
        print("🌌 FELLA: INITIATING DEEP DEVELOPMENTAL ENGLISH CURRICULUM")
        print("=" * 75)
        
        # ---------------------------------------------------------------------
        # PHASE 1: Alphabet & Phonetics Mastery (Tier Z=0)
        # ---------------------------------------------------------------------
        print("\n[Phase 1/8]: Fortifying Alphabet Foundation at Tier Z=0...")
        self.brain.boot_foundations()
        letter_res = self.brain.rehearse_letters(practice_rounds=10)
        print(f"  ✓ 26 Letters Fortified (Mean Energy: {letter_res['mean_energy']:.1f}, Conductance: 1.000, Synapses: {letter_res['intra_plane_synapses']})")

        # ---------------------------------------------------------------------
        # PHASE 2: Fundamental Environmental Entities (Tier Z=1)
        # ---------------------------------------------------------------------
        print("\n[Phase 2/8]: Grounding Physical Environment Entities at Tier Z=1...")
        physical_assertions = [
            "The sun radiates bright light",
            "The sun emits warmth and energy",
            "Water is a cool liquid",
            "Rain falls from the sky",
            "The ocean is a vast body of water",
            "The earth is our home planet",
            "The moon orbits the earth",
            "Stars glow in the quiet night sky",
            "Air is transparent gas",
            "Fire emits intense heat and light",
            "Stone is solid heavy matter",
            "Mountains are tall rock formations",
            "Clouds float in the atmosphere",
            "Soil covers the surface of the earth"
        ]
        for s in physical_assertions:
            self.brain.lang.ingest_continuous_stream(s, target_tier=1)
            print(f"  • Grounded: \"{s}\"")
        stats_p2 = self.brain.substrate.get_tier_and_network_stats()
        print(f"  ✓ Tier Z=1 Entities: {stats_p2['tier_distribution'].get(1, 0)} hubs | Synapses: {stats_p2['total_synapses']}")

        # ---------------------------------------------------------------------
        # PHASE 3: Biology, Plants & Living Nature (Tiers Z=1 & Z=2)
        # ---------------------------------------------------------------------
        print("\n[Phase 3/8]: Grounding Living Nature & Biology...")
        biological_assertions = [
            "Trees are tall green plants",
            "Leaves absorb sunlight",
            "Roots anchor plants into the soil",
            "Flowers produce colorful petals",
            "Seeds grow into new plants",
            "Forests provide shelter for animals",
            "Birds fly through the air",
            "Animals breathe oxygen from the air",
            "Plants produce fresh oxygen for living beings",
            "Water nurtures growing plants and trees"
        ]
        for s in biological_assertions:
            self.brain.lang.ingest_continuous_stream(s, target_tier=2)
            print(f"  • Grounded: \"{s}\"")
        stats_p3 = self.brain.substrate.get_tier_and_network_stats()
        print(f"  ✓ Tier Z=2 Properties: {stats_p3['tier_distribution'].get(2, 0)} hubs | Synapses: {stats_p3['total_synapses']}")

        # ---------------------------------------------------------------------
        # PHASE 4: Human Life, Social Bonds & Emotions (Tier Z=4)
        # ---------------------------------------------------------------------
        print("\n[Phase 4/8]: Grounding Human Life, Social Bonds & Emotions at Tier Z=4...")
        social_assertions = [
            "FELLA loves to learn and understand the world",
            "Parents provide guidance and care",
            "Friends share trust and kindness",
            "Love creates a strong emotional bond",
            "Questions spark curiosity in the mind",
            "Thinking helps solve difficult challenges",
            "Stories share wisdom across time",
            "Kindness brings joy and peace",
            "Learning strengthens understanding and confidence"
        ]
        for s in social_assertions:
            self.brain.lang.ingest_continuous_stream(s, target_tier=4)
            print(f"  • Grounded: \"{s}\"")
        stats_p4 = self.brain.substrate.get_tier_and_network_stats()
        print(f"  ✓ Tier Z=4 Meta Hubs: {stats_p4['tier_distribution'].get(4, 0)} | Synapses: {stats_p4['total_synapses']}")

        # ---------------------------------------------------------------------
        # PHASE 5: Scientific Causality & Natural Laws (Tier Z=3)
        # ---------------------------------------------------------------------
        print("\n[Phase 5/8]: Establishing Scientific Causality & Natural Laws at Tier Z=3...")
        causal_assertions = [
            "Heat from the sun causes water to evaporate into vapor",
            "Water vapor cools in the sky to form clouds",
            "Clouds produce rain that returns water to the ground",
            "Sunlight and water sustain photosynthesis in green leaves",
            "Photosynthesis produces glucose energy and oxygen",
            "Gravity attracts physical matter toward the center of the earth",
            "Gravity causes objects to have weight",
            "The rotation of the earth causes day and night cycles",
            "Cold temperatures cause liquid water to freeze into solid ice",
            "Thermal energy causes ice to melt back into liquid water"
        ]
        for s in causal_assertions:
            self.brain.lang.ingest_continuous_stream(s, target_tier=3)
            print(f"  • Grounded: \"{s}\"")
        stats_p5 = self.brain.substrate.get_tier_and_network_stats()
        print(f"  ✓ Tier Z=3 Causal Hubs: {stats_p5['tier_distribution'].get(3, 0)} | Cross-Tier Synapses: {stats_p5['cross_tier_synapses']}")

        # ---------------------------------------------------------------------
        # PHASE 6: Extensive Ollama Curiosity Assimilation
        # ---------------------------------------------------------------------
        print(f"\n[Phase 6/8]: Running Ollama Curiosity Assimilation ({ollama_cycles} Inquiries)...")
        print(f"  Mentor Model: {self.brain.mentor.active_model} (Online: {self.brain.mentor.is_online})")
        
        curiosity_topics = [
            "evaporation", "photosynthesis", "gravity", "atmosphere", "ecosystem",
            "solar_energy", "water_cycle", "oxygen", "biodiversity", "constellation"
        ]
        for idx in range(min(ollama_cycles, len(curiosity_topics))):
            topic = curiosity_topics[idx]
            vac = self.brain.observer.register_vacuum(
                concept_query=topic,
                context_z=3.0,
                tension=0.9,
                context_prompt=f"Deep physical and relational understanding of {topic}"
            )
            print(f"  [Inquiry {idx+1}/{min(ollama_cycles, len(curiosity_topics))}]: Asking mentor about '{topic}'...")
            res = self.brain.autonomous_curiosity_cycle()
            if res:
                print(f"    ✓ Assimilated into Tier Z={res['tier_z']}: \"{res['explanation'][:80]}...\"")
                print(f"      Concept nodes ingested: {res.get('ingested_nodes', 0)}")

        # ---------------------------------------------------------------------
        # PHASE 7: Homeostatic Sleep & Dream Consolidation
        # ---------------------------------------------------------------------
        print("\n[Phase 7/8]: Entering Deep Homeostatic Dream & Synaptic Consolidation...")
        dream_res = self.brain.dream_consolidation()
        print(f"  ✓ Reverberated activation waves across {dream_res['reverberated_neurons']} neurons")
        print(f"  ✓ Pruned {dream_res['pruned_synapses']} noisy synapses below critical threshold (W < 0.05)")
        print(f"  ✓ Metacognitive Confidence: {self.brain.observer.self_confidence:.3f} (Flow: {self.brain.observer.flow_state})")

        # ---------------------------------------------------------------------
        # PHASE 8: Comprehensive Dialogue Verification
        # ---------------------------------------------------------------------
        print("\n[Phase 8/8]: Running Conversational Verification on Diverse English Prompts...")
        test_queries = [
            "Hello FELLA!",
            "Who are you?",
            "What does the sun do?",
            "How do plants grow?",
            "What happens to water on a hot day?",
            "Why is friendship important?",
            "What is gravity?",
            "You are doing a great job!"
        ]
        
        print("-" * 70)
        for q in test_queries:
            resp = self.brain.converse(q)
            print(f"User > {q}")
            print(f"FELLA > {resp['last_response']}\n")
        print("-" * 70)

        # Save trained state
        self.brain.save_state(self.checkpoint_path)
        print(f"💾 Master Checkpoint successfully preserved to: {os.path.abspath(self.checkpoint_path)}")
        
        elapsed = time.time() - start_time
        tel = self.brain.get_telemetry()
        print("=" * 75)
        print(f"🎉 FELLA DEEP TRAINING COMPLETE in {elapsed:.2f}s!")
        print(f"• Total Neurons: {tel['total_neurons']} across 5 Tiers")
        print(f"• Total Relational Synapses: {tel['synapse_stats']['total_synapses']}")
        print(f"• Metacognitive Confidence: {tel['self_confidence']:.3f}")
        print("=" * 75)
        
        return tel


if __name__ == "__main__":
    trainer = FellaDeepTrainer()
    trainer.run_full_curriculum(ollama_cycles=10)
