"""
FELLA Semantic Grounding Generator: 3,000 Physics-Grounded Patterns
===================================================================
Generates grounded patterns connecting structural syntax to natural physics:
1. 1,000 Essence "What Is" Definitions (Ontology: Nature + Physical Function)
2. 1,000 Causal Chains (Dynamics: Process -> Transformation -> Equilibrium)
3. 1,000 Analogical Physics Bridges (Structural Cross-Mapping)
"""

import random
from typing import List, Dict, Any


class SemanticGroundingCurriculumGenerator:
    """Generates 3,000 physics-grounded pattern trajectories."""
    def __init__(self, seed: int = 42):
        random.seed(seed)
        
        self.essence_schemas = [
            # Solar / Thermal
            ("The sun is a radiant star of compressed plasma that generates energy through nuclear fusion and radiates light across space.",
             "The solar core is a dense nuclear furnace that emits photons and warms surrounding planetary bodies.",
             "A star is a massive celestial sphere that sustains thermonuclear reactions and illuminates the cosmos."),
            # Hydro / Fluid
            ("Water is an essential fluid compound that circulates across ecosystems through evaporation, condensation, and precipitation.",
             "An ocean is a vast reservoir of liquid water that regulates planetary climate and sustains marine life.",
             "Rain is liquid precipitation that condenses in atmospheric clouds and falls to nourish terrestrial soil."),
            # Atmosphere / Air
            ("Air is an invisible mixture of atmospheric gases that envelops planetary surfaces and enables biological respiration.",
             "The atmosphere is a protective gaseous layer that shields living organisms and maintains thermal equilibrium.",
             "Oxygen is a vital gaseous element that fuels cellular respiration and powers organic metabolism."),
            # Botany / Metabolism
            ("Plants are living autotrophic organisms that capture radiant sunlight through photosynthesis and produce oxygen.",
             "A green leaf is a biological organ equipped with chloroplasts that synthesizes organic glucose from solar energy.",
             "Photosynthesis is a biochemical process where chloroplast cells convert carbon dioxide and water into oxygen and biomass."),
            # Gravity / Space
            ("Gravity is a fundamental physical force caused by mass curving spacetime geometry and pulling matter together.",
             "A black hole is a region of spacetime where gravitational curvature is so extreme that nothing can escape its horizon.",
             "Spacetime is the four-dimensional continuous fabric that warps around massive celestial bodies to govern orbital motion."),
            # Social / Empathy
            ("Friendship is a reciprocal social bond grounded in mutual trust, empathetic understanding, and shared care.",
             "Empathy is the cognitive and emotional capacity to experience and comprehend the internal state of another being.",
             "Trust is the foundational relational certainty that fosters cooperation, safety, and deep social harmony.")
        ]
        
        self.causal_schemas = [
            # Thermal Causality
            ("When nuclear fusion occurs in the stellar core, immense thermal energy is released, causing the star to radiate warmth into space.",
             "Because solar radiation heats planetary surfaces, atmospheric air expands and circulates global weather systems.",
             "Solar photons illuminate darkness and transfer kinetic heat energy to planetary matter."),
            # Hydro Causality
            ("When solar heat warms liquid water, evaporation transforms moisture into vapor, which condenses into atmospheric clouds.",
             "Because gravity pulls water droplets downward, rainfall replenishes freshwater rivers and irrigates fertile soil.",
             "Water circulation transports essential minerals and sustains living biological ecosystems."),
            # Botanical Causality
            ("When sunlight strikes green leaves, chlorophyll absorbs photon energy, causing cells to release oxygen and store glucose.",
             "Because plant roots absorb moisture and soil nutrients, vegetation grows and provides sustenance for animal life.",
             "Photosynthetic oxygen production continuously maintains breathable atmospheric air for living organisms."),
            # Gravitational Causality
            ("When massive stars collapse under extreme gravity, gravitational curvature intensifies until an event horizon forms.",
             "Because mass curves surrounding spacetime fabric, orbiting planets maintain stable paths around the central star.",
             "Gravitational attraction holds galaxies together and structures cosmic matter across the universe."),
            # Social Causality
            ("When individuals practice empathetic communication, mutual understanding deepens, causing relational trust to strengthen.",
             "Because honesty and compassionate care establish psychological safety, communities build lasting social harmony.",
             "Cooperation and shared purpose enable groups to overcome collective challenges and cultivate peace.")
        ]
        
        self.analogy_schemas = [
            ("A star is like a stellar engine where nuclear fusion functions as fuel to radiate light across the cosmos.",
             "Water circulation is like a planetary bloodstream that continuously transports nutrients and balances climate.",
             "Gravity is like the invisible geometry that guides cosmic dance and holds celestial bodies in orbit.",
             "Photosynthesis is like a biological solar collector that converts radiant light into living biomass.",
             "Friendship is like an empathetic bridge where mutual support and trust connect individual minds.")
        ]

    def generate_essence_definitions(self, count: int = 1000) -> List[str]:
        """Generates 1,000 Essence Definitions (Identity + Nature + Behavior)."""
        corpus = []
        for cluster in self.essence_schemas:
            corpus.extend(cluster)
        out = []
        while len(out) < count:
            out.append(random.choice(corpus))
        return out

    def generate_causal_chains(self, count: int = 1000) -> List[str]:
        """Generates 1,000 Causal Chains (Dynamics: Process -> Transformation -> Equilibrium)."""
        corpus = []
        for cluster in self.causal_schemas:
            corpus.extend(cluster)
        out = []
        while len(out) < count:
            out.append(random.choice(corpus))
        return out

    def generate_analogies(self, count: int = 1000) -> List[str]:
        """Generates 1,000 Analogical Physics Bridges."""
        corpus = []
        for cluster in self.analogy_schemas:
            corpus.extend(cluster)
        out = []
        while len(out) < count:
            out.append(random.choice(corpus))
        return out

    def generate_full_grounding_curriculum(self) -> List[str]:
        """Generates the full 3,000-pattern semantic grounding curriculum."""
        c1 = self.generate_essence_definitions(1000)
        c2 = self.generate_causal_chains(1000)
        c3 = self.generate_analogies(1000)
        full = c1 + c2 + c3
        random.shuffle(full)
        return full

