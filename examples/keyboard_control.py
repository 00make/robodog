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

# 速度参数 - 减小增量使控制更精细
SPEED_INCREMENT = 0.8  # 从0.1降低到0.05，使变化更平滑
MAX_SPEED = 4.0  # 降低最大速度，使控制更稳定
MIN_SPEED = -1.0

# 新增：参数平滑设置
SMOOTHING_FACTOR = 0.3  # 平滑因子，值越小变化越平滑
UPDATE_RATE = 0.02  # 控制更新频率(秒)，相当于50Hz

# 机器狗状态
dog_state = {
    'vx': 0.0,  # 前进/后退速度
    'vy': 0.0,  # 左右速度
    'wz': 0.0,  # 旋转速度
    'body_height': 0.23,  # 身体高度
    'running': True,  # 程序运行状态
    'display_update_needed': True,  # 是否需要更新显示
    # 新增：目标状态和上次发送时间
    'target_vx': 0.0,
    'target_vy': 0.0,
    'target_wz': 0.0,
    'target_body_height': 0.23,
    'last_send_time': 0,
    'network_delay': 0  # 用于跟踪网络延迟
}

# 按键状态字典（跟踪哪些键被按下）
pressed_keys = set()

# 按键映射
key_mapping = {
    # 前进/后退控制
    'w': {'param': 'target_vx', 'change': SPEED_INCREMENT, 'description': '前进'},
    's': {'param': 'target_vx', 'change': -SPEED_INCREMENT, 'description': '后退'},
    keyboard.Key.up: {'param': 'target_vx', 'change': SPEED_INCREMENT, 'description': '前进'},
    keyboard.Key.down: {'param': 'target_vx', 'change': -SPEED_INCREMENT, 'description': '后退'},
    
    # 左右移动控制
    'a': {'param': 'target_vy', 'change': SPEED_INCREMENT, 'description': '左移'},
    'd': {'param': 'target_vy', 'change': -SPEED_INCREMENT, 'description': '右移'},
    keyboard.Key.left: {'param': 'target_vy', 'change': SPEED_INCREMENT, 'description': '左移'},
    keyboard.Key.right: {'param': 'target_vy', 'change': -SPEED_INCREMENT, 'description': '右移'},
    
    # 旋转控制
    'q': {'param': 'target_wz', 'change': SPEED_INCREMENT, 'description': '左转'},
    'e': {'param': 'target_wz', 'change': -SPEED_INCREMENT, 'description': '右转'},
    
    # 高度控制
    'z': {'param': 'target_body_height', 'change': 0.01, 'description': '升高'},  # 减小增量
    'x': {'param': 'target_body_height', 'change': -0.01, 'description': '降低'},  # 减小增量
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
    print(f"前进/后退速度 (vx): {dog_state['vx']:.2f} → {dog_state['target_vx']:.2f}")
    print(f"左右移动速度 (vy): {dog_state['vy']:.2f} → {dog_state['target_vy']:.2f}")
    print(f"旋转速度 (wz): {dog_state['wz']:.2f} → {dog_state['target_wz']:.2f}")
    print(f"身体高度: {dog_state['body_height']:.2f}")
    print(f"网络延迟: {dog_state['network_delay']*1000:.1f}ms")

def update_dog(dog):
    """更新机器狗状态 - 使用平滑过渡"""
    start_time = time.time()
    
    # 检查是否有实际变化，避免发送无变化的指令
    changed = False
    params = {}
    
    # 平滑过渡到目标值
    for param in ['vx', 'vy', 'wz', 'body_height']:
        target_param = f'target_{param}'
        # 计算当前值和目标值之间的差异
        diff = dog_state[target_param] - dog_state[param]
        if abs(diff) > 0.001:  # 仅在有明显差异时更新
            # 使用平滑因子计算新值
            dog_state[param] += diff * SMOOTHING_FACTOR
            params[param] = dog_state[param]
            changed = True
    
    # 只有在有变化时才发送指令
    if changed:
        # 更新机器狗
        if 'vx' in params:
            dog.vx = params['vx']
        if 'vy' in params:
            dog.vy = params['vy']
        if 'wz' in params:
            dog.wz = params['wz']
        if 'body_height' in params:
            dog.body_height = params['body_height']
        
        # 记录网络延迟
        dog_state['network_delay'] = time.time() - start_time
        dog_state['last_send_time'] = time.time()
        
        # 更新显示
        dog_state['display_update_needed'] = True

def process_keys():
    """处理当前按下的所有键"""
    # 如果空格键被按下，重置移动速度
    if keyboard.Key.space in pressed_keys:
        dog_state['target_vx'] = 0.0
        dog_state['target_vy'] = 0.0
        dog_state['target_wz'] = 0.0
        dog_state['display_update_needed'] = True
        return
    
    # 处理其他按键
    for k in pressed_keys:
        if k in key_mapping:
            param = key_mapping[k]['param']
            change = key_mapping[k]['change']
            
            # 更新目标参数值并确保在有效范围内
            if param == 'target_body_height':
                dog_state[param] = max(0.1, min(0.35, dog_state[param] + change))
            else:
                dog_state[param] = max(MIN_SPEED, min(MAX_SPEED, dog_state[param] + change))
            
            dog_state['display_update_needed'] = True

def on_press(key):
    """处理按键按下事件"""
    try:
        # 将键盘输入转换为字符
        k = key.char.lower() if hasattr(key, 'char') else key
    except AttributeError:
        k = key
    
    # 处理ESC键 - 退出程序
    if k == keyboard.Key.esc:
        dog_state['running'] = False
        return False
    
    # 添加到已按下的键列表
    pressed_keys.add(k)

def on_release(key):
    """处理按键释放事件"""
    try:
        k = key.char.lower() if hasattr(key, 'char') else key
    except AttributeError:
        k = key
    
    # 从已按下的键列表中移除
    if k in pressed_keys:
        pressed_keys.remove(k)

def display_thread_function():
    """UI显示线程"""
    last_update_time = 0
    while dog_state['running']:
        current_time = time.time()
        # 每0.5秒更新一次显示，或者当状态改变时
        if (current_time - last_update_time >= 0.5 or dog_state['display_update_needed']) and dog_state['running']:
            display_controls()
            dog_state['display_update_needed'] = False
            last_update_time = current_time
        time.sleep(0.1)  # 降低CPU使用率，但不影响控制响应性

def control_thread_function(dog):
    """控制线程 - 高频率更新机器狗"""
    last_time = time.time()
    while dog_state['running']:
        current_time = time.time()
        elapsed = current_time - last_time
        
        # 基于固定的更新频率运行
        if elapsed >= UPDATE_RATE:
            process_keys()  # 处理当前按下的所有键
            update_dog(dog)  # 更新机器狗状态
            last_time = current_time
        else:
            # 短暂睡眠以降低CPU使用率
            time.sleep(0.001)

def keyboard_control_loop(dog):
    """键盘控制主循环"""
    display_controls()
    
    # 创建并启动显示线程
    display_thread = threading.Thread(target=display_thread_function)
    display_thread.daemon = True
    display_thread.start()
    
    # 创建并启动控制线程
    control_thread = threading.Thread(target=control_thread_function, args=(dog,))
    control_thread.daemon = True
    control_thread.start()
    
    # 设置键盘监听器
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while dog_state['running']:
            time.sleep(0.1)  # 主线程可以较低频率运行
            if not listener.running:
                break
        
        listener.stop()

if __name__ == '__main__':
    # 替换为您的机器狗IP地址
    host = '192.168.31.148'  # 默认值，根据实际情况修改
    
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
