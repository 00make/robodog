from robodog import Dog, UserMode
from utils import print_state, reset_posture
import time

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
            reset_posture(dog)
