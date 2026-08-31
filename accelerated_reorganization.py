import time
import sys
from typing import List
from fella.fella_brain import FellaBrain

def run_accelerated_reorganization(max_concepts=50):
    print("Loading Brain for Hyper-Accelerated Reorganization...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    
    # 1. Identify Target Concepts (Shallow words from the book that lack semantic meaning)
    # We filter out tiny words and prioritize strong nouns and verbs.
    targets = []
    for n in brain.substrate.neurons.values():
        if len(n.text) > 3 and (n.syntax_valence[0] > 0.4 or n.syntax_valence[1] > 0.4):
            # Check if it lacks Tier 3 grounding
            targets.append(n)
            
    # Sort by how central they are to the graph (energy/out-degree)
    targets.sort(key=lambda x: len(x.synapses) + x.energy, reverse=True)
    targets = targets[:max_concepts]
    
    total = len(targets)
    print(f"\n[INITIATING REORGANIZATION ENGINE]")
    print(f"Identified {total} high-priority shallow concepts to semantically ground.\n")
    
    if total == 0:
        print("No concepts need reorganization!")
        return

    start_time = time.time()
    
    for i, concept in enumerate(targets):
        iter_start = time.time()
        
        # Register the physical need for knowledge
        vacuum = brain.observer.register_vacuum(
            concept_query=concept.text,
            context_z=float(concept.tier_z),
            tension=1.0,
            context_prompt=f"Define the physical reality and causality of {concept.text}"
        )
        
        sys.stdout.write(f"[{i+1}/{total}] Pondering: '{concept.text}'... ")
        sys.stdout.flush()
        
        # Query Ollama
        mentor_bundle = brain.mentor.ask_about_vacuum(vacuum)
        explanation = mentor_bundle.get("explanation", "")
        
        if explanation:
            # Re-wire the brain permanently in Tier 3 (Causal Laws)
            brain.lang.ingest_continuous_stream(explanation, target_tier=3)
            brain.observer.resolve_vacuum(vacuum.vacuum_id, explanation)
            sys.stdout.write("Grounded!\n")
        else:
            sys.stdout.write("Failed to connect to Mentor.\n")
            break
            
        # Time Tracking & ETA
        iter_time = time.time() - iter_start
        elapsed = time.time() - start_time
        avg_time = elapsed / (i + 1)
        remaining = total - (i + 1)
        eta_seconds = remaining * avg_time
        
        mins, secs = divmod(int(eta_seconds), 60)
        sys.stdout.write(f"    -> Speed: {iter_time:.1f}s/concept | ETA: {mins}m {secs}s\n")
        
        # Save progress every 5 concepts so we don't lose data
        if (i + 1) % 5 == 0:
            brain.save_state('fella_checkpoint.json')
            
    # Final Save
    brain.save_state('fella_checkpoint.json')
    print("\n[REORGANIZATION COMPLETE]")
    print("Fella has successfully transformed raw story data into structured semantic reality.")

if __name__ == '__main__':
    run_accelerated_reorganization(max_concepts=20)
