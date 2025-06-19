from robodog import Dog, UserMode
from pynput import keyboard
import time
import os
import threading

# 控制参数
DEFAULT_POSTURE = {
    'body_height': 0.23,
    'roll': 0.0,
    'pitch': 0.0,
    'yaw': 0.0,
    'vx': 0.0,
    'vy': 0.0,
    'wz': 0.0
}

class RobodogController:
    def __init__(self, host='192.168.118.29'):
        self.host = host
        self.dog = None
        
        # 速度设置
        self.speed_levels = [0.2, 0.5, 0.8, 1.2, 1.5, 2.0]
        self.current_speed_index = 2  # 默认中等速度 (0.8)
        self.max_turn_speed = 1.0
        
        # 高度设置
        self.height_levels = [0.15, 0.20, 0.25, 0.30, 0.35]
        self.current_height_index = 2  # 默认中等高度 (0.25)
        
        # 当前状态
        self.current_vx = 0.0
        self.current_vy = 0.0
        self.current_wz = 0.0
        self.current_height = self.height_levels[self.current_height_index]
        
        # 按键状态 - 用于即按即走模式
        self.pressed_keys = set()
        self.running = True
        self.display_update_needed = True
        
        # 按键映射 - 即按即走模式
        self.movement_keys = {
            'w': {'vx': 1.0, 'vy': 0.0, 'wz': 0.0, 'name': '前进'},
            's': {'vx': -1.0, 'vy': 0.0, 'wz': 0.0, 'name': '后退'},
            'a': {'vx': 0.0, 'vy': 1.0, 'wz': 0.0, 'name': '左移'},
            'd': {'vx': 0.0, 'vy': -1.0, 'wz': 0.0, 'name': '右移'},
            'q': {'vx': 0.0, 'vy': 0.0, 'wz': 1.0, 'name': '左转'},
            'e': {'vx': 0.0, 'vy': 0.0, 'wz': -1.0, 'name': '右转'},
        }
        
        # 方向键映射
        self.arrow_keys = {
            keyboard.Key.up: 'w',
            keyboard.Key.down: 's',
            keyboard.Key.left: 'a',
            keyboard.Key.right: 'd',
        }

    def get_current_speed(self):
        """获取当前速度"""
        return self.speed_levels[self.current_speed_index]
    
    def get_current_height(self):
        """获取当前高度"""
        return self.height_levels[self.current_height_index]
    
    def speed_up(self):
        """提高速度"""
        if self.current_speed_index < len(self.speed_levels) - 1:
            self.current_speed_index += 1
            self.display_update_needed = True
    
    def speed_down(self):
        """降低速度"""
        if self.current_speed_index > 0:
            self.current_speed_index -= 1
            self.display_update_needed = True
    
    def height_up(self):
        """提高身高"""
        if self.current_height_index < len(self.height_levels) - 1:
            self.current_height_index += 1
            self.current_height = self.height_levels[self.current_height_index]
            self.display_update_needed = True
    
    def height_down(self):
        """降低身高"""
        if self.current_height_index > 0:
            self.current_height_index -= 1
            self.current_height = self.height_levels[self.current_height_index]
            self.display_update_needed = True

    def clear_screen(self):
        """清屏函数"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_status(self):
        """显示当前状态"""
        self.clear_screen()
        print("=" * 50)
        print("       机器狗即按即走键盘遥控 v2.0")
        print("=" * 50)
        print("\n移动控制（即按即走）:")
        print("  W / ↑    : 前进")
        print("  S / ↓    : 后退")
        print("  A / ←    : 左移")
        print("  D / →    : 右移")
        print("  Q        : 左转")
        print("  E        : 右转")
        print("  空格     : 紧急停止")
        
        print("\n速度调节:")
        print("  + / =    : 提高速度")
        print("  - / _    : 降低速度")
        
        print("\n高度调节:")
        print("  Z        : 提高身高")
        print("  X        : 降低身高")
        
        print("\n程序控制:")
        print("  R        : 重置姿态")
        print("  ESC      : 退出程序")
        
        print("\n" + "=" * 50)
        print("当前状态:")
        print(f"  速度等级: {self.current_speed_index + 1}/6 ({self.get_current_speed():.1f} m/s)")
        print(f"  身高等级: {self.current_height_index + 1}/5 ({self.get_current_height():.2f} m)")
        print(f"  当前速度: vx={self.current_vx:.2f}, vy={self.current_vy:.2f}, wz={self.current_wz:.2f}")
        
        # 显示当前按下的键
        if self.pressed_keys:
            pressed_names = []
            for key in self.pressed_keys:
                if key in self.movement_keys:
                    pressed_names.append(self.movement_keys[key]['name'])
            if pressed_names:
                print(f"  当前动作: {', '.join(pressed_names)}")
        else:
            print("  当前动作: 静止")
        
        print("=" * 50)

    def calculate_movement(self):
        """根据当前按下的键计算移动速度"""
        vx, vy, wz = 0.0, 0.0, 0.0
        current_speed = self.get_current_speed()
        
        # 累加所有按下的移动键的效果
        for key in self.pressed_keys:
            if key in self.movement_keys:
                move = self.movement_keys[key]
                vx += move['vx'] * current_speed
                vy += move['vy'] * current_speed
                wz += move['wz'] * self.max_turn_speed
        
        return vx, vy, wz

    def update_dog_movement(self):
        """更新机器狗移动状态"""
        if not self.dog:
            return
            
        vx, vy, wz = self.calculate_movement()
        
        # 只有在速度发生变化时才更新
        if (abs(vx - self.current_vx) > 0.01 or 
            abs(vy - self.current_vy) > 0.01 or 
            abs(wz - self.current_wz) > 0.01):
            
            self.current_vx = vx
            self.current_vy = vy
            self.current_wz = wz
            
            # 更新机器狗
            self.dog.vx = vx
            self.dog.vy = vy
            self.dog.wz = wz
            
            self.display_update_needed = True

    def update_dog_height(self):
        """更新机器狗身高"""
        if self.dog:
            self.dog.body_height = self.current_height

    def reset_posture(self):
        """重置机器狗姿态"""
        if self.dog:
            print("重置机器狗姿态...")
            self.dog.set_parameters(DEFAULT_POSTURE)
            self.current_vx = 0.0
            self.current_vy = 0.0
            self.current_wz = 0.0
            self.current_height = DEFAULT_POSTURE['body_height']
            self.current_height_index = 2
            self.display_update_needed = True

    def emergency_stop(self):
        """紧急停止"""
        if self.dog:
            self.dog.vx = 0.0
            self.dog.vy = 0.0
            self.dog.wz = 0.0
            self.current_vx = 0.0
            self.current_vy = 0.0
            self.current_wz = 0.0
            self.display_update_needed = True

    def on_press(self, key):
        """处理按键按下事件"""
        try:
            # 将键盘输入转换为字符
            k = key.char.lower() if hasattr(key, 'char') else key
        except AttributeError:
            k = key
        
        # 退出程序
        if k == keyboard.Key.esc:
            self.running = False
            return False
        
        # 方向键映射
        if k in self.arrow_keys:
            k = self.arrow_keys[k]
        
        # 移动键
        if isinstance(k, str) and k in self.movement_keys:
            self.pressed_keys.add(k)
        
        # 速度调节
        elif k in ['+', '=']:
            self.speed_up()
        elif k in ['-', '_']:
            self.speed_down()
        
        # 高度调节
        elif k == 'z':
            self.height_up()
        elif k == 'x':
            self.height_down()
        
        # 特殊功能键
        elif k == keyboard.Key.space:
            self.emergency_stop()
        elif k == 'r':
            self.reset_posture()

    def on_release(self, key):
        """处理按键释放事件"""
        try:
            k = key.char.lower() if hasattr(key, 'char') else key
        except AttributeError:
            k = key
        
        # 方向键映射
        if k in self.arrow_keys:
            k = self.arrow_keys[k]
        
        # 移动键释放
        if isinstance(k, str) and k in self.movement_keys:
            self.pressed_keys.discard(k)

    def control_loop(self):
        """控制主循环"""
        last_update_time = 0
        
        while self.running:
            current_time = time.time()
            
            # 更新机器狗移动
            self.update_dog_movement()
            
            # 更新机器狗身高
            self.update_dog_height()
            
            # 更新显示（每0.2秒或状态改变时）
            if (current_time - last_update_time >= 0.2 or self.display_update_needed):
                self.display_status()
                self.display_update_needed = False
                last_update_time = current_time
            
            time.sleep(0.05)  # 20Hz更新频率

    def start(self):
        """启动控制器"""
        try:
            with Dog(host=self.host) as dog:
                self.dog = dog
                
                # 设置用户模式
                dog.set_user_mode(UserMode.NORMAL)
                print(f"成功连接到机器狗 ({self.host})")
                time.sleep(1)
                
                # 显示初始状态
                self.display_status()
                
                # 启动控制循环线程
                control_thread = threading.Thread(target=self.control_loop)
                control_thread.daemon = True
                control_thread.start()
                
                # 键盘监听
                with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                    listener.join()
                
                # 程序结束时重置姿态
                self.reset_posture()
                
        except Exception as e:
            print(f"连接失败: {e}")
            print(f"请确保机器狗已开机并位于同一网络中，IP地址正确为: {self.host}")

if __name__ == '__main__':
    # 机器狗IP地址
    host = '192.168.118.29'  # 根据实际情况修改
    
    controller = RobodogController(host)
    controller.start()
