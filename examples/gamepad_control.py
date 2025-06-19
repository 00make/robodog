import pygame
import time
import threading
from robodog import Dog, UserMode

class GamepadController:
    def __init__(self, host='192.168.118.29'):
        self.host = host
        self.dog = None
        self.running = False
        
        # 初始化pygame
        pygame.init()
        pygame.joystick.init()
        
        # 检查手柄
        if pygame.joystick.get_count() == 0:
            print("未检测到游戏手柄！")
            return
        
        # 连接第一个手柄
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"已连接手柄: {self.joystick.get_name()}")
        
        # 控制参数
        self.max_speed = 1.5
        self.max_turn_speed = 1.0
        self.height_levels = [0.15, 0.20, 0.25, 0.30, 0.35]
        self.current_height_index = 2
        
        # 死区设置
        self.deadzone = 0.1
        
        # 按钮映射 (Xbox手柄)
        self.button_map = {
            0: 'A',      # A按钮
            1: 'B',      # B按钮
            2: 'X',      # X按钮
            3: 'Y',      # Y按钮
            4: 'LB',     # 左肩键
            5: 'RB',     # 右肩键
            6: 'BACK',   # 返回键
            7: 'START',  # 开始键
            8: 'LS',     # 左摇杆按键
            9: 'RS',     # 右摇杆按键
        }
        
    def apply_deadzone(self, value):
        """应用死区"""
        if abs(value) < self.deadzone:
            return 0.0
        return value
    
    def get_movement_from_gamepad(self):
        """从手柄获取移动数据"""
        pygame.event.pump()
        
        # 左摇杆控制移动
        left_x = self.apply_deadzone(self.joystick.get_axis(0))  # 左右移动
        left_y = self.apply_deadzone(-self.joystick.get_axis(1)) # 前后移动 (反向)
        
        # 右摇杆控制旋转
        right_x = self.apply_deadzone(self.joystick.get_axis(2))  # 旋转
        
        # 计算移动速度
        vx = left_y * self.max_speed
        vy = left_x * self.max_speed
        wz = right_x * self.max_turn_speed
        
        return vx, vy, wz
    
    def handle_buttons(self):
        """处理按钮输入"""
        pygame.event.pump()
        
        # 检查按钮状态
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                button_name = self.button_map.get(i, f'Button{i}')
                
                # 高度控制
                if button_name == 'Y':  # Y按钮 - 升高
                    if self.current_height_index < len(self.height_levels) - 1:
                        self.current_height_index += 1
                        print(f"身高升高: {self.height_levels[self.current_height_index]:.2f}m")
                        time.sleep(0.2)  # 防止重复触发
                        
                elif button_name == 'A':  # A按钮 - 降低
                    if self.current_height_index > 0:
                        self.current_height_index -= 1
                        print(f"身高降低: {self.height_levels[self.current_height_index]:.2f}m")
                        time.sleep(0.2)
                        
                # 紧急停止
                elif button_name == 'B':  # B按钮 - 紧急停止
                    if self.dog:
                        self.dog.vx = 0.0
                        self.dog.vy = 0.0
                        self.dog.wz = 0.0
                        print("紧急停止!")
                        time.sleep(0.2)
                        
                # 重置姿态
                elif button_name == 'X':  # X按钮 - 重置
                    self.reset_posture()
                    time.sleep(0.2)
                    
                # 退出程序
                elif button_name == 'START':  # 开始键 - 退出
                    print("退出程序...")
                    self.running = False
                    
    def reset_posture(self):
        """重置机器狗姿态"""
        if self.dog:
            print("重置机器狗姿态...")
            self.dog.vx = 0.0
            self.dog.vy = 0.0
            self.dog.wz = 0.0
            self.dog.body_height = 0.23
            self.current_height_index = 2
    
    def display_status(self, vx, vy, wz):
        """显示当前状态"""
        print(f"\r状态 - 速度: vx={vx:.2f} vy={vy:.2f} wz={wz:.2f} | "
              f"身高: {self.height_levels[self.current_height_index]:.2f}m | "
              f"手柄: {self.joystick.get_name()}", end='', flush=True)
    
    def control_loop(self):
        """主控制循环"""
        print("\n手柄控制说明:")
        print("- 左摇杆: 前后左右移动")
        print("- 右摇杆: 左右旋转")
        print("- Y按钮: 升高身体")
        print("- A按钮: 降低身体")
        print("- B按钮: 紧急停止")
        print("- X按钮: 重置姿态")
        print("- START按钮: 退出程序")
        print("\n开始控制...")
        
        last_status_time = 0
        
        while self.running:
            try:
                # 获取移动数据
                vx, vy, wz = self.get_movement_from_gamepad()
                
                # 处理按钮
                self.handle_buttons()
                
                # 更新机器狗
                if self.dog:
                    self.dog.vx = vx
                    self.dog.vy = vy
                    self.dog.wz = wz
                    self.dog.body_height = self.height_levels[self.current_height_index]
                
                # 显示状态 (每0.5秒更新一次)
                current_time = time.time()
                if current_time - last_status_time >= 0.5:
                    self.display_status(vx, vy, wz)
                    last_status_time = current_time
                
                time.sleep(0.05)  # 20Hz更新频率
                
            except Exception as e:
                print(f"\n控制错误: {e}")
                break
    
    def start(self):
        """启动手柄控制"""
        if not hasattr(self, 'joystick'):
            print("无法启动，未检测到手柄")
            return
            
        try:
            with Dog(host=self.host) as dog:
                self.dog = dog
                self.running = True
                
                # 设置用户模式
                dog.set_user_mode(UserMode.NORMAL)
                print(f"成功连接到机器狗 ({self.host})")
                time.sleep(1)
                
                # 开始控制循环
                self.control_loop()
                
                # 程序结束时重置姿态
                self.reset_posture()
                
        except Exception as e:
            print(f"连接失败: {e}")
            print(f"请确保机器狗已开机并位于同一网络中，IP地址正确为: {self.host}")
        finally:
            pygame.quit()

if __name__ == '__main__':
    # 机器狗IP地址
    host = '192.168.118.29'  # 根据实际情况修改
    
    controller = GamepadController(host)
    controller.start()
