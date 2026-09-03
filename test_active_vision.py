import numpy as np
import cv2
from fella.fella_entity import FellaEntity

def test_active_vision():
    print("=========================================")
    print("PHASE 4: BIOLOGICAL ACTIVE VISION & CURIOSITY")
    print("=========================================")
    
    fella = FellaEntity(dim=256)
    
    # Simulate a wide-angle 1080p camera feed (1920x1080)
    print("\n[ENVIRONMENT] Wide-angle 1080p camera initialized. Processing background traces...")
    
    # 1. 20 Frames of a static background room
    for i in range(20):
        # A static room
        frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 100 
        cv2.putText(frame, "Static Desk", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        
        fella.watch_video_stream(frame)
        
    print(f"[METRICS] Processed 20 frames of static background.")
    memories = len([k for k in fella.brain.neurons.keys() if "FOCUS_" in k])
    print(f"[METRICS] Total heavy 256D Focus extractions performed: {memories}. (She is bored/saving CPU)")
    
    # 2. A Car drives through the bottom right of the peripheral vision
    print("\n[ENVIRONMENT] A Car suddenly drives into the bottom-right periphery (1500, 900)...")
    
    for i in range(5):
        frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 100 
        cv2.putText(frame, "Static Desk", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        
        # The moving car anomaly
        cv2.rectangle(frame, (1500 + i*10, 900), (1600 + i*10, 950), (0, 0, 255), -1)
        
        fella.watch_video_stream(frame)
        
    # 3. A Girl walks into the top left of the peripheral vision
    print("\n[ENVIRONMENT] The car stops. A Girl walks into the top-left periphery (200, 300)...")
    
    for i in range(5):
        frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 100 
        cv2.putText(frame, "Static Desk", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        
        # The car stopped (no longer generating curiosity delta spikes)
        cv2.rectangle(frame, (1500 + 4*10, 900), (1600 + 4*10, 950), (0, 0, 255), -1)
        
        # The new moving girl anomaly
        cv2.circle(frame, (200 + i*5, 300), 40, (0, 255, 0), -1)
        
        fella.watch_video_stream(frame)

if __name__ == '__main__':
    test_active_vision()
