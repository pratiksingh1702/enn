"""
FELLA Test Suite: Multi-Network Tiered Relational Verification
=============================================================
Verifies:
1. Multi-Network Tiered Substrate (Z=0..4) and Concept Deduplication
2. Relational Synaptic Bridges (is_a, causes, has_property, sustains)
3. Relational Triad Parsing & Knowledge Grounding
4. Semantic Wave Propagation Reasoning
5. Trait Attractor Dynamics & Inward Metacognition
6. Brain Booting, Dialogue & State Persistence
"""

import unittest
import numpy as np
import os
import json
import tempfile
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.core_substrate import StackedSubstrate, FellaNeuron
from fella.trait_field import TraitField
from fella.metacognition import InwardObserver, EpistemicVacuum
from fella.language_grounding import LanguageGroundingEngine
from fella.ollama_mentor import OllamaMentor
from fella.fella_brain import FellaBrain


class TestFellaCoreSubstrate(unittest.TestCase):
    def setUp(self):
        self.sub = StackedSubstrate(dim=8, decay_rate=0.01, pruning_threshold=0.05)

    def test_strict_concept_deduplication(self):
        x_sun = np.ones(8) * 0.5
        n1, created1 = self.sub.find_or_birth_concept("sun", x_sun, tier_z=1, network_id="net_celestial")
        self.assertTrue(created1)
        self.assertEqual(n1.text, "sun")
        self.assertEqual(n1.tier_z, 1)
        
        # Second insertion of "sun" MUST reuse existing neuron
        n2, created2 = self.sub.find_or_birth_concept("sun", x_sun, tier_z=1, network_id="net_celestial")
        self.assertFalse(created2)
        self.assertEqual(n1.id, n2.id)
        self.assertEqual(len(self.sub.neurons), 1)

    def test_relational_synaptic_bridges(self):
        x_water = np.ones(8) * 0.3
        x_vapor = np.ones(8) * 0.7
        n_water, _ = self.sub.find_or_birth_concept("water", x_water, tier_z=1, network_id="net_fluids")
        n_vapor, _ = self.sub.find_or_birth_concept("vapor", x_vapor, tier_z=2, network_id="net_states")
        
        # Build relational bridge
        w = self.sub.build_synaptic_bridge(n_water.id, n_vapor.id, 0.85, relation_type="transforms_into")
        self.assertAlmostEqual(w, 0.85)
        self.assertEqual(n_water.synapse_relations[n_vapor.id], "transforms_into")
        
        stats = self.sub.get_tier_and_network_stats()
        self.assertEqual(stats["cross_tier_synapses"], 1)
        self.assertEqual(stats["total_neurons"], 2)


class TestFellaTraitAndMetacognition(unittest.TestCase):
    def test_trait_attractor_dynamics(self):
        tf = TraitField(dim=4)
        active = tf.step(external_drive=np.array([0.9, 0.2, 0.8, 0.3]))
        self.assertEqual(active, "INQUIRE")
        
        tf.inject_aspiration(0.9)
        active_aspire = tf.step()
        self.assertIn(active_aspire, ["ASPIRE", "SYNTHESIZE", "INQUIRE"])

    def test_metacognitive_observer(self):
        obs = InwardObserver(base_plasticity=0.15)
        res_flow = obs.observe(np.ones(8) * 0.5, np.ones(8) * 0.5)
        self.assertLess(res_flow["epistemic_friction"], 0.1)
        self.assertGreater(res_flow["self_confidence"], 0.8)
        
        vac = obs.register_vacuum("quantum", context_z=2.0, tension=0.9)
        self.assertEqual(vac.concept_query, "quantum")
        self.assertFalse(vac.resolved)
        obs.resolve_vacuum(vac.vacuum_id, "Quantum physics is the study of matter and energy.")
        self.assertTrue(vac.resolved)


class TestFellaRelationalGroundingAndReasoning(unittest.TestCase):
    def setUp(self):
        self.sub = StackedSubstrate(dim=16)
        self.lang = LanguageGroundingEngine(self.sub)

    def test_continuous_stream_ingestion(self):
        nodes = self.lang.ingest_continuous_stream("the sun causes warmth water transforms into vapor", target_tier=1)
        self.assertGreaterEqual(len(nodes), 4)
        
        # Verify concept reuse
        neurons = {n.text: n for n in self.sub.neurons.values()}
        self.assertIn("sun", neurons)
        self.assertIn("warmth", neurons)
        self.assertIn("water", neurons)
        self.assertIn("vapor", neurons)
        
        # Verify physical bridge exists from sun to causes
        sun_n = neurons["sun"]
        self.assertGreater(len(sun_n.synapses), 0)

    def test_semantic_wave_reasoning(self):
        self.lang.ingest_continuous_stream("sun causes warmth and light", target_tier=1)
        
        # Query reasoning on 'sun'
        res = self.lang.reason_over_query("sun", max_depth=4)
        self.assertEqual(res["seed_concept"], "sun")
        self.assertIn("sun", res["reasoning_narrative"].lower())


class TestFellaBrainAndTrainer(unittest.TestCase):
    def test_brain_boot_and_converse(self):
        brain = FellaBrain(name="FELLA", dim=16)
        brain.boot_foundations()
        self.assertGreater(len(brain.substrate.neurons), 26)
        
        # Converse and verify relational integration
        tel = brain.converse("Sun shines warmly upon the earth")
        self.assertIn("active_trait", tel)
        self.assertGreater(tel["total_neurons"], 26)
        
        # Ask question to trigger reasoning
        q_tel = brain.converse("What does the sun do?")
        self.assertTrue(len(brain.dialogue_history) >= 4)

    def test_curiosity_cycle_and_dream(self):
        brain = FellaBrain(name="FELLA", dim=16)
        brain.boot_foundations()
        
        # Trigger curiosity cycle
        res = brain.autonomous_curiosity_cycle()
        if res:
            self.assertIn("explanation", res)
            self.assertIn("tier_z", res)
            
        # Dream consolidation
        dream_res = brain.dream_consolidation()
        self.assertIn("reverberated_neurons", dream_res)
        self.assertGreater(brain.observer.self_confidence, 0.8)

    def test_serialization_integrity(self):
        brain = FellaBrain(name="FELLA", dim=16)
        brain.boot_foundations()
        brain.converse("Stars radiate light in space")
        
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name
            
        try:
            brain.save_state(temp_path)
            loaded_brain = FellaBrain.load_state(temp_path)
            self.assertEqual(loaded_brain.name, "FELLA")
            self.assertEqual(len(loaded_brain.substrate.neurons), len(brain.substrate.neurons))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
