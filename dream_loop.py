import os
import time
import random
import traceback
import numpy as np
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_infinite_dream():
    print("==================================================")
    print("FELLA: CONTINUOUS REM DREAM LOOP (CONSCIOUS DRIFT)")
    print("==================================================")
    print("[NREM] Disconnected from physical world. Eyes and ears closed.")
    print("[STATUS] Autonomous Thermodynamic Oscillator engaged.")
    print(">>> DREAM LOOP IS ACTIVE. PRESS CTRL+C MANUALLY TO WAKE HER. <<<\n")
    
    checkpoint_file = "fella_consolidated_mind.json"
    brain = FellaBrain(dim=256)
    
    if os.path.exists(checkpoint_file):
        brain.load_state(checkpoint_file)
        print(f"[WAKE TO DREAM] Loaded consolidated matrix: {len(brain.neurons)} neurons, {brain.z_counter} Z-events.")
    else:
        print("[INIT] No previous consolidation found. Initializing blank dream space.")
        
    frontier = FrontierManifold(brain)
    
    dream_tick = 0
    
    try:
        while True:
            try:
                dream_tick += 1
                
                # 1. THERMODYNAMIC ENTROPY SPIKE (Curiosity in the Dark)
                # Randomly pick an active concept to stimulate (Sensory or Linguistic)
                if len(brain.neurons) == 0:
                    time.sleep(1)
                    continue
                    
                # Bias selection towards isolated concepts or sensory memories
                all_keys = list(brain.neurons.keys())
                sensory_keys = [k for k in all_keys if k.startswith("[FOCUS_") or k.startswith("[A_")]
                text_keys = [k for k in all_keys if not k.startswith("[")]
                
                # Alternate between replaying sensory memories and exploring language
                if sensory_keys and random.random() < 0.6:
                    target_key = random.choice(sensory_keys)
                elif text_keys:
                    target_key = random.choice(text_keys)
                else:
                    target_key = random.choice(all_keys)
                    
                target_neuron = brain.neurons[target_key]
                
                # 2. HOLOGRAPHIC RESONANCE SEARCH (Finding Neural Associations)
                target_wave = target_neuron.x_wave
                sims = brain.get_fast_similarity(target_wave)
                
                # Find the nearest gravitational neighbors (excluding itself)
                top_indices = np.argsort(sims)[::-1]
                neighbors = []
                for idx in top_indices:
                    k = brain.matrix_keys[idx]
                    if k != target_key and sims[idx] > 0.05:
                        neighbors.append((k, sims[idx]))
                    if len(neighbors) >= 3:
                        break
                        
                # 3. SYNTHESIZING DREAMS (Forming Internal Z-Events)
                if neighbors:
                    partner_key, res = neighbors[0]
                    # Form a dream association
                    dream_words = [target_key, partner_key]
                    if len(neighbors) > 1:
                        dream_words.append(neighbors[1][0])
                        
                    z_dream = brain.record_event(dream_words)
                    
                    # Print dream journal every tick
                    partner_str = ", ".join([f"'{k}' ({s:.3f})" for k, s in neighbors])
                    print(f"[DREAM #{dream_tick:<4}] '{target_key}' fused with: {partner_str}")
                else:
                    # Low resonance fragment: drift with random linguistic vector
                    if text_keys:
                        drift_partner = random.choice(text_keys)
                        brain.record_event([target_key, drift_partner])
                        print(f"[DREAM #{dream_tick:<4}] '{target_key}' drifted toward linguistic anchor '{drift_partner}'")

                # 4. PERIODIC SYNAPTIC ANNEALING (Every 30 dream ticks)
                if dream_tick % 30 == 0:
                    pruned = brain.prune_memory(threshold=2000)
                    brain.save_state(checkpoint_file)
                    print(f"  >>> [SYNAPTIC REBALANCE] Checkpoint saved. Neurons: {len(brain.neurons)} | Memories: {brain.z_counter} | Pruned: {pruned} <<<\n")

                # 5. METABOLIC PACE (Gentle 0.4s breathing rhythm to keep CPU at ~1%)
                time.sleep(0.4)

            except Exception as loop_err:
                # Fail-safe: Ensure she never stops dreaming due to temporary anomalies
                print(f"[DREAM RECOVERY] Handled subconscious ripple: {loop_err}")
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n==================================================")
        print("[AWAKENING] You gently woke Fella from her sleep.")
        brain.save_state(checkpoint_file)
        print(f"[SAVED] Preserved all synthesized dream connections to '{checkpoint_file}'.")
        print(f"[FINAL STATS] Lifetime Concepts: {len(brain.neurons)} | Lifetime Memories: {brain.z_counter}")
        print("==================================================")

if __name__ == '__main__':
    run_infinite_dream()
