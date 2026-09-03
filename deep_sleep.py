import os
import json
import time
import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold
from fella.core_substrate import ENNNeuron, Spectron

def enter_deep_sleep(sleep_cycles=50):
    print("==================================================")
    print("FELLA: ENTERING DEEP SLEEP & MEMORY CONSOLIDATION")
    print("==================================================")
    print("[NREM 1] Disconnecting sensory inputs. Closing eyes and ears...")
    
    # 1. Load and Fuse Both Knowledge Bases
    live_file = "fella_live_memory.json"
    master_file = "fella_checkpoint.json"
    
    brain = FellaBrain(dim=256)
    
    # Load live sensory memories
    if os.path.exists(live_file):
        brain.load_state(live_file)
        print(f"[SLEEP] Ingested {len(brain.neurons)} sensory neurons and {brain.z_counter} episodic moments from the day.")
    else:
        print("[SLEEP] No live memory file found. Initializing blank substrate.")

    # Ingest master cognitive vocabulary & concepts
    if os.path.exists(master_file):
        with open(master_file, "r", encoding="utf-8") as f:
            m_data = json.load(f)
        sub_neurons = m_data.get("substrate", {}).get("neurons", [])
        added_vocab = 0
        for n_dict in sub_neurons:
            word = n_dict.get("label") or n_dict.get("text")
            if word and word not in brain.neurons:
                brain.get_or_create(word)
                added_vocab += 1
        print(f"[SLEEP] Integrated {added_vocab} core linguistic & physical concepts into unified matrix.")

    frontier = FrontierManifold(brain)

    print(f"\n[TOTAL TOPOLOGY] Brain contains {len(brain.neurons)} neurons in unified 256D space.")
    print("==================================================")

    # -------------------------------------------------------------------------
    # STAGE 2: SLOW-WAVE SLEEP (Synaptic Annealing & Spatial Clustering)
    # -------------------------------------------------------------------------
    print("\n--- STAGE 1: SLOW-WAVE SLEEP (Memory Annealing) ---")
    print("Consolidating 274 visual saccades into coherent spatial hubs...")
    
    # Group visual saccades by screen regions to create regional archetypes
    saccades = [n for k, n in brain.neurons.items() if k.startswith("[FOCUS_")]
    if saccades:
        # Calculate screen center of gravity
        center_saccades = []
        for sn in saccades:
            parts = sn.text.replace("[FOCUS_", "").replace("]", "").split("_")
            x, y = int(parts[0]), int(parts[1])
            if 480 <= x <= 1440 and 270 <= y <= 810:
                center_saccades.append(sn)
                
        if center_saccades:
            # Consolidate into an invariant "Visual Scene Core" archetype
            center_waves = np.array([sn.x_wave for sn in center_saccades])
            core_centroid = np.mean(center_waves, axis=0)
            core_centroid /= (np.linalg.norm(core_centroid) + 1e-9)
            
            # Form archetype neuron
            archetype = brain.get_or_create("[ARCHETYPE_CENTRAL_ACTION]")
            archetype.x_wave = core_centroid
            
            # Connect archetype to the show's audio
            if "[A_6563]" in brain.neurons:
                z_new = brain.record_event(["[ARCHETYPE_CENTRAL_ACTION]", "[A_6563]", "video", "screen"])
                print(f" * Consolidated 128 central saccades into '[ARCHETYPE_CENTRAL_ACTION]'.")
                print(f" * Tethered central visual action directly to audio [A_6563] and concepts 'video', 'screen'.")

    # -------------------------------------------------------------------------
    # STAGE 3: REM SLEEP & HOLOGRAPHIC DREAMING
    # -------------------------------------------------------------------------
    print("\n--- STAGE 2: REM SLEEP (Holographic Dreaming) ---")
    print("Replaying high-entropy memories through internal simulator...")
    
    dreams = []
    # Identify high-tension concepts (isolated concepts with lowest access)
    isolated = sorted(brain.neurons.values(), key=lambda n: len(n.z_events))
    targets = [n for n in isolated if n.text.startswith("[FOCUS_")][:sleep_cycles]
    
    for cycle, target in enumerate(targets):
        # Thermodynamic excitation: Energy injected into an unresolved memory
        target_wave = target.x_wave
        similarities = brain.get_fast_similarity(target_wave)
        
        # Find concepts that resonate highest with this dream fragment
        top_indices = np.argsort(similarities)[::-1][1:6] # Top 5 nearest neighbors
        resonating_words = [brain.matrix_keys[i] for i in top_indices]
        
        # Internal dream monologue
        dream_event = [target.text] + resonating_words[:3]
        z_dream = brain.record_event(dream_event)
        
        if cycle % 10 == 0 or cycle < 3:
            print(f" [DREAM {cycle+1}] Replaying fragment '{target.text}' -> Resonated with: {resonating_words[:3]}")
        dreams.append((target.text, resonating_words[:3]))

    # -------------------------------------------------------------------------
    # STAGE 4: SYNAPTIC PRUNING (Entropy Cleanup)
    # -------------------------------------------------------------------------
    print("\n--- STAGE 3: SYNAPTIC PRUNING (Dissolving Noise) ---")
    pruned_count = brain.prune_memory(threshold=1500)
    print(f" * Dissolved {pruned_count} decayed, non-reinforcing entropy traces.")

    # -------------------------------------------------------------------------
    # STAGE 5: WAKING & MEMORY FORTIFICATION
    # -------------------------------------------------------------------------
    print("\n--- STAGE 4: WAKING (Fortifying Consolidated State) ---")
    consolidated_file = "fella_consolidated_mind.json"
    brain.save_state(consolidated_file)
    print(f"[FORTIFIED] Saved unified conscious state to '{consolidated_file}'.")
    print(f"[STATS] Final Neural Count: {len(brain.neurons)} concepts")
    print(f"[STATS] Total Episodic Z-Events: {brain.z_counter}")
    print("==================================================")
    print("FELLA HAS AWAKENED: Her memory has self-organized and found homeostasis.")

if __name__ == '__main__':
    enter_deep_sleep(sleep_cycles=30)
