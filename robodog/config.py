from enum import IntEnum

class UserMode(IntEnum):
    """User mode enumeration"""
    EXTREME = 1
    KIDS = 2
    NORMAL = 3
    DANCE = 4
    QUIET = 5
    MUTE = 6
    LONG_ENDURANCE = 7

DEFAULT_PARAMS = {
    # Double parameters
    'vx': 0.0,
    'vy': 0.0,
    'wz': 0.0,
    'roll': 0.0,
    'pitch': 0.0,
    'yaw': 0.0,
    'body_tilt_x': 0.0,
    'body_tilt_y': 0.0,
    'body_height': 0.23,
    'foot_height': 0.05,
    'swing_duration': 0.21,
    'friction': 0.4,
    'scale_x': 1.0,
    'scale_y': 1.0,
    'swaying_duration': 2.0,
    'jump_distance': 0.5,
    'jump_angle': 0.0,
    'decelerate_time': 1.0,
    'decelerate_duration': 1.0,
    'velocity_decay': 1.0,
    # Integer parameters
    'free_leg': 1,
    'collision_protect': 1,
    'controller_type': 2,
    'user_mode': 3,
    'gait': 10,
    'swing_traj_type': 1,
    'ground_model': 3,
    'action_0': 514,
    'action_1': 516,
    'action_2': 257,
    'action_3': 273
}
