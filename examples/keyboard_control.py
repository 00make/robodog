from robodog import Dog, UserMode
from pynput import keyboard
import time
import os
import threading

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

# 速度参数
SPEED_INCREMENT = 0.1
MAX_SPEED = 0.5
MIN_SPEED = -0.5

# 机器狗状态
dog_state = {
    'vx': 0.0,  # 前进/后退速度
    'vy': 0.0,  # 左右速度
    'wz': 0.0,  # 旋转速度
    'body_height': 0.23,  # 身体高度
    'running': True  # 程序运行状态
}

# 按键映射
key_mapping = {
    # 前进/后退控制
    'w': {'param': 'vx', 'change': SPEED_INCREMENT, 'description': '前进'},
    's': {'param': 'vx', 'change': -SPEED_INCREMENT, 'description': '后退'},
    keyboard.Key.up: {'param': 'vx', 'change': SPEED_INCREMENT, 'description': '前进'},
    keyboard.Key.down: {'param': 'vx', 'change': -SPEED_INCREMENT, 'description': '后退'},
    
    # 左右移动控制
    'a': {'param': 'vy', 'change': SPEED_INCREMENT, 'description': '左移'},
    'd': {'param': 'vy', 'change': -SPEED_INCREMENT, 'description': '右移'},
    keyboard.Key.left: {'param': 'vy', 'change': SPEED_INCREMENT, 'description': '左移'},
    keyboard.Key.right: {'param': 'vy', 'change': -SPEED_INCREMENT, 'description': '右移'},
    
    # 旋转控制
    'q': {'param': 'wz', 'change': SPEED_INCREMENT, 'description': '左转'},
    'e': {'param': 'wz', 'change': -SPEED_INCREMENT, 'description': '右转'},
    
    # 高度控制
    'z': {'param': 'body_height', 'change': 0.02, 'description': '升高'},
    'x': {'param': 'body_height', 'change': -0.02, 'description': '降低'},
}

def clear_screen():
    """清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_controls():
    """显示控制说明"""
    clear_screen()
    print("===== 机器狗键盘遥控 =====")
    print("W / ↑: 前进")
    print("S / ↓: 后退")
    print("A / ←: 左移")
    print("D / →: 右移")
    print("Q   : 左转")
    print("E   : 右转")
    print("Z   : 升高身体")
    print("X   : 降低身体")
    print("空格: 停止移动")
    print("ESC : 退出程序")
    print("\n当前状态:")
    print(f"前进/后退速度 (vx): {dog_state['vx']:.2f}")
    print(f"左右移动速度 (vy): {dog_state['vy']:.2f}")
    print(f"旋转速度 (wz): {dog_state['wz']:.2f}")
    print(f"身体高度: {dog_state['body_height']:.2f}")

def update_dog(dog):
    """更新机器狗状态"""
    dog.vx = dog_state['vx']
    dog.vy = dog_state['vy']
    dog.wz = dog_state['wz']
    dog.body_height = dog_state['body_height']
    display_controls()

def on_press(key, dog):
    """处理按键按下事件"""
    try:
        # 将键盘输入转换为字符
        k = key.char.lower() if hasattr(key, 'char') else key
    except AttributeError:
        k = key
    
    # 处理空格键 - 停止运动
    if k == keyboard.Key.space:
        dog_state['vx'] = 0.0
        dog_state['vy'] = 0.0
        dog_state['wz'] = 0.0
        update_dog(dog)
        return
    
    # 处理ESC键 - 退出程序
    if k == keyboard.Key.esc:
        dog_state['running'] = False
        return False
    
    # 处理其他控制键
    if k in key_mapping:
        param = key_mapping[k]['param']
        change = key_mapping[k]['change']
        
        # 更新参数值并确保在有效范围内
        if param == 'body_height':
            dog_state[param] = max(0.1, min(0.35, dog_state[param] + change))
        else:
            dog_state[param] = max(MIN_SPEED, min(MAX_SPEED, dog_state[param] + change))
        
        update_dog(dog)

def on_release(key, dog):
    """处理按键释放事件"""
    pass  # 这里可以添加按键释放时的行为，如停止移动等

def keyboard_control_loop(dog):
    """键盘控制主循环"""
    display_controls()
    
    # 设置监听器
    with keyboard.Listener(
        on_press=lambda key: on_press(key, dog),
        on_release=lambda key: on_release(key, dog)) as listener:
        
        while dog_state['running']:
            time.sleep(0.1)  # 减少CPU使用率
            if not listener.running:
                break
        
        listener.stop()

if __name__ == '__main__':
    # 替换为您的机器狗IP地址
    host = '192.168.31.189'  # 默认值，根据实际情况修改
    
    try:
        with Dog(host=host) as dog:
            try:
                # 设置用户模式
                dog.set_user_mode(UserMode.NORMAL)
                
                # 开始键盘控制
                print(f"正在连接到机器狗 ({host})...")
                time.sleep(1)  # 等待连接建立
                
                keyboard_control_loop(dog)
                
            except KeyboardInterrupt:
                print("\n程序被用户中断")
            finally:
                # 重置为默认姿态
                print("重置机器狗姿态...")
                dog.set_parameters(DEFAULT_POSTURE)
    except Exception as e:
        print(f"连接失败: {e}")
        print(f"请确保机器狗已开机并位于同一网络中，IP地址正确为: {host}")
        print("如需修改IP地址，请编辑脚本中的host变量")
