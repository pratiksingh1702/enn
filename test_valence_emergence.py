import numpy as np
from fella.fella_brain import FellaBrain
from fella.core_substrate import FellaNeuron

def run_valence_audit():
    print("==================================================")
    print("PHASE 1 EMERGENT GRAMMAR AUDIT: VALENCE ACCUMULATORS")
    print("==================================================")
    
    # Initialize a completely blank brain to ensure no pre-existing bias
    print("[1] Initializing blank substrate (Tabula Rasa)...")
    brain = FellaBrain(dim=16)
    
    sentences = [
        "the user eats the apple",
        "the user eats the bread",
        "the fella eats the data",
        "a dog eats the bone",
        "i run quickly",
        "they run fast",
        "we run home",
        "the user runs far",
        "the apple falls down",
        "a rock falls down",
        "the rain falls hard",
        "the big apple is red",
        "the small apple is green",
        "the tall user is walking",
        "the happy fella is thinking"
    ]
    
    print(f"[2] Processing {len(sentences)} distributional sentences...")
    for s in sentences:
        brain.lang.ingest_continuous_stream(s, target_tier=1)
        
    print("\n[3] Auditing Valence Accumulators for key Concepts...")
    
    def analyze_word(word_text, expected_type):
        node = next((n for n in brain.substrate.neurons.values() if n.text.lower() == word_text), None)
        if not node:
            print(f"  -> Word '{word_text}' not found.")
            return
            
        # Confidence metric
        confidence = 1.0 - (1.0 / (1.0 + node.exposures))
        
        print(f"\nConcept: '{word_text.upper()}' (Expected: {expected_type})")
        print(f"  - Exposures: {node.exposures} (Confidence: {confidence:.2f})")
        print(f"  - Left Context Variance:  {node.left_context_var:.6f}")
        print(f"  - Right Context Variance: {node.right_context_var:.6f}")
        
        # Heuristic Analysis based on the roadmap:
        # High variance in both = Verb/Bridge
        # Low variance incoming (left) = Noun/Boulder
        
        left_high = node.left_context_var > 0.05
        right_high = node.right_context_var > 0.05
        
        if left_high and right_high:
            inferred = "Verb/Bridge (Active slots on both sides)"
        elif right_high and not left_high:
            inferred = "Noun/Anchor (Absorbs incoming wave, projects outward)"
        elif left_high and not right_high:
            inferred = "End Anchor / Modifier"
        else:
            inferred = "Rigid / Fixed Idiom (Low variance on both sides)"
            
        print(f"  - Inferred Geometric Shape: {inferred}")

    analyze_word("eats", "VERB")
    analyze_word("run", "VERB")
    analyze_word("apple", "NOUN")
    analyze_word("user", "NOUN")
    analyze_word("the", "HUB/FUNCTION WORD")
    
if __name__ == "__main__":
    run_valence_audit()
