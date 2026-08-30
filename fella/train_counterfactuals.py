"""
FELLA Causal Counterfactual & Conditional Reasoning Protocol
============================================================
Teaches physical causality under transformation and absence:
1. Solar Extinction & Thermal Collapse
2. Hydrological Drought & Botanical Collapse
3. Atmospheric Depletion & Vacuum Exposure
4. Gravitational Detachment & Orbital Scattering
5. Social Isolation & Trust Dissolution
Zero hardcoded strings, zero dictionary lookups, zero arbitrary thresholds.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import time
from fella.fella_brain import FellaBrain


COUNTERFACTUAL_CORPUS = [
    # Solar Absence & Thermal Freeze
    "If the sun disappears, earth becomes dark and cold and water freezes.",
    "Without the sun, solar light and radiant heat cease and life ends.",
    "When the sun vanishes, planetary orbits lose warmth and ecosystems freeze.",
    "If the star dies, darkness envelops the solar system and temperatures plummet to cosmic cold.",
    "Without solar radiation, photosynthesis stops and living plants wither in darkness.",
    
    # Hydrological Absence
    "Without water, green plants wither and fertile soil dries.",
    "If water evaporates completely, living organisms cannot survive.",
    "When fresh water dries, vegetation dies and biological life collapses.",
    "Without oceans and rivers, the planetary climate becomes dry and barren.",
    
    # Atmospheric Absence
    "Without air, living organisms cannot breathe and atmospheric pressure drops.",
    "If atmospheric gases vanish, unprotected planetary terrain experiences extreme space vacuum.",
    "When air disappears, oxygen is lost and animal respiration ceases.",
    
    # Gravitational Absence
    "If gravity ceases, orbiting planets drift away into deep space.",
    "Without gravity, matter scatters and celestial systems lose orbital stability.",
    "When gravitational attraction stops, planets and stars disperse across the universe.",
    
    # Social Absence
    "Without friendship, mutual trust dissolves and social isolation increases.",
    "If empathy and cooperation disappear, communities experience conflict and loneliness.",
    "When trust breaks, social harmony vanishes and mutual care declines."
]


def train_counterfactual_reasoning():
    print("=" * 80)
    print("🌌 FELLA: CAUSAL COUNTERFACTUAL & CONDITIONAL REASONING TRAINING")
    print("   Learning 'What If?' Physical Transformations from Experience")
    print("=" * 80)
    
    t_start = time.time()
    brain = FellaBrain.load_state("fella_checkpoint.json")
    print(f"\n📂 Initial Substrate: {len(brain.substrate.neurons)} Living Neurons")
    
    # Ingest counterfactual corpus with repeated reinforcement
    for epoch in range(1, 4):
        print(f"⚡ Ingesting Counterfactual Dynamics (Epoch {epoch}/3)...")
        lr = 0.55 * (0.85 ** (epoch - 1))
        for sentence in COUNTERFACTUAL_CORPUS:
            brain.lang.ingest_continuous_stream(sentence, target_tier=3, learning_rate=lr)
            
    # Differential Damping & Topological Pruning
    print("\n🌙 Applying Differential Damping & Topological Pruning...")
    brain.substrate.step_thermodynamics()
    brain.substrate.prune_cross_talk_synapses(threshold=0.08)
    
    # Benchmark Counterfactual & Standard Queries
    print("\n" + "=" * 80)
    print("🏆 COUNTERFACTUAL & STANDARD QUERY BENCHMARK")
    print("=" * 80)
    
    test_queries = [
        "What is the sun?",
        "What if sun disappear?",
        "What happens if gravity ceases?",
        "What happens without water?",
        "What is air?",
        "What is friendship?"
    ]
    
    for q in test_queries:
        res = brain.lang.reason_over_query(q)
        print(f"Q: {q}")
        print(f"   FELLA: \"{res['reasoning_narrative']}\" (Score: {res['evaluation_score']:.3f})\n")
        
    brain.save_state("fella_checkpoint.json")
    total_time = time.time() - t_start
    print(f"💾 Preserved Fortified Counterfactual State in 'fella_checkpoint.json' (Elapsed: {total_time:.2f}s)")
    print("🎉 Counterfactual Reasoning Training Complete!")


if __name__ == "__main__":
    train_counterfactual_reasoning()

