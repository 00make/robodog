from robodog import Dog, UserMode
import time

def print_state(dog, title="Current Status"):
    """Print detailed status information"""
    print(f"\n===== {title} =====")
    print(f"User Mode: {dog.ctrl_state.user_mode}")
    print(f"Position: x={dog.x:.2f}, y={dog.y:.2f}, z={dog.z:.2f}")
    print(f"Velocity: vx={dog.vx:.2f}, vy={dog.vy:.2f}")
    print(f"Posture: roll={dog.roll:.2f}, pitch={dog.pitch:.2f}, yaw={dog.yaw:.2f}")

def demo_modes(dog):
    """User modes demonstration"""
    print("\n===== User Mode Demo =====")
    
    modes = [UserMode.QUIET, UserMode.NORMAL, UserMode.KIDS]
    for mode in modes:
        print(f"\nSwitching to {mode.name} mode...")
        dog.set_user_mode(mode)
        time.sleep(2)
        print_state(dog, f"In {mode.name} mode")

if __name__ == '__main__':
    with Dog() as dog:
        try:
            demo_modes(dog)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        finally:
            dog.set_user_mode(UserMode.NORMAL)
