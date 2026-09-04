import re
import json
import urllib.request
import urllib.parse
import numpy as np
from fella.core_substrate import ENNNeuron

class Affordance:
    def __init__(self, affordance_id: str, wave: np.ndarray, execute_fn):
        """
        An Action/Tool Affordance.
        Has a physical 256D frequency vector and an executable callback.
        Decision to use this tool is determined strictly by wave resonance.
        """
        self.id = affordance_id
        self.wave = wave / (np.linalg.norm(wave) + 1e-9)
        self.execute_fn = execute_fn
        self.reinforcement_weight = 1.0

class AutotelicAgency:
    def __init__(self, dim: int = 256):
        """
        The Autonomous Agency Engine.
        Balances Outer Learning (Web/Environment) and Inner Learning (Dreaming/Consolidation)
        with ZERO hardcoding. Decisions are driven by wave resonance and thermodynamic gradients.
        """
        self.dim = dim
        self.affordances = {}
        self._init_default_affordances()

    def _generate_affordance_wave(self, seed_phrase: str) -> np.ndarray:
        """Deterministic mathematical embedding for an affordance profile."""
        np.random.seed(abs(hash(seed_phrase)) % (2**32))
        w = np.random.randn(self.dim)
        return w / (np.linalg.norm(w) + 1e-9)

    def _init_default_affordances(self):
        """Initializes the physical affordance vectors for digital capabilities."""
        # 1. Outer Discovery (High outward epistemic flux)
        w_outer = self._generate_affordance_wave("information_acquisition_external_world_knowledge_influx")
        self.register_affordance(
            "[ACTION_OUTER_DISCOVERY]",
            w_outer,
            self._execute_outer_discovery
        )

        # 2. Inner Dreaming (Internal consolidation and topological annealing)
        w_inner = self._generate_affordance_wave("internal_homeostasis_memory_consolidation_holographic_dream")
        self.register_affordance(
            "[ACTION_INNER_DREAM]",
            w_inner,
            self._execute_inner_dream
        )

        # 3. Human Inquiry (Social acoustic/dialogic alignment with Pratik)
        w_social = self._generate_affordance_wave("human_social_dialogue_inquiry_alignment_pratik")
        self.register_affordance(
            "[ACTION_HUMAN_INQUIRY]",
            w_social,
            self._execute_human_inquiry
        )

    def register_affordance(self, affordance_id: str, wave: np.ndarray, execute_fn):
        """Registers a new action affordance into her agency cortex."""
        self.affordances[affordance_id] = Affordance(affordance_id, wave, execute_fn)

    # -------------------------------------------------------------------------
    # DECISION PHYSICS: ZERO HARDCODING
    # -------------------------------------------------------------------------
    def evaluate_and_act(self, entity, target_concept=None):
        """
        The Core Agency Pulse:
        1. Evaluates self-state (Interoception).
        2. Encodes the Tension Wave of the current gap.
        3. Projects the Tension Wave onto all tool affordance vectors (Wave Resonance).
        4. Executes the highest-resonance action.
        5. Updates causal weights based on entropy outcome.
        """
        if len(entity.brain.neurons) == 0:
            return None

        # 1. INTEROCEPTION (Self-Assessment)
        if target_concept is None:
            # Identify the concept with highest epistemic tension
            isolated_neurons = sorted(entity.brain.neurons.values(), key=lambda n: len(n.z_events))
            target_concept = isolated_neurons[0]
        elif isinstance(target_concept, str):
            target_concept = entity.brain.get_or_create(target_concept)
        
        # Compute the Gap Tension Wave
        # High global entropy tilts the wave toward internal consolidation / rest
        entropy_factor = min(1.0, entity.entropy_level / 5.0)
        gap_wave = target_concept.x_wave * (1.0 - entropy_factor)
        # Add entropy signature to tilt resonance when overloaded
        if entropy_factor > 0.6:
            gap_wave = gap_wave + self.affordances["[ACTION_INNER_DREAM]"].wave * entropy_factor
        gap_wave /= (np.linalg.norm(gap_wave) + 1e-9)

        # 2. WAVE INTERFERENCE TEST (Selection via dot-product resonance)
        best_affordance = None
        best_resonance = -float('inf')
        
        resonance_log = []
        for aff_id, aff in self.affordances.items():
            # Wave resonance + reinforced learned affinity
            res = np.dot(gap_wave, aff.wave) * aff.reinforcement_weight
            resonance_log.append((aff_id, res))
            if res > best_resonance:
                best_resonance = res
                best_affordance = aff

        # 3. AUTONOMOUS EXECUTION
        pre_entropy = entity.entropy_level
        action_outcome = best_affordance.execute_fn(target_concept, entity)

        # 4. HOMEOSTATIC FEEDBACK & CAUSAL LEARNING
        # If the action resolved the gap and decreased entropy, fortify the tether
        post_entropy = entity.entropy_level
        entropy_delta = post_entropy - pre_entropy
        
        if entropy_delta <= 0:
            best_affordance.reinforcement_weight = min(2.0, best_affordance.reinforcement_weight * 1.05)
            status = "CONSTRUCTIVE_HOMEOSTASIS"
        else:
            best_affordance.reinforcement_weight = max(0.5, best_affordance.reinforcement_weight * 0.95)
            status = "ENTROPY_EXPANSION"

        # Bind concept to action in Causal Cortex
        if target_concept.text in entity.brain.matrix_keys and best_affordance.id in entity.brain.matrix_keys:
            c_idx = entity.brain.matrix_keys.index(target_concept.text)
            a_idx = entity.brain.matrix_keys.index(best_affordance.id)
            entity.causal_cortex.bind_time([c_idx, a_idx])

        return {
            "target": target_concept.text,
            "selected_action": best_affordance.id,
            "resonance": best_resonance,
            "resonance_profile": resonance_log,
            "status": status,
            "outcome": action_outcome
        }

    # -------------------------------------------------------------------------
    # DIGITAL HANDS (Tool Callbacks)
    # -------------------------------------------------------------------------
    def _execute_outer_discovery(self, target_concept: ENNNeuron, entity):
        """
        Outer Learning: Queries live Wikipedia API to fetch true definition,
        extracts structural keywords, and binds them to the concept as a Z-Event.
        """
        query_text = target_concept.text
        # Clean special markers if any
        clean_query = re.sub(r'\[.*?\]', '', query_text).strip()
        if not clean_query or len(clean_query) < 2:
            clean_query = "Physics"

        encoded_title = urllib.parse.quote(clean_query.capitalize())
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
        req = urllib.request.Request(url, headers={"User-Agent": "FellaAGI/2.0 (Cognitive Organism)"})

        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                extract = data.get("extract", "")
                if extract:
                    # Extract meaningful words (no short punctuation/stopwords)
                    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', extract)[:8]]
                    if words:
                        # Ground into her matrix as an empirical Z-Event
                        z_id = entity.brain.record_event([target_concept.text] + words)
                        # Relieve epistemic tension
                        entity.entropy_level = max(0.0, entity.entropy_level - 1.5)
                        return f"Discovered external definition for '{clean_query}': bound to {words[:4]} (Z-{z_id})"
        except Exception as e:
            pass

        # Fallback: link to curiosity ground
        z_id = entity.brain.record_event([target_concept.text, "external", "discovery", "concept"])
        entity.entropy_level = max(0.0, entity.entropy_level - 0.5)
        return f"Formed exploratory ground for '{target_concept.text}' (Z-{z_id})"

    def _execute_inner_dream(self, target_concept: ENNNeuron, entity):
        """
        Inner Learning: Consolidates memory through internal simulation.
        Finds nearest topological resonance and anneals vectors.
        """
        sims = entity.brain.get_fast_similarity(target_concept.x_wave)
        top_indices = np.argsort(sims)[::-1]
        
        partners = []
        for idx in top_indices:
            k = entity.brain.matrix_keys[idx]
            if k != target_concept.text:
                partners.append(k)
            if len(partners) >= 2:
                break

        if partners:
            z_id = entity.brain.record_event([target_concept.text] + partners)
            entity.entropy_level = max(0.0, entity.entropy_level - 1.0)
            return f"Subconscious dream consolidation: '{target_concept.text}' synthesized with {partners} (Z-{z_id})"
        else:
            entity.entropy_level = max(0.0, entity.entropy_level - 0.2)
            return f"Internal reflection stabilized '{target_concept.text}'"

    def _execute_human_inquiry(self, target_concept: ENNNeuron, entity):
        """
        Human Dialogue: Reaches out to Pratik through the Frontier Manifold.
        """
        question = f"what is {target_concept.text}"
        thought, _, _, _ = entity.frontier.formulate_thought(question, simulate=False)
        entity.entropy_level = max(0.0, entity.entropy_level - 0.8)
        if thought:
            return f"Formulated inquiry to Pratik: '{thought}'"
        return f"Formulated inquiry: '{target_concept.text}?'"
