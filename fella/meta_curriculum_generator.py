"""
FELLA Meta-Learning Curriculum Generator: 20,000 Grounded Pattern Trajectories
=============================================================================
Generates 20,000 domain-grounded noise-free sentences across 5 hierarchical categories:
1. Simple Transitive & Intransitive Patterns (4,000 sentences)
2. Spatial & Temporal Modifier Patterns (4,000 sentences)
3. Causal & Transformative Dynamics Patterns (4,000 sentences)
4. Hierarchical & Analogical Conceptual Patterns (4,000 sentences)
5. Multi-Hop Downstream Consequence Patterns (4,000 sentences)
"""

import random
from typing import List, Dict, Any


class MetaPatternCurriculumGenerator:
    """Generates 20,000 structured pattern sentences grounded in natural physics."""
    def __init__(self, seed: int = 42):
        random.seed(seed)
        
        # Grounded Domain Clusters
        self.domains = {
            "solar": {
                "subjects": ["sun", "star", "solar core", "radiant star", "bright sun"],
                "actions": ["radiates", "emits", "illuminates", "shines", "warms"],
                "objects": ["solar light", "thermal radiation", "intense heat", "outer space", "planetary surfaces"],
                "modifiers": ["across the universe", "through empty vacuum", "upon planetary terrain", "into vast cosmos"],
                "causes": ["nuclear fusion generates energy", "thermal radiation transfers heat", "gravitational pressure compresses plasma"],
                "effects": ["warming planet earth", "illuminating dark planets", "sustaining living ecosystems"]
            },
            "hydro": {
                "subjects": ["water", "liquid ocean", "cool rain", "mountain river", "fresh water"],
                "actions": ["flows", "circulates", "evaporates", "condenses", "precipitates"],
                "objects": ["moisture", "droplets", "coastal terrain", "atmospheric clouds", "fertile soil"],
                "modifiers": ["across fertile valleys", "into upper atmosphere", "through river channels", "upon dry soil"],
                "causes": ["solar heat evaporates moisture", "atmospheric cooling condenses vapor", "gravity pulls water downward"],
                "effects": ["nourishing thirsty plants", "filling fresh lakes", "sustaining terrestrial life"]
            },
            "botany": {
                "subjects": ["plants", "green leaves", "forest trees", "growing vegetation", "healthy flora"],
                "actions": ["absorb", "conduct", "release", "produce", "generate"],
                "objects": ["radiant sunlight", "fresh oxygen", "organic nutrients", "cellular energy", "green biomass"],
                "modifiers": ["through photosynthesis", "inside chloroplast cells", "from fertile soil", "during daylight hours"],
                "causes": ["sunlight fuels photosynthesis", "roots absorb minerals", "leaves capture carbon"],
                "effects": ["purifying atmospheric air", "providing organic food", "supporting animal life"]
            },
            "gravity": {
                "subjects": ["gravity", "black holes", "massive planets", "cosmic mass", "dense stars"],
                "actions": ["attracts", "warps", "curves", "traps", "pulls"],
                "objects": ["spacetime fabric", "surrounding matter", "orbiting satellites", "celestial bodies", "nearby light"],
                "modifiers": ["across deep spacetime", "within event horizons", "through gravitational fields", "around massive centers"],
                "causes": ["mass curves spacetime geometry", "extreme density creates horizons", "orbital momentum balances attraction"],
                "effects": ["forming stable orbits", "holding solar systems together", "shaping vast galaxies"]
            },
            "social": {
                "subjects": ["friendship", "mutual trust", "empathy", "cooperation", "shared dialogue"],
                "actions": ["strengthens", "cultivates", "builds", "fosters", "sustains"],
                "objects": ["peaceful bonds", "social harmony", "compassionate care", "deep understanding", "mutual support"],
                "modifiers": ["through honest communication", "upon mutual respect", "across human communities", "between caring individuals"],
                "causes": ["empathy enables shared feeling", "honesty establishes trust", "collaboration solves challenges"],
                "effects": ["creating peaceful societies", "deepening social connection", "reducing emotional conflict"]
            }
        }

    def generate_category1_simple(self, count: int = 4000) -> List[str]:
        """Simple SVO & SV Kernel Patterns (4,000 sentences)."""
        sentences = set()
        dom_keys = list(self.domains.keys())
        while len(sentences) < count:
            d = self.domains[random.choice(dom_keys)]
            subj = random.choice(d["subjects"])
            act = random.choice(d["actions"])
            obj = random.choice(d["objects"])
            sentences.add(f"The {subj} {act} {obj}.")
        return list(sentences)

    def generate_category2_modifiers(self, count: int = 4000) -> List[str]:
        """Spatial & Temporal Modifier Patterns (4,000 sentences)."""
        sentences = set()
        dom_keys = list(self.domains.keys())
        while len(sentences) < count:
            d = self.domains[random.choice(dom_keys)]
            subj = random.choice(d["subjects"])
            act = random.choice(d["actions"])
            obj = random.choice(d["objects"])
            mod = random.choice(d["modifiers"])
            sentences.add(f"The {subj} {act} {obj} {mod}.")
        return list(sentences)

    def generate_category3_causal(self, count: int = 4000) -> List[str]:
        """Causal & Transformative Dynamics Patterns (4,000 sentences)."""
        sentences = set()
        dom_keys = list(self.domains.keys())
        while len(sentences) < count:
            d = self.domains[random.choice(dom_keys)]
            subj = random.choice(d["subjects"])
            act = random.choice(d["actions"])
            obj = random.choice(d["objects"])
            cause = random.choice(d["causes"])
            sentences.add(f"The {subj} {act} {obj} because {cause}.")
        return list(sentences)

    def generate_category4_hierarchical(self, count: int = 4000) -> List[str]:
        """Hierarchical & Analogical Conceptual Patterns (4,000 sentences)."""
        sentences = set()
        dom_keys = list(self.domains.keys())
        while len(sentences) < count:
            d = self.domains[random.choice(dom_keys)]
            subj = random.choice(d["subjects"])
            act = random.choice(d["actions"])
            obj = random.choice(d["objects"])
            mod = random.choice(d["modifiers"])
            sentences.add(f"{subj.capitalize()} that {act} {obj} operates {mod}.")
        return list(sentences)

    def generate_category5_multihop(self, count: int = 4000) -> List[str]:
        """Multi-Hop Downstream Consequence Patterns (4,000 sentences)."""
        sentences = set()
        dom_keys = list(self.domains.keys())
        while len(sentences) < count:
            d = self.domains[random.choice(dom_keys)]
            subj = random.choice(d["subjects"])
            act = random.choice(d["actions"])
            obj = random.choice(d["objects"])
            eff = random.choice(d["effects"])
            sentences.add(f"When {subj} {act} {obj}, it leads to {eff}.")
        return list(sentences)

    def generate_full_20k_curriculum(self) -> List[str]:
        """Generates the full 20,000 structured pattern curriculum."""
        c1 = self.generate_category1_simple(4000)
        c2 = self.generate_category2_modifiers(4000)
        c3 = self.generate_category3_causal(4000)
        c4 = self.generate_category4_hierarchical(4000)
        c5 = self.generate_category5_multihop(4000)
        full = c1 + c2 + c3 + c4 + c5
        random.shuffle(full)
        return full

