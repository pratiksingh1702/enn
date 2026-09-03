import numpy as np
import cv2

class LiveVideoCortex:
    def __init__(self, target_dim=256, delta_threshold=0.05):
        """
        Phase 3: The Live Video Cortex with Biological Predictive Coding.
        Processes continuous video frames, mathematically ignoring simple translation/movement
        via the Fourier Shift Theorem. 
        Only triggers a Z-Axis update when the structural geometry changes (Prediction Error).
        """
        self.target_dim = target_dim
        self.crop_size = int(np.sqrt(target_dim))
        self.delta_threshold = delta_threshold
        
        # Memory of the last geometric state (for the Temporal Delta Filter)
        self.last_wave = None

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Takes a raw BGR frame from cv2.VideoCapture or screen capture.
        Returns a 256D wave ONLY if a structural anomaly (delta spike) occurs.
        Returns None if the object is static or simply moving.
        """
        # 1. Grayscale and standardize spatial domain
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
            
        img_resized = cv2.resize(gray, (128, 128))
        
        # 2. 2D Fast Fourier Transform
        f_transform = np.fft.fft2(img_resized)
        f_shift = np.fft.fftshift(f_transform)
        
        # 3. Magnitude Spectrum (Translation Invariant Physics)
        magnitude = np.abs(f_shift)
        
        # 4. Extract invariant core frequencies
        cx, cy = 64, 64
        half_crop = self.crop_size // 2 
        core_frequencies = magnitude[cy-half_crop : cy+half_crop, cx-half_crop : cx+half_crop]
        
        # 5. Flatten and Normalize
        wave = core_frequencies.flatten()
        wave = wave / (np.linalg.norm(wave) + 1e-9)
        
        # 6. Temporal Delta Filter (Predictive Coding)
        if self.last_wave is None:
            self.last_wave = wave
            return wave # First frame always spikes
            
        # Calculate the mathematical prediction error
        delta = np.linalg.norm(wave - self.last_wave)
        
        if delta < self.delta_threshold:
            # The structural wave has not changed (e.g., Apple just moved).
            # Send ZERO energy to the deep brain.
            return None
        else:
            # Structural geometry changed (e.g., Apple smashed, or new object appeared)
            # Update baseline and send the Prediction Error wave to the deep brain
            self.last_wave = wave
            return wave
