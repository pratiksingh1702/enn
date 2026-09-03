import numpy as np
import cv2

class VisualCortex:
    def __init__(self, target_dim=256):
        """
        Phase 1: The Static Visual Cortex.
        Takes physical 2D image arrays and mathematically collapses them into 
        invariant structural frequency waves using 2D-FFT.
        """
        self.target_dim = target_dim
        # We need a perfect square crop from the center of the frequency domain
        self.crop_size = int(np.sqrt(target_dim))
        assert self.crop_size * self.crop_size == target_dim, "Target dim must be a perfect square."

    def process_image(self, image_path: str) -> np.ndarray:
        # 1. Read and strip color noise (focus on raw structural geometry/luminance)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")
        
        # 2. Standardize spatial domain (scale invariance baseline)
        img_resized = cv2.resize(img, (128, 128))
        
        # 3. 2D Fast Fourier Transform (Extract raw structural frequencies, NO neural networks)
        f_transform = np.fft.fft2(img_resized)
        f_shift = np.fft.fftshift(f_transform)
        
        # 4. Magnitude Spectrum (Discard phase to achieve translation invariance)
        # An apple shifted 10 pixels to the left has the same magnitude spectrum.
        magnitude = np.abs(f_shift)
        
        # 5. Extract the invariant core (low/mid frequencies at the center)
        # Center of 128x128 is 64,64
        cx, cy = 64, 64
        half_crop = self.crop_size // 2 
        
        core_frequencies = magnitude[cy-half_crop : cy+half_crop, cx-half_crop : cx+half_crop]
        
        # 6. Flatten to a 1D wave tensor
        wave = core_frequencies.flatten()
        
        # 7. Thermodynamic Normalization (L2 Norm to match brain topology)
        wave = wave / (np.linalg.norm(wave) + 1e-9)
        
        return wave
