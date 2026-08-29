"""
Unit Test Suite for Metacognitive Pre-Articulatory Simulation
============================================================
Tests:
- Multi-candidate internal thought simulation
- Continuous Coherence & Valence evaluation Q(P)
- Reflexive tail-trimming of open pointers ('and', 'the', 'to')
- Verification on 'earth', 'gravity', 'volcano'
"""

import unittest
import numpy as np
from fella.core_substrate import StackedSubstrate
from fella.language_grounding import LanguageGroundingEngine
from fella.fella_brain import FellaBrain


class TestPreArticulatorySimulation(unittest.TestCase):
    def setUp(self):
        self.substrate = StackedSubstrate(dim=16)
        self.lang = LanguageGroundingEngine(self.substrate)

    def test_reflexive_tail_trimming(self):
        # Ingest sentence ending on a preposition/determiner
        self.lang.ingest_continuous_stream("earth is a terrestrial planet with crust and", target_tier=3)
        
        neurons = {n.text: n for n in self.substrate.neurons.values()}
        earth_id = neurons["earth"].id
        
        verified_tokens, score = self.lang.simulate_and_evaluate_thoughts(earth_id, max_candidates=3, max_depth=8)
        
        # Verify that trailing 'and' was reflexively trimmed
        self.assertNotEqual(verified_tokens[-1], "and")
        self.assertGreater(score, 0.40)

    def test_metacognitive_query_reasoning(self):
        self.lang.ingest_continuous_stream("volcanoes erupt molten liquid lava from deep earth", target_tier=3)
        
        res = self.lang.reason_over_query("What is a volcano?", max_depth=8)
        self.assertEqual(res["seed_concept"], "volcanoes")
        self.assertTrue(len(res["active_path"]) >= 2)
        self.assertIn("volcanoes", res["active_path"])
        self.assertTrue(any(w in res["active_path"] for w in ["lava", "molten", "earth", "erupt"]))
        # Ensure no trailing open pointer
        self.assertNotIn(res["active_path"][-1], ["from", "the", "and", "to"])

    def test_brain_simulation_dialogue(self):
        brain = FellaBrain(dim=16)
        brain.boot_foundations()
        
        brain.converse("The earth is a terrestrial planet with a solid crust and atmosphere")
        tel = brain.converse("What is earth?")
        
        resp = tel["last_response"]
        self.assertIn("earth", resp.lower())
        self.assertTrue(any(w in resp.lower() for w in ["planet", "crust", "atmosphere", "terrestrial"]))


if __name__ == "__main__":
    unittest.main()
