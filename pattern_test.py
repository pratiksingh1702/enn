"""
ENN 4D: Advanced Cognitive Topology & Morphogenesis Test
Simulates semantic concept trees, associative bridges, temporal wave cycles,
and evolutionary cluster reorganization.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
import time
from enn4d import ENN4D

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def run_advanced_pattern_test():
    print("=" * 75)
    print("ENN 4D: ADVANCED COGNITIVE TOPOLOGY EXPERIMENT")
    print("=" * 75)
    print("Simulating structured conceptual manifolds, category clustering,")
    print("associative synaptic bridges, and harmonic wave fields.\n")
    
    system = ENN4D(dim=4)
    
    # -------------------------------------------------------------
    # 1. DEFINE STRUCTURED DOMAINS (Semantic Taxonomies)
    # -------------------------------------------------------------
    # Domain A: "Organic / Flora" (Shared base [0.7, 0.7, 0, 0] + variations)
    flora_base = np.array([0.7, 0.7, 0.0, 0.0])
    pattern_flora_1 = normalize(flora_base + np.array([0.1, -0.1, 0.05, 0.0])) # "Rose"
    pattern_flora_2 = normalize(flora_base + np.array([-0.1, 0.1, -0.05, 0.0])) # "Oak"
    pattern_flora_3 = normalize(flora_base + np.array([0.05, 0.05, 0.1, 0.0])) # "Lotus"

    # Domain B: "Fauna / Animals" (Shared base [0, 0.7, 0.7, 0] + variations)
    fauna_base = np.array([0.0, 0.7, 0.7, 0.0])
    pattern_fauna_1 = normalize(fauna_base + np.array([0.0, 0.1, -0.1, 0.05])) # "Hawk"
    pattern_fauna_2 = normalize(fauna_base + np.array([0.0, -0.1, 0.1, -0.05])) # "Wolf"
    pattern_fauna_3 = normalize(fauna_base + np.array([0.0, 0.05, 0.05, 0.1])) # "Dolphin"

    # Domain C: "Celestial / Energy" (Shared base [0, 0, 0.7, 0.7] + variations)
    celestial_base = np.array([0.0, 0.0, 0.7, 0.7])
    pattern_celestial_1 = normalize(celestial_base + np.array([0.05, 0.0, 0.1, -0.1])) # "Solar"
    pattern_celestial_2 = normalize(celestial_base + np.array([-0.05, 0.0, -0.1, 0.1])) # "Lunar"
    pattern_celestial_3 = normalize(celestial_base + np.array([0.0, 0.05, 0.05, 0.05])) # "Nebula"

    # Domain D: "Cybernetic / Synthetic" (Shared base [0.7, 0, 0, 0.7] + variations)
    cyber_base = np.array([0.7, 0.0, 0.0, 0.7])
    pattern_cyber_1 = normalize(cyber_base + np.array([0.1, 0.05, 0.0, -0.1])) # "Quantum"
    pattern_cyber_2 = normalize(cyber_base + np.array([-0.1, -0.05, 0.0, 0.1])) # "Matrix"

    # -------------------------------------------------------------
    # PHASE 1: Category Genesis & Branching
    # -------------------------------------------------------------
    print("[Phase 1] Category Genesis & Internal Clustering (Flora & Fauna)")
    for i in range(25):
        system.step(pattern_flora_1, pattern_flora_1, np.array([0.1]))
        system.step(pattern_flora_2, pattern_flora_2, np.array([0.1]))
        system.step(pattern_flora_3, pattern_flora_3, np.array([0.1]))
    print(f"   Flora Domain planted -> {len(system.neurons)} neurons, {len(set(n.w for n in system.neurons))} families")

    for i in range(25):
        system.step(pattern_fauna_1, pattern_fauna_1, np.array([0.2]))
        system.step(pattern_fauna_2, pattern_fauna_2, np.array([0.2]))
        system.step(pattern_fauna_3, pattern_fauna_3, np.array([0.2]))
    print(f"   Fauna Domain planted -> {len(system.neurons)} neurons, {len(set(n.w for n in system.neurons))} families")

    # -------------------------------------------------------------
    # PHASE 2: Expanding the Ontology (Celestial & Cybernetic)
    # -------------------------------------------------------------
    print("\n[Phase 2] Expanding Dimensions (Celestial & Cybernetic Constellations)")
    for i in range(25):
        system.step(pattern_celestial_1, pattern_celestial_1, np.array([0.3]))
        system.step(pattern_celestial_2, pattern_celestial_2, np.array([0.3]))
        system.step(pattern_celestial_3, pattern_celestial_3, np.array([0.3]))
    print(f"   Celestial Domain added -> {len(system.neurons)} neurons, {len(set(n.w for n in system.neurons))} families")

    for i in range(25):
        system.step(pattern_cyber_1, pattern_cyber_1, np.array([0.4]))
        system.step(pattern_cyber_2, pattern_cyber_2, np.array([0.4]))
    print(f"   Cybernetic Domain added -> {len(system.neurons)} neurons, {len(set(n.w for n in system.neurons))} families")

    # -------------------------------------------------------------
    # PHASE 3: Cross-Category Associative Bridges (Hebbian Synapses)
    # -------------------------------------------------------------
    print("\n[Phase 3] Synaptic Bridge Formation (Cross-Domain Resonance)")
    print("   Firing correlated concepts (Flora <-> Celestial) & (Fauna <-> Cybernetic)...")
    for i in range(30):
        # Bi-modal resonance
        blend_1 = normalize(0.6 * pattern_flora_1 + 0.4 * pattern_celestial_1)
        blend_2 = normalize(0.6 * pattern_fauna_1 + 0.4 * pattern_cyber_1)
        system.step(blend_1, blend_1, np.array([0.5]))
        system.step(blend_2, blend_2, np.array([0.5]))

    total_conns = sum(len(n.connections) for n in system.neurons)
    print(f"   Synaptic Highway constructed: {total_conns} total synaptic links established!")

    # -------------------------------------------------------------
    # PHASE 4: Harmonic Oscillation (Orbital Wave Field)
    # -------------------------------------------------------------
    print("\n[Phase 4] Harmonic Wavefield Cycle (Continuous Manifold Traversal)")
    print("   Feeding 4D continuous rotational wave trajectory...")
    for t in np.linspace(0, 2 * np.pi, 40):
        # Continuous 4D torus orbit
        wave = normalize(np.array([np.sin(t), np.cos(t), np.sin(2*t), np.cos(2*t)]))
        z_time = np.array([float(np.sin(t) * 0.5 + 0.5)])
        system.step(wave, wave, z_time)

    # -------------------------------------------------------------
    # PHASE 5: Consolidation & Homeostasis
    # -------------------------------------------------------------
    print("\n[Phase 5] Metabolic Consolidation (Pruning weak noise & stabilizing core)")
    for i in range(50):
        zero = np.zeros(4)
        system.step(zero, zero, np.array([0.0]))

    # -------------------------------------------------------------
    # SUMMARY & SNAPSHOT
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print("FINAL SYSTEM STATE")
    print("=" * 75)
    system.display()
    
    total_energy = sum(n.energy for n in system.neurons)
    num_families = len(set(n.w for n in system.neurons))
    total_synapses = sum(len(n.connections) for n in system.neurons) // 2
    
    print("\nEmergent Topology Metrics:")
    print(f"   * Active Living Neurons:   {len(system.neurons)}")
    print(f"   * Discovered Taxonomies:   {num_families} distinct species/families")
    print(f"   * Synaptic Bridges:        {total_synapses} functional neural links")
    print(f"   * Total Living Energy:     {total_energy:.2f} units")
    print(f"   * Total Events Processed:  {system.event_count}")
    
    # Save the rich universe state to universe.json
    system.save("universe.json")
    print("\nEvolved universe state saved to 'universe.json'.")
    print("Open 'viewer.html' to explore the new neural constellation in 3D/4D!")

if __name__ == "__main__":
    run_advanced_pattern_test()
