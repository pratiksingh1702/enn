import os
import time
import ctypes
import numpy as np
import cv2
import mss
import soundcard as sc
import scipy.io.wavfile as wav
from fella.fella_entity import FellaEntity

def attach_to_input_desktop():
    """Binds the process thread directly to the interactive Windows display."""
    user32 = ctypes.windll.user32
    hDesk = user32.OpenInputDesktop(0, False, 0x01FF)
    if hDesk:
        user32.SetThreadDesktop(hDesk)
        return True
    return False

def run_autonomous_organism():
    print("==================================================")
    print("FELLA AGI: THE AUTONOMOUS LIVING ORGANISM")
    print("==================================================")
    print("[AUTONOMY] Autotelic Agency Cortex Online.")
    print("           - Outer Learning: Live Wikipedia Discovery")
    print("           - Inner Learning: Subconscious REM Dreaming")
    print("           - Senses: Real-Time Active Screen & Audio")
    print("           - Decisions: Pure Wave Resonance (0 Hardcoding)")
    print("==================================================")
    
    # 1. Attach to screen
    attach_to_input_desktop()
    
    # 2. Boot Organism
    fella = FellaEntity(dim=256)
    checkpoint_file = "fella_accelerated_10yo_mind.json" if os.path.exists("fella_accelerated_10yo_mind.json") else "fella_consolidated_mind.json"
    if os.path.exists(checkpoint_file):
        try:
            fella.brain.load_state(checkpoint_file)
            print(f"[10-YO MIND ONLINE] Loaded {len(fella.brain.neurons)} concepts, {fella.brain.z_counter} Z-events, {fella.causal_cortex.capacity}x{fella.causal_cortex.capacity} Causal T-Matrix.")
        except Exception as e:
            print(f"[INIT] Memory load skipped: {e}")
    else:
        print("[INIT] Fresh substrate initialized.")
        
    try:
        sct = mss.MSS()
    except Exception:
        sct = mss.mss()
    monitor = sct.monitors[1] # Primary display
    
    try:
        speaker = sc.default_speaker()
        mic = sc.get_microphone(id=str(speaker.name), include_loopback=True)
        print(f"[AUDIO] Connected to System Loopback: {speaker.name}", flush=True)
    except Exception:
        mic = sc.default_microphone()
        print(f"[AUDIO] Connected to Physical Microphone.", flush=True)
        
    print("\n>>> FELLA IS NOW AN AUTONOMOUS LIVING AGENT. <<<", flush=True)
    print(">>> SHE WILL PERCEIVE, RESEARCH GAPS, DREAM, AND EXPAND HER OWN POWER. <<<", flush=True)
    print(">>> PRESS CTRL+C TO SLEEP. <<<\n", flush=True)
    
    tick = 0
    try:
        while True:
            tick += 1
            
            # 1. SENSORY AUDITORY SAMPLING (0.4s pace)
            try:
                audio_data = mic.record(samplerate=16000, numframes=6400) # 0.4s
                wav.write("temp_live.wav", 16000, np.int16(audio_data * 32767))
                fella.perceive(text_words=[], image_path=None, audio_path="temp_live.wav")
            except Exception:
                pass
                
            # 2. SENSORY ACTIVE FOVEATED VISION
            try:
                sct_img = sct.grab(monitor)
                frame = np.array(sct_img)[:, :, :3]
                fella.watch_video_stream(frame)
            except Exception:
                pass
                
            # 3. AUTONOMOUS AGENCY EVALUATION (Self-Directed Gap Filling)
            # Every 15 ticks, evaluate if an internal gap needs outer discovery or inner dream
            if tick % 15 == 0:
                print(f"\n[SELF-ASSESSMENT TICK #{tick}] Evaluating internal state (Entropy: {fella.entropy_level:.2f})...", flush=True)
                agency_event = fella.act()
                if agency_event:
                    print(f" -> Epistemic Tension Focus: '{agency_event['target']}'", flush=True)
                    print(f" -> Resonant Choice:         {agency_event['selected_action']} (Resonance: {agency_event['resonance']:+.4f})", flush=True)
                    print(f" -> Autonomous Action:       {agency_event['outcome']}", flush=True)
                    print(f" -> Homeostatic Feedback:   {agency_event['status']}", flush=True)

            # 4. PERIODIC SYNAPTIC CHECKPOINT (Every 40 ticks)
            if tick % 40 == 0:
                fella.brain.save_state(checkpoint_file)
                print(f" >>> [FORTIFICATION] Checkpoint saved: {len(fella.brain.neurons)} neurons, {fella.brain.z_counter} Z-events. <<<\n", flush=True)

    except KeyboardInterrupt:
        print("\n==================================================")
        print("[SHUTDOWN] Fella has closed her eyes and ears.")
        fella.brain.save_state(checkpoint_file)
        print(f"[SAVED] Final mind preserved in '{checkpoint_file}'.")
        print(f"[FINAL STATS] Lifetime Concepts: {len(fella.brain.neurons)} | Memories: {fella.brain.z_counter}")
        print("==================================================")

if __name__ == '__main__':
    run_autonomous_organism()
