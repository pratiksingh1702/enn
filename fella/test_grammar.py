"""
Unit Test Suite for FELLA Continuous Cognitive Grammar Engine
============================================================
Tests:
- 4D Syntactic Valence Vectors [v_noun, v_verb, v_adj, v_pointer]
- Syntactic Tension Energy (H_syntax)
- Complete Sentence vs Incomplete Sentence Detection
- Broken Sentence Grammar Explanation & Auto-Correction
- Structured Thought Formulation (Subject + Verb + Object/Property)
"""

import unittest
import numpy as np
from fella.core_substrate import StackedSubstrate
from fella.language_grounding import LanguageGroundingEngine
from fella.fella_brain import FellaBrain


class TestFellaCognitiveGrammar(unittest.TestCase):
    def setUp(self):
        self.substrate = StackedSubstrate(dim=16)
        self.lang = LanguageGroundingEngine(self.substrate)

    def test_syntactic_valence_estimation(self):
        role_n, val_n, tier_n = self.lang.estimate_syntactic_valence("gravity")
        self.assertEqual(role_n, "noun")
        self.assertEqual(val_n[0], 1.0)
        self.assertEqual(tier_n, 1)

        role_v, val_v, tier_v = self.lang.estimate_syntactic_valence("radiates")
        self.assertEqual(role_v, "verb")
        self.assertEqual(val_v[1], 1.0)
        self.assertEqual(tier_v, 2)

        role_a, val_a, tier_a = self.lang.estimate_syntactic_valence("bright")
        self.assertEqual(role_a, "adj")
        self.assertEqual(val_a[2], 1.0)
        self.assertEqual(tier_a, 3)

        role_p, val_p, tier_p = self.lang.estimate_syntactic_valence("the")
        self.assertEqual(role_p, "pointer")
        self.assertEqual(val_p[3], -1.0)

    def test_well_formed_sentence_analysis(self):
        res_valid = self.lang.evaluate_syntactic_well_formedness("The sun radiates bright light")
        self.assertTrue(res_valid.is_valid)
        self.assertLess(res_valid.tension_energy, 0.20)
        self.assertEqual(res_valid.identified_subject, "sun")
        self.assertEqual(res_valid.identified_verb, "radiates")

    def test_broken_sentence_detection_trailing_determiner(self):
        res_broken = self.lang.evaluate_syntactic_well_formedness("The radiating sun is the")
        self.assertFalse(res_broken.is_valid)
        self.assertGreater(res_broken.tension_energy, 0.70)
        self.assertIn("Unresolved trailing token", res_broken.error_explanation)

    def test_broken_sentence_detection_missing_verb(self):
        res_broken = self.lang.evaluate_syntactic_well_formedness("The water liquid")
        self.assertFalse(res_broken.is_valid)
        self.assertIn("Missing predicate verb", res_broken.error_explanation)

    def test_brain_raw_dialogue(self):
        brain = FellaBrain(dim=16)
        brain.boot_foundations()
        
        # Ingest declarative knowledge
        brain.converse("The sun radiates bright light")
        
        # Query raw thought path
        tel = brain.converse("What does the sun do?")
        self.assertIn("sun", tel["last_response"].lower())


if __name__ == "__main__":
    unittest.main()
