import urllib.request
import re
import time
import os
from fella.fella_brain import FellaBrain

def run():
    print("[FELLA: HIGH-SPEED TOPOLOGICAL DUMP]")
    print("Fetching 'Alice in Wonderland'...")
    url = "https://www.gutenberg.org/cache/epub/11/pg11.txt"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        raw_text = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch from Gutenberg: {e}")
        # Fallback text if network fails
        raw_text = "Alice was beginning to get very tired of sitting by her sister on the bank. The rabbit ran down the hole. The hole went straight down like a tunnel. She found herself in a long, low hall. The king and queen of hearts were seated on their throne. The cat vanished slowly, starting with its tail and ending with its grin."
        print("Using emergency local corpus.")

    # Clean text
    start_idx = raw_text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    if start_idx != -1:
        # Jump past the header
        raw_text = raw_text[start_idx+150:]
    end_idx = raw_text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if end_idx != -1:
        raw_text = raw_text[:end_idx]

    # Normalize whitespace and split sentences
    raw_text = re.sub(r'\s+', ' ', raw_text)
    sentences = [s.strip() for s in re.split(r'[.!?]+', raw_text) if len(s.strip().split()) > 2]
    
    # Cap at the first 500 sentences to keep this initial dump around 3-5 minutes
    sentences = sentences[:500]

    print(f"Extracted {len(sentences)} valid sentences for rapid ingestion.")
    
    print("\nLoading physical substrate...")
    brain = FellaBrain.load_state('fella_checkpoint.json')
    initial_neurons = len(brain.substrate.neurons)
    print(f"Initial Neurons: {initial_neurons}")
    
    print("\n[STARTING HIGH-SPEED INGESTION]")
    print("Ollama Mentor is turned OFF. Fella is carving geometry and wiring synapses purely through physics.")
    
    start_time = time.time()
    for i, sentence in enumerate(sentences):
        # We pass autonomous_exploration=False so she doesn't stop to ask Ollama
        brain.converse(sentence, autonomous_exploration=False)
        
        # Print progress every 25 sentences
        if (i + 1) % 25 == 0:
            elapsed = time.time() - start_time
            current_neurons = len(brain.substrate.neurons)
            print(f"[{i+1}/{len(sentences)}] Ingested. Neurons: {current_neurons} (+{current_neurons - initial_neurons}). Elapsed: {elapsed:.1f}s")
            
    print("\n[DUMP COMPLETE]")
    final_neurons = len(brain.substrate.neurons)
    print(f"Final Neurons: {final_neurons} (Total New Concepts Mapped: {final_neurons - initial_neurons})")
    
    print("Saving massive structural updates...")
    brain.save_state('fella_checkpoint.json')
    print("Brain saved successfully!")

if __name__ == '__main__':
    run()
