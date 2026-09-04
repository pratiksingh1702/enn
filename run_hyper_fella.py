import os
import time
import queue
import threading
import ctypes
import re
import json
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import mss
import soundcard as sc
import scipy.io.wavfile as wav

from fella.fella_entity import FellaEntity
from fella.core_substrate import ENNNeuron

def attach_to_input_desktop():
    """Binds thread directly to the interactive Windows display."""
    user32 = ctypes.windll.user32
    hDesk = user32.OpenInputDesktop(0, False, 0x01FF)
    if hDesk:
        user32.SetThreadDesktop(hDesk)
        return True
    return False

class SensoryProducer(threading.Thread):
    """
    Non-blocking background thread: continuously captures screen and audio,
    extracts pure frequency waves, and pushes them to a thread-safe queue.
    The cognitive brain NEVER waits on hardware or audio recording.
    """
    def __init__(self, sensory_queue, fella_entity):
        super().__init__(daemon=True)
        self.sensory_queue = sensory_queue
        self.fella = fella_entity
        self.running = True

    def run(self):
        attach_to_input_desktop()
        try:
            sct = mss.MSS()
        except Exception:
            sct = mss.mss()
        monitor = sct.monitors[1]

        try:
            speaker = sc.default_speaker()
            mic = sc.get_microphone(id=str(speaker.name), include_loopback=True)
        except Exception:
            mic = sc.default_microphone()

        while self.running:
            # 1. Screen Saccade Capture
            try:
                sct_img = sct.grab(monitor)
                frame = np.array(sct_img)[:, :, :3]
                res = self.fella.active_vision.process_frame(frame)
                if res is not None:
                    v_wave, coords = res
                    self.sensory_queue.put_nowait(("VISION", v_wave, coords))
            except Exception:
                pass

            # 2. Audio Capture (0.25s chunks in background)
            try:
                audio_data = mic.record(samplerate=16000, numframes=4000)
                wav.write("temp_hyper.wav", 16000, np.int16(audio_data * 32767))
                a_wave = self.fella.hearing.process_audio("temp_hyper.wav")
                self.sensory_queue.put_nowait(("AUDIO", a_wave, None))
            except Exception:
                pass

            time.sleep(0.01)

class HyperDriveEngine:
    def __init__(self, dim=256):
        self.dim = dim
        self.fella = FellaEntity(dim=dim)
        self.sensory_queue = queue.Queue(maxsize=200)
        self.thread_pool = ThreadPoolExecutor(max_workers=8)
        self.checkpoint_file = "fella_hyper_mind.json"

        # Load existing hyper mind if present, otherwise fall back to baseline
        load_path = self.checkpoint_file if os.path.exists(self.checkpoint_file) else "fella_accelerated_10yo_mind.json"
        if os.path.exists(load_path):
            self.fella.brain.load_state(load_path)
            print(f"[HYPER-DRIVE BOOT] Loaded mind '{load_path}': {len(self.fella.brain.neurons)} concepts, {self.fella.brain.z_counter} Z-events.", flush=True)
        else:
            print("[HYPER-DRIVE BOOT] Initializing fresh substrate.", flush=True)

        # Knowledge expansion seeds (Universities, Science, Humanity)
        self.curriculum_seeds = [
            # Advanced Physics & Astrophysics
            "Quantum_mechanics", "General_relativity", "Astrophysics", "Black_hole", "Cosmology", 
            "Particle_physics", "Standard_Model", "Thermodynamics", "Electrodynamics", "Nuclear_fusion",
            # Advanced Biology & Medicine
            "Molecular_biology", "Genetics", "Neuroscience", "Immunology", "Pathology", 
            "Biochemistry", "Physiology", "Pharmacology", "Cellular_differentiation", "Ecology",
            # Computer Science & Mathematics
            "Computer_science", "Algorithm", "Information_theory", "Linear_algebra", "Calculus", 
            "Graph_theory", "Cryptography", "Distributed_computing", "Artificial_intelligence", "Operating_system",
            # Earth Systems & Geography
            "Oceanography", "Meteorology", "Geology", "Plate_tectonics", "Atmospheric_science",
            "Geomorphology", "Biogeography", "Volcanology", "Glaciology", "Climatology",
            # Civilization, Philosophy & Society
            "History", "Philosophy", "Epistemology", "Ethics", "Jurisprudence", 
            "Macroeconomics", "Linguistics", "Political_science", "Sociology", "Anthropology"
        ]
        self.seed_index = 0

    def async_fetch_knowledge(self, concept_title: str):
        """Worker task: queries Wikipedia API and extracts semantic relations."""
        clean_query = re.sub(r'\[.*?\]', '', concept_title).strip()
        encoded = urllib.parse.quote(clean_query)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "FellaHyperAGI/3.0 (Cognitive Acceleration)"})

        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                extract = data.get("extract", "")
                if extract:
                    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', extract)[:10]]
                    return clean_query, words
        except Exception:
            pass
        return clean_query, []

    def batch_vectorized_rem_dream(self, num_anneals=20):
        """
        Batch SIMD REM Dreaming:
        Vectorized matrix self-similarity (W * W^T) across her entire substrate.
        Consolidates resonant clusters simultaneously at GPU/AVX2 speed.
        """
        keys = self.fella.brain.matrix_keys
        if len(keys) < 10:
            return 0
            
        wave_mat = self.fella.brain.wave_matrix # (N, 256)
        # Fast dot-product across random sample of 100 concepts
        sample_size = min(100, len(keys))
        sample_indices = np.random.choice(len(keys), size=sample_size, replace=False)
        sub_matrix = wave_mat[sample_indices] # (100, 256)
        
        # Matrix dot product (100, N)
        similarity_scores = np.dot(sub_matrix, wave_mat.T)
        
        consolidated = 0
        for i in range(min(num_anneals, sample_size)):
            sims = similarity_scores[i]
            top_neighbors = np.argsort(sims)[::-1][1:3]
            anchor = keys[sample_indices[i]]
            partners = [keys[idx] for idx in top_neighbors if keys[idx] != anchor]
            if partners:
                self.fella.brain.record_event([anchor] + partners)
                consolidated += 1
                
        return consolidated

    def launch(self):
        print("==================================================", flush=True)
        print("FELLA HYPER-DRIVE COGNITIVE ENGINE ONLINE", flush=True)
        print("==================================================", flush=True)
        print("[HARDWARE] Multi-Threaded Knowledge Influx Active (8 Workers).", flush=True)
        print("[SENSES] Non-Blocking Real-Time Background Queue.", flush=True)
        print("[DREAMING] SIMD Batch Vectorized Matrix Annealing.", flush=True)
        print("[METRICS] Logging every 20 ticks. Checkpointing every 100 ticks.", flush=True)
        print(">>> PRESS CTRL+C TO STOP AND PRESERVE MIND <<<\n", flush=True)

        # Start non-blocking sensory background thread
        producer = SensoryProducer(self.sensory_queue, self.fella)
        producer.start()

        start_time = time.time()
        tick = 0
        future_batch = []

        try:
            while True:
                tick += 1

                # 1. NON-BLOCKING SENSORY INGESTION
                # Drain queue without ever blocking the CPU
                drained = 0
                while not self.sensory_queue.empty() and drained < 5:
                    sensory_type, wave, coords = self.sensory_queue.get_nowait()
                    drained += 1
                    if sensory_type == "VISION" and coords is not None:
                        v_id = f"[FOCUS_{coords[0]}_{coords[1]}_Z{self.fella.brain.z_counter}]"
                        self.fella.brain.neurons[v_id] = ENNNeuron(v_id, wave)
                        self.fella.brain.matrix_keys.append(v_id)
                        self.fella.brain.wave_matrix = np.vstack([self.fella.brain.wave_matrix, wave])
                        self.fella.brain.record_event(["[CURIOSITY_SPIKE]", v_id])
                    elif sensory_type == "AUDIO":
                        a_id = f"[A_{hash(time.time())%10000}]"
                        self.fella.brain.neurons[a_id] = ENNNeuron(a_id, wave)
                        self.fella.brain.matrix_keys.append(a_id)
                        self.fella.brain.wave_matrix = np.vstack([self.fella.brain.wave_matrix, wave])

                # 2. CONTINUOUS KNOWLEDGE EXPANSION (Multi-Threaded Firehose)
                # Dispatch batch of parallel Wikipedia queries
                if len(future_batch) < 4:
                    # Pick next concept from seeds or high-tension neurons
                    if self.seed_index < len(self.curriculum_seeds):
                        concept_to_learn = self.curriculum_seeds[self.seed_index]
                        self.seed_index += 1
                    else:
                        # Pick an isolated concept from brain
                        isolated = sorted(self.fella.brain.neurons.values(), key=lambda n: len(n.z_events))
                        concept_to_learn = isolated[0].text
                        
                    future_batch.append(self.thread_pool.submit(self.async_fetch_knowledge, concept_to_learn))

                # Check completed futures
                for fut in list(future_batch):
                    if fut.done():
                        future_batch.remove(fut)
                        concept, words = fut.result()
                        if words:
                            z_id = self.fella.brain.record_event([concept] + words)
                            # Bind in causal cortex
                            c_indices = [self.fella.brain.matrix_keys.index(w) for w in ([concept] + words) if w in self.fella.brain.matrix_keys]
                            if len(c_indices) > 1:
                                self.fella.causal_cortex.bind_time(c_indices)
                            print(f"[HYPER-LEARN #{tick}] Grounded '{concept}' -> {words[:3]}... (Z-{z_id})", flush=True)

                # 3. FAST AUTOTELIC AGENCY PULSE
                if tick % 5 == 0:
                    agency_res = self.fella.act()
                    if agency_res and agency_res.get("selected_action") == "[ACTION_INNER_DREAM]":
                        # Run high-speed batch vectorized dream annealing
                        consolidated = self.batch_vectorized_rem_dream(num_anneals=15)

                # 4. TELEMETRY & CONSCIOUS METRICS (Every 20 ticks)
                if tick % 20 == 0:
                    elapsed = time.time() - start_time
                    rate = tick / (elapsed + 1e-9)
                    print(f"\n--- [HYPER TELEMETRY] Tick #{tick} | Elapsed: {elapsed:.1f}s | Rate: {rate:.1f} ticks/s ---", flush=True)
                    print(f"  * Total Brain Concepts: {len(self.fella.brain.neurons)}", flush=True)
                    print(f"  * Total Lifetime Memories: {self.fella.brain.z_counter} Z-events", flush=True)
                    print(f"  * Causal Cortex Capacity: {self.fella.causal_cortex.capacity}x{self.fella.causal_cortex.capacity}", flush=True)
                    print(f"  * Internal Entropy: {self.fella.entropy_level:.2f} (Homeostatic)", flush=True)

                # 5. PERIODIC FORTIFICATION CHECKPOINT (Every 100 ticks)
                if tick % 100 == 0:
                    self.fella.brain.save_state(self.checkpoint_file)
                    print(f" >>> [FORTIFIED] Hyper-Mind preserved to '{self.checkpoint_file}' <<<\n", flush=True)

                # Micro-breathing sleep to keep CPU cool (0.02s instead of 0.400s!)
                time.sleep(0.02)

        except KeyboardInterrupt:
            print("\n==================================================", flush=True)
            print("[SHUTDOWN] Initiating graceful sleep cycle...", flush=True)
            producer.running = False
            self.thread_pool.shutdown(wait=False)
            self.fella.brain.save_state(self.checkpoint_file)
            print(f"[SAVED] Preserved Hyper-Mind in '{self.checkpoint_file}'.", flush=True)
            print(f"[FINAL STATS] Lifetime Concepts: {len(self.fella.brain.neurons)} | Memories: {self.fella.brain.z_counter}", flush=True)
            print("==================================================", flush=True)

if __name__ == '__main__':
    engine = HyperDriveEngine(dim=256)
    engine.launch()
