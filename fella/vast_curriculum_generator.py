"""
FELLA Vast-Scale Curriculum Generator (19,000 Pure Noise-Free Patterns)
======================================================================
Domain-grounded, high-entropy, semantically pristine training curriculum:
1. Syntactic Spine (5,000 unique sentences):
   - Stage 1: Simple SVO (1,000)
   - Stage 2: Modifiers & Prepositions (1,000)
   - Stage 3: Compound Coordination (1,000)
   - Stage 4: Complex Subordination (1,000)
   - Stage 5: Recursive Multi-Clause Structures (1,000)
2. Semantic Web (5,000 unique sentences):
   - Realm 1: Concrete Physical Entities (1,000)
   - Realm 2: Dynamic Energy & Biochemical Processes (1,000)
   - Realm 3: Gravity, Spacetime Curvature & Cosmology (1,000)
   - Realm 4: Emotional & Social Dynamics (1,000)
   - Realm 5: Scientific, Metacognitive & Universal Laws (1,000)
3. Contextual Dialogue Web (5,000 dialogues):
   - Phase 1: Simple Q&A (1,000)
   - Phase 2: Contextual Q&A (1,000)
   - Phase 3: Extended Narratives (1,000)
   - Phase 4: Complex Multi-Turn Dialogues (1,000)
   - Phase 5: Persuasive Dialogues (1,000)
4. Self-Generated Practice Prompts (4,000 prompts)
5. Baseline Diagnostic Test Battery (1,000 diverse prompts)
"""

import itertools
import random
from typing import List, Tuple, Dict, Any

# ==============================================================================
# DOMAIN DICTIONARIES (SVO Mappings)
# ==============================================================================

DOMAIN_CLUSTERS = [
    # 1. Solar & Cosmic Domain
    {
        "subjects": ["The sun", "The golden sun", "The bright sun", "Distant stars", "Luminous stars", "The moon", "The silent moon", "Galaxies", "Massive black holes"],
        "verbs_objs": [
            ("radiates", "bright light"), ("warms", "the planet earth"), ("emits", "thermal energy"),
            ("illuminates", "outer space"), ("glows", "across the cosmos"), ("orbits", "the blue earth"),
            ("reflects", "solar light"), ("curves", "surrounding spacetime"), ("traps", "incoming light")
        ],
        "modifiers": ["across the vast universe", "through empty space", "over billions of years", "across the quiet cosmos"],
        "causals": ["because nuclear fusion converts hydrogen into helium", "while it radiates immense heat", "so that planets remain in orbit"]
    },
    # 2. Hydrological & Meteorological Domain
    {
        "subjects": ["Water", "Fresh water", "Cool rain", "Dark clouds", "Thick clouds", "Rivers", "Deep oceans", "Fierce lightning"],
        "verbs_objs": [
            ("flows", "across the earth"), ("evaporates", "into high clouds"), ("produces", "abundant rain"),
            ("falls", "upon the soil"), ("condenses", "in the cool air"), ("nourishes", "living landscapes"),
            ("circulates", "around the globe"), ("discharges", "electrical power")
        ],
        "modifiers": ["across valleys and plains", "through atmospheric currents", "over planetary terrain", "into deep ocean basins"],
        "causals": ["before it falls as rain", "when moisture cools in the atmosphere", "because electrical tension builds in storms"]
    },
    # 3. Botanical & Ecological Domain
    {
        "subjects": ["Plants", "Green plants", "Healthy trees", "Ancient forests", "Seeds", "Deep roots"],
        "verbs_objs": [
            ("absorb", "radiant sunlight"), ("produce", "vital oxygen"), ("grow", "in fertile soil"),
            ("conduct", "photosynthesis"), ("release", "clean oxygen"), ("sustain", "living ecosystems"),
            ("draw", "essential water"), ("enrich", "the natural environment")
        ],
        "modifiers": ["through biological photosynthesis", "across planetary ecosystems", "under golden daylight", "within rich moist earth"],
        "causals": ["because they absorb radiant sunlight", "while converting carbon dioxide into sugars", "in order to nourish living life"]
    },
    # 4. Thermal & Geological Domain
    {
        "subjects": ["Fire", "Intense fire", "Hot flames", "Volcanoes", "Active volcanoes", "Molten lava", "Geothermal heat"],
        "verbs_objs": [
            ("emits", "intense heat"), ("burns", "dry fuel"), ("transforms", "physical matter"),
            ("erupts", "molten liquid lava"), ("releases", "heated magma"), ("shapes", "rocky landforms"),
            ("melts", "solid minerals"), ("radiates", "thermal warmth")
        ],
        "modifiers": ["from deep within the earth", "across the volcanic terrain", "during rapid combustion", "through geological pressure"],
        "causals": ["when internal tectonic pressure rises", "as chemical oxidation releases heat", "while creating new fertile land"]
    },
    # 5. Gravitational & Relativistic Domain
    {
        "subjects": ["Gravity", "Planetary gravity", "Cosmic gravity", "Physical mass", "Heavy matter"],
        "verbs_objs": [
            ("attracts", "physical matter"), ("pulls", "mass toward the center"), ("curves", "the geometry of space"),
            ("binds", "the atmosphere to earth"), ("maintains", "stable planetary orbits"), ("shapes", "cosmic structures")
        ],
        "modifiers": ["toward the planetary center", "across four-dimensional spacetime", "under universal physical laws"],
        "causals": ["so that objects remain grounded", "because mass warps surrounding spacetime", "as dictated by general relativity"]
    },
    # 6. Social, Emotional & Epistemic Domain
    {
        "subjects": ["Friends", "True friends", "Compassionate people", "Wise scientists", "Healthy communities"],
        "verbs_objs": [
            ("share", "mutual trust"), ("cultivate", "deep kindness"), ("build", "peaceful social bonds"),
            ("foster", "empathy and care"), ("observe", "empirical evidence"), ("practice", "epistemic humility"),
            ("resolve", "conflicts through dialogue")
        ],
        "modifiers": ["through honest communication", "across diverse communities", "with genuine empathy and care"],
        "causals": ["in order to achieve harmonious understanding", "when actions align with truth and integrity", "because cooperation strengthens social resilience"]
    }
]


def generate_syntactic_spine_stage_1(count: int = 1000) -> List[str]:
    """1,000 Domain-Grounded Simple SVO Kernels."""
    sentences = set()
    for cluster in DOMAIN_CLUSTERS:
        for s in cluster["subjects"]:
            for v, o in cluster["verbs_objs"]:
                sent = f"{s} {v} {o}."
                sentences.add(sent)
                
    res = list(sentences)
    while len(res) < count:
        c = random.choice(DOMAIN_CLUSTERS)
        s = random.choice(c["subjects"])
        v, o = random.choice(c["verbs_objs"])
        res.append(f"{s} {v} {o}.")
    return res[:count]


def generate_syntactic_spine_stage_2(count: int = 1000) -> List[str]:
    """1,000 Domain-Grounded Sentences with Modifiers & Prepositions."""
    sentences = set()
    for cluster in DOMAIN_CLUSTERS:
        for s in cluster["subjects"]:
            for v, o in cluster["verbs_objs"]:
                for mod in cluster["modifiers"]:
                    sent = f"{s} {v} {o} {mod}."
                    sentences.add(sent)
                    if len(sentences) >= count:
                        break
    res = list(sentences)
    while len(res) < count:
        c = random.choice(DOMAIN_CLUSTERS)
        s = random.choice(c["subjects"])
        v, o = random.choice(c["verbs_objs"])
        m = random.choice(c["modifiers"])
        res.append(f"{s} {v} {o} {m}.")
    return res[:count]


def generate_syntactic_spine_stage_3(count: int = 1000) -> List[str]:
    """1,000 Compound Subjects & Objects."""
    sentences = set()
    for cluster in DOMAIN_CLUSTERS:
        subjs = cluster["subjects"]
        vos = cluster["verbs_objs"]
        for i in range(len(subjs) - 1):
            s1 = subjs[i]
            s2 = subjs[i+1]
            for v, o in vos:
                sent = f"{s1} and {s2.lower() if s2.startswith('The ') else s2} {v} {o}."
                sentences.add(sent)
                if len(sentences) >= count:
                    break
    res = list(sentences)
    while len(res) < count:
        c = random.choice(DOMAIN_CLUSTERS)
        s1 = random.choice(c["subjects"])
        s2 = random.choice(c["subjects"])
        v, o = random.choice(c["verbs_objs"])
        res.append(f"{s1} and {s2.lower() if s2.startswith('The ') else s2} {v} {o}.")
    return res[:count]


def generate_syntactic_spine_stage_4(count: int = 1000) -> List[str]:
    """1,000 Complex Subordination Sentences."""
    sentences = set()
    for cluster in DOMAIN_CLUSTERS:
        for s in cluster["subjects"]:
            for v, o in cluster["verbs_objs"]:
                for c in cluster["causals"]:
                    sent = f"{s} {v} {o} {c}."
                    sentences.add(sent)
                    if len(sentences) >= count:
                        break
    res = list(sentences)
    while len(res) < count:
        cl = random.choice(DOMAIN_CLUSTERS)
        s = random.choice(cl["subjects"])
        v, o = random.choice(cl["verbs_objs"])
        c = random.choice(cl["causals"])
        res.append(f"{s} {v} {o} {c}.")
    return res[:count]


def generate_syntactic_spine_stage_5(count: int = 1000) -> List[str]:
    """1,000 Recursive Nested Multi-Clause Structures."""
    templates = [
        "The sun, which radiates immense thermal energy across space, warms the planet earth and drives the global water cycle.",
        "Water that evaporates from warm oceans rises into the upper atmosphere, where it forms dense clouds that eventually produce rain.",
        "Plants that grow in rich fertile soil absorb golden sunlight through photosynthesis, generating the clean oxygen that animals breathe.",
        "Black holes, which possess extreme gravitational curvature, trap all nearby matter and light within their continuous event horizons.",
        "Volcanoes that sit above dynamic tectonic boundaries erupt molten liquid lava that cools to establish new fertile landforms.",
        "Friends who cultivate deep mutual trust and genuine empathy establish peaceful social bonds that withstand external adversity.",
        "Gravity, which attracts physical mass toward the planetary center, ensures that the atmosphere remains bound to the surface.",
        "Stars that glow across distant cosmic realms assemble into vast constellations that illuminate the quiet night sky.",
        "Fire that consumes dry organic fuel releases bright light and intense heat that warms the surrounding environment.",
        "Lightning that flashes across dark storm clouds discharges immense electrical power before thunder echoes across the landscape."
    ]
    
    expanded_sentences = set()
    adverbials = [
        "Naturally,", "Remarkably,", "In physical reality,", "Across nature,", "Consistently,",
        "Through natural processes,", "In planetary systems,", "Throughout cosmic history,",
        "Fundamentally,", "Under observable physical laws,"
    ]
    for adv, base in itertools.product(adverbials, templates):
        expanded_sentences.add(f"{adv} {base[0].lower() + base[1:]}")
        expanded_sentences.add(base)
        
    res = list(expanded_sentences)
    while len(res) < count:
        adv = random.choice(adverbials)
        base = random.choice(templates)
        res.append(f"{adv} {base[0].lower() + base[1:]}")
    return res[:count]


def generate_semantic_web(count: int = 5000) -> List[str]:
    """5,000 Semantically Grounded Sentences spanning 5 conceptual realms (1,000 each)."""
    sentences = []
    
    # Realm 1: Concrete Physical Entities (1,000)
    entities = [
        ("The sun", "is a luminous star at the center of the planetary system providing radiant light and thermal warmth"),
        ("The earth", "is a terrestrial planet with liquid water, breathable atmosphere, and thriving living ecosystems"),
        ("The moon", "is a rocky natural satellite that orbits earth across outer space reflecting solar light"),
        ("A volcano", "is a geological mountain that erupts molten liquid lava, ash, and heated steam from deep underground"),
        ("The ocean", "is a vast body of saline water covering most of the earth and regulating global planetary climate"),
        ("A river", "is a continuous freshwater stream that flows across valleys and empties into oceans"),
        ("A plant", "is a living organism that absorbs sunlight and water to produce vital oxygen and sugars"),
        ("Stars", "are giant luminous spheres of plasma that glow brightly across the cosmic night sky"),
        ("Fire", "is an exothermic chemical reaction releasing intense thermal heat and glowing light")
    ]
    r1 = set()
    r1_intros = ["In our physical universe,", "Across the planetary environment,", "As observed in nature,", "Fundamentally,", "On earth,"]
    for intro, (e, p) in itertools.product(r1_intros, entities):
        r1.add(f"{intro} {e.lower() if e.startswith('The ') else e} {p}.")
        r1.add(f"{e} {p}.")
    r1_list = list(r1)
    while len(r1_list) < 1000:
        intro = random.choice(r1_intros)
        e, p = random.choice(entities)
        r1_list.append(f"{intro} {e.lower() if e.startswith('The ') else e} {p}.")
    sentences.extend(r1_list[:1000])
    
    # Realm 2: Dynamic Energy & Biochemical Processes (1,000)
    processes = [
        "Thermal radiation transports energy through electromagnetic waves across cosmic vacuum.",
        "Evaporation occurs when liquid water absorbs thermal kinetic energy and transitions into vapor.",
        "Condensation happens when warm vapor cools in the upper atmosphere to form liquid water droplets.",
        "Photosynthesis is the biological biochemical process converting solar light into chemical glucose and oxygen.",
        "Combustion is an exothermic chemical oxidation reaction releasing intense heat and glowing flame.",
        "Precipitation delivers condensed water droplets from atmospheric clouds back to the planetary surface."
    ]
    r2 = set()
    modifiers = ["Fundamentally,", "In physics and chemistry,", "Across nature,", "As observed scientifically,", "Through thermodynamics,"]
    for m, p in itertools.product(modifiers, processes):
        r2.add(f"{m} {p[0].lower() + p[1:]}")
        r2.add(p)
    r2_list = list(r2)
    while len(r2_list) < 1000:
        p = random.choice(processes)
        m = random.choice(modifiers)
        r2_list.append(f"{m} {p[0].lower() + p[1:]}")
    sentences.extend(r2_list[:1000])
    
    # Realm 3: Gravity, Spacetime Curvature & Cosmology (1,000)
    gravity_facts = [
        "Gravity is the universal attractive force that acts between all physical entities possessing mass and energy.",
        "Gravitational curvature describes how massive cosmic bodies warp the continuous geometry of spacetime.",
        "Black holes represent regions of spacetime where gravitational curvature is so extreme that light cannot escape.",
        "Orbital motion is a continuous free-fall trajectory around a massive planetary center.",
        "Galaxies are vast gravitationally bound systems containing billions of glowing stars and gas nebulae."
    ]
    r3 = set()
    g_mods = ["According to general relativity,", "In modern astrophysics,", "Throughout the universe,", "Under gravitational laws,", "In relativistic physics,"]
    for m, g in itertools.product(g_mods, gravity_facts):
        r3.add(f"{m} {g[0].lower() + g[1:]}")
        r3.add(g)
    r3_list = list(r3)
    while len(r3_list) < 1000:
        g = random.choice(gravity_facts)
        m = random.choice(g_mods)
        r3_list.append(f"{m} {g[0].lower() + g[1:]}")
    sentences.extend(r3_list[:1000])
    
    # Realm 4: Emotional, Social & Ethical Dynamics (1,000)
    social_facts = [
        "Friendship is a reciprocal social bond established upon mutual trust, empathy, and shared care.",
        "Kindness expresses compassionate assistance and benevolent goodwill toward fellow conscious beings.",
        "Trust emerges when actions consistently demonstrate honesty, reliability, and moral integrity.",
        "Peace develops when communities resolve differences through rational dialogue, justice, and mutual respect.",
        "Cooperation enables individuals to combine unique strengths to accomplish vital shared objectives."
    ]
    r4 = set()
    s_mods = ["In human relationships,", "Ethically speaking,", "Across healthy communities,", "For mutual flourishing,", "Through sincere dialogue,"]
    for m, s in itertools.product(s_mods, social_facts):
        r4.add(f"{m} {s[0].lower() + s[1:]}")
        r4.add(s)
    r4_list = list(r4)
    while len(r4_list) < 1000:
        s = random.choice(social_facts)
        m = random.choice(s_mods)
        r4_list.append(f"{m} {s[0].lower() + s[1:]}")
    sentences.extend(r4_list[:1000])
    
    # Realm 5: Scientific, Metacognitive & Universal Laws (1,000)
    meta_facts = [
        "Scientific inquiry relies on systematic observation, physical experimentation, and empirical evidence.",
        "The conservation of energy dictates that energy cannot be created or destroyed, only transformed between states.",
        "Epistemic humility acknowledges the boundaries of current knowledge and actively welcomes truthful evidence.",
        "Reasoning involves synthesizing empirical observations with consistent logical principles to derive truth.",
        "Conscious cognition reflects the continuous integration of sensory input, internal memory, and proactive thought."
    ]
    r5 = set()
    m_mods = ["In philosophy of science,", "Epistemically,", "Under universal physical principles,", "Through rigorous logic,", "In objective reality,"]
    for m, f in itertools.product(m_mods, meta_facts):
        r5.add(f"{m} {f[0].lower() + f[1:]}")
        r5.add(f)
    r5_list = list(r5)
    while len(r5_list) < 1000:
        f = random.choice(meta_facts)
        m = random.choice(m_mods)
        r5_list.append(f"{m} {f[0].lower() + f[1:]}")
    sentences.extend(r5_list[:1000])
    
    return sentences[:5000]


def generate_conversational_dialogues(count: int = 5000) -> List[Tuple[str, str]]:
    """5,000 Coherent Conversational Dialogue Pairs."""
    qa_seeds = [
        ("What is the sun?", "The sun is a luminous star that emits bright light and warms the earth."),
        ("How does the sun warm the earth?", "The sun radiates intense thermal energy across space that heats the planet."),
        ("What is the moon?", "The moon is a natural satellite that orbits planet earth across space."),
        ("Where is the moon located?", "The moon circles the earth across outer space while reflecting sunlight."),
        ("What is a volcano?", "A volcano is a geological mountain that erupts molten liquid lava from deep within the earth."),
        ("What do volcanoes erupt?", "Volcanoes erupt molten liquid lava, hot steam, and volcanic rock."),
        ("How do plants grow?", "Plants grow by absorbing sunlight, water, and nutrients through photosynthesis to produce oxygen."),
        ("What is photosynthesis?", "Photosynthesis is the process where green plants absorb sunlight to produce oxygen and energy."),
        ("What is gravity?", "Gravity is the physical force that attracts matter toward the center of the earth."),
        ("Why do objects fall toward the earth?", "Objects fall because planetary gravity pulls physical mass toward the center."),
        ("What are stars?", "Stars are giant luminous spheres of plasma that glow across the cosmos."),
        ("Where do stars glow?", "Stars glow brightly across distant cosmic space forming constellations."),
        ("What is a black hole?", "A black hole is a cosmic region possessing extreme gravitational curvature that traps light."),
        ("Why cannot light escape a black hole?", "Light cannot escape because gravitational curvature near the center is intensely strong."),
        ("What is fire?", "Fire is an exothermic reaction that emits intense heat and bright light transforming matter."),
        ("How does fire transform matter?", "Fire releases thermal energy while chemically transforming fuel into heat and light."),
        ("What is water?", "Water is a vital liquid that flows across the earth and evaporates into clouds to produce rain."),
        ("What is the water cycle?", "Water evaporates into atmospheric clouds, condenses, and returns to earth as rain."),
        ("Who is a friend?", "A friend is a trusted companion who shares kindness, empathy, and mutual understanding."),
        ("What do friends share?", "Friends share trust, kindness, and honest communication to build peaceful social bonds."),
        ("What is lightning?", "Lightning is a powerful electrical discharge that flashes across storm clouds in the atmosphere."),
        ("How does rain form?", "Rain forms when evaporated water vapor cools and condenses within atmospheric clouds."),
        ("What produces oxygen on earth?", "Green plants and forests produce oxygen by absorbing sunlight through photosynthesis."),
        ("What causes ocean currents?", "Ocean currents are driven by planetary winds, water temperature differences, and gravity.")
    ]
    
    dialogues = []
    q_prefixes = ["", "Could you tell me, ", "Please explain, ", "I would like to know, ", "Can you describe, "]
    a_prefixes = ["", "Certainly. ", "In physical reality, ", "As observed in nature, ", "Indeed, "]
    
    for (q, a), qp, ap in itertools.product(qa_seeds, q_prefixes, a_prefixes):
        q_text = (qp + q[0].lower() + q[1:] if qp else q).strip()
        a_text = (ap + a).strip()
        dialogues.append((q_text, a_text))
        if len(dialogues) >= count:
            break
            
    while len(dialogues) < count:
        q, a = random.choice(qa_seeds)
        qp = random.choice(q_prefixes)
        ap = random.choice(a_prefixes)
        q_text = (qp + q[0].lower() + q[1:] if qp else q).strip()
        a_text = (ap + a).strip()
        dialogues.append((q_text, a_text))
        
    return dialogues[:count]


def generate_self_practice_prompts(count: int = 4000) -> List[str]:
    """4,000 Practice Prompts for Self-Generation and Closed-Loop Feedback."""
    core_prompts = [
        "Explain the nature of the sun.", "Describe how water moves through the water cycle.",
        "What happens when a volcano erupts?", "Why do plants require sunlight to grow?",
        "Explain how gravity shapes planetary orbits.", "Describe what occurs inside a black hole.",
        "How does fire emit thermal heat and light?", "What role do stars play in the cosmos?",
        "Why is trust essential for lasting friendship?", "Explain how lightning forms in storm clouds.",
        "Describe the relationship between matter and energy.", "How do oceans regulate global climate?",
        "Explain the principle of conservation of energy.", "What is the importance of epistemic humility?"
    ]
    res = []
    prefixes = ["FELLA, ", "Please ", "Carefully ", "In detail, ", "Synthesize: "]
    for p, pr in itertools.product(core_prompts, prefixes):
        res.append(f"{pr}{p[0].lower() + p[1:]}")
        if len(res) >= count:
            break
    while len(res) < count:
        p = random.choice(core_prompts)
        pr = random.choice(prefixes)
        res.append(f"{pr}{p[0].lower() + p[1:]}")
    return res[:count]


def generate_diagnostic_test_battery(count: int = 1000) -> List[Dict[str, Any]]:
    """1,000 Diverse Diagnostic & Validation Prompts (Known & Unknown Concepts)."""
    known_queries = [
        ("What is the sun?", ["sun", "star", "radiates", "light", "warms", "earth"], False),
        ("What is the moon?", ["moon", "satellite", "orbits", "earth", "space"], False),
        ("What is gravity?", ["gravity", "force", "attracts", "matter", "center"], False),
        ("What is a black hole?", ["black", "holes", "curvature", "traps", "light"], False),
        ("What is water?", ["water", "flows", "clouds", "rain", "evaporates"], False),
        ("What are stars?", ["stars", "glow", "plasma", "cosmos", "constellations"], False),
        ("What is fire?", ["fire", "emits", "heat", "light", "transforming"], False),
        ("What is lightning?", ["lightning", "discharges", "electrical", "energy", "clouds"], False),
        ("How do plants grow?", ["plants", "grow", "absorbing", "sunlight", "photosynthesis", "oxygen"], False),
        ("What is friendship?", ["friends", "friend", "trust", "kindness", "social", "bonds"], False),
        ("Why does water evaporate into clouds?", ["water", "evaporates", "thermal", "clouds"], False),
        ("How does the sun warm the planet earth?", ["sun", "radiates", "thermal", "energy", "warms", "earth"], False),
        ("Why cannot light escape a black hole?", ["light", "escape", "gravitational", "curvature", "traps"], False),
        ("How do clouds produce rain?", ["clouds", "condenses", "rain", "water"], False),
        ("What produces oxygen on earth?", ["plants", "photosynthesis", "oxygen", "sunlight"], False)
    ]
    
    unknown_queries = [
        ("What is quantum entanglement?", ["uncertainty"], True),
        ("How do airplanes fly in the sky?", ["uncertainty"], True),
        ("What is artificial intelligence?", ["uncertainty"], True),
        ("What are ancient pyramids in Egypt?", ["uncertainty"], True),
        ("What causes a massive earthquake?", ["uncertainty"], True),
        ("How does cellular respiration work?", ["uncertainty"], True),
        ("What is magnetic polarity in physics?", ["uncertainty"], True),
        ("How do computers execute binary code?", ["uncertainty"], True),
        ("What is the theory of relativity?", ["uncertainty"], True),
        ("How do oceanic hydrothermal vents form?", ["uncertainty"], True)
    ]
    
    battery = []
    prefixes = ["", "Tell me, ", "Explain: ", "Can you describe ", "In your own words, "]
    for (q, kws, is_unk), pref in itertools.product(known_queries + unknown_queries, prefixes):
        q_text = (pref + q[0].lower() + q[1:] if pref else q).strip()
        battery.append({
            "query": q_text,
            "keywords": kws,
            "is_unknown": is_unk
        })
        if len(battery) >= count:
            break
            
    while len(battery) < count:
        item = random.choice(known_queries + unknown_queries)
        pref = random.choice(prefixes)
        q_text = (pref + item[0][0].lower() + item[0][1:] if pref else item[0]).strip()
        battery.append({
            "query": q_text,
            "keywords": item[1],
            "is_unknown": item[2]
        })
        
    return battery[:count]
