from robodog import Dog
import time
from robodog.config import UserMode


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


def demo_advanced_movement(dog):
    """展示高级运动控制"""
    print("\n===== Advanced Movement Demo =====")

    # 1. 调整步态参数
    print("1. 设置步态参数...")
    dog.foot_height = 0.08  # 设置抬脚高度
    dog.swing_duration = 0.3  # 设置摆动周期
    dog.set_gait_params(friction=0.6, scale_x=1.2, scale_y=1.0)
    time.sleep(1)

    # 2. 身体姿态调整
    print("2. 调整身体位置...")
    dog.body_tilt_x = 0.01  # 身体前倾
    dog.body_tilt_y = 0.05  # 身体偏左
    time.sleep(2)

    # 3. 复合运动展示
    print("3. 展示复合运动...")
    dog.vx = 0.2  # 向前走
    dog.wz = 0.2  # 同时转向
    time.sleep(2)
    dog.vx = 0.0
    dog.wz = 0.0

    # 4. 设置运动参数
    print("4. 设置高级运动参数...")
    dog.set_motion_params(
        swaying_duration=2.0,  # 摇摆周期
        jump_distance=0.3,     # 跳跃距离
        jump_angle=0.1         # 跳跃旋转角度
    )

    # # 5. 设置控制参数
    # print("5. 设置控制参数...")
    # dog.set_control_params(
    #     velocity_decay=0.8,      # 速度衰减
    #     collision_protect=1,      # 开启碰撞保护
    #     decelerate_time=2.0,     # 减速延迟
    #     decelerate_duration=1.0  # 减速时间
    # )


def demo_all_params(dog):
    """展示所有参数的设置"""
    print("\n===== All Parameters Demo =====")

    # 1. 基本运动参数
    print("1. 设置基本运动参数...")
    dog.vx = 0.2            # 前进速度
    dog.vy = 0.1           # 左移速度
    dog.wz = 0.1           # 旋转速度
    time.sleep(2)
    dog.vx = 0.0
    dog.vy = 0.0
    dog.wz = 0.0

    # 2. 姿态参数
    print("2. 设置姿态参数...")
    dog.roll = 0.1         # 横滚角
    dog.pitch = 0.1        # 俯仰角
    dog.yaw = 0.1          # 偏航角
    dog.body_height = 0.25  # 身体高度
    time.sleep(1)

    # 3. 身体偏移
    print("3. 设置身体偏移...")
    dog.body_tilt_x = 0.05  # 前后偏移
    dog.body_tilt_y = 0.05  # 左右偏移
    time.sleep(1)

    # 4. 步态参数
    print("4. 设置步态参数...")
    dog.foot_height = 0.08    # 抬脚高度
    dog.swing_duration = 0.3   # 摆动周期
    dog.friction = 0.6        # 摩擦系数
    dog.scale_x = 1.2         # 支撑面X缩放
    dog.scale_y = 1.0         # 支撑面Y缩放
    time.sleep(1)

    # 5. 特殊动作参数
    print("5. 设置特殊动作参数...")
    dog.swaying_duration = 2.0  # 摇摆周期
    dog.jump_distance = 0.3     # 跳跃距离
    dog.jump_angle = 0.1        # 跳跃角度
    time.sleep(1)

    # 6. 控制参数
    print("6. 设置控制参数...")
    dog.velocity_decay = 0.8       # 速度衰减
    dog.collision_protect = 1       # 开启碰撞保护
    dog.decelerate_time = 2.0      # 减速延迟
    dog.decelerate_duration = 1.0   # 减速持续时间

    # 7. 自由腿设置
    print("7. 设置自由腿...")
    dog.free_leg = 1               # 设置自由腿序号

    print_state(dog, "After all parameter settings")

    # 恢复默认状态
    reset_posture(dog)


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
            # Initial setup - 给更多时间初始化
            print("Initializing system...")
            time.sleep(1)
            dog.set_user_mode(UserMode.NORMAL)
            time.sleep(1)
            print_state(dog, "Initial State")

            # Run demos
            demo_movement(dog)
            demo_advanced_movement(dog)
            demo_all_params(dog)
            demo_modes(dog)

        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
        finally:
            # Cleanup with all parameters reset
            dog.set_parameters({
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
            })
            dog.set_user_mode(UserMode.NORMAL)


if __name__ == '__main__':
    main()
