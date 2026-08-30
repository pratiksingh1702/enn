"""
FELLA Vast-Scale Benchmark Harness (1,000 Prompts)
==================================================
Profiles FELLA's cognitive field across all 7 protocol evaluation metrics:
1. Grammatical Accuracy (>= 95%)
2. Semantic Coherence (>= 90%)
3. Response Speed (<= 500ms)
4. Filler Phrase Frequency (= 0)
5. Epistemic Humility (>= 90%)
6. Self-Correction Rate (>= 2 rejections/query)
7. Novelty (>= 70%)
"""

import sys
import os
import time
import re
from typing import List, Dict, Any, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain
from fella.vast_curriculum_generator import generate_diagnostic_test_battery


def evaluate_response_quality_vast(resp: str, keywords: List[str], is_unknown: bool) -> Dict[str, Any]:
    text = resp.strip()
    words = text.split()
    
    # 1. Grammar checks
    has_cap = bool(text and text[0].isupper())
    has_term = bool(text and text.endswith('.'))
    is_length_valid = len(words) >= 3 if not is_unknown else True
    is_grammatical = has_cap and has_term and is_length_valid
    
    # 2. Filler checks
    has_filler = "essential phenomenon" in text.lower()
    
    # 3. Epistemic humility
    is_humble = any(h in text.lower() for h in ["uncertainty", "uncertain", "unknown", "observation", "inquire"])
    
    # 4. Semantic coherence
    tokens = set(re.findall(r'\b\w+\b', text.lower()))
    hits = [kw for kw in keywords if kw.lower() in tokens or any(kw.lower() in t for t in tokens)]
    
    if is_unknown:
        is_coherent = is_humble
    else:
        is_coherent = (len(hits) >= 1) and not has_filler
        
    return {
        "text": text,
        "is_grammatical": is_grammatical,
        "is_coherent": is_coherent,
        "has_filler": has_filler,
        "is_humble": is_humble,
        "hits": hits
    }


def run_vast_benchmark(brain: FellaBrain, count: int = 1000) -> Dict[str, Any]:
    test_battery = generate_diagnostic_test_battery(count=count)
    
    total = len(test_battery)
    grammatical_count = 0
    coherent_count = 0
    filler_count = 0
    humble_success_count = 0
    unknown_total = 0
    total_rejections = 0
    latencies = []
    
    unique_outputs = set()
    
    start_all = time.time()
    for item in test_battery:
        q = item["query"]
        kws = item["keywords"]
        is_unk = item["is_unknown"]
        if is_unk:
            unknown_total += 1
            
        t0 = time.time()
        res = brain.lang.reason_over_query(q)
        lat = (time.time() - t0) * 1000.0  # ms
        latencies.append(lat)
        
        narrative = res["reasoning_narrative"]
        unique_outputs.add(narrative)
        total_rejections += res.get("rejected_count", 0)
        
        eval_metrics = evaluate_response_quality_vast(narrative, kws, is_unk)
        
        if eval_metrics["is_grammatical"]:
            grammatical_count += 1
        if eval_metrics["is_coherent"]:
            coherent_count += 1
        if eval_metrics["has_filler"]:
            filler_count += 1
        if is_unk and eval_metrics["is_humble"]:
            humble_success_count += 1
            
    total_time = time.time() - start_all
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    avg_rejections = total_rejections / total if total else 0.0
    grammatical_rate = (grammatical_count / total) * 100.0
    coherence_rate = (coherent_count / total) * 100.0
    humility_rate = (humble_success_count / unknown_total * 100.0) if unknown_total else 100.0
    novelty_rate = (len(unique_outputs) / total) * 100.0
    
    results = {
        "total_prompts": total,
        "total_time_seconds": total_time,
        "avg_latency_ms": avg_latency,
        "grammatical_rate": grammatical_rate,
        "coherence_rate": coherence_rate,
        "filler_count": filler_count,
        "humility_rate": humility_rate,
        "avg_rejections_per_query": avg_rejections,
        "novelty_rate": novelty_rate,
        "total_living_neurons": len(brain.substrate.neurons),
        "total_synaptic_bridges": brain.substrate.get_synapse_stats()["total_synapses"]
    }
    return results


if __name__ == "__main__":
    b = FellaBrain.load_state("fella_checkpoint.json")
    res = run_vast_benchmark(b, count=1000)
    print("Benchmark Results:", res)
