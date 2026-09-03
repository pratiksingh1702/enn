import numpy as np
import scipy.io.wavfile as wav

class AcousticCortex:
    def __init__(self, target_dim=256):
        """
        Phase 2: The Acoustic Cortex.
        Takes raw .wav physical audio and collapses it into a 256D 
        invariant structural frequency wave using 1D-FFT.
        """
        self.target_dim = target_dim

    def process_audio(self, audio_path: str) -> np.ndarray:
        # 1. Read the raw physical sound wave
        rate, data = wav.read(audio_path)
        
        # 2. Convert to mono if it's stereo
        if len(data.shape) > 1:
            data = data.mean(axis=1)
            
        # 3. Apply 1D Fast Fourier Transform to extract frequency signature
        f_transform = np.fft.fft(data)
        magnitude = np.abs(f_transform)
        
        # 4. Extract the primary invariant acoustic frequencies (skip DC offset at 0)
        # We need exactly 256 structural nodes to match the matrix dimension
        if len(magnitude) < self.target_dim + 1:
            pad = np.zeros(self.target_dim + 1 - len(magnitude))
            magnitude = np.concatenate([magnitude, pad])
            
        core_frequencies = magnitude[1:self.target_dim + 1]
        
        # 5. Thermodynamic Normalization (L2 Norm to match brain topology)
        wave = core_frequencies / (np.linalg.norm(core_frequencies) + 1e-9)
        return wave
