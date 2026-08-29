"""
ENN 4D Robotics Substrate & Real-World Hardware Abstraction Layer
=================================================================
Enables deploying ENN 4D on physical edge hardware (NVIDIA Jetson, Raspberry Pi, PC)
and controlling physical mobile robots, quadrupeds, and manipulators via ROS / hardware serial.

Components:
1. SensorHardwareAdapter:
   - Ingests raw LiDAR ranges (1D/2D/3D), RGB-D depth frames, IMU orientation, and acoustic microphones.
   - Proposes continuous 4D receptive sensory waves: x_percept = [d_min/d_max, theta_bearing/pi, acoustic_flux, elevation].

2. MotorHardwareAdapter:
   - Decodes ENN 4D action waves into real-world control targets:
     - geometry_msgs/Twist (linear.x, angular.z) for differential & Ackermann ground robots.
     - Multi-channel PWM servo joint angles for robotic limbs and manipulators.

3. ROSBridgeInterface:
   - Plug-and-play ROS 1 / ROS 2 node bridge for real-time robotic pairing.
"""

import numpy as np
import time
from typing import Dict, Any, List, Tuple, Optional


class SensorHardwareAdapter:
    """
    Translates physical sensor streams (LiDAR, RGB-D, IMU, Audio)
    into continuous 4D receptive field sensory waves.
    """
    def __init__(self, max_lidar_range: float = 20.0, num_azimuth_sectors: int = 16):
        self.max_lidar_range = float(max_lidar_range)
        self.num_azimuth_sectors = int(num_azimuth_sectors)
        self.last_imu_accel = np.zeros(3, dtype=np.float32)

    def lidar_to_4d_sensory_wave(
        self,
        ranges: np.ndarray,
        angle_min: float = -np.pi,
        angle_max: float = np.pi,
        sound_pressure: float = 0.0,
        imu_accel: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Converts 1D/2D LiDAR ranges array (e.g., 360 laser points)
        into normalized 4D receptive wave: [min_dist_norm, bearing_norm, acoustic_pressure, spatial_trace].
        """
        ranges = np.array(ranges, dtype=np.float32)
        # Filter NaNs and infs
        valid_mask = np.isfinite(ranges) & (ranges > 0.05) & (ranges < self.max_lidar_range)
        
        if not np.any(valid_mask):
            min_dist = self.max_lidar_range
            bearing = 0.0
        else:
            angles = np.linspace(angle_min, angle_max, len(ranges))
            valid_ranges = ranges[valid_mask]
            valid_angles = angles[valid_mask]
            min_idx = np.argmin(valid_ranges)
            min_dist = float(valid_ranges[min_idx])
            bearing = float(valid_angles[min_idx])

        norm_dist = float(np.clip(min_dist / self.max_lidar_range, 0.0, 1.0))
        norm_bearing = float(np.clip((bearing - angle_min) / (angle_max - angle_min + 1e-5), 0.0, 1.0))
        norm_sound = float(np.clip(sound_pressure / 100.0, 0.0, 1.0))
        
        if imu_accel is not None:
            self.last_imu_accel = np.array(imu_accel, dtype=np.float32)
        norm_accel = float(np.clip(np.linalg.norm(self.last_imu_accel) / 15.0, 0.0, 1.0))

        return np.array([norm_dist, norm_bearing, norm_sound, norm_accel], dtype=np.float32)

    def rgbd_depth_to_depth_matrix(self, depth_image: np.ndarray, target_rows: int = 3, target_cols: int = 16) -> np.ndarray:
        """
        Compresses an RGB-D depth matrix (e.g. 480x640) into a compact (rows, cols) visual ray matrix.
        """
        depth = np.nan_to_num(depth_image, nan=self.max_lidar_range, posinf=self.max_lidar_range)
        h, w = depth.shape[:2]
        row_bins = np.linspace(0, h, target_rows + 1, dtype=int)
        col_bins = np.linspace(0, w, target_cols + 1, dtype=int)
        
        depth_matrix = np.zeros((target_rows, target_cols), dtype=np.float32)
        for r in range(target_rows):
            for c in range(target_cols):
                patch = depth[row_bins[r]:row_bins[r+1], col_bins[c]:col_bins[c+1]]
                depth_matrix[r, c] = float(np.median(patch)) if patch.size > 0 else self.max_lidar_range
                
        return np.clip(depth_matrix, 0.0, self.max_lidar_range)


class MotorHardwareAdapter:
    """
    Decodes ENN 4D action waves into real-world robot control signals:
    1. ROS geometry_msgs/Twist (linear.x, angular.z).
    2. Multi-channel PWM servo angles for multi-joint limbs / robotic arms.
    """
    def __init__(self, max_linear_vel: float = 1.2, max_angular_vel: float = 1.0):
        self.max_linear_vel = float(max_linear_vel)
        self.max_angular_vel = float(max_angular_vel)

    def output_to_ros_twist(self, motor_decision: Dict[str, Any]) -> Dict[str, float]:
        """
        Maps ENN 4D motor dictionary (d_yaw, d_pitch, thrust) to standard ROS Twist format.
        """
        d_yaw = float(motor_decision.get("d_yaw", 0.0))
        thrust = float(motor_decision.get("thrust", 1.0))
        
        linear_x = float(np.clip(thrust * self.max_linear_vel, -self.max_linear_vel, self.max_linear_vel))
        angular_z = float(np.clip(d_yaw * 2.5 * self.max_angular_vel, -self.max_angular_vel, self.max_angular_vel))
        
        return {
            "linear": {"x": round(linear_x, 3), "y": 0.0, "z": 0.0},
            "angular": {"x": 0.0, "y": 0.0, "z": round(angular_z, 3)}
        }

    def output_to_servo_pwm_angles(self, output_wave: np.ndarray, num_servos: int = 6) -> List[float]:
        """
        Decodes continuous 4D wave superposition into standard PWM servo angles (0.0 to 180.0 degrees).
        """
        angles = []
        wave = np.array(output_wave, dtype=np.float32)
        dim = len(wave)
        for i in range(num_servos):
            # Phase-shifted projection across wave dimensions
            weight = float(wave[i % dim])
            angle = float(np.clip((weight + 1.0) * 90.0, 0.0, 180.0))
            angles.append(round(angle, 1))
        return angles


class ROSBridgeInterface:
    """
    Lightweight ROS 1 / ROS 2 Python bridge wrapper.
    Can be imported inside a standard ROS node or run standalone in simulation mode.
    """
    def __init__(self, agent_brain, node_name: str = "enn_4d_robot_controller"):
        self.brain = agent_brain
        self.node_name = node_name
        self.sensor_adapter = SensorHardwareAdapter()
        self.motor_adapter = MotorHardwareAdapter()
        self.is_ros_available = False
        
        try:
            import rospy
            self.is_ros_available = True
            self.ros_version = 1
        except ImportError:
            try:
                import rclpy
                self.is_ros_available = True
                self.ros_version = 2
            except ImportError:
                self.is_ros_available = False
                self.ros_version = 0

    def process_hardware_tick(self, raw_lidar_ranges: np.ndarray, sound_level: float = 0.0) -> Dict[str, Any]:
        """
        Executes one full hardware perception-inference-actuation cycle.
        """
        # 1. Ingest hardware sensory stream
        sensory_4d = self.sensor_adapter.lidar_to_4d_sensory_wave(raw_lidar_ranges, sound_pressure=sound_level)
        
        # 2. Resonate through sparse ENN 4D substrate
        forces = self.brain.world_field.compute_resonance(sensory_4d, sensory_4d, np.zeros(4))
        action_wave = self.brain.world_field.interfere(sensory_4d, forces, sensory_4d)
        
        # 3. Formulate motor command
        motor_dict = {
            "d_yaw": float(action_wave[1] - 0.5) * 0.8,
            "thrust": float(action_wave[0])
        }
        twist = self.motor_adapter.output_to_ros_twist(motor_dict)
        servos = self.motor_adapter.output_to_servo_pwm_angles(action_wave, num_servos=6)
        
        return {
            "sensory_4d": sensory_4d.tolist(),
            "action_wave": action_wave.tolist(),
            "ros_twist": twist,
            "servo_angles_deg": servos,
            "active_neurons": len(self.brain.world_field.neurons)
        }
