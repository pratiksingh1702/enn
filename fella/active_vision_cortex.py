import cv2
import numpy as np

class ActiveVisionCortex:
    def __init__(self, target_dim=256, curiosity_threshold=10.0):
        """
        The Biological Eye (Bottom-Up Active Vision).
        Processes the environment using a Low-Energy Trace, creates a Curiosity Heatmap,
        and uses a Magnetic Saccade to focus heavy math ONLY on anomalies.
        """
        self.target_dim = target_dim
        self.crop_size = int(np.sqrt(target_dim))
        self.curiosity_threshold = curiosity_threshold
        self.last_trace = None

    def process_frame(self, frame: np.ndarray):
        """
        Takes a high-res raw frame (e.g., 1920x1080).
        Returns a 256D wave and the (x, y) coordinates of the focus window,
        OR returns None if the environment is boring.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        
        # 1. THE LOW-ENERGY TRACE (Cost: Near Zero)
        # Downsample the entire 1080p frame to a tiny 32x32 trace
        trace = cv2.resize(gray, (32, 32))
        
        if self.last_trace is None:
            self.last_trace = trace
            return None # Need a baseline to compare against
            
        # 2. THE CURIOSITY HEATMAP
        # Find exactly where the mathematical entropy (movement/anomaly) is happening
        heatmap = cv2.absdiff(trace, self.last_trace)
        self.last_trace = trace
        
        # Locate the coordinate of maximum entropy in the trace
        _, max_val, _, max_loc = cv2.minMaxLoc(heatmap)
        
        # 3. THE BOREDOM OPTIMIZER
        if max_val < self.curiosity_threshold:
            # Nothing interesting is happening. Trace is static. 
            # Send zero energy to the deep brain.
            return None
            
        # 4. THE MAGNETIC SACCADE (Focus Shift)
        # Map the tiny 32x32 coordinate back to the original high-resolution frame
        h, w = gray.shape
        scale_x = w / 32.0
        scale_y = h / 32.0
        center_x = int(max_loc[0] * scale_x)
        center_y = int(max_loc[1] * scale_y)
        
        # 5. THE DEEP FOCUS WINDOW (128x128 Bounding Box)
        half_box = 64
        x1 = max(0, center_x - half_box)
        y1 = max(0, center_y - half_box)
        x2 = min(w, center_x + half_box)
        y2 = min(h, center_y + half_box)
        
        focus_crop = gray[y1:y2, x1:x2]
        
        # Handle edge collisions by scaling to perfect 128x128
        if focus_crop.shape != (128, 128):
            focus_crop = cv2.resize(focus_crop, (128, 128))
            
        # 6. THE HEAVY PROCESSING (256D Phase Signature)
        # We now run the massive 2D-FFT physics calculation ONLY on this small 128x128 box,
        # completely ignoring the other 2 million pixels in the background trace.
        f_transform = np.fft.fft2(focus_crop)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        
        cx, cy = 64, 64
        half_freq = self.crop_size // 2 
        core_frequencies = magnitude[cy-half_freq : cy+half_freq, cx-half_freq : cx+half_freq]
        
        wave = core_frequencies.flatten()
        wave = wave / (np.linalg.norm(wave) + 1e-9)
        
        return wave, (center_x, center_y)
