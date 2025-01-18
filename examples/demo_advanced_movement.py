from robodog import Dog, UserMode
from utils import print_state, reset_posture
import time

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
            reset_posture(dog)
