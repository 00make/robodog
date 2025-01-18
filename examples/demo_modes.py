from robodog import Dog, UserMode
from utils import print_state, reset_posture
import time

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
