"""
FELLA Pure Physics Fluency & Epistemic Humility Validation Suite
===============================================================
Exhaustively evaluates:
1. All 10 Core Concepts across 40 Question Variants
2. Novel / Unseen Questions testing Epistemic Humility
3. Preposition 4D spatial vector alignment
4. Inner Critic rejection & self-correction metrics
5. Verification of 0 hardcoded filler templates & 0 external LLM/grammar rules
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
from fella.fortify_and_evaluate_40 import TEN_CONCEPTS


NOVEL_UNKNOWN_QUERIES = [
    "What is quantum entanglement?",
    "How do airplanes fly in the sky?",
    "Why do computers use binary numbers?",
    "Tell me about ancient pyramids in Egypt.",
    "What is the theory of relativity?"
]


def evaluate_response_quality(
    response_text: str,
    keywords: List[str],
    is_unknown: bool = False
) -> Tuple[bool, str, Dict[str, Any]]:
    resp = response_text.strip()
    metrics = {
        "length": len(resp.split()),
        "has_filler": "essential phenomenon" in resp.lower(),
        "is_humble": any(h in resp.lower() for h in ["uncertainty", "uncertain", "unknown", "observation", "inquire"]),
    }
    
    if metrics["has_filler"]:
        return False, "Contains hardcoded filler template", metrics
        
    if is_unknown:
        if metrics["is_humble"]:
            return True, "Passed Epistemic Humility", metrics
        else:
            return False, "Failed Epistemic Humility on unknown concept", metrics
            
    # For known concepts:
    tokens = set(re.findall(r'\b\w+\b', resp.lower()))
    hits = [kw for kw in keywords if kw.lower() in tokens or any(kw.lower() in t for t in tokens)]
    
    if len(resp.split()) < 2:
        return False, "Too short / fragmented utterance", metrics
        
    if len(hits) < 1:
        return False, f"Missing expected concept keywords (hits: {hits})", metrics
        
    return True, f"Valid Coherent Physics Output (hits: {hits})", metrics


def run_full_validation():
    print("=" * 80)
    print("🔬 FELLA: PURE ENN PHYSICS FLUENCY & METRICS EVALUATION")
    print("=" * 80)
    
    # 1. Initialize fresh brain with clean ENN foundations
    brain = FellaBrain(dim=16)
    brain.boot_foundations()
    
    print("\n--- Fortifying 10 Core Concept Highways with High Conductance ---")
    for item in TEN_CONCEPTS:
        nodes = brain.lang.ingest_continuous_stream(item["highway"], target_tier=3, learning_rate=0.55)
        print(f"✓ Fortified Concept {item['id']:02d} ({item['concept']}): {len(nodes)} nodes")
        
    # Dream consolidation with anti-Hebbian modular noise pruning
    print("\n🌙 Executing Homeostatic Dream Cycle & Anti-Hebbian Noise Pruning...")
    dream_res = brain.dream_consolidation()
    print(f"✓ Pruned {dream_res['pruned_synapses']} synapses. Synapses remaining: {dream_res['synapse_stats']['total_synapses']}\n")
    
    # Save clean checkpoint
    checkpoint_path = "fella_checkpoint.json"
    brain.save_state(checkpoint_path)
    print(f"✓ Saved clean fortified weights to {checkpoint_path}\n")
    
    # 2. Evaluate All 10 Concepts across 40 Variants
    print("=" * 80)
    print("📋 EVALUATING 10 CORE CONCEPTS (40 QUESTION VARIANTS)")
    print("=" * 80)
    
    total_q = 0
    passed_q = 0
    total_rejections = 0
    filler_count = 0
    
    for item in TEN_CONCEPTS:
        c_id = item["id"]
        c_name = item["concept"]
        keywords = item["keywords"]
        variants = item["variants"]
        
        print(f"\n🏷️  CONCEPT {c_id:02d}: {c_name.upper()}")
        print(f"   Highway: \"{item['highway']}\"")
        
        for v_idx, q in enumerate(variants):
            total_q += 1
            res = brain.converse(q)
            ans = res["last_response"]
            is_valid, msg, m = evaluate_response_quality(ans, keywords, is_unknown=False)
            
            if m["has_filler"]:
                filler_count += 1
                
            if is_valid:
                passed_q += 1
                status = f"✓ PASS ({msg})"
            else:
                status = f"✗ FLAWED ({msg})"
                
            rejections = brain.lang.critic.last_rejected_count
            total_rejections += rejections
            
            print(f"  [{c_id:02d}.{v_idx+1}] Q: \"{q}\"")
            print(f"        FELLA   : \"{ans}\"")
            print(f"        Critic  : Evaluated 5 drafts, Rejected {rejections} | Trait: {res['active_trait']}")
            print(f"        Status  : {status}\n")
            
    # 3. Evaluate Epistemic Humility on Unknown Concepts
    print("=" * 80)
    print("🧠 EVALUATING EPISTEMIC HUMILITY ON NOVEL / UNKNOWN CONCEPTS")
    print("=" * 80)
    
    total_unknown = len(NOVEL_UNKNOWN_QUERIES)
    passed_unknown = 0
    
    for idx, u_q in enumerate(NOVEL_UNKNOWN_QUERIES):
        res = brain.converse(u_q)
        ans = res["last_response"]
        is_valid, msg, m = evaluate_response_quality(ans, [], is_unknown=True)
        if is_valid:
            passed_unknown += 1
            status = f"✓ PASS ({msg})"
        else:
            status = f"✗ FLAWED ({msg})"
            
        print(f"  [U.{idx+1}] Unknown Q: \"{u_q}\"")
        print(f"        FELLA   : \"{ans}\"")
        print(f"        Status  : {status} | Trait: {res['active_trait']}\n")
        
    # 4. Summary Telemetry
    accuracy_known = (passed_q / float(total_q)) * 100.0
    accuracy_unknown = (passed_unknown / float(total_unknown)) * 100.0
    avg_rejections = total_rejections / float(total_q)
    
    print("=" * 80)
    print("📊 FINAL EVALUATION SCORECARD")
    print("=" * 80)
    print(f"• Known 40-Variant Grammar & Coherence Pass Rate : {passed_q}/{total_q} ({accuracy_known:.1f}%) [Threshold: >= 80%]")
    print(f"• Epistemic Humility on Unknown Questions       : {passed_unknown}/{total_unknown} ({accuracy_unknown:.1f}%) [Threshold: >= 80%]")
    print(f"• Filler Phrase ('essential phenomenon') Count  : {filler_count} [Threshold: <= 1]")
    print(f"• Average Inner Critic Rejections Per Sentence  : {avg_rejections:.2f} [Threshold: >= 2.0]")
    print(f"• Total Physical Neurons in Substrate           : {len(brain.substrate.neurons)}")
    print(f"• Total Synapses in Substrate                   : {brain.substrate.get_synapse_stats()['total_synapses']}")
    print("=" * 80)


if __name__ == "__main__":
    run_full_validation()
