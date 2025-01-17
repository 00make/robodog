from robodog import Dog
import time
from robodog.config import UserMode

def print_state(dog):
    """Print current status information"""
    print("\nCurrent Status:")
    print(f"User Mode: {dog.ctrl_state.user_mode}")
    print(f"Body Height: {dog.body_status.z:.2f}")
    print(f"Posture: roll={dog.body_status.roll:.2f}, "
          f"pitch={dog.body_status.pitch:.2f}, "
          f"yaw={dog.body_status.yaw:.2f}")

def main():
    with Dog() as dog:
        try:
            # Wait for initialization
            print("Waiting for system initialization...")
            time.sleep(1)
            
            # Switch to normal mode
            print("Switching to normal mode...")
            dog.set_user_mode(UserMode.NORMAL)
            time.sleep(1)
            
            # Basic posture adjustment demo
            print("\n===== Basic Posture Adjustment Demo =====")
            print("1. Adjusting standing height...")
            dog.set_parameters({'body_height': 0.25})
            time.sleep(2)
            print_state(dog)
            
            print("\n2. Tilting body...")
            dog.set_parameters({
                'roll': 0.1,
                'pitch': 0.05
            })
            time.sleep(2)
            print_state(dog)
            
            print("\n3. Restoring default posture...")
            dog.set_parameters({
                'body_height': 0.23,
                'roll': 0.0,
                'pitch': 0.0
            })
            time.sleep(2)
            print_state(dog)
            
            # Demonstrate different user modes
            print("\n===== User Mode Switching Demo =====")
            modes = [UserMode.QUIET, UserMode.KIDS, UserMode.NORMAL]
            for mode in modes:
                print(f"\nSwitching to {mode.name} mode...")
                dog.set_user_mode(mode)
                time.sleep(2)
                print_state(dog)
                
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        except Exception as e:
            print(f"\nError occurred: {e}")
        finally:
            # Ensure default state is restored
            dog.set_parameters({
                'body_height': 0.23,
                'roll': 0.0,
                'pitch': 0.0
            })
            dog.set_user_mode(UserMode.NORMAL)

if __name__ == '__main__':
    main()