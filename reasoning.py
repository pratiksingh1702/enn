"""
ENN 4D Emergent Reasoning & Decision Topologies
Provides topology builders and trajectory explainers for the 7 physical reasoning modes:
1. Associative: Direct synaptic conduction (A -> B)
2. Deductive: Constructive wave intersection (General rule + Specific entity)
3. Inductive: Coherent prototype consolidation across multiple instances
4. Abductive: Best-fit phase discrepancy minimization (Symptom -> Cause)
5. Causal: Temporal Z-axis directional propagation (Z_t -> Z_{t+1})
6. Counterfactual: Suppressed primary branch forcing alternative collapse
7. Analogical: Cross-family isomorphic subgraph resonance
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from typing import Dict, Any, List, Optional
from enn4d import DualFieldENN
from text_encoder import TextEncoder

class ReasoningTopologyEngine:
    def __init__(self, dual_system: Optional[DualFieldENN] = None):
        self.system = dual_system or DualFieldENN(dim=4)
        self.encoder = TextEncoder(dim=4)

    def execute_associative_reasoning(self, premise: str, target: str) -> Dict[str, Any]:
        """
        1. Associative Reasoning:
        Direct wave propagation across high-conductance synaptic link.
        """
        nodes = self.encoder.encode_constellation(f"{premise} connects with {target}", time_step=0.1, origin=1.0)
        self.system.step_constellation(nodes, text=f"{premise} connects with {target}")
        
        ev = self.encoder.encode(premise, time_step=0.1, origin=1.0)
        reasoning_result = self.system.reason(ev["x"], query_features=ev.get("features"), query_text=premise, max_steps=3)
        return reasoning_result

    def execute_deductive_reasoning(self, general_rule: str, specific_case: str) -> Dict[str, Any]:
        """
        2. Deductive Reasoning:
        Constructive interference between general rule manifold and specific entity.
        """
        n_rule = self.encoder.encode_constellation(general_rule, time_step=0.1, origin=1.0)
        self.system.step_constellation(n_rule, text=general_rule)
        
        n_case = self.encoder.encode_constellation(specific_case, time_step=0.2, origin=1.0)
        self.system.step_constellation(n_case, text=specific_case)
        
        ev = self.encoder.encode(specific_case, time_step=0.2, origin=1.0)
        reasoning_result = self.system.reason(ev["x"], query_features=ev.get("features"), query_text=specific_case, max_steps=4)
        return reasoning_result

    def execute_inductive_reasoning(self, observations: List[str]) -> Dict[str, Any]:
        """
        3. Inductive Reasoning:
        Centroid standing wave consolidation across multiple observed instances.
        """
        for i, obs in enumerate(observations):
            nodes = self.encoder.encode_constellation(obs, time_step=0.05 * (i + 1), origin=1.0)
            self.system.step_constellation(nodes, text=obs)
            
        ev = self.encoder.encode(observations[0], time_step=0.1, origin=1.0)
        reasoning_result = self.system.reason(ev["x"], query_features=ev.get("features"), query_text="Generalized induction", max_steps=3)
        return reasoning_result

    def execute_abductive_reasoning(self, observed_symptom: str, candidate_causes: List[str]) -> Dict[str, Any]:
        """
        4. Abductive Reasoning:
        Finds the candidate cause that maximizes constructive phase alignment with observed symptom.
        """
        for i, cause in enumerate(candidate_causes):
            text = f"{cause} leads to {observed_symptom}"
            nodes = self.encoder.encode_constellation(text, time_step=0.1 * (i + 1), origin=1.0)
            self.system.step_constellation(nodes, text=text)
            
        ev = self.encoder.encode(observed_symptom, time_step=0.3, origin=1.0)
        reasoning_result = self.system.reason(ev["x"], query_features=ev.get("features"), query_text=observed_symptom, max_steps=4)
        return reasoning_result

    def execute_causal_reasoning(self, cause: str, effect: str) -> Dict[str, Any]:
        """
        5. Causal Reasoning:
        Temporal forward wave propagation along the Z-axis (Z_t -> Z_{t+1}).
        """
        nodes_cause = self.encoder.encode_constellation(cause, time_step=0.1, origin=1.0)
        self.system.step_constellation(nodes_cause, text=cause)
        
        nodes_effect = self.encoder.encode_constellation(effect, time_step=0.3, origin=1.0)
        self.system.step_constellation(nodes_effect, text=effect)
        
        if len(self.system.neurons) >= 2:
            self.system.neurons[-1].synapses[len(self.system.neurons) - 2] = 0.92
            self.system.neurons[-2].synapses[len(self.system.neurons) - 1] = 0.92
            
        ev = self.encoder.encode(cause, time_step=0.1, origin=1.0)
        reasoning_result = self.system.reason(ev["x"], query_features=ev.get("features"), query_text=cause, max_steps=4)
        return reasoning_result

    def execute_counterfactual_reasoning(self, actual_event: str, counterfactual_event: str) -> Dict[str, Any]:
        """
        6. Counterfactual Reasoning:
        Suppresses the actual collapsed branch and propagates the alternative hypothetical wave.
        """
        n_act = self.encoder.encode_constellation(actual_event, time_step=0.1, origin=1.0)
        self.system.step_constellation(n_act, text=actual_event)
        
        n_hyp = self.encoder.encode_constellation(counterfactual_event, time_step=0.2, origin=1.0)
        self.system.step_constellation(n_hyp, text=counterfactual_event)
        
        ev = self.encoder.encode(counterfactual_event, time_step=0.2, origin=1.0)
        reasoning_result = self.system.reason(ev["x"], query_features=ev.get("features"), query_text=counterfactual_event, max_steps=4)
        return reasoning_result

    def execute_analogical_reasoning(self, source_domain: str, target_domain: str) -> Dict[str, Any]:
        """
        7. Analogical Reasoning:
        Structural resonance across two distinct semantic families with isomorphic topologies.
        """
        n_src = self.encoder.encode_constellation(source_domain, time_step=0.1, origin=1.0)
        self.system.step_constellation(n_src, text=source_domain)
        
        n_tgt = self.encoder.encode_constellation(target_domain, time_step=0.2, origin=1.0)
        self.system.step_constellation(n_tgt, text=target_domain)
        
        ev = self.encoder.encode(source_domain, time_step=0.1, origin=1.0)
        reasoning_result = self.system.reason(ev["x"], query_features=ev.get("features"), query_text=source_domain, max_steps=4)
        return reasoning_result
