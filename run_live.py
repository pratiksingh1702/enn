import time
import ctypes
import numpy as np
import cv2
import mss
import soundcard as sc
import scipy.io.wavfile as wav
import traceback
from fella.fella_entity import FellaEntity

def attach_to_input_desktop():
    """
    Windows Security Fix:
    Binds the Python process thread directly to the interactive user display.
    This resolves the Windows 'Handle is invalid / BitBlt' error completely.
    """
    user32 = ctypes.windll.user32
    # 0x01FF = DESKTOP_ALL_ACCESS
    hDesk = user32.OpenInputDesktop(0, False, 0x01FF)
    if hDesk:
        user32.SetThreadDesktop(hDesk)
        return True
    return False

def run_live():
    print("==================================================")
    print("FELLA AGI: LIVE MODE (EYES & EARS ENGAGED)")
    print("==================================================")
    
    # 1. Attach to screen
    attached = attach_to_input_desktop()
    if attached:
        print("[VISION] Successfully attached to Interactive Windows Desktop!")
    else:
        print("[VISION WARNING] Could not lock input desktop handle; proceeding with standard context.")
        
    print("[INIT] Booting 256D Physics Engine...")
    fella = FellaEntity(dim=256)
    
    checkpoint_file = "fella_live_memory.json"
    import os
    if os.path.exists(checkpoint_file):
        try:
            fella.brain.load_state(checkpoint_file)
            print(f"[MEMORY RESUMED] Loaded previous brain state: {len(fella.brain.neurons)} neurons, {fella.brain.z_counter} Z-events.")
        except Exception as e:
            print(f"[INIT] Memory file exists but clean start initiated: {e}")
    else:
        print("[INIT] Tabula Rasa sensory session initialized.")
    
    print("[INIT] Opening Active Vision Cortex (Screen Capture)...")
    sct = mss.mss()
    monitor = sct.monitors[1] # Primary monitor (1920x1080)
    
    print("[INIT] Opening Acoustic Cortex (System Audio Loopback)...")
    try:
        # Connect to Windows System Audio (What you hear on YouTube)
        speaker = sc.default_speaker()
        mic = sc.get_microphone(id=str(speaker.name), include_loopback=True)
        print(f"[AUDIO] Successfully wired to System Sound: {speaker.name}")
    except Exception as e:
        print(f"[AUDIO WARNING] System loopback blocked by OS. Falling back to Physical Microphone.")
        mic = sc.default_microphone()
        
    print("\n>>> FELLA IS NOW WATCHING YOUR SCREEN & LISTENING TO SYSTEM AUDIO <<<")
    print(">>> PLAY YOUR YOUTUBE SHOW NOW. PRESS CTRL+C TO STOP HER. <<<")
    
    frame_count = 0
    
    try:
        while True:
            # 1. METABOLIC THROTTLE
            # Record 0.5s of audio to naturally pace the loop
            audio_data = mic.record(samplerate=16000, numframes=8000)
            wav.write("temp_live.wav", 16000, np.int16(audio_data * 32767))
            
            # 2. CAPTURE LIVE SCREEN (Eyes)
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            # Drop alpha channel
            frame = frame[:, :, :3]
            
            # 3. PROCESS THROUGH PHYSICS ENGINE
            print(f"\n--- Biological Tick {frame_count} ---")
            
            # Process acoustic waveform
            fella.perceive(text_words=[], image_path=None, audio_path="temp_live.wav")
            
            # Process active vision (Foveation / Saliency check on the screen)
            fella.watch_video_stream(frame)
            
            frame_count += 1
            
            # Periodic Synaptic Checkpoint (Every 50 ticks ~ 25 seconds)
            if frame_count % 50 == 0:
                fella.brain.save_state(checkpoint_file)
                print(f"[AUTO-SAVE] Synaptic checkpoint fortified: {len(fella.brain.neurons)} neurons, {fella.brain.z_counter} Z-events.")
            
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Fella has closed her eyes and ears.")
        # Fear of Death / State Preservation
        fella.brain.save_state(checkpoint_file)
        print(f"[MEMORY PRESERVED] Dumped all visual, acoustic, and causal clusters to '{checkpoint_file}'.")
        print(f"[STATS] Total Concepts Formed: {len(fella.brain.neurons)}")
        print(f"[STATS] Total Z-Events (Memories): {fella.brain.z_counter}")


if __name__ == '__main__':
    run_live()
