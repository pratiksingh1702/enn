import itertools

class OntologicalCurriculum:
    """
    The 10-Year-Old Human Ontological Knowledge Base.
    Encodes the comprehensive structural foundation of elementary human reality:
    Physics, Chemistry, Biology, Earth Systems, Geography, Mathematics, Logic, and Society.
    Zero hardcoded logic—pure relational tuples designed for geometric entanglement.
    """
    
    @staticmethod
    def get_physics_and_chemistry():
        return [
            # Matter & Atomic Structure
            ["matter", "occupies", "space", "has", "mass"],
            ["atom", "nucleus", "protons", "neutrons", "electrons"],
            ["proton", "positive", "charge", "nucleus", "atom"],
            ["electron", "negative", "charge", "orbit", "cloud"],
            ["neutron", "neutral", "charge", "nucleus", "atom"],
            ["element", "pure", "substance", "atomic", "number"],
            ["molecule", "bonded", "atoms", "chemical", "compound"],
            ["water", "molecule", "hydrogen", "oxygen", "liquid"],
            ["carbon", "dioxide", "carbon", "oxygen", "gas"],
            
            # States of Matter & Phase Transitions
            ["matter", "exists", "solid", "liquid", "gas", "plasma"],
            ["solid", "fixed", "shape", "fixed", "volume", "rigid"],
            ["liquid", "fixed", "volume", "takes", "container", "shape"],
            ["gas", "expands", "fills", "container", "compressible"],
            ["freezing", "turns", "liquid", "into", "solid", "cooling"],
            ["melting", "turns", "solid", "into", "liquid", "heating"],
            ["boiling", "turns", "liquid", "into", "gas", "vaporization"],
            ["condensation", "turns", "gas", "into", "liquid", "cooling"],
            ["sublimation", "turns", "solid", "directly", "gas"],
            
            # Classical Mechanics & Forces
            ["force", "push", "pull", "causes", "motion", "acceleration"],
            ["gravity", "attracts", "masses", "pulls", "downward", "earth"],
            ["friction", "resists", "motion", "between", "surfaces", "heat"],
            ["velocity", "speed", "direction", "motion", "displacement"],
            ["acceleration", "rate", "change", "velocity", "force"],
            ["inertia", "resistance", "change", "motion", "mass"],
            ["momentum", "product", "mass", "velocity", "conservation"],
            
            # Energy & Thermodynamics
            ["energy", "ability", "perform", "work", "cause", "change"],
            ["kinetic", "energy", "energy", "motion", "velocity"],
            ["potential", "energy", "stored", "energy", "position", "gravity"],
            ["conservation", "energy", "cannot", "created", "destroyed", "transformed"],
            ["heat", "thermal", "energy", "flows", "hot", "cold"],
            ["temperature", "measure", "average", "kinetic", "molecular", "motion"],
            ["conduction", "heat", "transfer", "direct", "contact", "solids"],
            ["convection", "heat", "transfer", "fluid", "motion", "currents"],
            ["radiation", "heat", "transfer", "electromagnetic", "waves", "vacuum"],
            
            # Electromagnetism & Waves
            ["electricity", "flow", "electrons", "current", "conductor"],
            ["magnetism", "force", "magnetic", "poles", "attract", "repel"],
            ["light", "electromagnetic", "wave", "photons", "travels", "straight"],
            ["sound", "mechanical", "wave", "requires", "medium", "vibration"],
            ["reflection", "light", "bounces", "smooth", "surface", "mirror"],
            ["refraction", "light", "bends", "passing", "different", "mediums"]
        ]

    @staticmethod
    def get_biology_and_life():
        return [
            # Cell Biology
            ["cell", "basic", "unit", "life", "microscopic"],
            ["dna", "genetic", "code", "instructions", "heredity", "nucleus"],
            ["membrane", "surrounds", "protects", "cell", "regulates", "entry"],
            ["nucleus", "command", "center", "cell", "contains", "dna"],
            ["mitochondria", "powerhouse", "cell", "generates", "atp", "energy"],
            
            # Plant Kingdom
            ["plant", "autotroph", "produces", "own", "food", "photosynthesis"],
            ["chlorophyll", "green", "pigment", "absorbs", "sunlight", "chloroplast"],
            ["photosynthesis", "converts", "water", "carbon", "dioxide", "sunlight", "glucose", "oxygen"],
            ["roots", "anchor", "plant", "absorb", "water", "minerals", "soil"],
            ["leaves", "site", "photosynthesis", "transpiration", "gas", "exchange"],
            
            # Animal Kingdom & Taxonomy
            ["animal", "heterotroph", "consumes", "other", "organisms", "energy"],
            ["vertebrate", "animal", "possesses", "backbone", "spinal", "column"],
            ["invertebrate", "animal", "lacks", "backbone", "exoskeleton", "soft"],
            ["mammal", "vertebrate", "warm_blooded", "has", "hair", "produces", "milk"],
            ["bird", "vertebrate", "warm_blooded", "has", "feathers", "beak", "lays", "eggs"],
            ["reptile", "vertebrate", "cold_blooded", "scaly", "skin", "lays", "eggs"],
            ["amphibian", "vertebrate", "cold_blooded", "metamorphosis", "moist", "skin", "water", "land"],
            ["fish", "vertebrate", "cold_blooded", "aquatic", "gills", "fins", "scales"],
            
            # Human Physiology
            ["brain", "central", "organ", "nervous", "system", "thought", "control"],
            ["heart", "muscular", "pump", "circulates", "blood", "body", "vessels"],
            ["lungs", "respiratory", "organs", "absorb", "oxygen", "release", "carbon", "dioxide"],
            ["stomach", "digestive", "organ", "breaks", "down", "food", "acid"],
            ["skeleton", "framework", "bones", "supports", "protects", "organs"],
            ["muscles", "contractile", "tissue", "enables", "movement", "locomotion"],
            
            # Ecology & Food Webs
            ["ecosystem", "community", "living", "organisms", "interacting", "environment"],
            ["producer", "organism", "makes", "food", "plants", "algae"],
            ["consumer", "organism", "eats", "other", "organisms", "herbivore", "carnivore"],
            ["decomposer", "breaks", "down", "dead", "organic", "matter", "bacteria", "fungi"],
            ["herbivore", "primary", "consumer", "eats", "only", "plants"],
            ["carnivore", "predator", "consumer", "eats", "meat", "animals"],
            ["omnivore", "consumer", "eats", "both", "plants", "animals"]
        ]

    @staticmethod
    def get_earth_and_space():
        return [
            # Earth Structure
            ["earth", "spherical", "terrestrial", "planet", "supports", "life"],
            ["core", "dense", "metallic", "center", "earth", "iron", "nickel"],
            ["mantle", "hot", "semi_solid", "rock", "layer", "beneath", "crust"],
            ["crust", "outermost", "solid", "rocky", "surface", "earth"],
            ["plate", "tectonics", "continental", "drift", "causes", "earthquakes", "volcanoes", "mountains"],
            
            # Hydrology & Atmosphere
            ["water", "cycle", "evaporation", "condensation", "precipitation", "collection"],
            ["evaporation", "sun", "heats", "water", "transforms", "vapor", "atmosphere"],
            ["condensation", "water", "vapor", "cools", "forms", "clouds"],
            ["precipitation", "water", "falls", "clouds", "rain", "snow", "sleet", "hail"],
            ["atmosphere", "layer", "gases", "surrounding", "earth", "nitrogen", "oxygen"],
            ["troposphere", "lowest", "atmospheric", "layer", "weather", "clouds", "air"],
            
            # Solar System & Astronomy
            ["sun", "yellow", "dwarf", "star", "center", "solar", "system", "gravity"],
            ["mercury", "first", "planet", "closest", "sun", "terrestrial"],
            ["venus", "second", "planet", "thick", "atmosphere", "hottest", "greenhouse"],
            ["earth", "third", "planet", "liquid", "water", "oxygen", "moon"],
            ["mars", "fourth", "planet", "red", "planet", "iron", "oxide"],
            ["jupiter", "fifth", "planet", "largest", "gas", "giant", "great", "red", "spot"],
            ["saturn", "sixth", "planet", "gas", "giant", "prominent", "rings"],
            ["uranus", "seventh", "planet", "ice", "giant", "tilted", "axis"],
            ["neptune", "eighth", "planet", "ice", "giant", "furthest", "blue"],
            ["rotation", "earth", "spins", "axis", "twenty_four", "hours", "day", "night"],
            ["revolution", "earth", "orbits", "sun", "three_hundred_sixty_five", "days", "year", "seasons"]
        ]

    @staticmethod
    def get_mathematics_and_piaget_logic():
        return [
            # Concrete Operational Logic (Transitivity, Conservation, Seriation)
            ["transitivity", "logic", "rule", "if", "a", "greater", "b", "and", "b", "greater", "c", "then", "a", "greater", "c"],
            ["conservation", "logic", "quantity", "remains", "same", "despite", "shape", "transformation"],
            ["reversibility", "logic", "action", "can", "undone", "returned", "original", "state"],
            ["classification", "grouping", "objects", "hierarchical", "categories", "shared", "properties"],
            ["seriation", "arranging", "elements", "quantitative", "order", "size", "weight", "length"],
            
            # Numbers, Fractions & Operations
            ["addition", "combining", "quantities", "sum", "inverse", "subtraction"],
            ["subtraction", "removing", "quantity", "difference", "inverse", "addition"],
            ["multiplication", "repeated", "addition", "product", "scaling"],
            ["division", "splitting", "equal", "parts", "quotient", "inverse", "multiplication"],
            ["fraction", "part", "whole", "numerator", "divided", "denominator"],
            ["zero", "represents", "absence", "quantity", "additive", "identity"],
            
            # Geometry & Dimensions
            ["dimension", "one", "line", "length", "distance"],
            ["dimension", "two", "plane", "length", "width", "area"],
            ["dimension", "three", "space", "length", "width", "height", "volume"],
            ["polygon", "closed", "two_dimensional", "shape", "straight", "sides"],
            ["triangle", "polygon", "three", "sides", "three", "angles", "one_eighty", "degrees"],
            ["quadrilateral", "polygon", "four", "sides", "four", "angles"],
            ["rectangle", "quadrilateral", "four", "right", "angles", "opposite", "equal"],
            ["square", "rectangle", "four", "equal", "sides", "four", "right", "angles"],
            ["circle", "continuous", "curve", "equidistant", "center", "radius", "diameter"]
        ]

    @staticmethod
    def get_geography_tools_and_society():
        return [
            # Geography
            ["continent", "large", "continuous", "landmass", "seven", "earth"],
            ["asia", "largest", "continent", "highest", "population", "mount", "everest"],
            ["africa", "second", "largest", "continent", "sahara", "nile", "river"],
            ["north_america", "continent", "canada", "united_states", "mexico"],
            ["south_america", "continent", "amazon", "rainforest", "andes", "mountains"],
            ["antarctica", "southernmost", "continent", "ice", "sheet", "coldest"],
            ["europe", "continent", "borders", "asia", "ural", "mountains"],
            ["australia", "smallest", "continent", "oceania", "island"],
            ["ocean", "vast", "body", "saltwater", "covers", "seventy", "percent", "earth"],
            ["pacific", "ocean", "largest", "deepest", "ocean", "mariana", "trench"],
            ["atlantic", "ocean", "separates", "americas", "europe", "africa"],
            
            # Simple Machines & Tools
            ["machine", "device", "modifies", "force", "direction", "mechanical", "advantage"],
            ["lever", "simple", "machine", "rigid", "beam", "pivots", "fulcrum"],
            ["wheel", "axle", "simple", "machine", "reduces", "rotational", "friction"],
            ["pulley", "wheel", "groove", "rope", "changes", "force", "direction"],
            ["inclined", "plane", "slanted", "surface", "reduces", "effort", "lifting"],
            ["wedge", "portable", "inclined", "plane", "splits", "cuts", "objects"],
            ["screw", "inclined", "plane", "wrapped", "around", "cylinder"],
            
            # Society & Communication
            ["language", "system", "communication", "sounds", "symbols", "grammar", "meaning"],
            ["writing", "visual", "representation", "speech", "preserves", "knowledge", "time"],
            ["rule", "standard", "guide", "conduct", "fairness", "community", "safety"],
            ["trade", "exchange", "goods", "services", "currency", "mutual", "benefit"]
        ]

    @classmethod
    def get_full_curriculum(cls):
        """Compiles the entire Grade 1–5 human ontological foundation."""
        all_events = (
            cls.get_physics_and_chemistry() +
            cls.get_biology_and_life() +
            cls.get_earth_and_space() +
            cls.get_mathematics_and_piaget_logic() +
            cls.get_geography_tools_and_society()
        )
        return all_events
