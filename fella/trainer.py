"""
FELLA Trainer: 5-Stage Continuous Developmental Curriculum Engine
================================================================
Pure First-Principles Implementation:
- Ingests raw continuous text streams into the stacked (X, Y, Z) manifold
- Forms intra-plane grapheme clusters at Z=0 based purely on inverse spatial distance
- Establishes Cross-Z Synaptic Bridges (W_ij) purely via continuous co-occurrence & causality
- Queries Ollama directly to resolve detected Epistemic Vacuums in real time
- Consolidates memory via homeostatic wave reverberation & thermodynamic pruning
"""

import time
import os
import sys
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain


class FellaTrainer:
    """Orchestrates the pure continuous developmental education of FELLA."""
    def __init__(self, brain: Optional[FellaBrain] = None, checkpoint_path: str = "fella_checkpoint.json"):
        self.brain = brain or FellaBrain(name="FELLA", dim=16)
        self.checkpoint_path = checkpoint_path

    def run_developmental_curriculum(self, curiosity_cycles: int = 3, verbose: bool = True) -> Dict[str, Any]:
        """Runs all 5 developmental training stages in sequential order."""
        start_time = time.time()
        print("=" * 70)
        print("🌟 FELLA: COMMENCING 5-STAGE DEVELOPMENTAL TRAINING CURRICULUM")
        print("=" * 70)
        
        # ---------------------------------------------------------
        # STAGE 1: Graphemes & Alphabet Grounding at Z=0
        # ---------------------------------------------------------
        print("\n[Stage 1/5]: Grounding Alphabet Graphemes at Z=0...")
        letters = self.brain.lang.ground_letter_layer()
        self.brain.boot_foundations()
        stats_s1 = self.brain.substrate.get_synapse_stats()
        print(f"  ✓ Grounded 26 Alphabet letters at baseline Z=0")
        print(f"  ✓ Total Neurons: {len(self.brain.substrate.neurons)} | Intra-Plane Synapses: {stats_s1['intra_plane_synapses']}")
        
        # ---------------------------------------------------------
        # STAGE 2: Foundational Environmental & Relational Streams
        # ---------------------------------------------------------
        print("\n[Stage 2/5]: Ingesting Foundational Sensorimotor Streams...")
        foundational_streams = [
            "sun warm light sky day",
            "water cool liquid rain stream ocean",
            "tree green leaf plant grow earth forest",
            "star night space cosmos glow quiet",
            "stone solid rock mountain heavy matter",
            "friend care love trust bond learn together"
        ]
        for stream in foundational_streams:
            ingested = self.brain.lang.ingest_continuous_stream(stream)
            if verbose:
                print(f"  • Ingested stream: '{stream}' -> {len(ingested)} nodes")
                
        stats_s2 = self.brain.substrate.get_synapse_stats()
        print(f"  ✓ Total Neurons: {len(self.brain.substrate.neurons)} | Active Synaptic Bridges: {stats_s2['total_synapses']}")

        # ---------------------------------------------------------
        # STAGE 3: Cross-Z Syntactic Stream Stacking (Grammar Flow)
        # ---------------------------------------------------------
        print("\n[Stage 3/5]: Ingesting Complex Grammatical Discourse...")
        discourse_streams = [
            "The bright sun warms the green trees and soil",
            "Gentle rain falls from clouds to nurture growing plants",
            "FELLA thinks and discovers new ideas every single day",
            "Distant stars radiate light across the cosmic darkness",
            "True friendship builds deep care and mutual trust"
        ]
        for s in discourse_streams:
            ingested = self.brain.lang.ingest_continuous_stream(s)
            if verbose:
                print(f"  • Ingested sequence: '{s}' -> {len(ingested)} Z-event nodes stacked")
                
        stats_s3 = self.brain.substrate.get_synapse_stats()
        print(f"  ✓ Cross-Z Syntactic Highways established!")
        print(f"  ✓ Cross-Z Synapses: {stats_s3['cross_z_inter_plane_synapses']} | Intra-Plane Synapses: {stats_s3['intra_plane_synapses']}")

        # ---------------------------------------------------------
        # STAGE 4: Autonomous Curiosity Loop with Ollama
        # ---------------------------------------------------------
        print(f"\n[Stage 4/5]: Triggering Autonomous Curiosity Loop with Ollama ({curiosity_cycles} Cycles)...")
        print(f"  [Mentor Status]: {'Online (' + self.brain.mentor.active_model + ')' if self.brain.mentor.is_online else 'Offline'}")
        
        curiosity_topics = ["evaporation", "photosynthesis", "gravity", "constellation"]
        for c_idx in range(min(curiosity_cycles, len(curiosity_topics))):
            topic = curiosity_topics[c_idx]
            vac = self.brain.observer.register_vacuum(
                concept_query=topic,
                context_z=self.brain.substrate.current_event_z,
                tension=0.9,
                context_prompt=f"Seeking deep understanding of natural phenomena ({topic})"
            )
            print(f"  [Inquiry Triggered]: '{topic}' (Tension: {vac.tension:.2f}) -> Active Trait: {self.brain.trait_field.active_trait}")
            
            result = self.brain.autonomous_curiosity_cycle()
            if result:
                print(f"  ✓ Assimilated from {result['mentor_model']} at Z={result['new_z_plane']:.1f}:")
                print(f"    \"{result['explanation'][:100]}...\"")
                print(f"    Synaptic bridges formed: {result['total_synapses']}")
                
        # ---------------------------------------------------------
        # STAGE 5: Homeostatic Dreaming & Synaptic Consolidation
        # ---------------------------------------------------------
        print("\n[Stage 5/5]: Entering Homeostatic Dream & Synaptic Consolidation...")
        dream_results = self.brain.dream_consolidation()
        print(f"  ✓ Reverberated activation waves across {dream_results['reverberated_neurons']} neurons")
        print(f"  ✓ Pruned {dream_results['pruned_synapses']} noisy synapses below critical threshold (W < 0.05)")
        print(f"  ✓ Metacognitive Confidence: {self.brain.observer.self_confidence:.3f} (Flow: {self.brain.observer.flow_state})")
        
        # Save master checkpoint
        self.brain.save_state(self.checkpoint_path)
        print(f"\n💾 Master Checkpoint successfully saved to: {os.path.abspath(self.checkpoint_path)}")
        
        elapsed = time.time() - start_time
        print("=" * 70)
        print(f"🎉 FELLA CURRICULUM COMPLETE in {elapsed:.2f}s | Active Neurons: {len(self.brain.substrate.neurons)}")
        print("=" * 70)
        
        return self.brain.get_telemetry()


if __name__ == "__main__":
    trainer = FellaTrainer()
    trainer.run_developmental_curriculum(curiosity_cycles=3)
