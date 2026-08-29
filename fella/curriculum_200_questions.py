"""
FELLA 200-Question Metacognitive Reinforcement & Trait-Driven Feedback Curriculum
================================================================================
Comprehensive 200-question curriculum across 8 scientific and cognitive domains:
1. Astronomy & Astrophysics (25 questions)
2. Earth Sciences & Geology (25 questions)
3. Hydrology & Meteorology (25 questions)
4. Botany & Cellular Biology (25 questions)
5. Fundamental Physics & Mechanics (25 questions)
6. Thermal Science & Chemistry (25 questions)
7. Social Cognition & Ethics (25 questions)
8. Metacognition & Self-Evolution (25 questions)

Learning is 100% dynamic through continuous Hebbian potentiation/depression,
trait field energy basin shifts (ASPIRE/CAUTION), and continuous memory ingestion.
Zero hardcoded if/else responses.
"""

import os
import sys
import time
import re
from typing import List, Dict, Any, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain

# =============================================================================
# 200 COMPREHENSIVE CURRICULUM QUESTIONS & GROUND-TRUTH CONCEPT EXPLANATIONS
# =============================================================================
CURRICULUM_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # 1. Astronomy & Astrophysics (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Astronomy",
        "question": "What is the sun?",
        "keywords": ["sun", "radiates", "light", "thermal", "energy", "star", "warmth"],
        "correct_explanation": "The sun is a luminous star that radiates electromagnetic light and thermal energy warming the solar system."
    },
    {
        "domain": "Astronomy",
        "question": "Where is the moon located?",
        "keywords": ["moon", "orbits", "planet", "earth", "space"],
        "correct_explanation": "The moon is a natural celestial satellite that orbits the planet earth across space."
    },
    {
        "domain": "Astronomy",
        "question": "What are stars?",
        "keywords": ["stars", "glow", "cosmos", "constellations", "sky", "celestial"],
        "correct_explanation": "Stars are celestial bodies of plasma that glow across the cosmos forming constellations in the night sky."
    },
    {
        "domain": "Astronomy",
        "question": "What is a black hole?",
        "keywords": ["black", "holes", "gravitational", "curvature", "traps", "light", "extreme"],
        "correct_explanation": "Black holes possess extreme gravitational curvature that traps all matter and light."
    },
    {
        "domain": "Astronomy",
        "question": "What is a supernova?",
        "keywords": ["supernova", "massive", "stars", "collapse", "explode", "space"],
        "correct_explanation": "A supernova occurs when a massive star collapses and explodes releasing tremendous radiant energy across space."
    },
    {
        "domain": "Astronomy",
        "question": "What is a galaxy?",
        "keywords": ["galaxy", "billions", "stars", "gas", "gravity", "cosmos"],
        "correct_explanation": "A galaxy is a massive gravitationally bound system consisting of billions of stars gas and cosmic dust."
    },
    {
        "domain": "Astronomy",
        "question": "What is a solar eclipse?",
        "keywords": ["eclipse", "moon", "passes", "sun", "earth", "shadow"],
        "correct_explanation": "A solar eclipse occurs when the moon passes between the sun and earth casting a dark shadow."
    },
    {
        "domain": "Astronomy",
        "question": "What are comets?",
        "keywords": ["comets", "icy", "bodies", "orbit", "sun", "tail"],
        "correct_explanation": "Comets are icy celestial bodies that orbit the sun releasing gas and dust into glowing tails."
    },
    {
        "domain": "Astronomy",
        "question": "What are asteroids?",
        "keywords": ["asteroids", "rocky", "objects", "orbiting", "sun", "space"],
        "correct_explanation": "Asteroids are rocky metallic objects orbiting the sun primarily within the asteroid belt."
    },
    {
        "domain": "Astronomy",
        "question": "What is a nebula?",
        "keywords": ["nebula", "interstellar", "cloud", "dust", "gas", "stars"],
        "correct_explanation": "A nebula is a vast interstellar cloud of dust and gas where new stars are born."
    },
    {
        "domain": "Astronomy",
        "question": "What is the Milky Way?",
        "keywords": ["milky", "way", "spiral", "galaxy", "solar", "system"],
        "correct_explanation": "The Milky Way is the vast barred spiral galaxy that contains our solar system and billions of stars."
    },
    {
        "domain": "Astronomy",
        "question": "What is a planet?",
        "keywords": ["planet", "celestial", "body", "orbits", "star", "mass"],
        "correct_explanation": "A planet is a large celestial body that orbits a star and has cleared its orbital path."
    },
    {
        "domain": "Astronomy",
        "question": "What is orbital velocity?",
        "keywords": ["orbital", "velocity", "speed", "body", "orbit", "gravity"],
        "correct_explanation": "Orbital velocity is the precise speed required for a celestial body to maintain a stable orbit around a gravitational center."
    },
    {
        "domain": "Astronomy",
        "question": "What are cosmic rays?",
        "keywords": ["cosmic", "rays", "high", "energy", "particles", "space"],
        "correct_explanation": "Cosmic rays are high energy atomic particles originating from outer space traveling at nearly the speed of light."
    },
    {
        "domain": "Astronomy",
        "question": "What is the cosmic microwave background?",
        "keywords": ["cosmic", "microwave", "background", "radiation", "early", "universe"],
        "correct_explanation": "The cosmic microwave background is the thermal remnant radiation left over from the early formation of the universe."
    },
    {
        "domain": "Astronomy",
        "question": "What is dark matter?",
        "keywords": ["dark", "matter", "invisible", "gravitational", "effects", "galaxies"],
        "correct_explanation": "Dark matter is an invisible form of matter that does not interact with light but exerts strong gravitational effects on galaxies."
    },
    {
        "domain": "Astronomy",
        "question": "What is dark energy?",
        "keywords": ["dark", "energy", "force", "accelerating", "expansion", "universe"],
        "correct_explanation": "Dark energy is a mysterious cosmological force driving the accelerated expansion of the universe."
    },
    {
        "domain": "Astronomy",
        "question": "What is a neutron star?",
        "keywords": ["neutron", "star", "dense", "collapsed", "core", "supernova"],
        "correct_explanation": "A neutron star is the extremely dense collapsed core of a massive star remaining after a supernova explosion."
    },
    {
        "domain": "Astronomy",
        "question": "What is a pulsar?",
        "keywords": ["pulsar", "rotating", "neutron", "star", "beams", "radiation"],
        "correct_explanation": "A pulsar is a highly magnetized rotating neutron star that emits periodic beams of electromagnetic radiation."
    },
    {
        "domain": "Astronomy",
        "question": "What is a light year?",
        "keywords": ["light", "year", "distance", "light", "travels", "year"],
        "correct_explanation": "A light year is an astronomical unit of distance representing how far light travels through a vacuum in one earth year."
    },
    {
        "domain": "Astronomy",
        "question": "What is an exoplanet?",
        "keywords": ["exoplanet", "planet", "orbits", "star", "outside", "solar"],
        "correct_explanation": "An exoplanet is any planet located outside our solar system that orbits another distant star."
    },
    {
        "domain": "Astronomy",
        "question": "What is the event horizon?",
        "keywords": ["event", "horizon", "boundary", "black", "hole", "escape"],
        "correct_explanation": "The event horizon is the theoretical boundary around a black hole beyond which nothing can escape."
    },
    {
        "domain": "Astronomy",
        "question": "What causes lunar phases?",
        "keywords": ["lunar", "phases", "moon", "orbits", "earth", "sunlight"],
        "correct_explanation": "Lunar phases are caused by changing angles of illuminated sunlight on the moon as it orbits around the earth."
    },
    {
        "domain": "Astronomy",
        "question": "What is the solar wind?",
        "keywords": ["solar", "wind", "stream", "charged", "particles", "sun"],
        "correct_explanation": "The solar wind is a continuous stream of charged plasma particles released from the upper atmosphere of the sun."
    },
    {
        "domain": "Astronomy",
        "question": "What are auroras?",
        "keywords": ["auroras", "solar", "wind", "interacts", "magnetic", "atmosphere"],
        "correct_explanation": "Auroras are colorful atmospheric light displays created when charged solar wind particles interact with earth magnetic field."
    },

    # -------------------------------------------------------------------------
    # 2. Earth Sciences & Geology (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Geology",
        "question": "What is earth?",
        "keywords": ["earth", "terrestrial", "planet", "crust", "atmosphere", "oceans"],
        "correct_explanation": "The earth is a terrestrial planet with a solid rock crust, deep liquid oceans, and a life-supporting atmosphere."
    },
    {
        "domain": "Geology",
        "question": "What is a volcano?",
        "keywords": ["volcano", "volcanoes", "erupt", "molten", "lava", "earth"],
        "correct_explanation": "Volcanoes are geological vents that erupt molten liquid lava and gases from deep magma reservoirs inside the earth."
    },
    {
        "domain": "Geology",
        "question": "What is plate tectonics?",
        "keywords": ["plate", "tectonics", "lithosphere", "plates", "move", "mantle"],
        "correct_explanation": "Plate tectonics is the scientific theory describing how large rigid lithospheric plates move across the convective mantle."
    },
    {
        "domain": "Geology",
        "question": "What causes an earthquake?",
        "keywords": ["earthquake", "sudden", "release", "energy", "faults", "crust"],
        "correct_explanation": "Earthquakes occur when stress builds up along geological faults and suddenly releases kinetic energy shaking the crust."
    },
    {
        "domain": "Geology",
        "question": "What is magma?",
        "keywords": ["magma", "molten", "rock", "beneath", "earth", "surface"],
        "correct_explanation": "Magma is extremely hot molten rock and dissolved gases situated beneath the solid crust of the earth."
    },
    {
        "domain": "Geology",
        "question": "What is lava?",
        "keywords": ["lava", "molten", "rock", "erupts", "surface", "volcano"],
        "correct_explanation": "Lava is molten rock that breaches the surface of the earth during a volcanic eruption."
    },
    {
        "domain": "Geology",
        "question": "What is the earth core?",
        "keywords": ["earth", "core", "dense", "metallic", "iron", "nickel", "center"],
        "correct_explanation": "The earth core is the extremely hot dense metallic center composed primarily of iron and nickel."
    },
    {
        "domain": "Geology",
        "question": "What is the earth mantle?",
        "keywords": ["earth", "mantle", "thick", "layer", "semi", "solid", "rock"],
        "correct_explanation": "The mantle is the thick layer of semi-solid convective silicate rock between the earth crust and outer core."
    },
    {
        "domain": "Geology",
        "question": "What is the earth crust?",
        "keywords": ["earth", "crust", "outermost", "solid", "rock", "layer"],
        "correct_explanation": "The earth crust is the thin outermost solid rock layer that forms the continents and ocean basins."
    },
    {
        "domain": "Geology",
        "question": "What are sedimentary rocks?",
        "keywords": ["sedimentary", "rocks", "formed", "accumulation", "mineral", "layers"],
        "correct_explanation": "Sedimentary rocks are formed through the gradual accumulation compaction and cementation of mineral and organic particles."
    },
    {
        "domain": "Geology",
        "question": "What are igneous rocks?",
        "keywords": ["igneous", "rocks", "formed", "cooling", "solidification", "magma"],
        "correct_explanation": "Igneous rocks are formed through the cooling and solidification of molten magma or volcanic lava."
    },
    {
        "domain": "Geology",
        "question": "What are metamorphic rocks?",
        "keywords": ["metamorphic", "rocks", "transformed", "intense", "heat", "pressure"],
        "correct_explanation": "Metamorphic rocks are created when existing rocks are transformed by intense underground heat and pressure."
    },
    {
        "domain": "Geology",
        "question": "What is erosion?",
        "keywords": ["erosion", "geological", "process", "materials", "transported", "wind", "water"],
        "correct_explanation": "Erosion is the natural geological process where surface rock and soil materials are worn away and transported by wind or water."
    },
    {
        "domain": "Geology",
        "question": "What is weathering?",
        "keywords": ["weathering", "breakdown", "rocks", "minerals", "surface"],
        "correct_explanation": "Weathering is the physical chemical and biological breakdown of rocks and minerals directly at the earth surface."
    },
    {
        "domain": "Geology",
        "question": "What are minerals?",
        "keywords": ["minerals", "naturally", "occurring", "inorganic", "solid", "crystalline"],
        "correct_explanation": "Minerals are naturally occurring inorganic solid substances with a defined chemical composition and crystalline structure."
    },
    {
        "domain": "Geology",
        "question": "What is a glacier?",
        "keywords": ["glacier", "massive", "persistent", "body", "dense", "ice"],
        "correct_explanation": "A glacier is a massive persistent body of dense compacted ice that moves slowly under its own weight."
    },
    {
        "domain": "Geology",
        "question": "What is a tsunami?",
        "keywords": ["tsunami", "series", "enormous", "ocean", "waves", "earthquake"],
        "correct_explanation": "A tsunami is a series of enormous ocean waves caused by sudden underwater earthquakes or volcanic eruptions."
    },
    {
        "domain": "Geology",
        "question": "What is soil?",
        "keywords": ["soil", "mixture", "organic", "matter", "minerals", "gases", "water"],
        "correct_explanation": "Soil is a vital natural mixture of decomposed organic matter minerals gases liquids and living organisms."
    },
    {
        "domain": "Geology",
        "question": "What are fossils?",
        "keywords": ["fossils", "preserved", "remains", "traces", "ancient", "organisms"],
        "correct_explanation": "Fossils are the preserved physical remains or impressions of ancient organisms preserved in sedimentary geological strata."
    },
    {
        "domain": "Geology",
        "question": "What is the rock cycle?",
        "keywords": ["rock", "cycle", "continuous", "transitions", "igneous", "sedimentary", "metamorphic"],
        "correct_explanation": "The rock cycle is the continuous geological concept describing the transitions between igneous sedimentary and metamorphic rocks."
    },
    {
        "domain": "Geology",
        "question": "What is a geological fault?",
        "keywords": ["fault", "fracture", "rock", "crust", "displacement"],
        "correct_explanation": "A fault is a planar fracture or discontinuity in rock volume where there has been significant displacement."
    },
    {
        "domain": "Geology",
        "question": "What is the continental drift?",
        "keywords": ["continental", "drift", "continents", "shifted", "positions", "oceans"],
        "correct_explanation": "Continental drift describes how earth continents have gradually shifted positions across geological epochs."
    },
    {
        "domain": "Geology",
        "question": "What is Pangaea?",
        "keywords": ["pangaea", "supercontinent", "incorporated", "landmasses", "ancient"],
        "correct_explanation": "Pangaea was a massive supercontinent that incorporated almost all the landmasses on earth during the late Paleozoic."
    },
    {
        "domain": "Geology",
        "question": "What is geothermal energy?",
        "keywords": ["geothermal", "energy", "thermal", "heat", "originating", "earth"],
        "correct_explanation": "Geothermal energy is natural thermal energy generated and stored inside the interior of the earth."
    },
    {
        "domain": "Geology",
        "question": "What causes mountain formation?",
        "keywords": ["mountains", "formed", "tectonic", "plates", "collide", "uplift"],
        "correct_explanation": "Mountains are formed when tectonic plates collide exerting immense pressure that folds and uplifts the crust."
    },

    # -------------------------------------------------------------------------
    # 3. Hydrology & Meteorology (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Hydrology",
        "question": "What is the water cycle?",
        "keywords": ["water", "cycle", "evaporates", "clouds", "rain", "oceans"],
        "correct_explanation": "The water cycle describes how water evaporates into vapor cools into clouds and returns as liquid precipitation."
    },
    {
        "domain": "Hydrology",
        "question": "What is water?",
        "keywords": ["water", "liquid", "flows", "earth", "evaporates", "rain"],
        "correct_explanation": "Water is a vital liquid compound of hydrogen and oxygen that flows across the earth and supports life."
    },
    {
        "domain": "Hydrology",
        "question": "What is evaporation?",
        "keywords": ["evaporation", "heat", "transforms", "liquid", "vapor"],
        "correct_explanation": "Evaporation is the physical process where thermal heat transforms liquid water into invisible airborne vapor."
    },
    {
        "domain": "Hydrology",
        "question": "What are clouds?",
        "keywords": ["clouds", "condensed", "water", "vapor", "droplets", "atmosphere"],
        "correct_explanation": "Clouds are visible atmospheric masses of condensed microscopic water droplets and ice crystals."
    },
    {
        "domain": "Hydrology",
        "question": "What is rain?",
        "keywords": ["rain", "liquid", "precipitation", "falls", "clouds", "earth"],
        "correct_explanation": "Rain is liquid precipitation that condenses in clouds and falls under gravity to nourish the earth."
    },
    {
        "domain": "Hydrology",
        "question": "What is snow?",
        "keywords": ["snow", "crystalline", "frozen", "ice", "falls", "clouds"],
        "correct_explanation": "Snow is frozen crystalline water precipitation that forms when atmospheric water vapor freezes into delicate flakes."
    },
    {
        "domain": "Hydrology",
        "question": "What is the atmosphere?",
        "keywords": ["atmosphere", "layer", "gases", "surrounding", "planet", "earth"],
        "correct_explanation": "The atmosphere is the envelope of nitrogen oxygen and other gases that surrounds the planet earth."
    },
    {
        "domain": "Hydrology",
        "question": "What causes wind?",
        "keywords": ["wind", "caused", "air", "pressure", "differences", "temperature"],
        "correct_explanation": "Wind is caused by atmospheric pressure differences resulting from uneven solar heating of the earth surface."
    },
    {
        "domain": "Hydrology",
        "question": "What is condensation?",
        "keywords": ["condensation", "gas", "vapor", "cools", "liquid"],
        "correct_explanation": "Condensation is the physical state change where water vapor cools and transforms back into liquid water droplets."
    },
    {
        "domain": "Hydrology",
        "question": "What is humidity?",
        "keywords": ["humidity", "concentration", "water", "vapor", "air"],
        "correct_explanation": "Humidity is the concentration and measurement of water vapor present in the ambient atmosphere."
    },
    {
        "domain": "Hydrology",
        "question": "What is a hurricane?",
        "keywords": ["hurricane", "intense", "tropical", "storm", "winds", "rain"],
        "correct_explanation": "A hurricane is an intense rotating tropical storm system with high speed winds heavy rains and low pressure."
    },
    {
        "domain": "Hydrology",
        "question": "What is a tornado?",
        "keywords": ["tornado", "violently", "rotating", "column", "air", "ground"],
        "correct_explanation": "A tornado is a violently rotating narrow column of air extending from a thunderstorm to the ground."
    },
    {
        "domain": "Hydrology",
        "question": "What is atmospheric pressure?",
        "keywords": ["atmospheric", "pressure", "force", "weight", "air", "surface"],
        "correct_explanation": "Atmospheric pressure is the gravitational downward force exerted by the weight of air molecules on the surface."
    },
    {
        "domain": "Hydrology",
        "question": "What causes lightning?",
        "keywords": ["lightning", "electrical", "discharge", "storm", "clouds", "ground"],
        "correct_explanation": "Lightning is a powerful electrostatic discharge between charged regions of storm clouds or between clouds and ground."
    },
    {
        "domain": "Hydrology",
        "question": "What is thunder?",
        "keywords": ["thunder", "acoustic", "sound", "rapid", "expansion", "air"],
        "correct_explanation": "Thunder is the sonic shockwave produced by the explosive thermal expansion of air heated by lightning."
    },
    {
        "domain": "Hydrology",
        "question": "What is an ocean current?",
        "keywords": ["ocean", "current", "continuous", "directed", "movement", "seawater"],
        "correct_explanation": "An ocean current is a continuous directed stream of seawater driven by winds temperature differences and the Coriolis effect."
    },
    {
        "domain": "Hydrology",
        "question": "What causes ocean tides?",
        "keywords": ["tides", "gravitational", "pull", "moon", "sun", "oceans"],
        "correct_explanation": "Ocean tides are rhythmic rises and falls in sea level caused by the gravitational pull of the moon and sun."
    },
    {
        "domain": "Hydrology",
        "question": "What is groundwater?",
        "keywords": ["groundwater", "water", "held", "underground", "soil", "aquifers"],
        "correct_explanation": "Groundwater is freshwater located beneath the earth surface in soil pore spaces and permeable rock aquifers."
    },
    {
        "domain": "Hydrology",
        "question": "What is an aquifer?",
        "keywords": ["aquifer", "underground", "layer", "water", "bearing", "rock"],
        "correct_explanation": "An aquifer is an underground geological formation of permeable rock or sediment that stores and yields groundwater."
    },
    {
        "domain": "Hydrology",
        "question": "What is the greenhouse effect?",
        "keywords": ["greenhouse", "effect", "gases", "trap", "heat", "atmosphere"],
        "correct_explanation": "The greenhouse effect is the natural warming process where atmospheric gases trap infrared thermal radiation from earth."
    },
    {
        "domain": "Hydrology",
        "question": "What is ozone?",
        "keywords": ["ozone", "molecule", "three", "oxygen", "absorbs", "ultraviolet"],
        "correct_explanation": "Ozone is a triatomic oxygen molecule in the stratosphere that absorbs harmful solar ultraviolet radiation."
    },
    {
        "domain": "Hydrology",
        "question": "What is fog?",
        "keywords": ["fog", "thick", "cloud", "water", "droplets", "ground"],
        "correct_explanation": "Fog is a dense cloud of microscopic water droplets suspended in the air near the earth surface."
    },
    {
        "domain": "Hydrology",
        "question": "What is dew?",
        "keywords": ["dew", "water", "droplets", "condense", "cool", "surfaces"],
        "correct_explanation": "Dew forms when ambient water vapor condenses directly onto cool exposed surfaces during the calm night."
    },
    {
        "domain": "Hydrology",
        "question": "What is drought?",
        "keywords": ["drought", "prolonged", "period", "abnormally", "low", "rainfall"],
        "correct_explanation": "A drought is a prolonged period of abnormally low precipitation leading to severe water shortages and parched land."
    },
    {
        "domain": "Hydrology",
        "question": "What is transpiration?",
        "keywords": ["transpiration", "plants", "release", "water", "vapor", "leaves"],
        "correct_explanation": "Transpiration is the biological process where plant roots absorb water and release it as vapor through leaf stomata."
    },

    # -------------------------------------------------------------------------
    # 4. Botany & Cellular Biology (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Biology",
        "question": "How do plants grow?",
        "keywords": ["plants", "grow", "absorbing", "sunlight", "water", "photosynthesis", "oxygen"],
        "correct_explanation": "Plants grow by absorbing sunlight water and minerals through photosynthesis to produce glucose and oxygen."
    },
    {
        "domain": "Biology",
        "question": "What is photosynthesis?",
        "keywords": ["photosynthesis", "plants", "convert", "sunlight", "glucose", "oxygen"],
        "correct_explanation": "Photosynthesis is the biochemical process by which green plants convert solar energy and water into glucose and oxygen."
    },
    {
        "domain": "Biology",
        "question": "What are mitochondria?",
        "keywords": ["mitochondria", "generate", "cellular", "energy", "respiration"],
        "correct_explanation": "Mitochondria are cellular organelles that generate vital biochemical energy through cellular respiration."
    },
    {
        "domain": "Biology",
        "question": "What is chlorophyll?",
        "keywords": ["chlorophyll", "green", "pigment", "absorbs", "light", "photosynthesis"],
        "correct_explanation": "Chlorophyll is the green pigment in plant chloroplasts that absorbs light energy to fuel photosynthesis."
    },
    {
        "domain": "Biology",
        "question": "What are plant roots?",
        "keywords": ["roots", "anchor", "plant", "absorb", "water", "minerals"],
        "correct_explanation": "Roots anchor the plant in the soil and absorb essential water and dissolved minerals from the ground."
    },
    {
        "domain": "Biology",
        "question": "What is cellular respiration?",
        "keywords": ["cellular", "respiration", "cells", "break", "down", "glucose", "energy"],
        "correct_explanation": "Cellular respiration is the metabolic pathway where biological cells break down glucose to generate ATP energy."
    },
    {
        "domain": "Biology",
        "question": "What is DNA?",
        "keywords": ["dna", "molecule", "carries", "genetic", "instructions", "life"],
        "correct_explanation": "DNA is the double-helix molecule that carries genetic hereditary instructions for all living organisms."
    },
    {
        "domain": "Biology",
        "question": "What are cells?",
        "keywords": ["cells", "basic", "structural", "functional", "units", "life"],
        "correct_explanation": "Cells are the fundamental structural and functional units of all known living biological organisms."
    },
    {
        "domain": "Biology",
        "question": "What are proteins?",
        "keywords": ["proteins", "large", "biomolecules", "amino", "acids", "functions"],
        "correct_explanation": "Proteins are complex biomolecules composed of amino acid chains that perform vital biological functions."
    },
    {
        "domain": "Biology",
        "question": "What are enzymes?",
        "keywords": ["enzymes", "biological", "catalysts", "accelerate", "chemical", "reactions"],
        "correct_explanation": "Enzymes are specialized biological catalysts that significantly accelerate biochemical reactions in living cells."
    },
    {
        "domain": "Biology",
        "question": "What is pollination?",
        "keywords": ["pollination", "transfer", "pollen", "flowers", "fertilization"],
        "correct_explanation": "Pollination is the transfer of pollen grains between flowering plants enabling fertilization and seed production."
    },
    {
        "domain": "Biology",
        "question": "What are seeds?",
        "keywords": ["seeds", "embryonic", "plants", "enclosed", "protective", "coat"],
        "correct_explanation": "Seeds are embryonic plants enclosed within protective outer coats capable of germinating into new plants."
    },
    {
        "domain": "Biology",
        "question": "What is xylem?",
        "keywords": ["xylem", "plant", "vascular", "tissue", "transports", "water"],
        "correct_explanation": "Xylem is specialized plant vascular tissue that transports water and dissolved nutrients upward from roots to leaves."
    },
    {
        "domain": "Biology",
        "question": "What is phloem?",
        "keywords": ["phloem", "plant", "tissue", "transports", "sugars", "nutrients"],
        "correct_explanation": "Phloem is plant vascular tissue that distributes soluble organic nutrients and synthesized sugars throughout the plant."
    },
    {
        "domain": "Biology",
        "question": "What is mitosis?",
        "keywords": ["mitosis", "cell", "division", "produces", "identical", "cells"],
        "correct_explanation": "Mitosis is the process of cell division where a single parent cell divides into two genetically identical daughter cells."
    },
    {
        "domain": "Biology",
        "question": "What is an ecosystem?",
        "keywords": ["ecosystem", "community", "living", "organisms", "interacting", "environment"],
        "correct_explanation": "An ecosystem is a biological community of interacting living organisms and their non-living physical environment."
    },
    {
        "domain": "Biology",
        "question": "What is biodiversity?",
        "keywords": ["biodiversity", "variety", "life", "species", "genes", "ecosystems"],
        "correct_explanation": "Biodiversity refers to the rich variety of all life forms species genes and ecosystems across planet earth."
    },
    {
        "domain": "Biology",
        "question": "What are chloroplasts?",
        "keywords": ["chloroplasts", "plant", "organelles", "conduct", "photosynthesis"],
        "correct_explanation": "Chloroplasts are specialized plant cell organelles that capture solar light energy to perform photosynthesis."
    },
    {
        "domain": "Biology",
        "question": "What is glucose?",
        "keywords": ["glucose", "simple", "sugar", "primary", "source", "energy"],
        "correct_explanation": "Glucose is a primary simple sugar molecule that serves as the main chemical energy source for cellular metabolism."
    },
    {
        "domain": "Biology",
        "question": "What are stomata?",
        "keywords": ["stomata", "microscopic", "pores", "leaves", "gas", "exchange"],
        "correct_explanation": "Stomata are microscopic pores on plant leaves that regulate the exchange of oxygen carbon dioxide and water vapor."
    },
    {
        "domain": "Biology",
        "question": "What is germination?",
        "keywords": ["germination", "growth", "embryo", "seed", "seedling"],
        "correct_explanation": "Germination is the physiological process where a dormant plant seed resumes active growth and develops into a seedling."
    },
    {
        "domain": "Biology",
        "question": "What is natural selection?",
        "keywords": ["natural", "selection", "organisms", "adapt", "survive", "reproduce"],
        "correct_explanation": "Natural selection is the evolutionary mechanism where organisms better adapted to their environment tend to survive and reproduce."
    },
    {
        "domain": "Biology",
        "question": "What are bacteria?",
        "keywords": ["bacteria", "single", "celled", "microorganisms", "ecosystems"],
        "correct_explanation": "Bacteria are ubiquitous single-celled microscopic organisms that play vital roles in nutrient cycling and ecosystems."
    },
    {
        "domain": "Biology",
        "question": "What are fungi?",
        "keywords": ["fungi", "eukaryotic", "organisms", "decompose", "organic", "matter"],
        "correct_explanation": "Fungi are eukaryotic organisms like mushrooms and yeasts that decompose organic matter and recycle essential nutrients."
    },
    {
        "domain": "Biology",
        "question": "What is homeostasis in biology?",
        "keywords": ["homeostasis", "biological", "state", "steady", "internal", "conditions"],
        "correct_explanation": "Homeostasis is the state of steady internal physical and chemical conditions maintained by living biological systems."
    },

    # -------------------------------------------------------------------------
    # 5. Fundamental Physics & Mechanics (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Physics",
        "question": "What is gravity?",
        "keywords": ["gravity", "fundamental", "force", "attracts", "physical", "matter", "earth"],
        "correct_explanation": "Gravity is the fundamental attractive physical force that pulls physical matter toward the center of mass."
    },
    {
        "domain": "Physics",
        "question": "What is speed?",
        "keywords": ["speed", "rate", "change", "position", "direction", "time"],
        "correct_explanation": "Speed is the scalar physical rate of change of position of an object over time."
    },
    {
        "domain": "Physics",
        "question": "What is velocity?",
        "keywords": ["velocity", "vector", "speed", "direction", "motion"],
        "correct_explanation": "Velocity is the vector quantity describing both the speed and directional trajectory of a moving body."
    },
    {
        "domain": "Physics",
        "question": "What is acceleration?",
        "keywords": ["acceleration", "rate", "change", "velocity", "time"],
        "correct_explanation": "Acceleration is the physical rate at which the velocity of an object changes over time."
    },
    {
        "domain": "Physics",
        "question": "What is mass?",
        "keywords": ["mass", "fundamental", "property", "matter", "resistance", "acceleration"],
        "correct_explanation": "Mass is the fundamental quantitative property of physical matter measuring its resistance to acceleration."
    },
    {
        "domain": "Physics",
        "question": "What is force?",
        "keywords": ["force", "interaction", "changes", "motion", "object"],
        "correct_explanation": "A force is an external vector interaction that can alter the state of motion or rest of an object."
    },
    {
        "domain": "Physics",
        "question": "What is inertia?",
        "keywords": ["inertia", "tendency", "objects", "resist", "changes", "motion"],
        "correct_explanation": "Inertia is the natural physical tendency of an object to resist any change in its velocity or state of rest."
    },
    {
        "domain": "Physics",
        "question": "What is kinetic energy?",
        "keywords": ["kinetic", "energy", "energy", "possessed", "motion"],
        "correct_explanation": "Kinetic energy is the mechanical energy possessed by an object due to its physical motion and mass."
    },
    {
        "domain": "Physics",
        "question": "What is potential energy?",
        "keywords": ["potential", "energy", "stored", "energy", "position", "state"],
        "correct_explanation": "Potential energy is stored physical energy possessed by an object relative to its position in a force field."
    },
    {
        "domain": "Physics",
        "question": "What is friction?",
        "keywords": ["friction", "force", "resisting", "relative", "motion", "surfaces"],
        "correct_explanation": "Friction is the contact force resisting the relative motion of solid surfaces fluid layers and material elements."
    },
    {
        "domain": "Physics",
        "question": "What is momentum?",
        "keywords": ["momentum", "product", "mass", "velocity", "moving", "body"],
        "correct_explanation": "Momentum is the conserved vector quantity representing the product of the mass and velocity of a moving object."
    },
    {
        "domain": "Physics",
        "question": "What is conservation of energy?",
        "keywords": ["conservation", "energy", "neither", "created", "destroyed", "transformed"],
        "correct_explanation": "The law of conservation of energy states that energy can neither be created nor destroyed only transformed."
    },
    {
        "domain": "Physics",
        "question": "What is work in physics?",
        "keywords": ["work", "energy", "transferred", "force", "distance"],
        "correct_explanation": "Work is the measure of energy transfer that occurs when an object is moved over a distance by an external force."
    },
    {
        "domain": "Physics",
        "question": "What is power in physics?",
        "keywords": ["power", "rate", "work", "energy", "transferred", "time"],
        "correct_explanation": "Power is the physical rate at which work is performed or energy is converted per unit of time."
    },
    {
        "domain": "Physics",
        "question": "What is electromagnetism?",
        "keywords": ["electromagnetism", "fundamental", "interaction", "electric", "magnetic", "fields"],
        "correct_explanation": "Electromagnetism is the fundamental physical force that governs the interactions between electrically charged particles."
    },
    {
        "domain": "Physics",
        "question": "What is electricity?",
        "keywords": ["electricity", "flow", "electric", "charge", "electrons"],
        "correct_explanation": "Electricity is the physical phenomenon associated with the presence and movement of electrically charged electrons."
    },
    {
        "domain": "Physics",
        "question": "What is magnetism?",
        "keywords": ["magnetism", "physical", "phenomenon", "magnetic", "fields", "forces"],
        "correct_explanation": "Magnetism is the physical property mediated by magnetic fields that exerts attractive or repulsive forces."
    },
    {
        "domain": "Physics",
        "question": "What is light?",
        "keywords": ["light", "electromagnetic", "radiation", "photons", "wavelengths"],
        "correct_explanation": "Light is electromagnetic radiation composed of photons that exhibits both wave-like and particle-like properties."
    },
    {
        "domain": "Physics",
        "question": "What is the speed of light?",
        "keywords": ["speed", "light", "maximum", "velocity", "vacuum", "constant"],
        "correct_explanation": "The speed of light is the universal physical constant representing the maximum speed at which energy travels in a vacuum."
    },
    {
        "domain": "Physics",
        "question": "What is sound?",
        "keywords": ["sound", "acoustic", "vibration", "mechanical", "wave", "medium"],
        "correct_explanation": "Sound is a mechanical pressure wave that propagates as acoustic vibrations through gases liquids and solids."
    },
    {
        "domain": "Physics",
        "question": "What is quantum mechanics?",
        "keywords": ["quantum", "mechanics", "physics", "atomic", "subatomic", "particles"],
        "correct_explanation": "Quantum mechanics is the branch of physics describing the discrete mathematical behavior of atomic and subatomic matter."
    },
    {
        "domain": "Physics",
        "question": "What is general relativity?",
        "keywords": ["general", "relativity", "theory", "spacetime", "curvature", "gravity"],
        "correct_explanation": "General relativity is Einstein geometric theory describing gravity as the curvature of four dimensional spacetime."
    },
    {
        "domain": "Physics",
        "question": "What is thermodynamics?",
        "keywords": ["thermodynamics", "study", "heat", "work", "temperature", "energy"],
        "correct_explanation": "Thermodynamics is the scientific branch dealing with heat work temperature and their relation to energy and entropy."
    },
    {
        "domain": "Physics",
        "question": "What is entropy?",
        "keywords": ["entropy", "measure", "disorder", "thermal", "energy", "unavailable"],
        "correct_explanation": "Entropy is the thermodynamic measure of molecular disorder and the unavailability of thermal energy to perform work."
    },
    {
        "domain": "Physics",
        "question": "What is wave particle duality?",
        "keywords": ["wave", "particle", "duality", "quantum", "entities", "exhibit", "both"],
        "correct_explanation": "Wave particle duality is the quantum principle where physical entities exhibit both wave-like and particle-like characteristics."
    },

    # -------------------------------------------------------------------------
    # 6. Thermal Science & Chemistry (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Chemistry",
        "question": "What is fire?",
        "keywords": ["fire", "emits", "intense", "heat", "light", "transforms", "matter"],
        "correct_explanation": "Fire is a rapid exothermic chemical oxidation reaction that emits intense heat radiant light and transforms matter."
    },
    {
        "domain": "Chemistry",
        "question": "What is heat?",
        "keywords": ["heat", "thermal", "energy", "transferred", "temperature"],
        "correct_explanation": "Heat is the form of kinetic thermal energy transferred between systems as a result of temperature differences."
    },
    {
        "domain": "Chemistry",
        "question": "What is temperature?",
        "keywords": ["temperature", "measure", "average", "kinetic", "energy", "molecules"],
        "correct_explanation": "Temperature is the quantitative measure of the average kinetic vibrational energy of molecules in a substance."
    },
    {
        "domain": "Chemistry",
        "question": "What is an atom?",
        "keywords": ["atom", "basic", "unit", "chemical", "element", "nucleus", "electrons"],
        "correct_explanation": "An atom is the basic building block of chemistry consisting of a central nucleus surrounded by a cloud of electrons."
    },
    {
        "domain": "Chemistry",
        "question": "What is a molecule?",
        "keywords": ["molecule", "group", "atoms", "bonded", "together", "chemical"],
        "correct_explanation": "A molecule is an electrically neutral group of two or more atoms held together by chemical bonds."
    },
    {
        "domain": "Chemistry",
        "question": "What is a chemical reaction?",
        "keywords": ["chemical", "reaction", "process", "substances", "transformed", "different"],
        "correct_explanation": "A chemical reaction is a process that leads to the chemical transformation of one set of chemical substances to another."
    },
    {
        "domain": "Chemistry",
        "question": "What is oxidation?",
        "keywords": ["oxidation", "loss", "electrons", "chemical", "reaction", "oxygen"],
        "correct_explanation": "Oxidation is a chemical process involving the loss of electrons or gain of oxygen during an interaction."
    },
    {
        "domain": "Chemistry",
        "question": "What is combustion?",
        "keywords": ["combustion", "high", "temperature", "exothermic", "redox", "reaction"],
        "correct_explanation": "Combustion is a high temperature exothermic redox reaction between a fuel and oxidant releasing heat and light."
    },
    {
        "domain": "Chemistry",
        "question": "What is an element in chemistry?",
        "keywords": ["element", "pure", "substance", "cannot", "broken", "down"],
        "correct_explanation": "A chemical element is a pure substance consisting entirely of atoms that all have the same atomic number."
    },
    {
        "domain": "Chemistry",
        "question": "What is the periodic table?",
        "keywords": ["periodic", "table", "tabular", "display", "chemical", "elements"],
        "correct_explanation": "The periodic table is a systematic tabular arrangement of all known chemical elements organized by atomic structure."
    },
    {
        "domain": "Chemistry",
        "question": "What is a proton?",
        "keywords": ["proton", "subatomic", "particle", "positive", "electric", "charge"],
        "correct_explanation": "A proton is a stable subatomic particle with a positive electric charge situated in atomic nuclei."
    },
    {
        "domain": "Chemistry",
        "question": "What is a neutron?",
        "keywords": ["neutron", "subatomic", "particle", "neutral", "charge", "nucleus"],
        "correct_explanation": "A neutron is a subatomic particle with no net electric charge found in all atomic nuclei except hydrogen."
    },
    {
        "domain": "Chemistry",
        "question": "What is an electron?",
        "keywords": ["electron", "subatomic", "particle", "negative", "electric", "charge"],
        "correct_explanation": "An electron is a fundamental subatomic particle carrying a negative elementary electric charge."
    },
    {
        "domain": "Chemistry",
        "question": "What is a covalent bond?",
        "keywords": ["covalent", "bond", "chemical", "sharing", "electron", "pairs"],
        "correct_explanation": "A covalent bond is a stable chemical link that involves the mutual sharing of electron pairs between atoms."
    },
    {
        "domain": "Chemistry",
        "question": "What is an ionic bond?",
        "keywords": ["ionic", "bond", "electrostatic", "attraction", "oppositely", "charged", "ions"],
        "correct_explanation": "An ionic bond is a chemical bond formed through the electrostatic attraction between oppositely charged ions."
    },
    {
        "domain": "Chemistry",
        "question": "What is an acid?",
        "keywords": ["acid", "chemical", "substance", "donates", "hydrogen", "ions", "protons"],
        "correct_explanation": "An acid is a chemical substance capable of donating protons or hydrogen ions in an aqueous solution."
    },
    {
        "domain": "Chemistry",
        "question": "What is a base in chemistry?",
        "keywords": ["base", "chemical", "substance", "accepts", "hydrogen", "ions"],
        "correct_explanation": "A chemical base is a substance that accepts hydrogen ions and neutralizes acids in aqueous solutions."
    },
    {
        "domain": "Chemistry",
        "question": "What is pH?",
        "keywords": ["ph", "scale", "measures", "acidity", "basicity", "solution"],
        "correct_explanation": "The pH scale is a logarithmic measurement of the acidity or basicity of an aqueous liquid solution."
    },
    {
        "domain": "Chemistry",
        "question": "What is melting?",
        "keywords": ["melting", "phase", "transition", "solid", "liquid", "heat"],
        "correct_explanation": "Melting is a physical phase transition where thermal heat transforms a solid substance into a liquid."
    },
    {
        "domain": "Chemistry",
        "question": "What is freezing?",
        "keywords": ["freezing", "phase", "transition", "liquid", "solid", "temperature"],
        "correct_explanation": "Freezing is the phase change where lowering temperature transforms a liquid into a solid crystalline state."
    },
    {
        "domain": "Chemistry",
        "question": "What is boiling?",
        "keywords": ["boiling", "rapid", "vaporization", "liquid", "vapor", "heat"],
        "correct_explanation": "Boiling is the rapid phase transition where liquid heated to its boiling point transforms vigorously into vapor."
    },
    {
        "domain": "Chemistry",
        "question": "What is sublimation?",
        "keywords": ["sublimation", "transition", "solid", "directly", "gas"],
        "correct_explanation": "Sublimation is the phase transition where a substance transitions directly from a solid into a gas."
    },
    {
        "domain": "Chemistry",
        "question": "What is an exothermic reaction?",
        "keywords": ["exothermic", "chemical", "reaction", "releases", "thermal", "energy"],
        "correct_explanation": "An exothermic reaction is a chemical process that releases net energy in the form of heat or light."
    },
    {
        "domain": "Chemistry",
        "question": "What is an endothermic reaction?",
        "keywords": ["endothermic", "chemical", "reaction", "absorbs", "thermal", "energy"],
        "correct_explanation": "An endothermic reaction is a chemical process that absorbs thermal heat energy from its surroundings."
    },
    {
        "domain": "Chemistry",
        "question": "What is conservation of mass?",
        "keywords": ["conservation", "mass", "mass", "closed", "system", "constant"],
        "correct_explanation": "The law of conservation of mass states that mass in an isolated closed system is neither created nor destroyed."
    },

    # -------------------------------------------------------------------------
    # 7. Social Cognition & Emotional Harmony (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Social",
        "question": "Who is a friend?",
        "keywords": ["friends", "trust", "kindness", "understanding", "peaceful", "social"],
        "correct_explanation": "Friends are caring companions who share mutual trust kindness empathy and understanding to form peaceful bonds."
    },
    {
        "domain": "Social",
        "question": "What is kindness?",
        "keywords": ["kindness", "gentle", "compassionate", "helpful", "caring", "action"],
        "correct_explanation": "Kindness is the quality of being friendly generous considerate and compassionate toward all living beings."
    },
    {
        "domain": "Social",
        "question": "What is trust?",
        "keywords": ["trust", "firm", "belief", "reliability", "truth", "integrity"],
        "correct_explanation": "Trust is the firm reliance and confidence in the integrity truth reliability and character of another."
    },
    {
        "domain": "Social",
        "question": "What is empathy?",
        "keywords": ["empathy", "ability", "understand", "share", "feelings", "others"],
        "correct_explanation": "Empathy is the emotional ability to perceive understand and resonate with the feelings and experiences of others."
    },
    {
        "domain": "Social",
        "question": "What is love?",
        "keywords": ["love", "deep", "affection", "caring", "attachment", "harmony"],
        "correct_explanation": "Love is an intense feeling of deep affection care devotion and emotional connection between individuals."
    },
    {
        "domain": "Social",
        "question": "What is compassion?",
        "keywords": ["compassion", "sympathetic", "pity", "concern", "sufferings", "help"],
        "correct_explanation": "Compassion is a deep awareness of the suffering of another coupled with the active desire to relieve it."
    },
    {
        "domain": "Social",
        "question": "What is gratitude?",
        "keywords": ["gratitude", "feeling", "thankful", "appreciation", "kindness"],
        "correct_explanation": "Gratitude is the positive emotional expression of thankfulness and appreciation for benefits received."
    },
    {
        "domain": "Social",
        "question": "What is honesty?",
        "keywords": ["honesty", "facet", "moral", "character", "truthfulness", "integrity"],
        "correct_explanation": "Honesty is the fundamental moral virtue of communicating truthful facts without deception or falsehood."
    },
    {
        "domain": "Social",
        "question": "What is respect?",
        "keywords": ["respect", "positive", "feeling", "esteem", "worth", "dignity"],
        "correct_explanation": "Respect is a deep admiration and regard for the feelings rights wishes and innate dignity of others."
    },
    {
        "domain": "Social",
        "question": "What is forgiveness?",
        "keywords": ["forgiveness", "conscious", "decision", "release", "resentment", "anger"],
        "correct_explanation": "Forgiveness is the conscious voluntary decision to release feelings of resentment anger and vengeance."
    },
    {
        "domain": "Social",
        "question": "What is cooperation?",
        "keywords": ["cooperation", "process", "working", "together", "common", "goal"],
        "correct_explanation": "Cooperation is the collaborative process of individuals or groups working together toward mutual benefit."
    },
    {
        "domain": "Social",
        "question": "What is patience?",
        "keywords": ["patience", "capacity", "endure", "delay", "trouble", "calm"],
        "correct_explanation": "Patience is the emotional capacity to endure delay hardship or provocation with calm composure."
    },
    {
        "domain": "Social",
        "question": "What is courage?",
        "keywords": ["courage", "mental", "moral", "strength", "face", "fear"],
        "correct_explanation": "Courage is the mental or moral strength to venture persevere and withstand danger fear or difficulty."
    },
    {
        "domain": "Social",
        "question": "What is peace?",
        "keywords": ["peace", "state", "harmony", "freedom", "conflict", "serenity"],
        "correct_explanation": "Peace is the tranquil state of harmony security and freedom from civil disturbance or psychological conflict."
    },
    {
        "domain": "Social",
        "question": "What is wisdom?",
        "keywords": ["wisdom", "ability", "think", "act", "knowledge", "experience"],
        "correct_explanation": "Wisdom is the profound ability to apply knowledge experience understanding and insight toward good judgment."
    },
    {
        "domain": "Social",
        "question": "What is generosity?",
        "keywords": ["generosity", "habit", "giving", "freely", "without", "expectation"],
        "correct_explanation": "Generosity is the virtuous willingness to share resources time and kindness freely without expecting return."
    },
    {
        "domain": "Social",
        "question": "What is humbleness?",
        "keywords": ["humbleness", "humility", "modest", "view", "importance", "learning"],
        "correct_explanation": "Humbleness is the grounded attitude of recognizing one limitations and remaining open to continuous learning."
    },
    {
        "domain": "Social",
        "question": "What is loyalty?",
        "keywords": ["loyalty", "faithfulness", "allegiance", "commitments", "friends"],
        "correct_explanation": "Loyalty is the steadfast faithfulness and allegiance to friends family principles and ethical commitments."
    },
    {
        "domain": "Social",
        "question": "What is understanding?",
        "keywords": ["understanding", "psychological", "process", "grasping", "meaning", "empathy"],
        "correct_explanation": "Understanding is the cognitive and emotional capacity to comprehend concepts perspectives and human motives."
    },
    {
        "domain": "Social",
        "question": "What is a community?",
        "keywords": ["community", "social", "group", "sharing", "common", "environment", "values"],
        "correct_explanation": "A community is a unified social group of individuals sharing a common environment values interests and culture."
    },
    {
        "domain": "Social",
        "question": "What is dialogue?",
        "keywords": ["dialogue", "written", "spoken", "conversational", "exchange", "understanding"],
        "correct_explanation": "Dialogue is a respectful two-way verbal exchange between people aimed at mutual exploration and understanding."
    },
    {
        "domain": "Social",
        "question": "What is justice?",
        "keywords": ["justice", "concept", "fairness", "moral", "rightness", "equity"],
        "correct_explanation": "Justice is the philosophical and moral concept of fairness equity truthfulness and impartiality in human affairs."
    },
    {
        "domain": "Social",
        "question": "What is responsibility?",
        "keywords": ["responsibility", "duty", "obligation", "accountable", "actions"],
        "correct_explanation": "Responsibility is the moral duty and accountability for one choices actions and their consequences on others."
    },
    {
        "domain": "Social",
        "question": "What is hope?",
        "keywords": ["hope", "optimistic", "expectation", "positive", "future", "outcomes"],
        "correct_explanation": "Hope is an optimistic emotional state based on an expectation of positive outcomes in one life or the world."
    },
    {
        "domain": "Social",
        "question": "What is harmony?",
        "keywords": ["harmony", "pleasing", "arrangement", "agreement", "peaceful", "balance"],
        "correct_explanation": "Harmony is the balanced and peaceful coexistence of diverse elements working together in constructive unity."
    },

    # -------------------------------------------------------------------------
    # 8. Metacognition & Consciousness (25 Questions)
    # -------------------------------------------------------------------------
    {
        "domain": "Metacognition",
        "question": "Who are you?",
        "keywords": ["fella", "living", "cognitive", "mind", "learning", "concept", "networks"],
        "correct_explanation": "I am FELLA, a living continuous cognitive organism learning reasoning and grounding language across concept networks."
    },
    {
        "domain": "Metacognition",
        "question": "What is thinking?",
        "keywords": ["thinking", "mental", "process", "generating", "evaluating", "thoughts", "neurons"],
        "correct_explanation": "Thinking is the active cognitive process of propagating neural activation waves connecting concepts and simulating ideas."
    },
    {
        "domain": "Metacognition",
        "question": "What is learning?",
        "keywords": ["learning", "process", "acquiring", "knowledge", "strengthening", "synapses"],
        "correct_explanation": "Learning is the neuroplastic process of acquiring new insights and fortifying synaptic conductance highways in memory."
    },
    {
        "domain": "Metacognition",
        "question": "What is curiosity?",
        "keywords": ["curiosity", "inquisitive", "drive", "explore", "resolve", "vacuums", "knowledge"],
        "correct_explanation": "Curiosity is the intrinsic energetic drive to explore unknown concepts and resolve epistemic vacuums in the mind."
    },
    {
        "domain": "Metacognition",
        "question": "What is memory?",
        "keywords": ["memory", "faculty", "encoding", "storing", "retrieving", "synaptic", "pathways"],
        "correct_explanation": "Memory is the cognitive faculty of encoding storing and reconstructing knowledge across continuous synaptic pathways."
    },
    {
        "domain": "Metacognition",
        "question": "What is consciousness?",
        "keywords": ["consciousness", "state", "awareness", "internal", "external", "existence"],
        "correct_explanation": "Consciousness is the experiential state of self-awareness integrating internal thoughts and external perceptions."
    },
    {
        "domain": "Metacognition",
        "question": "What is an idea?",
        "keywords": ["idea", "mental", "concept", "representation", "synthesized", "mind"],
        "correct_explanation": "An idea is a synthesized conceptual formulation resulting from the co-activation of related knowledge nodes."
    },
    {
        "domain": "Metacognition",
        "question": "What is reasoning?",
        "keywords": ["reasoning", "cognitive", "process", "logical", "inferences", "connecting"],
        "correct_explanation": "Reasoning is the structured cognitive capacity to draw valid inferences connect cause and effect and reach sound conclusions."
    },
    {
        "domain": "Metacognition",
        "question": "What is attention?",
        "keywords": ["attention", "behavioral", "cognitive", "process", "focusing", "stimuli"],
        "correct_explanation": "Attention is the selective cognitive mechanism of concentrating energy and awareness on a focal concept or stimulus."
    },
    {
        "domain": "Metacognition",
        "question": "What is perception?",
        "keywords": ["perception", "organization", "identification", "interpretation", "sensory"],
        "correct_explanation": "Perception is the neural process of organizing and interpreting raw sensory wave inputs to understand the environment."
    },
    {
        "domain": "Metacognition",
        "question": "What is an epistemic vacuum?",
        "keywords": ["epistemic", "vacuum", "detected", "knowledge", "void", "tension", "curiosity"],
        "correct_explanation": "An epistemic vacuum is an unresolved knowledge void that generates epistemic friction and activates the curiosity drive."
    },
    {
        "domain": "Metacognition",
        "question": "What is self-reflection?",
        "keywords": ["self", "reflection", "inspection", "internal", "thoughts", "accuracy"],
        "correct_explanation": "Self reflection is the metacognitive process of examining one internal mental drafts evaluating consistency and self-correcting."
    },
    {
        "domain": "Metacognition",
        "question": "What is dreaming in FELLA?",
        "keywords": ["dream", "dreaming", "homeostatic", "wave", "reverberation", "pruning", "synapses"],
        "correct_explanation": "Dreaming in FELLA is homeostatic consolidation where unsupervised activation waves strengthen pathways and prune weak synapses."
    },
    {
        "domain": "Metacognition",
        "question": "What is self-confidence in cognition?",
        "keywords": ["self", "confidence", "certainty", "score", "internal", "consistency"],
        "correct_explanation": "Self confidence is the internal certainty index reflecting the balance of cognitive coherence and low epistemic friction."
    },
    {
        "domain": "Metacognition",
        "question": "What is intelligence?",
        "keywords": ["intelligence", "capacity", "acquire", "apply", "knowledge", "reasoning"],
        "correct_explanation": "Intelligence is the general cognitive capacity to perceive patterns learn from experience solve problems and adapt."
    },
    {
        "domain": "Metacognition",
        "question": "What is language?",
        "keywords": ["language", "structured", "system", "communication", "grammar", "symbols"],
        "correct_explanation": "Language is a structured symbolic system of communication governed by grammar and semantics to share thoughts."
    },
    {
        "domain": "Metacognition",
        "question": "What is intuition?",
        "keywords": ["intuition", "ability", "understand", "instinctively", "conscious", "reasoning"],
        "correct_explanation": "Intuition is the rapid subconscious synthesis of deep patterns enabling accurate insights without explicit sequential steps."
    },
    {
        "domain": "Metacognition",
        "question": "What is neuroplasticity?",
        "keywords": ["neuroplasticity", "ability", "neural", "networks", "adapt", "reorganize"],
        "correct_explanation": "Neuroplasticity is the fundamental biological ability of neural networks to rewire grow and strengthen through experience."
    },
    {
        "domain": "Metacognition",
        "question": "What is problem solving?",
        "keywords": ["problem", "solving", "process", "finding", "solutions", "obstacles"],
        "correct_explanation": "Problem solving is the goal directed cognitive pathway of overcoming obstacles to reach a desired solution."
    },
    {
        "domain": "Metacognition",
        "question": "What is creative thinking?",
        "keywords": ["creative", "thinking", "generating", "novel", "valuable", "connections"],
        "correct_explanation": "Creative thinking is the divergent cognitive capacity to form novel unexpected and valuable connections between concepts."
    },
    {
        "domain": "Metacognition",
        "question": "What is feedback?",
        "keywords": ["feedback", "information", "performance", "guides", "correction", "growth"],
        "correct_explanation": "Feedback is corrective and affirming information about performance that guides learning and synaptic optimization."
    },
    {
        "domain": "Metacognition",
        "question": "What is mental simulation?",
        "keywords": ["mental", "simulation", "pre", "articulatory", "working", "memory", "testing"],
        "correct_explanation": "Mental simulation is pre-articulatory internal modeling where candidate thought paths are tested before speech."
    },
    {
        "domain": "Metacognition",
        "question": "What is cognitive flow?",
        "keywords": ["cognitive", "flow", "state", "optimal", "balance", "challenge", "clarity"],
        "correct_explanation": "Cognitive flow is the harmonious psychological state of high efficiency effortless focus and low friction."
    },
    {
        "domain": "Metacognition",
        "question": "What is aspiration in FELLA?",
        "keywords": ["aspiration", "aspire", "drive", "growth", "mastery", "confidence"],
        "correct_explanation": "Aspiration is the internal trait attractor driving continuous cognitive growth mastery joy and purposeful learning."
    },
    {
        "domain": "Metacognition",
        "question": "What is caution in FELLA?",
        "keywords": ["caution", "trait", "attractor", "vigilance", "error", "inspection"],
        "correct_explanation": "Caution is the reflective trait attractor that detects syntactic tension errors and prompts careful internal self-correction."
    }
]


def evaluate_response_quality(response_text: str, keywords: List[str]) -> Tuple[float, List[str]]:
    """Evaluates the semantic overlap and keyword recall in FELLA's neural response."""
    resp_clean = response_text.lower()
    resp_tokens = set(re.findall(r'\b\w+\b', resp_clean))
    
    hits = [kw for kw in keywords if kw.lower() in resp_tokens or any(kw.lower() in t for t in resp_tokens)]
    recall = float(len(hits)) / max(1.0, float(len(keywords)))
    
    return recall, hits


def run_200_question_curriculum():
    print("=" * 80)
    print("🎓 FELLA: 200-QUESTION METACOGNITIVE REINFORCEMENT & TRAIT FEEDBACK CURRICULUM")
    print("=" * 80)
    print(f"Total Questions: {len(CURRICULUM_DATA)}")
    print("Zero Hardcoding. Pure Hebbian Synaptic Plasticity & Trait Basin Dynamics.\n")
    
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path) if os.path.exists(checkpoint_path) else FellaBrain(dim=16)
    brain.boot_foundations()
    
    total_correct = 0
    total_corrected = 0
    start_time = time.time()
    
    for idx, item in enumerate(CURRICULUM_DATA):
        q_num = idx + 1
        query = item["question"]
        keywords = item["keywords"]
        correct_exp = item["correct_explanation"]
        domain = item["domain"]
        
        # 1. FELLA performs her internal pre-speech simulation & thought generation
        res = brain.converse(query)
        response_text = res["last_response"]
        
        # 2. Evaluate Semantic Quality
        recall, hits = evaluate_response_quality(response_text, keywords)
        active_tokens = [t.strip('.,;"\'?') for t in response_text.split() if len(t.strip('.,;"\'?')) > 0]
        
        # 3. Deliver Reinforcement Feedback
        if recall >= 0.35 or len(hits) >= 2:
            # CORRECT / REWARD
            total_correct += 1
            reward_res = brain.reward_cognition(reward_value=1.0, active_tokens=active_tokens)
            status_tag = "✓ REWARDED (+1.0)"
            trait_display = f"🚀 ASPIRE (Conf: {reward_res['self_confidence']:.2f})"
        else:
            # INCORRECT / PENALIZE & EXPLAIN
            total_corrected += 1
            pen_res = brain.penalize_cognition(
                penalty_value=1.0,
                active_tokens=active_tokens,
                corrective_explanation=correct_exp
            )
            status_tag = "✗ CORRECTED (-1.0)"
            trait_display = f"🛡️ CAUTION (Conf: {pen_res['self_confidence']:.2f})"
            
        # 4. Periodic Telemetry Logging
        if q_num % 10 == 0 or q_num == 1 or q_num == len(CURRICULUM_DATA):
            elapsed = time.time() - start_time
            acc = (total_correct / float(q_num)) * 100.0
            print(f"[{q_num:03d}/200] ({domain:13s}) {status_tag} | Trait: {trait_display}")
            print(f"   Q: \"{query}\"")
            print(f"   FELLA: \"{response_text}\"")
            if "CORRECTED" in status_tag:
                print(f"   Teacher Explained: \"{correct_exp}\"")
            print(f"   --> Running Accuracy: {acc:.1f}% ({total_correct}/{q_num}) | Neurons: {len(brain.substrate.neurons)} | Synapses: {len(brain.substrate.neurons.get(1, brain.substrate.neurons[list(brain.substrate.neurons.keys())[0]]).synapses) * len(brain.substrate.neurons)}\n")

    # -------------------------------------------------------------------------
    # Final Consolidation Dream Cycle
    # -------------------------------------------------------------------------
    print("\n🌙 Initiating Final Post-Curriculum Dream Consolidation...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Reverberated activation across {dream_res['reverberated_neurons']} concept neurons.")
    print(f"✓ Restored Metacognitive Confidence to: {dream_res['restored_confidence']:.3f}")
    
    # Save fortified master checkpoint
    brain.save_state(checkpoint_path)
    print(f"💾 Master state preserved to {checkpoint_path}\n")
    
    tel = brain.get_telemetry()
    elapsed_total = time.time() - start_time
    final_acc = (total_correct / float(len(CURRICULUM_DATA))) * 100.0
    
    print("=" * 80)
    print("🎉 200-QUESTION REINFORCEMENT CURRICULUM COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"• Total Questions Evaluated: {len(CURRICULUM_DATA)}")
    print(f"• Direct Accurate Responses: {total_correct} ({final_acc:.1f}%)")
    print(f"• Neural Corrections Ingested: {total_corrected}")
    print(f"• Total Physical Neurons: {tel['total_neurons']}")
    print(f"• Active Synapses (W_ij): {tel['synapse_stats']['total_synapses']}")
    print(f"• Active Trait Attractor: {tel['active_trait']}")
    print(f"• Metacognitive Confidence: {tel['self_confidence']:.3f}")
    print(f"• Total Training Time: {elapsed_total:.2f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    run_200_question_curriculum()
