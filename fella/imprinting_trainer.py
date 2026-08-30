"""
FELLA Resonant Imprinting Trainer: Progressive Multi-Stage Continuous Protocol
==============================================================================
Implements the 24-Hour Resonant Imprinting Protocol:
1. Syntactic Spine (Stages 1 through 5: Kernels -> Modifiers -> Compounds -> Subordination -> Recursion)
2. Semantic Web (5 Conceptual Realms: Entities -> Processes -> Gravity/Cosmology -> Social -> Scientific)
3. Conversational Context & Q&A Phase Coupling
4. Homeostatic Wave Consolidation & Anti-Hebbian Lateral Pruning
5. Checkpoint Fortification
"""

import sys
import os
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain
from fella.imprinting_corpus import get_full_imprinting_curriculum


class ResonantImprintingTrainer:
    """Executes the progressive resonant imprinting curriculum into FELLA's 4D neural field."""
    def __init__(self, checkpoint_path: str = "fella_checkpoint.json", dim: int = 16):
        self.checkpoint_path = checkpoint_path
        self.dim = dim
        self.brain = FellaBrain(dim=dim)
        self.brain.boot_foundations()
        
    def imprint_curriculum(self):
        print("=" * 80)
        print("🌌 FELLA: 24-HOUR RESONANT IMPRINTING PROTOCOL")
        print("   Executing progressive multi-stage 4D neural field imprinting")
        print("=" * 80)
        
        curriculum = get_full_imprinting_curriculum()
        
        # ----------------------------------------------------------------------
        # PHASE 1: SYNTACTIC SPINE IMPRINTING (Stages 1 to 5)
        # ----------------------------------------------------------------------
        print("\n" + "=" * 70)
        print("⚡ PHASE 1: SYNTACTIC SPINE IMPRINTING (Hierarchical Attractor Basins)")
        print("=" * 70)
        
        stages = [
            ("Stage 1: Simple SVO & SV Kernels", curriculum["spine_stage_1"], 1, 0.60),
            ("Stage 2: Property & Spatial Modifiers", curriculum["spine_stage_2"], 2, 0.55),
            ("Stage 3: Compound Subjects & Objects", curriculum["spine_stage_3"], 2, 0.50),
            ("Stage 4: Complex Subordination & Causation", curriculum["spine_stage_4"], 3, 0.45),
            ("Stage 5: Recursive Nested Multi-Clause Structures", curriculum["spine_stage_5"], 3, 0.40),
        ]
        
        for name, sentences, tier, lr in stages:
            print(f"\n▶ Imprinting [{name}] ({len(sentences)} structured patterns, Tier Z={tier}, LR={lr:.2f})...")
            start_t = time.time()
            for sentence in sentences:
                self.brain.lang.ingest_continuous_stream(sentence, target_tier=tier, learning_rate=lr)
            elapsed = time.time() - start_t
            syn_stats = self.brain.substrate.get_synapse_stats()
            print(f"  ✓ Stage complete in {elapsed:.3f}s | Active Neurons: {len(self.brain.substrate.neurons)} | Synaptic Bridges: {syn_stats['total_synapses']}")
            
        # Mid-Phase Consolidation
        print("\n🌙 Running Homeostatic Wave Consolidation after Syntactic Spine...")
        c_res = self.brain.dream_consolidation()
        print(f"  ✓ Consolidation Complete: Pruned {c_res.get('pruned_synapses', 0)} noisy bridges.")

        # ----------------------------------------------------------------------
        # PHASE 2: SEMANTIC WEB IMPRINTING (5 Conceptual Realms)
        # ----------------------------------------------------------------------
        print("\n" + "=" * 70)
        print("🌐 PHASE 2: SEMANTIC WEB IMPRINTING (Concepts, Processes & Physics)")
        print("=" * 70)
        
        realms = [
            ("Realm 1: Concrete Physical Entities", curriculum["semantic_entities"], 2, 0.50),
            ("Realm 2: Energy & Biochemical Processes", curriculum["semantic_energy"], 3, 0.50),
            ("Realm 3: Gravity, Curvature & Cosmology", curriculum["semantic_gravity"], 3, 0.50),
            ("Realm 4: Social, Emotional & Ethical Bonds", curriculum["semantic_social"], 4, 0.50),
            ("Realm 5: Scientific, Metacognitive & Universal Laws", curriculum["semantic_scientific"], 4, 0.45)
        ]
        
        for name, sentences, tier, lr in realms:
            print(f"\n▶ Imprinting [{name}] ({len(sentences)} semantic definitions, Tier Z={tier})...")
            start_t = time.time()
            for sentence in sentences:
                self.brain.lang.ingest_continuous_stream(sentence, target_tier=tier, learning_rate=lr)
            elapsed = time.time() - start_t
            syn_stats = self.brain.substrate.get_synapse_stats()
            print(f"  ✓ Realm complete in {elapsed:.3f}s | Active Neurons: {len(self.brain.substrate.neurons)} | Synapses: {syn_stats['total_synapses']}")

        # ----------------------------------------------------------------------
        # PHASE 3: CONVERSATIONAL CONTEXT & Q&A PHASE COUPLING
        # ----------------------------------------------------------------------
        print("\n" + "=" * 70)
        print("💬 PHASE 3: CONVERSATIONAL Q&A RESONANCE COUPLING")
        print("=" * 70)
        
        qa_pairs = curriculum["conversational_qa"]
        print(f"▶ Coupling {len(qa_pairs)} conversational question-answer manifolds...")
        start_t = time.time()
        for q, a in qa_pairs:
            # Ingest answer as high-conductance target highway
            self.brain.lang.ingest_continuous_stream(a, target_tier=3, learning_rate=0.55)
            # Synaptically link question content words to answer highway
            q_tokens = [t.strip('.,;:"\'?').lower() for t in q.split() if len(t.strip('.,;:"\'?')) > 3]
            a_tokens = [t.strip('.,;:"\'?').lower() for t in a.split() if len(t.strip('.,;:"\'?')) > 3]
            if q_tokens and a_tokens:
                q_neurons = [n for n in self.brain.substrate.neurons.values() if n.text.lower() == q_tokens[0]]
                a_neurons = [n for n in self.brain.substrate.neurons.values() if n.text.lower() == a_tokens[0]]
                if q_neurons and a_neurons:
                    self.brain.substrate.build_synaptic_bridge(q_neurons[0].id, a_neurons[0].id, 0.95)
                    
        elapsed = time.time() - start_t
        print(f"  ✓ Conversational coupling complete in {elapsed:.3f}s.")

        # ----------------------------------------------------------------------
        # PHASE 4: FINAL HOMEOSTATIC WAVE CONSOLIDATION & PRUNING
        # ----------------------------------------------------------------------
        print("\n" + "=" * 70)
        print("✨ PHASE 4: FINAL HOMEOSTATIC CONSOLIDATION & CHECKPOINT FORTIFICATION")
        print("=" * 70)
        
        dream_stats = self.brain.dream_consolidation()
        pruned = self.brain.substrate.prune_cross_talk_synapses(threshold=0.35, max_fanout=14)
        
        self.brain.save_state(self.checkpoint_path)
        final_syn = self.brain.substrate.get_synapse_stats()
        
        print(f"✓ Checkpoint saved successfully to '{self.checkpoint_path}'!")
        print(f"  • Total Physical Living Neurons : {len(self.brain.substrate.neurons)}")
        print(f"  • Total High-Conductance Synapses: {final_syn['total_synapses']}")
        print(f"  • Intra-Plane Relational Bridges : {final_syn['intra_plane_synapses']}")
        print(f"  • Inter-Tier Abstraction Bridges : {final_syn['cross_z_inter_plane_synapses']}")
        print("=" * 80)
        return self.brain


if __name__ == "__main__":
    trainer = ResonantImprintingTrainer()
    trainer.imprint_curriculum()
