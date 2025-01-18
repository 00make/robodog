from robodog import Dog
import time

# 默认参数常量
DEFAULT_POSTURE = {
    'body_height': 0.23,
    'body_tilt_x': 0.0,
    'body_tilt_y': 0.0,
    'roll': 0.0,
    'pitch': 0.0,
    'yaw': 0.0,
    'vx': 0.0,
    'vy': 0.0,
    'wz': 0.0,
    'foot_height': 0.05,
    'swing_duration': 0.21,
    'friction': 0.4,
    'scale_x': 1.0,
    'scale_y': 1.0
}

def print_state(dog, title="Current Status"):
    """Print detailed status information"""
    try:
        print(f"\n===== {title} =====")
        print(f"User Mode: {dog.ctrl_state.user_mode}")
        print(f"Position: x={dog.x:.2f}, y={dog.y:.2f}, z={dog.z:.2f}")
        print(f"Velocity: vx={dog.vx:.2f}, vy={dog.vy:.2f}")
        print(f"Posture: roll={dog.roll:.2f}, pitch={dog.pitch:.2f}, yaw={dog.yaw:.2f}")
    except RuntimeError as e:
        print(f"Warning: Could not get complete state - {e}")

def reset_posture(dog):
    """Reset dog to default posture"""
    print("\nResetting to default posture...")
    dog.set_parameters(DEFAULT_POSTURE)
    time.sleep(1)
