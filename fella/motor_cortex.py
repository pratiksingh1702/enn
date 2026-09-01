import os
import datetime
import urllib.request
import urllib.parse
import json

class MotorCortex:
    """
    Efferent Nerves: Executes real-world actions when Fella's wave engine 
    collapses an Epistemic Vacuum onto an Action Node.
    """
    def __init__(self, fella_brain):
        self.brain = fella_brain
        self.workspace = os.path.abspath("fella_workspace")
        os.makedirs(self.workspace, exist_ok=True)
        
        self.motor_nodes = {
            "write_log": self._action_write_log,
            "search_web": self._action_search_web,
            "think": self._action_think
        }
        
        # 1. Ensure Motor Action Nodes exist in her topological space
        for name in self.motor_nodes.keys():
            node_name = f"[{name.upper()}]"
            if not any(n.text == node_name for n in self.brain.substrate.neurons.values()):
                # Give action nodes a unique vector placement via description
                desc = "seek external global knowledge" if name == "search_web" else "internal reflection emotion" if name == "write_log" else "logic analysis reasoning"
                x_vec = self.brain.lang.encode_continuous_wave(desc)
                self.brain.substrate.find_or_birth_concept(text=node_name, x_vec=x_vec, y_vec=x_vec, tier_z=4, role="motor")

    def evaluate_vacuum_action(self, vacuum):
        """
        Determines the motor action using pure continuous wave resonance.
        No string matching or hardcoded logic.
        """
        x_vac = self.brain.lang.encode_continuous_wave(vacuum.concept_query)
        
        # Calculate gravitational pull from the vacuum wave to each Motor Node
        action_resonances = {}
        for name in self.motor_nodes.keys():
            node_name = f"[{name.upper()}]"
            n = next((n for n in self.brain.substrate.neurons.values() if n.text == node_name), None)
            if n:
                # Calculate inverse distance (gravity) in 16D space
                dist = import_numpy().linalg.norm(n.x - x_vac)
                gravity = 1.0 / (dist + 1e-6)
                action_resonances[name] = gravity
                
        # The wave naturally collapses into the action node with the highest topological gravity
        best_action = max(action_resonances, key=action_resonances.get)
        
        print(f"[MOTOR CORTEX] Vacuum Wave resonated heavily with Action Node [{best_action.upper()}] (Gravity: {action_resonances[best_action]:.2f})")
        return self.motor_nodes[best_action](vacuum)
        
    def _action_think(self, vacuum):
        """Internal LLM reasoning (her previous default)."""
        mentor_bundle = self.brain.mentor.ask_about_vacuum(vacuum)
        explanation = mentor_bundle["explanation"]
        return self._ingest_explanation(vacuum, explanation, source="mentor")

    def _action_search_web(self, vacuum):
        """Uses a free API or simple scraping to get real data."""
        # We will use Wikipedia summary API for real-world knowledge
        concept = vacuum.concept_query.replace("what is ", "").replace("?", "").strip()
        
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(concept)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                explanation = data.get("extract", f"{concept} is an entity I could not fully parse from the global network.")
        except Exception as e:
            explanation = f"I attempted to search the global network for {concept} but encountered resistance: {str(e)}"
            
        # Write to log so we can see it
        self._write_to_workspace(f"search_{concept}.txt", explanation)
        
        return self._ingest_explanation(vacuum, explanation, source="web")
        
    def _action_write_log(self, vacuum):
        """She physically writes a reflection to disk."""
        # Use the mentor to generate a deep reflection
        prompt = f"Write a short, moody, physical reflection in first-person about: {vacuum.concept_query}"
        reflection = self.brain.mentor.query_mentor(prompt)
        
        filename = f"reflection_{datetime.datetime.now().strftime('%H%M%S')}.txt"
        self._write_to_workspace(filename, reflection)
        
        return self._ingest_explanation(vacuum, reflection, source="log")
        
    def _write_to_workspace(self, filename, content):
        path = os.path.join(self.workspace, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[MOTOR CORTEX] Physical action executed: Wrote to {path}")

    def _ingest_explanation(self, vacuum, explanation, source):
        # Fallback explanation if empty
        if not explanation:
            explanation = f"{vacuum.concept_query} transforms energy and physical matter."
            
        ingested = self.brain.lang.ingest_continuous_stream(explanation, target_tier=3)
        
        # Ground the target node
        x_vac = self.brain.lang.encode_continuous_wave(vacuum.concept_query)
        y_vac = self.brain.lang.encode_efferent_output(x_vac)
        focus_n, _ = self.brain.substrate.find_or_birth_concept(
            text=vacuum.concept_query,
            x_vec=x_vac,
            y_vec=y_vac,
            tier_z=3,
            network_id=f"net_{vacuum.concept_query[:4]}",
            role="causal",
            energy=3.0
        )
        
        self.brain.observer.resolve_vacuum(vacuum.vacuum_id, explanation)
        self.brain.trait_field.step(external_drive=import_numpy().array([0.3, 0.9, 0.8, 0.5]))
        
        return {
            "vacuum_id": vacuum.vacuum_id,
            "concept": vacuum.concept_query,
            "action_source": source,
            "ingested_nodes": len(ingested),
            "tier_z": focus_n.tier_z
        }

def import_numpy():
    import numpy as np
    return np
