from robodog import Dog, UserMode
import time

# 默认参数
DEFAULT_POSTURE = {
    'body_height': 0.23,
    'roll': 0.0,
    'pitch': 0.0,
    'yaw': 0.0,
    'vx': 0.0,
    'vy': 0.0,
    'wz': 0.0
}

def print_state(dog, title="Current Status"):
    """Print detailed status information"""
    print(f"\n===== {title} =====")
    print(f"User Mode: {dog.ctrl_state.user_mode}")
    print(f"Position: x={dog.x:.2f}, y={dog.y:.2f}, z={dog.z:.2f}")
    print(f"Velocity: vx={dog.vx:.2f}, vy={dog.vy:.2f}")
    print(f"Posture: roll={dog.roll:.2f}, pitch={dog.pitch:.2f}, yaw={dog.yaw:.2f}")

def demo_basic_movement(dog):
    """Basic movement demonstration"""
    print("\n===== Basic Movement Demo =====")

    # Height adjustment
    print("1. Adjusting height...")
    dog.body_height = 0.25
    time.sleep(2)
    print_state(dog, "After height adjustment")

    # Forward and backward movement
    print("\n2. Testing forward/backward movement...")
    for speed in [0.1, -0.1, 0.0]:
        dog.vx = speed
        print(f"Setting forward speed to {speed}")
        time.sleep(2)
    print_state(dog, "After movement test")

    # Body tilt demonstration
    print("\n3. Testing body tilt...")
    dog.roll = 0.2
    time.sleep(1)
    dog.pitch = 0.2
    time.sleep(2)
    print_state(dog, "After tilt test")

if __name__ == '__main__':
    with Dog() as dog:
        try:
            dog.set_user_mode(UserMode.NORMAL)
            demo_basic_movement(dog)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        finally:
            # Reset to default posture
            dog.set_parameters(DEFAULT_POSTURE)
