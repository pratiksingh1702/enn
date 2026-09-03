import os
from fella.fella_brain import FellaBrain
from fella.frontier_manifold import FrontierManifold

def run_diluted_test():
    print("==================================================")
    print("APPLE DILUTION TEST: BREAKING THE CATALYST PARADOX")
    print("==================================================")
    
    brain = FellaBrain(dim=64)
    print("[VOID] Brain reset to blank slate.")
    
    # 1. Generate ~150 varied facts to dilute the "apple" exposure
    dilution_facts = [
        "pratik is human",
        "car is vehicle",
        "time is money",
        "dog is animal",
        "cat is animal",
        "water is liquid",
        "fire is hot",
        "the sun is bright",
        "the moon is white",
        "the grass is green",
        "birds fly in the sky",
        "fish swim in the water",
        "humans walk on the ground"
    ]
    
    nouns = ["car", "dog", "cat", "house", "bird", "plane", "boat", "computer", "phone", "pratik", "time", "money", "water", "fire", "earth", "wind", "man", "woman", "boy", "girl"]
    adjs = ["fast", "red", "big", "small", "good", "bad", "hot", "cold"]
    
    for n in nouns:
        for a in adjs:
            dilution_facts.append(f"the {n} is {a}")
            
    # 2. Add the 10 Apple facts
    apple_facts = [
        "apple is a fruit",
        "apple is red",
        "apple grows on a tree",
        "the fella eats the apple",
        "apple is sweet",
        "water makes the apple grow",
        "apple is round",
        "the woman likes the apple",
        "apple falls down to the ground",
        "apple is food"
    ]
    
    # Ingest the background universe (once each)
    print(f"[INGESTION] Learning {len(dilution_facts)} varied facts to build a massive grammar universe...")
    for fact in dilution_facts:
        brain.lang.ingest_continuous_stream(fact, target_tier=1)
        
    # Ingest the apple facts
    print("[INGESTION] Learning 10 facts about apples...")
    # Loop apple facts a few times to make the associations strong, but not enough to beat "the" and "is"
    for _ in range(3):
        for fact in apple_facts:
            brain.lang.ingest_continuous_stream(fact, target_tier=1)
            
    vocab = list(brain.substrate.neurons.values())
    print(f"[TOPOLOGY] Vocabulary Size: {len(vocab)}")
    
    # Find the top 3 most exposed words to prove the physics worked
    vocab.sort(key=lambda n: n.exposure_count, reverse=True)
    print("\n[PHYSICS] Top 5 Most Frequent Words (Catalyst Anchors):")
    for n in vocab[:5]:
        print(f"  - '{n.text}' (Exposure: {n.exposure_count})")
        
    apple_n = next((n for n in vocab if n.text == 'apple'), None)
    if apple_n:
        max_exp = vocab[0].exposure_count
        ratio = apple_n.exposure_count / max_exp
        print(f"\n[PHYSICS] 'apple' Exposure: {apple_n.exposure_count} ({ratio*100:.1f}% of max)")
        if ratio > 0.20:
            print("  -> 'apple' is STILL A CATALYST")
        else:
            print("  -> 'apple' IS NOW A SEMANTIC NOUN (Catalyst Paradox Broken!)")
            
    manifold = FrontierManifold(brain)
    question = "what is apple"
    
    print(f"\\n[FRONTIER] Asking '{question}'...")
    sentence = manifold.formulate_thought(question, persona_concept="the fella thinks about")
    
if __name__ == "__main__":
    run_diluted_test()
