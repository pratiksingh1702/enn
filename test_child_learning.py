import sys
import numpy as np
from fella.fella_brain import FellaBrain
from fella.emergent_spectron_engine import EmergentSpectronEngine

def run_child_learning():
    print("Initializing Tabula Rasa (Blank Slate) FELLA Brain...")
    brain = FellaBrain(dim=16) # Fast init
    
    # Use the pure emergent engine (no hardcoding)
    engine = EmergentSpectronEngine(brain.substrate, brain.lang)
    
    print("\n==================================================")
    print("STAGE 1: BABY EXPERIENCES (Learning Spectrons)")
    print("==================================================")
    
    # 1. Experience a question (intonation is '?' which injects heat)
    print("\nUSER (Pratik): what is apple ?")
    engine.parse_simultaneous_wave("what is apple ?", speaker_id="pratik")
    
    # 2. Experience an answer
    print("\nUSER (Pratik): apple is fruit")
    engine.parse_simultaneous_wave("apple is fruit", speaker_id="pratik")
    
    # 3. Experience another question
    print("\nUSER (Priya): what is sun ?")
    engine.parse_simultaneous_wave("what is sun ?", speaker_id="priya")
    
    print("\n==================================================")
    print("STAGE 2: CHECKING EMERGENT SPECTRONS")
    print("==================================================")
    
    def print_spectron(word):
        n = engine._get_or_create_neuron(word)
        stype = engine.determine_spectron_type(n)
        print(f"Word: '{word}' | Emerged Type: {stype.upper()} | Hot: {n.hot_potential}, Cold: {n.cold_potential}, Catalyst: {n.catalyst_potential}")
        
    print_spectron("what")
    print_spectron("is")
    print_spectron("apple")
    print_spectron("fruit")
    
    print("\n==================================================")
    print("STAGE 3: THE MIRROR EMERGENCE (Pronoun 'I')")
    print("==================================================")
    
    # Pratik says he likes fruit
    print("\nUSER (Pratik): pratik likes fruit")
    engine.parse_simultaneous_wave("pratik likes fruit", speaker_id="pratik")
    print("USER (Pratik): i like fruit")
    engine.parse_simultaneous_wave("i like fruit", speaker_id="pratik")
    
    # Priya says she likes fruit
    print("\nUSER (Priya): priya likes fruit")
    engine.parse_simultaneous_wave("priya likes fruit", speaker_id="priya")
    print("USER (Priya): i like fruit")
    engine.parse_simultaneous_wave("i like fruit", speaker_id="priya")
    
    print("\n[CHECKING MIRROR SPECTRON]")
    n_i = engine._get_or_create_neuron("i")
    print(f"Word: 'i' | Emerged Type: {engine.determine_spectron_type(n_i).upper()} | Mirror Potential: {getattr(n_i, 'mirror_potential', 0.0)}")

if __name__ == "__main__":
    run_child_learning()
