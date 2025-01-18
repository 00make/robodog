from robodog import Dog, UserMode
from utils import print_state, reset_posture
from demo_basic_movement import demo_basic_movement
from demo_advanced_movement import demo_advanced_movement
from demo_modes import demo_modes
import time

def main():
    with Dog() as dog:
        try:
            # Initial setup
            print("Initializing system...")
            dog.set_user_mode(UserMode.NORMAL)
            time.sleep(1)
            print_state(dog, "Initial State")

            # Run all demos
            demo_basic_movement(dog)
            demo_advanced_movement(dog)
            demo_modes(dog)

        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
        finally:
            reset_posture(dog)
            dog.set_user_mode(UserMode.NORMAL)

if __name__ == '__main__':
    main()
