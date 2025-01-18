from robodog import Dog
import time
from robodog.config import UserMode


def print_state(dog, title="Current Status"):
    """Print detailed status information"""
    print(f"\n===== {title} =====")
    print(f"User Mode: {dog.ctrl_state.user_mode}")
    print(f"Position: x={dog.x:.2f}, y={dog.y:.2f}, z={dog.z:.2f}")
    print(f"Velocity: vx={dog.vx:.2f}, vy={dog.vy:.2f}")
    print(f"Posture: roll={dog.roll:.2f}, pitch={
          dog.pitch:.2f}, yaw={dog.yaw:.2f}")


def reset_posture(dog):
    """Reset dog to default posture"""
    print("\nResetting to default posture...")
    dog.set_parameters({
        'body_height': 0.23,
        'roll': 0.0,
        'pitch': 0.0,
        'yaw': 0.0,
        'vx': 0.0,
        'vy': 0.0
    })
    time.sleep(1)


def demo_movement(dog):
    """Demonstrate basic movement capabilities"""
    print("\n===== Movement Demo =====")

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


def demo_modes(dog):
    """Demonstrate different user modes"""
    print("\n===== User Mode Demo =====")
    for mode in [UserMode.QUIET, UserMode.NORMAL]:
        print(f"\nSwitching to {mode.name} mode...")
        dog.set_user_mode(mode)
        time.sleep(2)
        print_state(dog, f"In {mode.name} mode")


def main():
    with Dog() as dog:
        try:
            # Initial setup
            print("Initializing system...")
            time.sleep(1)
            dog.set_user_mode(UserMode.NORMAL)
            print_state(dog, "Initial State")

            # Run demos
            demo_movement(dog)
            demo_modes(dog)

        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
        finally:
            # Cleanup
            reset_posture(dog)
            dog.set_user_mode(UserMode.NORMAL)
            print_state(dog, "Final State")


if __name__ == '__main__':
    main()
