"""
ENN 4D Scalability & Sparse Substrate Benchmark Suite
=====================================================
Benchmarks:
1. Dense O(N^2) vs. Sparse k-NN O(k log N) Resonance Speed across 1,000 to 50,000 neurons.
2. Synaptic Pruning and Memory Consumption bounds.
3. Hardware Robotics Sensor-Actuator Loop Frequency (Hz).
"""

import time
import numpy as np
from enn4d import ENN4D, Neuron, DualFieldENN
from robotics_substrate import SensorHardwareAdapter, MotorHardwareAdapter, ROSBridgeInterface


def benchmark_sparse_resonance():
    print("=" * 80)
    print("🧠 1. ENN 4D SPARSE k-NN RESONANCE BENCHMARK")
    print("=" * 80)
    
    neuron_counts = [500, 1000, 2500, 5000, 10000, 25000, 50000]
    
    for n_count in neuron_counts:
        brain = ENN4D(dim=4)
        # Synthesize population of neurons
        for i in range(n_count):
            x = np.random.uniform(-1.0, 1.0, 4)
            y = np.random.uniform(-1.0, 1.0, 4)
            z = np.zeros(4)
            n = Neuron(x, y, z, w=i % 16, text=f"Concept_{i}")
            brain.neurons.append(n)
        
        brain._is_buffer_dirty = True
        brain._sync_buffers()
        
        # Test Query
        test_x = np.array([0.25, -0.4, 0.8, 0.1], dtype=np.float32)
        test_y = np.array([0.1, 0.2, -0.3, 0.5], dtype=np.float32)
        test_z = np.zeros(4, dtype=np.float32)
        
        # Measure 1,000 resonance queries
        num_queries = 1000
        t0 = time.perf_counter()
        for _ in range(num_queries):
            forces = brain.compute_resonance(test_x, test_y, test_z, top_k=32)
        t_elapsed = time.perf_counter() - t0
        
        time_per_query_us = (t_elapsed / num_queries) * 1e6
        hz = num_queries / t_elapsed
        
        print(f"  • {n_count:>6,} Neurons: {time_per_query_us:6.2f} µs/query | Frequency: {hz:8,.0f} Hz (Sparse k-NN)")


def benchmark_synaptic_pruning():
    print("\n" + "=" * 80)
    print("✂️ 2. SYNAPTIC CONDUCTANCE PRUNING & MEMORY BOUND BENCHMARK")
    print("=" * 80)
    
    brain = ENN4D(dim=4)
    # Populate 1,000 neurons with random dense connections
    for i in range(1000):
        n = Neuron(np.random.randn(4), np.random.randn(4), np.zeros(4), w=i % 8)
        # Create many weak connections and a few strong ones
        for j in range(min(50, 1000)):
            if i != j:
                w = np.random.uniform(0.01, 0.80)
                n.synapses[j] = float(w)
        brain.neurons.append(n)
        
    total_synapses_before = sum(len(n.synapses) for n in brain.neurons)
    print(f"  • Total Synaptic Bridges Before Pruning: {total_synapses_before:,}")
    
    pruned = brain.prune_synapses(min_weight=0.05, max_synapses=16)
    total_synapses_after = sum(len(n.synapses) for n in brain.neurons)
    
    print(f"  • Pruned Conductance Channels:           {pruned:,} connections dissolved")
    print(f"  • Total Active Synaptic Bridges After:  {total_synapses_after:,} (Bounded <= 16/neuron)")
    print(f"  • Memory Reduction:                     {(1.0 - total_synapses_after/total_synapses_before)*100:.1f}% saved")


def benchmark_robotics_loop():
    print("\n" + "=" * 80)
    print("🤖 3. REAL-WORLD ROBOTICS HARDWARE CONTROL LOOP BENCHMARK")
    print("=" * 80)
    
    substrate = DualFieldENN()
    bridge = ROSBridgeInterface(agent_brain=substrate)
    
    # 360-degree simulated physical LiDAR scan
    raw_lidar = np.random.uniform(0.5, 15.0, 360).astype(np.float32)
    raw_lidar[45:55] = 0.8  # Obstacle at 45 degrees
    
    # Run 1,000 real-time control ticks
    num_ticks = 1000
    t0 = time.perf_counter()
    for _ in range(num_ticks):
        res = bridge.process_hardware_tick(raw_lidar, sound_level=12.5)
    t_elapsed = time.perf_counter() - t0
    
    hz = num_ticks / t_elapsed
    print(f"  • Physical Hardware Loop Rate: {hz:,.1f} Hz (Target: >60 Hz for ROS)")
    print(f"  • Sample ROS Twist Output:     linear.x = {res['ros_twist']['linear']['x']} m/s, angular.z = {res['ros_twist']['angular']['z']} rad/s")
    print(f"  • Sample Servo Joint Angles:   {res['servo_angles_deg']} degrees")
    print("=" * 80)


if __name__ == "__main__":
    benchmark_sparse_resonance()
    benchmark_synaptic_pruning()
    benchmark_robotics_loop()
