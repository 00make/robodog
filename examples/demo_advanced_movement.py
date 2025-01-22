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
    print(f"Posture: roll={dog.roll:.2f}, pitch={
          dog.pitch:.2f}, yaw={dog.yaw:.2f}")


def demo_advanced_movement(dog):
    """Advanced movement demonstration"""
    print("\n===== Advanced Movement Demo =====")

    # Gait parameters
    print("1. Setting gait parameters...")
    dog.set_gait_params(
        friction=0.6,
        scale_x=1.2,
        scale_y=1.0
    )
    dog.foot_height = 0.08
    dog.swing_duration = 0.3
    time.sleep(1)

    # Body posture adjustment
    print("2. Complex movement...")
    dog.body_tilt_x = 0.01
    dog.body_tilt_y = 0.05
    time.sleep(2)

    # Combined movement
    print("3. Forward movement with rotation...")
    dog.vx = 0.2
    dog.wz = 0.2
    time.sleep(2)
    dog.vx = 0.0
    dog.wz = 0.0


if __name__ == '__main__':
    with Dog() as dog:
        try:
            dog.set_user_mode(UserMode.NORMAL)
            demo_advanced_movement(dog)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        finally:
            dog.set_parameters(DEFAULT_POSTURE)
