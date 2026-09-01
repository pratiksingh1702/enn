import urllib.request
import re
import time
from fella.fella_brain import FellaBrain

def download_corpus():
    print("Downloading corpus (Alice in Wonderland)...")
    url = "https://www.gutenberg.org/files/11/11-0.txt"
    try:
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to download from Project Gutenberg: {e}")
        # Fallback mini-corpus
        text = """
        The sun is hot and bright. The dog runs fast down the street. 
        Water is clear and wet. Birds fly in the blue sky. 
        Trees grow tall and green in the forest. 
        The cat sleeps on the warm bed. We run quickly. 
        Data flows through the network. An apple falls from the tree.
        """ * 50
        
    # Basic cleaning
    text = text.replace('\r\n', ' ').replace('\n', ' ')
    # Extract sentences roughly
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    clean_sentences = []
    for s in sentences:
        # Note: No re.replace in the core engine, just doing basic data cleaning for the test script
        s = re.sub(r'[^a-zA-Z\s]', '', s).lower().strip()
        if len(s.split()) > 2 and len(s.split()) < 20:
            clean_sentences.append(s)
            
    return clean_sentences[:1500] # Use top 1500 sentences

def run_phase4():
    print("==================================================")
    print("PHASE 4: LARGE-SCALE CORPUS INGESTION")
    print("==================================================")
    
    sentences = download_corpus()
    print(f"Extracted {len(sentences)} clean sentences.")
    
    brain = FellaBrain(dim=16)
    
    print("\n[1] Rapid continuous streaming through the wave engine...")
    start = time.time()
    
    # Process batches
    for i, s in enumerate(sentences):
        if i % 100 == 0:
            print(f"  Ingested {i}/{len(sentences)} sentences... (Vocab size: {len(brain.substrate.neurons)})")
        brain.lang.ingest_continuous_stream(s, target_tier=1)
        
    print(f"Streaming complete in {time.time() - start:.2f} seconds.")
    print(f"Final Vocabulary Size: {len(brain.substrate.neurons)}")
    
    print("\n[2] Triggering Epistemic Vacuums (Tests)...")
    
    test_prompts = [
        "apple",
        "run",
        "user",
        "bread",
        "home",
        "fast",
        "eats",
        "thinking",
        "alice",
        "rabbit",
        "cat",
        "down the hole",
        "white rabbit runs"
    ]
    from fella.frontier_manifold import FrontierManifold
    manifold = FrontierManifold(brain)
    
    for prompt in test_prompts:
        manifold.formulate_thought(prompt, max_length=15)

if __name__ == "__main__":
    run_phase4()
