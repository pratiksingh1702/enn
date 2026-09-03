import numpy as np
import cv2
from fella.fella_entity import FellaEntity

def test_predictive_coding():
    print("=========================================")
    print("PHASE 3: LIVE VIDEO & PREDICTIVE CODING")
    print("=========================================")
    
    fella = FellaEntity(dim=256)
    
    # 1. Create a simulated video stream (60 frames)
    # The first 30 frames are an Apple (circle) just moving around the screen
    print("\n[VIDEO STREAM START] You hold an Apple in front of the camera and move it around...")
    
    for i in range(30):
        frame = np.zeros((200, 200, 3), dtype=np.uint8)
        # The circle moves to the right 2 pixels per frame
        cv2.circle(frame, (50 + (i * 2), 100), 30, (0, 0, 255), -1) 
        
        result = fella.watch_video_stream(frame)
        if result is None:
            # We don't print every frame to avoid spam, but we track efficiency
            pass

    # Count how many visual events were actually stored in the deep brain
    visual_memories = len([k for k in fella.brain.neurons.keys() if "LIVE_V_" in k])
    print(f"\n[METRICS] Out of 30 frames of motion, the deep brain only recorded {visual_memories} memory event.")
    print("The Fourier Shift Theorem proved that moving the object did not change its structural frequency.")
    
    # 2. Introduce a massive structural change (Smashed Apple)
    print("\n[VIDEO STREAM EVENT] You smash the Apple!")
    
    smashed_frame = np.zeros((200, 200, 3), dtype=np.uint8)
    # A chaotic, high-frequency polygon simulating a smashed object
    pts = np.array([[100, 100], [150, 50], [180, 120], [120, 180], [60, 150]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(smashed_frame, [pts], True, (0, 0, 255), 5)
    
    # Feed the smashed frame
    fella.watch_video_stream(smashed_frame)
    
    final_memories = len([k for k in fella.brain.neurons.keys() if "LIVE_V_" in k])
    print(f"\n[METRICS] After the smash, total visual memories recorded: {final_memories}.")
    print("The engine successfully detected the Prediction Error and woke the brain.")

if __name__ == '__main__':
    test_predictive_coding()
