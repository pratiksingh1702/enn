import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain

brain = FellaBrain(dim=16)
brain.boot_foundations()

lessons = [
    "The moon orbits the planet earth across space",
    "Stars glow across the cosmos forming constellations in the night sky",
    "Volcanoes erupt molten liquid lava from deep within the earth",
    "Plants grow by absorbing sunlight and water through photosynthesis to produce oxygen",
    "Gravity is the fundamental force that attracts physical matter toward the center of the earth",
    "The sun radiates bright light and emits thermal energy that warms the earth",
    "Fire emits intense heat and bright light as thermal energy transforms matter",
    "Water is a liquid that flows across the earth and evaporates into clouds to produce rain",
    "Black holes possess extreme gravitational curvature that traps light",
    "Speed is the rate of change of position and direction over time",
    "Friends share trust kindness and understanding to create peaceful social bonds",
    "I am FELLA a living cognitive mind learning and reasoning across concept networks"
]

print("=== GROUNDING SEQUENTIAL KNOWLEDGE HIGHWAYS INTO NEURAL SUBSTRATE ===")
for lesson in lessons:
    nodes = brain.lang.ingest_continuous_stream(lesson, target_tier=3, learning_rate=0.40)
    print(f"✓ Ingested ({len(nodes)} nodes): {lesson}")

brain.save_state("fella_checkpoint.json")
print("\n💾 Saved clean neural state to fella_checkpoint.json")
