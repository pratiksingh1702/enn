"""
FELLA Brain: Multi-Network Tiered Cognitive Organism
===================================================
Coordinates the Relational Multi-Network Cognitive Mind Loop:
1. Multi-Network Tiered Substrate (Z=0 Letters, Z=1 Entities, Z=2 Properties, Z=3 Causal, Z=4 Meta)
2. Trait Field (Attractor Basins: INQUIRE, ASPIRE, SYNTHESIZE, SELF_IDENTITY, CAUTION, AFFIRM)
3. Inward Metacognitive Observer (Epistemic Friction, Self-Confidence, Knowledge Vacuums)
4. Relational Triad Grounding & Wave Propagation Reasoning
5. Autonomous Ollama Mentor Assimilation into Existing Network Hubs
6. Homeostatic Dream Consolidation & Synaptic Pruning
"""

import numpy as np
import time
import json
import re
from typing import Dict, Any, List, Optional, Tuple

from fella.core_substrate import StackedSubstrate, FellaNeuron
from fella.trait_field import TraitField
from fella.metacognition import InwardObserver, EpistemicVacuum
from fella.language_grounding import LanguageGroundingEngine
from fella.ollama_mentor import OllamaMentor


class FellaBrain:
    """The complete living multi-network cognitive mind of FELLA."""
    def __init__(
        self,
        name: str = "FELLA",
        dim: int = 16,
        substrate: Optional[StackedSubstrate] = None,
        ollama_model: Optional[str] = None
    ):
        self.name = str(name)
        self.dim = int(dim)
        
        # 1. Multi-Network Tiered Substrate
        self.substrate = substrate or StackedSubstrate(dim=self.dim)
        
        # 2. Continuous Trait Drive Field
        self.trait_field = TraitField(dim=4)
        
        # 3. Metacognitive Inward Observer
        self.observer = InwardObserver(base_plasticity=0.15)
        
        # 4. Relational Language & Reasoning Engine
        self.lang = LanguageGroundingEngine(self.substrate)
        
        # 5. External Mentor Interface
        self.mentor = OllamaMentor(default_model=ollama_model)
        
        # Internal Memory & Lifespan
        self.age_steps = 0
        self.dialogue_history: List[Dict[str, str]] = []
        self.last_thought: str = "Multi-network tiered manifold active"
        self.last_response: str = "FELLA initialized."
        self.learned_insights: List[str] = []

    def boot_foundations(self):
        """Seeds the baseline alphabet network at Z=0 and foundational self-network at Z=4."""
        # 1. Grapheme foundation at Tier Z=0
        letter_count = len([n for n in self.substrate.neurons.values() if n.tier_z == 0])
        if letter_count == 0:
            self.lang.ground_letter_layer()
            self.lang.rehearse_and_fortify_alphabet(practice_rounds=5)
            
        # 2. Self-Model & Social Anchor at Tier Z=4 (Meta Tier)
        self.substrate.current_event_z = 4.0
        x_self = self.lang.encode_continuous_wave(self.name.lower())
        self.substrate.find_or_birth_concept(
            text=self.name.lower(),
            x_vec=x_self,
            tier_z=4,
            network_id="self_model",
            role="anchor",
            energy=5.0
        )

    def rehearse_letters(self, practice_rounds: int = 5) -> Dict[str, Any]:
        """Fortifies the Z=0 alphabet foundation."""
        res = self.lang.rehearse_and_fortify_alphabet(practice_rounds=practice_rounds)
        self.last_thought = f"Rehearsed alphabet across {practice_rounds} continuous cycles"
        return res

    def converse(self, user_speech: str) -> Dict[str, Any]:
        """
        Interactive Conversational Cycle:
        1. Encodes speech wave X_sensory and evaluates resonance.
        2. Measures Epistemic Friction and Self-Confidence.
        3. Detects novel concepts -> logs Epistemic Vacuum if high tension.
        4. Updates Trait Attractor Basin dynamics.
        5. Ingests structured relational triads, binding directly into existing network hubs.
        6. Performs Semantic Wave Reasoning over the active conceptual graph.
        7. Synthesizes a grounded, conscious response reflecting internal reasoning.
        """
        self.age_steps += 1
        text_clean = str(user_speech).strip()
        if not text_clean:
            return self.get_telemetry()
            
        self.dialogue_history.append({"speaker": "User", "text": text_clean})
        
        # 1. Sensory Wave Encoding & Field Resonance
        x_sensory = self.lang.encode_continuous_wave(text_clean)
        forces = self.substrate.compute_field_resonance(x_sensory)
        
        # Filter non-letter resonance to evaluate semantic novelty
        semantic_forces = {
            nid: f for nid, f in forces.items()
            if self.substrate.neurons[nid].tier_z > 0
        }
        max_resonance = max(semantic_forces.values()) if semantic_forces else 0.0
        
        # 2. Metacognitive Observation
        best_neuron = None
        if semantic_forces:
            best_id = max(semantic_forces.items(), key=lambda it: it[1])[0]
            best_neuron = self.substrate.neurons[best_id]
            expected_x = best_neuron.x
        else:
            expected_x = None
            
        self.observer.observe(expected_x, x_sensory)
        
        # 3. Trait Attractor Basin Dynamics
        is_question = bool("?" in text_clean or re.match(r'^(what|why|how|who|where|when|which|can|could|would|does|do|is\s+it|explain|tell)\b', text_clean.lower()))
        drive_vec = np.array([
            0.85 if is_question else (1.0 - max_resonance),  # Curiosity / Inquiry
            float(np.mean(x_sensory[:4])) + 0.3,             # Complexity / Aspiration
            max_resonance,                                   # Coherence / Synthesis
            float(np.std(x_sensory))                         # Self-Identity
        ])
        active_trait = self.trait_field.step(external_drive=drive_vec)
        
        # 4. Syntactic Analysis & Grammar Well-Formedness
        syntax_analysis = self.lang.evaluate_syntactic_well_formedness(text_clean)
        
        # Ingest Declarative Knowledge (Only when user is teaching valid complete sentences)
        ingested_nodes = []
        if not is_question and syntax_analysis.is_valid:
            ingested_nodes = self.lang.ingest_continuous_stream(text_clean, target_tier=int(round(self.substrate.current_event_z)))
        
        # 5. Novelty & Epistemic Vacuum Detection
        novelty = 1.0 - max_resonance
        if novelty > 0.55 and len(text_clean.split()) > 0:
            words = [w for w in text_clean.split() if len(w) > 2]
            if words:
                target_word = words[0] if is_question and len(words) > 1 else words[-1]
                self.observer.register_vacuum(
                    concept_query=target_word,
                    context_z=self.substrate.current_event_z,
                    tension=float(novelty),
                    context_prompt=text_clean
                )
                self.trait_field.inject_curiosity(float(novelty))
                
        # 6. Semantic Wave Reasoning over Query (Raw Synaptic Trajectory Traversal)
        reasoning_res = self.lang.reason_over_query(text_clean, max_depth=6)
        raw_narrative = reasoning_res.get("reasoning_narrative", "")
        seed_concept = reasoning_res.get("seed_concept", "")
        
        # 7. Formulate Raw Physical Response
        if is_question and raw_narrative:
            response_text = f"{raw_narrative}"
        elif len(ingested_nodes) > 0:
            integrated_path = " -> ".join([n.text for n in ingested_nodes])
            if raw_narrative and raw_narrative != text_clean.lower():
                response_text = f"[{integrated_path}] ==> {raw_narrative}"
            else:
                response_text = f"[{integrated_path}]"
        elif raw_narrative:
            response_text = f"{raw_narrative}"
        else:
            response_text = f"[{text_clean.lower()}]"
            
        self.last_thought = f"Excited '{seed_concept}' along W_ij (Trait: {active_trait}, Tension: {syntax_analysis.tension_energy:.2f})"
        self.last_response = response_text
        self.dialogue_history.append({"speaker": "FELLA", "text": response_text})
        
        # 8. Step Thermodynamics
        self.substrate.step_thermodynamics()
        
        return self.get_telemetry()

    def autonomous_curiosity_cycle(self) -> Optional[Dict[str, Any]]:
        """
        Autonomous Curiosity Self-Education:
        1. Selects highest-tension Epistemic Vacuum.
        2. Injects INQUIRE & ASPIRE trait drives.
        3. Queries local Ollama mentor.
        4. Distills explanation into relational assertions and binds into existing entity hubs!
        """
        vacuum = self.observer.get_highest_priority_vacuum()
        if not vacuum:
            candidates = [n for n in self.substrate.neurons.values() if n.tier_z > 0 and len(n.text) > 2]
            if not candidates:
                return None
            chosen = np.random.choice(candidates)
            vacuum = self.observer.register_vacuum(
                concept_query=chosen.text,
                context_z=float(chosen.tier_z),
                tension=0.75,
                context_prompt=f"Seeking deep relational understanding of {chosen.text}"
            )
            
        self.trait_field.inject_curiosity(0.8)
        self.trait_field.inject_aspiration(0.65)
        
        mentor_bundle = self.mentor.ask_about_vacuum(vacuum)
        explanation = mentor_bundle["explanation"]
        
        if not explanation:
            explanation = f"{vacuum.concept_query} is an important phenomenon in nature that affects energy and physical matter."
            
        # Ingest mentor explanation through continuous stream engine
        ingested = self.lang.ingest_continuous_stream(explanation, target_tier=3)
        
        # Ensure the vacuum concept itself is deeply grounded at Tier Z=3 (Causal Law)
        x_vac = self.lang.encode_continuous_wave(vacuum.concept_query)
        y_vac = self.lang.encode_efferent_output(x_vac)
        focus_n, _ = self.substrate.find_or_birth_concept(
            text=vacuum.concept_query,
            x_vec=x_vac,
            y_vec=y_vac,
            tier_z=3,
            network_id=f"net_{vacuum.concept_query[:4]}",
            role="causal",
            energy=3.0
        )
        
        # Resolve vacuum
        self.observer.resolve_vacuum(vacuum.vacuum_id, explanation)
        self.trait_field.step(external_drive=np.array([0.3, 0.9, 0.8, 0.5]))
        
        self.last_thought = f"Assimilated '{vacuum.concept_query}' from mentor, bound into Tier Z={focus_n.tier_z}"
        
        return {
            "vacuum_id": vacuum.vacuum_id,
            "concept": vacuum.concept_query,
            "mentor_model": mentor_bundle["mentor_model"],
            "explanation": explanation,
            "ingested_nodes": len(ingested),
            "tier_z": focus_n.tier_z,
            "focus_neuron_id": focus_n.id,
            "total_synapses": len(focus_n.synapses)
        }

    def dream_consolidation(self) -> Dict[str, Any]:
        """Homeostatic Dream Consolidation: strengthens high-utility concept pathways & prunes noise."""
        seed_neurons = [n.id for n in self.substrate.neurons.values() if n.energy > 2.0 or n.role in ["anchor", "causal"]]
        if not seed_neurons and self.substrate.neurons:
            seed_neurons = list(self.substrate.neurons.keys())[:8]
            
        wave_map = self.substrate.propagate_wave(seed_neurons, max_hops=4, damping=0.7)
        self.substrate.potentiate_hebbian(wave_map, learning_rate=0.10)
        
        stats = self.substrate.step_thermodynamics()
        syn_stats = self.substrate.get_synapse_stats()
        
        self.observer.epistemic_friction = 0.02
        self.observer.self_confidence = 0.97
        self.trait_field.active_trait = "AFFIRM"
        self.last_thought = "Waking peacefully from deep consolidation dream"
        
        return {
            "reverberated_neurons": len(wave_map),
            "pruned_synapses": stats["pruned_synapses"],
            "total_neurons": stats["total_neurons"],
            "restored_confidence": float(self.observer.self_confidence),
            "active_trait": self.trait_field.active_trait,
            "synapse_stats": syn_stats
        }

    def reward_cognition(self, reward_value: float = 1.0, active_tokens: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Positive Reinforcement Dynamics:
        1. Drives TraitField into ASPIRE & AFFIRM (curiosity satisfaction, confidence, joy).
        2. Strengthens active synaptic pathways via Hebbian potentiation.
        3. Boosts metabolic energy of active concept nodes.
        4. Increases metacognitive self-confidence index.
        """
        # Drive traits: Boost ASPIRE (growth) and AFFIRM (joy/confidence)
        self.trait_field.step(external_drive=np.array([0.15, 0.95, 0.40, 0.85]))
        self.trait_field.active_trait = "ASPIRE"
        
        # Metacognitive boost
        self.observer.self_confidence = float(np.clip(self.observer.self_confidence + 0.05 * reward_value, 0.1, 0.999))
        self.observer.epistemic_friction = float(np.clip(self.observer.epistemic_friction * 0.85, 0.01, 1.0))
        
        # Strengthen active concept neurons
        potentiated_count = 0
        if active_tokens:
            tok_set = {t.lower() for t in active_tokens}
            active_neurons = [n for n in self.substrate.neurons.values() if n.text.lower() in tok_set]
            for n in active_neurons:
                n.energy = float(np.clip(n.energy + 0.4 * reward_value, 0.5, 5.0))
                for tid in list(n.synapses.keys()):
                    if tid in self.substrate.neurons and self.substrate.neurons[tid].text.lower() in tok_set:
                        n.synapses[tid] = float(np.clip(n.synapses[tid] + 0.12 * reward_value, 0.05, 1.0))
                        potentiated_count += 1
                        
        self.last_thought = f"Rewarded cognition (+{reward_value:.2f}) -> Trait: ASPIRE (Confidence: {self.observer.self_confidence:.3f})"
        return {
            "reward": reward_value,
            "active_trait": self.trait_field.active_trait,
            "self_confidence": self.observer.self_confidence,
            "potentiated_synapses": potentiated_count
        }

    def penalize_cognition(
        self,
        penalty_value: float = 1.0,
        active_tokens: Optional[List[str]] = None,
        corrective_explanation: str = ""
    ) -> Dict[str, Any]:
        """
        Constructive Negative Feedback & Teacher Correction:
        1. Shifts TraitField into CAUTION & INQUIRE (vigilance, error-awareness, curiosity).
        2. Depresses faulty synapses.
        3. Ingests the correct explanation into continuous (X,Y,Z) memory with high plasticity.
        4. Adjusts metacognitive confidence.
        """
        # Drive traits: Shift to CAUTION (error inspection) and INQUIRE (curiosity)
        self.trait_field.step(external_drive=np.array([0.85, 0.10, 0.20, 0.90]))
        self.trait_field.active_trait = "CAUTION"
        
        # Metacognitive caution
        self.observer.self_confidence = float(np.clip(self.observer.self_confidence - 0.05 * penalty_value, 0.05, 0.95))
        self.observer.epistemic_friction = float(np.clip(self.observer.epistemic_friction + 0.15 * penalty_value, 0.05, 1.0))
        
        # Depress faulty pathways
        depressed_count = 0
        if active_tokens:
            tok_set = {t.lower() for t in active_tokens}
            active_neurons = [n for n in self.substrate.neurons.values() if n.text.lower() in tok_set]
            for n in active_neurons:
                for tid in list(n.synapses.keys()):
                    if tid in self.substrate.neurons and self.substrate.neurons[tid].text.lower() in tok_set:
                        n.synapses[tid] = float(np.clip(n.synapses[tid] - 0.10 * penalty_value, 0.05, 1.0))
                        depressed_count += 1
                        
        # Ingest corrective explanation into memory
        ingested_nodes = []
        if corrective_explanation:
            ingested_nodes = self.lang.ingest_continuous_stream(
                corrective_explanation,
                target_tier=3,
                learning_rate=0.35
            )
            
        self.last_thought = f"Corrected cognition (-{penalty_value:.2f}) -> Trait: CAUTION, Ingested {len(ingested_nodes)} corrective nodes"
        return {
            "penalty": penalty_value,
            "active_trait": self.trait_field.active_trait,
            "self_confidence": self.observer.self_confidence,
            "depressed_synapses": depressed_count,
            "corrective_nodes": len(ingested_nodes)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        syn_stats = self.substrate.get_synapse_stats()
        tier_stats = self.substrate.get_tier_and_network_stats()
        return {
            "name": self.name,
            "age_steps": self.age_steps,
            "current_event_z": float(self.substrate.current_event_z),
            "total_neurons": len(self.substrate.neurons),
            "tier_distribution": tier_stats["tier_distribution"],
            "network_distribution": tier_stats["network_distribution"],
            "synapse_stats": syn_stats,
            "active_trait": self.trait_field.active_trait,
            "trait_energy": self.trait_field.trait_energy,
            "epistemic_friction": self.observer.epistemic_friction,
            "self_confidence": self.observer.self_confidence,
            "plasticity": self.observer.plasticity,
            "flow_state": self.observer.flow_state,
            "active_vacuums": len([v for v in self.observer.vacuums.values() if not v.resolved]),
            "last_thought": self.last_thought,
            "last_response": self.last_response,
            "ollama_online": self.mentor.is_online,
            "ollama_model": self.mentor.active_model
        }

    def save_state(self, filepath: str):
        data = {
            "name": self.name,
            "age_steps": self.age_steps,
            "substrate": self.substrate.to_dict(),
            "trait_field": self.trait_field.to_dict(),
            "observer": self.observer.to_dict()
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_state(cls, filepath: str) -> 'FellaBrain':
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        substrate = StackedSubstrate.from_dict(data["substrate"])
        brain = cls(name=str(data.get("name", "FELLA")), dim=substrate.dim, substrate=substrate)
        brain.age_steps = int(data.get("age_steps", 0))
        brain.learned_insights = list(data.get("learned_insights", []))
        brain.dialogue_history = list(data.get("dialogue_history", []))
        brain.trait_field = TraitField.from_dict(data["trait_field"])
        brain.observer = InwardObserver.from_dict(data["observer"])
        return brain
