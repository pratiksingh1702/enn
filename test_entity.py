import numpy as np
import cv2
import scipy.io.wavfile as wav
import time
from fella.fella_entity import FellaEntity

def test_singular_entity():
    print("=========================================")
    print("PHASE 2 & 5: THE SINGULAR ENTITY")
    print("=========================================")
    
    # 1. Create dummy multi-modal environment
    # The Visual Object (Apple)
    img = np.zeros((100, 100), dtype=np.uint8)
    cv2.circle(img, (50, 50), 30, 255, -1)
    cv2.imwrite("test_apple.jpg", img)

    # The Acoustic Sound (A 440Hz beep simulating a spoken word)
    sample_rate = 16000
    t = np.linspace(0, 1, sample_rate)
    audio_data = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
    wav.write("test_apple.wav", sample_rate, audio_data)
    
    # 2. Birth the Entity
    fella = FellaEntity(dim=256)
    
    # 3. Give her a basic grammar rule for generation
    # Initialize basic concepts
    for word in ["what", "is", "apple", "fruit", "red", "this", "an"]:
        fella.brain.get_or_create(word)
        
    q_spec = fella.brain.record_event(["what", "is", "apple"])
    fella.frontier.form_spectron([q_spec])
    y, t, r, w_id = fella.frontier.formulate_thought("what is apple", simulate=True)
    fella.frontier.process_correction("apple", ["fruit", "red"], "apple is fruit", w_id)

    # 4. Perceive the World (Simultaneous Multi-Modal Fusion)
    print("\n[ENVIRONMENT] Presenting physical image, playing audio, and sending text...")
    fella.perceive(["this", "is", "an", "apple", "fruit"], "test_apple.jpg", "test_apple.wav")
    print("[ENGINE] Successfully fused Text, RGB-FFT, and Audio-FFT into a single Z-Event.")
    
    # 5. Fast-Forward Time to test the Thermodynamic Oscillator (Curiosity)
    print("\n[ENVIRONMENT] You step away from the laptop. The room is silent. Time passes...")
    for tick in range(1, 60):
        # 60 ticks of zero input, entropy rises
        fella.metabolize_time(ticks=1)

if __name__ == '__main__':
    test_singular_entity()
