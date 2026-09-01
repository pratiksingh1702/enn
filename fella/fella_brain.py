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
from collections import defaultdict

from fella.core_substrate import StackedSubstrate, FellaNeuron
from fella.trait_field import TraitField
from fella.metacognition import InwardObserver, EpistemicVacuum
from fella.language_grounding import LanguageGroundingEngine
from fella.ollama_mentor import OllamaMentor
from fella.heartbeat import CognitiveHeartbeat

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
        
        # 4. Relational Language & Reasoning Engine (Legacy Grounding)
        self.lang = LanguageGroundingEngine(self.substrate)
        
        # 4.5 True Wave Physics Engine (The core of Tabula Rasa)
        from fella.wave_physics_engine import WavePhysicsEngine
        self.wave_engine = WavePhysicsEngine(self.substrate, self.lang)
        
        # 5. External Mentor Interface
        self.mentor = OllamaMentor(default_model=ollama_model)
        
        # 6. Autonomous Background Heartbeat (True Learner / Dreaming)
        self.heartbeat = CognitiveHeartbeat(brain=self, pulse_interval=10.0)
        self.heartbeat.start()
        
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
        
        # The uncertainty anchor is removed. FELLA now uses emergent [Void] gaps.

    def rehearse_letters(self, practice_rounds: int = 5) -> Dict[str, Any]:
        """Fortifies the Z=0 alphabet foundation."""
        res = self.lang.rehearse_and_fortify_alphabet(practice_rounds=practice_rounds)
        self.last_thought = f"Rehearsed alphabet across {practice_rounds} continuous cycles"
        return res







    def converse(self, user_speech: str, autonomous_exploration: bool = False, speaker_id: str = "user", listener_id: str = "fella") -> Dict[str, Any]:
        self.age_steps += 1
        text_clean = str(user_speech).strip()
        if not text_clean:
            return self.get_telemetry()
            
        self.dialogue_history.append({"speaker": speaker_id, "text": text_clean})
        
        origin_node = self.wave_engine._get_or_create_neuron(speaker_id)
        anti_origin_node = self.wave_engine._get_or_create_neuron(listener_id)
        
        wave_state = self.wave_engine.parse_simultaneous_wave(
            text_clean, 
            origin_node=origin_node, 
            anti_origin_node=anti_origin_node
        )
        
        response_text = ""
        is_question = (wave_state.get("state") == "DESTRUCTIVE (VOID)")
        
        if is_question:
            void_targets = [op["target"] for op in wave_state.get("operations", []) if op["action"] == "void"]
            target_id = void_targets[0] if void_targets else None
            if target_id is not None:
                target_word = self.substrate.neurons[target_id].text
                
                # Retrieval Attempt (Wave Superposition / Concept Blooming)
                found_answer = False
                if self.wave_engine.determine_spectron_type(self.substrate.neurons[target_id]) == "hot":
                    words = text_clean.replace("?", "").split()
                    for w in words:
                        n = self.wave_engine._get_or_create_neuron(w)
                        # Ensure we are reasoning from a grounded mass, not the vacuum itself or a catalyst
                        if n.id != target_id and self.wave_engine.determine_spectron_type(n) != "catalyst":
                            # Wave Superposition: Activate ALL grounded nodes above the noise floor
                            resonant_nodes = []
                            for syn_id, weight in n.synapses.items():
                                syn_n = self.substrate.neurons[syn_id]
                                if syn_n.id != n.id and self.wave_engine.determine_spectron_type(syn_n) in ["mass", "cold"]:
                                    if weight > 0.0: # Any surviving gravity bond
                                        resonant_nodes.append((syn_n, weight))
                            
                            if resonant_nodes:
                                # Sort by gravity (strongest/most recent first)
                                resonant_nodes.sort(key=lambda x: x[1], reverse=True)
                                
                                attributes = [rn[0].text for rn in resonant_nodes]
                                
                                # Find the catalyst that bridges this node (for grammatical phrasing)
                                bridge_word = " "
                                for sid in n.synapses:
                                    sn = self.substrate.neurons[sid]
                                    if self.wave_engine.determine_spectron_type(sn) == "catalyst":
                                        bridge_word = f" {sn.text} "
                                        break
                                        
                                response_text = f"{n.text}{bridge_word}{' '.join(attributes)}"
                                found_answer = True
                                print(f"[REASONING] Wave Superposition retrieved: {response_text}")
                                break
                        if found_answer: break
                
                if not found_answer:
                    print(f"[CURIOSITY] FELLA's wave engine hit an unresolved void on '{target_word}'.")
                    response_text = f"{target_word} ?"
            else:
                response_text = "[Void]"
        else:
            response_text = "acknowledged."

        self.last_thought = f"Wave State: {wave_state.get('state')} (Avg Phase: {wave_state.get('average_phase', 0.0):.2f})"
        self.last_response = response_text
        self.dialogue_history.append({"speaker": "FELLA", "text": response_text})
        
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
            explanation = f"{vacuum.concept_query} transforms energy and physical matter."
            
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
        """
        Homeostatic Dream Consolidation:
        Modular wave reverberation within distinct concept clusters and topological anti-Hebbian noise pruning.
        """
        total_reverberated = 0
        
        # Group concept seeds by network cluster to prevent global clique cross-talk
        network_groups: Dict[str, List[int]] = defaultdict(list)
        for n in list(self.substrate.neurons.values()):
            if n.tier_z > 0 and (n.energy > 2.0 or n.role in ["anchor", "causal"]):
                network_groups[n.network_id].append(n.id)
                
        for net_id, seed_ids in network_groups.items():
            if not seed_ids:
                continue
            wave_map = self.substrate.propagate_wave(seed_ids, max_hops=3, damping=0.60)
            self.substrate.potentiate_hebbian(wave_map, learning_rate=0.08)
            total_reverberated += len(wave_map)
            
        # Anti-Hebbian topological pruning of spurious cross-talk
        pruned_spurious = self.substrate.prune_cross_talk_synapses(threshold=0.40, max_fanout=12)
        pruned_gravity = self.substrate.prune_gravity_wells(max_in_degree=35)
        
        thermo_stats = self.substrate.step_thermodynamics()
        syn_stats = self.substrate.get_synapse_stats()
        
        self.observer.epistemic_friction = 0.02
        self.observer.self_confidence = 0.97
        self.trait_field.active_trait = "AFFIRM"
        self.last_thought = "Waking peacefully from deep modular consolidation dream"
        
        return {
            "reverberated_neurons": total_reverberated,
            "pruned_synapses": pruned_spurious + thermo_stats["pruned_synapses"],
            "total_neurons": thermo_stats["total_neurons"],
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
            "observer": self.observer.to_dict(),
            "memory_bank": getattr(self.lang, "memory_bank", [])
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
        if "memory_bank" in data:
            brain.lang.memory_bank = list(data["memory_bank"])
        return brain

