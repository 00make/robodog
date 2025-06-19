import pygame
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import queue
from robodog import Dog, UserMode

class GamepadControllerGUI:
    def __init__(self):
        # 连接参数
        self.host = '192.168.118.29'
        self.dog = None
        self.connected = False
        self.running = False
        
        # pygame相关
        self.joystick = None
        self.gamepad_connected = False
        
        # 控制参数
        self.max_speed = 1.5
        self.max_turn_speed = 1.0
        self.height_levels = [0.15, 0.20, 0.25, 0.30, 0.35]
        self.current_height_index = 2
        
        # 当前状态
        self.current_vx = 0.0
        self.current_vy = 0.0
        self.current_wz = 0.0
        self.current_height = self.height_levels[self.current_height_index]
        
        # 死区设置
        self.deadzone = 0.1
        
        # 消息队列
        self.message_queue = queue.Queue()
        
        # 控制线程
        self.control_thread = None
        
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
        
        # 初始化pygame
        self.init_pygame()
        
        # 设置GUI
        self.setup_gui()
        
    def init_pygame(self):
        """初始化pygame和手柄"""
        try:
            pygame.init()
            pygame.joystick.init()
            self.check_gamepad()
        except Exception as e:
            print(f"初始化pygame失败: {e}")
    
    def check_gamepad(self):
        """检查游戏手柄连接"""
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.gamepad_connected = True
            self.message_queue.put(('gamepad_status', f"已连接手柄: {self.joystick.get_name()}"))
        else:
            self.gamepad_connected = False
            self.message_queue.put(('gamepad_status', "未检测到游戏手柄"))
    
    def setup_gui(self):
        """设置GUI界面"""
        self.root = tk.Tk()
        self.root.title("机器狗游戏手柄控制器 v2.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 手柄连接状态区域
        self.setup_gamepad_area(main_frame)
        
        # 机器狗连接区域
        self.setup_connection_area(main_frame)
        
        # 控制参数区域
        self.setup_control_params_area(main_frame)
        
        # 手柄控制说明区域
        self.setup_gamepad_guide_area(main_frame)
        
        # 状态显示区域
        self.setup_status_area(main_frame)
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gamepad_area(self, parent):
        """设置手柄连接区域"""
        gamepad_frame = ttk.LabelFrame(parent, text="游戏手柄状态", padding="10")
        gamepad_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        gamepad_frame.columnconfigure(1, weight=1)
        
        # 手柄状态标签
        self.gamepad_status_label = ttk.Label(gamepad_frame, text="检查中...")
        self.gamepad_status_label.grid(row=0, column=0, sticky=(tk.W,), padx=(0, 10))
        
        # 刷新手柄按钮
        self.refresh_gamepad_btn = ttk.Button(gamepad_frame, text="刷新手柄", 
                                            command=self.refresh_gamepad)
        self.refresh_gamepad_btn.grid(row=0, column=1, padx=(0, 10))
        
        # 手柄指示器
        self.gamepad_indicator = tk.Canvas(gamepad_frame, width=20, height=20)
        self.gamepad_indicator.grid(row=0, column=2)
        self.update_gamepad_indicator(False)
        
        # 手柄连接指导
        guide_text = ("手柄连接指导:\n"
                     "1. 确保手柄已正确连接到电脑\n"
                     "2. 对于无线手柄，确保已配对并开启\n"
                     "3. 点击'刷新手柄'按钮检测新连接的手柄")
        guide_label = ttk.Label(gamepad_frame, text=guide_text, foreground="gray")
        guide_label.grid(row=1, column=0, columnspan=3, sticky=(tk.W,), pady=(10, 0))
    
    def setup_connection_area(self, parent):
        """设置机器狗连接区域"""
        conn_frame = ttk.LabelFrame(parent, text="机器狗连接", padding="10")
        conn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # IP地址输入
        ttk.Label(conn_frame, text="机器狗IP:").grid(row=0, column=0, padx=(0, 5))
        self.ip_var = tk.StringVar(value=self.host)
        ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var, width=20)
        ip_entry.grid(row=0, column=1, padx=(0, 10))
        
        # 连接按钮
        self.connect_btn = ttk.Button(conn_frame, text="连接", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=2, padx=(0, 10))
        
        # 连接状态标签
        self.connection_status_label = ttk.Label(conn_frame, text="未连接")
        self.connection_status_label.grid(row=0, column=3)
        
        # 连接指示器
        self.connection_indicator = tk.Canvas(conn_frame, width=20, height=20)
        self.connection_indicator.grid(row=0, column=4, padx=(10, 0))
        self.update_connection_indicator(False)
    
    def setup_control_params_area(self, parent):
        """设置控制参数区域"""
        params_frame = ttk.LabelFrame(parent, text="控制参数", padding="10")
        params_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        params_frame.columnconfigure(1, weight=1)
        
        # 最大速度控制
        ttk.Label(params_frame, text="最大速度:").grid(row=0, column=0, sticky=(tk.W,), padx=(0, 10))
        self.speed_var = tk.DoubleVar(value=self.max_speed)
        speed_scale = ttk.Scale(params_frame, from_=0.5, to=3.0, variable=self.speed_var,
                               orient="horizontal", command=self.on_speed_change)
        speed_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.speed_label = ttk.Label(params_frame, text=f"{self.max_speed:.1f} m/s")
        self.speed_label.grid(row=0, column=2)
        
        # 转向速度控制
        ttk.Label(params_frame, text="转向速度:").grid(row=1, column=0, sticky=(tk.W,), padx=(0, 10))
        self.turn_var = tk.DoubleVar(value=self.max_turn_speed)
        turn_scale = ttk.Scale(params_frame, from_=0.3, to=2.0, variable=self.turn_var,
                              orient="horizontal", command=self.on_turn_change)
        turn_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.turn_label = ttk.Label(params_frame, text=f"{self.max_turn_speed:.1f} rad/s")
        self.turn_label.grid(row=1, column=2)
        
        # 死区控制
        ttk.Label(params_frame, text="摇杆死区:").grid(row=2, column=0, sticky=(tk.W,), padx=(0, 10))
        self.deadzone_var = tk.DoubleVar(value=self.deadzone)
        deadzone_scale = ttk.Scale(params_frame, from_=0.0, to=0.3, variable=self.deadzone_var,
                                  orient="horizontal", command=self.on_deadzone_change)
        deadzone_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.deadzone_label = ttk.Label(params_frame, text=f"{self.deadzone:.2f}")
        self.deadzone_label.grid(row=2, column=2)
    
    def setup_gamepad_guide_area(self, parent):
        """设置手柄控制说明区域"""
        guide_frame = ttk.LabelFrame(parent, text="手柄控制说明", padding="10")
        guide_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 创建两列布局
        left_frame = ttk.Frame(guide_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.N), padx=(0, 20))
        
        right_frame = ttk.Frame(guide_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.N))
        
        # 左列 - 摇杆控制
        ttk.Label(left_frame, text="摇杆控制:", font=("Arial", 10, "bold")).pack(anchor="w")
        stick_controls = [
            "• 左摇杆: 前后左右移动",
            "• 右摇杆: 左右旋转",
            "",
            "摇杆死区可调节敏感度"
        ]
        for control in stick_controls:
            ttk.Label(left_frame, text=control).pack(anchor="w")
        
        # 右列 - 按钮控制
        ttk.Label(right_frame, text="按钮控制:", font=("Arial", 10, "bold")).pack(anchor="w")
        button_controls = [
            "• Y按钮: 升高身体",
            "• A按钮: 降低身体", 
            "• B按钮: 紧急停止",
            "• X按钮: 重置姿态",
            "• START: 停止控制"
        ]
        for control in button_controls:
            ttk.Label(right_frame, text=control).pack(anchor="w")
    
    def setup_status_area(self, parent):
        """设置状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="实时状态", padding="10")
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # 状态文本框
        self.status_text = tk.Text(status_frame, height=8, width=70, state='disabled',
                                  font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 控制按钮
        button_frame = ttk.Frame(status_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        self.start_btn = ttk.Button(button_frame, text="开始控制", command=self.start_control,
                                   state="disabled")
        self.start_btn.pack(side="left", padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="停止控制", command=self.stop_control,
                                  state="disabled")
        self.stop_btn.pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame, text="清空日志", command=self.clear_log).pack(side="left")
    
    def update_gamepad_indicator(self, connected):
        """更新手柄连接指示器"""
        self.gamepad_indicator.delete("all")
        color = "green" if connected else "red"
        self.gamepad_indicator.create_oval(2, 2, 18, 18, fill=color, outline=color)
    
    def update_connection_indicator(self, connected):
        """更新机器狗连接指示器"""
        self.connection_indicator.delete("all")
        color = "green" if connected else "red"
        self.connection_indicator.create_oval(2, 2, 18, 18, fill=color, outline=color)
    
    def refresh_gamepad(self):
        """刷新手柄连接"""
        self.log_message("正在刷新手柄连接...")
        pygame.joystick.quit()
        pygame.joystick.init()
        self.check_gamepad()
    
    def on_speed_change(self, value):
        """速度滑块改变"""
        self.max_speed = float(value)
        self.speed_label.configure(text=f"{self.max_speed:.1f} m/s")
    
    def on_turn_change(self, value):
        """转向速度滑块改变"""
        self.max_turn_speed = float(value)
        self.turn_label.configure(text=f"{self.max_turn_speed:.1f} rad/s")
    
    def on_deadzone_change(self, value):
        """死区滑块改变"""
        self.deadzone = float(value)
        self.deadzone_label.configure(text=f"{self.deadzone:.2f}")
    
    def toggle_connection(self):
        """切换机器狗连接"""
        if not self.connected:
            self.connect_to_dog()
        else:
            self.disconnect_from_dog()
    
    def connect_to_dog(self):
        """连接到机器狗"""
        self.host = self.ip_var.get()
        self.log_message(f"正在连接到机器狗 {self.host}...")
        
        try:
            self.dog = Dog(host=self.host)
            self.dog.__enter__()
            self.dog.set_user_mode(UserMode.NORMAL)
            
            self.connected = True
            self.connect_btn.configure(text="断开连接")
            self.connection_status_label.configure(text="已连接")
            self.update_connection_indicator(True)
            
            # 启用开始控制按钮
            if self.gamepad_connected:
                self.start_btn.configure(state="normal")
            
            self.log_message("✓ 成功连接到机器狗")
            
        except Exception as e:
            self.log_message(f"✗ 连接失败: {e}")
            messagebox.showerror("连接错误", f"无法连接到机器狗:\n{e}")
    
    def disconnect_from_dog(self):
        """断开机器狗连接"""
        self.stop_control()
        
        if self.dog:
            try:
                self.dog.vx = 0.0
                self.dog.vy = 0.0
                self.dog.wz = 0.0
                self.dog.body_height = 0.23
                self.dog.__exit__(None, None, None)
            except:
                pass
            finally:
                self.dog = None
        
        self.connected = False
        self.connect_btn.configure(text="连接")
        self.connection_status_label.configure(text="未连接")
        self.update_connection_indicator(False)
        self.start_btn.configure(state="disabled")
        
        self.log_message("已断开机器狗连接")
    
    def start_control(self):
        """开始手柄控制"""
        if not self.gamepad_connected:
            messagebox.showwarning("警告", "请先连接游戏手柄")
            return
        
        if not self.connected:
            messagebox.showwarning("警告", "请先连接机器狗")
            return
        
        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # 启动控制线程
        self.control_thread = threading.Thread(target=self.control_loop)
        self.control_thread.daemon = True
        self.control_thread.start()
        
        self.log_message("开始手柄控制")
    
    def stop_control(self):
        """停止手柄控制"""
        self.running = False
        
        if self.control_thread and self.control_thread.is_alive():
            self.control_thread.join(timeout=1)
        
        # 停止机器狗移动
        if self.dog:
            self.dog.vx = 0.0
            self.dog.vy = 0.0
            self.dog.wz = 0.0
        
        self.start_btn.configure(state="normal" if self.gamepad_connected else "disabled")
        self.stop_btn.configure(state="disabled")
        
        self.log_message("停止手柄控制")
    
    def log_message(self, message):
        """记录消息到状态显示"""
        current_time = time.strftime("%H:%M:%S")
        log_text = f"[{current_time}] {message}\n"
        
        self.status_text.configure(state='normal')
        self.status_text.insert('end', log_text)
        self.status_text.see('end')
        self.status_text.configure(state='disabled')
    
    def clear_log(self):
        """清空日志"""
        self.status_text.configure(state='normal')
        self.status_text.delete(1.0, 'end')
        self.status_text.configure(state='disabled')
    
    def apply_deadzone(self, value):
        """应用死区"""
        if abs(value) < self.deadzone:
            return 0.0
        return value
    
    def get_movement_from_gamepad(self):
        """从手柄获取移动数据"""
        if not self.gamepad_connected or not self.joystick:
            return 0.0, 0.0, 0.0
            
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
        if not self.gamepad_connected or not self.joystick:
            return
            
        pygame.event.pump()
        
        # 使用静态变量跟踪按钮状态，避免重复触发
        if not hasattr(self, '_button_states'):
            self._button_states = {}
        
        # 检查按钮状态
        for i in range(self.joystick.get_numbuttons()):
            current_state = self.joystick.get_button(i)
            previous_state = self._button_states.get(i, False)
            
            # 只在按键从未按下变为按下时触发
            if current_state and not previous_state:
                button_name = self.button_map.get(i, f'Button{i}')
                
                # 高度控制
                if button_name == 'Y':  # Y按钮 - 升高
                    if self.current_height_index < len(self.height_levels) - 1:
                        self.current_height_index += 1
                        self.current_height = self.height_levels[self.current_height_index]
                        self.log_message(f"身高升高: {self.current_height:.2f}m")
                        
                elif button_name == 'A':  # A按钮 - 降低
                    if self.current_height_index > 0:
                        self.current_height_index -= 1
                        self.current_height = self.height_levels[self.current_height_index]
                        self.log_message(f"身高降低: {self.current_height:.2f}m")
                        
                # 紧急停止
                elif button_name == 'B':  # B按钮 - 紧急停止
                    if self.dog:
                        self.dog.vx = 0.0
                        self.dog.vy = 0.0
                        self.dog.wz = 0.0
                        self.current_vx = 0.0
                        self.current_vy = 0.0
                        self.current_wz = 0.0
                        self.log_message("紧急停止!")
                        
                # 重置姿态
                elif button_name == 'X':  # X按钮 - 重置
                    self.reset_posture()
                    
                # 停止控制
                elif button_name == 'START':  # 开始键 - 停止控制
                    self.stop_control()
            
            # 更新按钮状态
            self._button_states[i] = current_state
    
    def reset_posture(self):
        """重置机器狗姿态"""
        if self.dog:
            self.dog.vx = 0.0
            self.dog.vy = 0.0
            self.dog.wz = 0.0
            self.dog.body_height = 0.23
            self.current_vx = 0.0
            self.current_vy = 0.0
            self.current_wz = 0.0
            self.current_height = 0.23
            self.current_height_index = 2
            self.log_message("重置机器狗姿态")
    
    def control_loop(self):
        """主控制循环"""
        self.log_message("手柄控制循环开始")
        last_status_time = 0
        
        while self.running and self.connected:
            try:
                # 获取移动数据
                vx, vy, wz = self.get_movement_from_gamepad()
                
                # 处理按钮
                self.handle_buttons()
                
                # 更新机器狗
                if self.dog:
                    # 只有在速度发生变化时才更新
                    if (abs(vx - self.current_vx) > 0.01 or 
                        abs(vy - self.current_vy) > 0.01 or 
                        abs(wz - self.current_wz) > 0.01):
                        
                        self.current_vx = vx
                        self.current_vy = vy
                        self.current_wz = wz
                        
                        self.dog.vx = vx
                        self.dog.vy = vy
                        self.dog.wz = wz
                    
                    # 更新身高
                    self.dog.body_height = self.current_height
                
                # 定期更新状态显示
                current_time = time.time()
                if current_time - last_status_time >= 1.0:  # 每秒更新一次
                    self.update_realtime_status(vx, vy, wz)
                    last_status_time = current_time
                
                time.sleep(0.05)  # 20Hz更新频率
                
            except Exception as e:
                self.log_message(f"控制错误: {e}")
                break
        
        self.log_message("手柄控制循环结束")
    
    def update_realtime_status(self, vx, vy, wz):
        """更新实时状态显示"""
        status_info = f"""实时状态:
  速度: vx={vx:.2f} vy={vy:.2f} wz={wz:.2f}
  身高: {self.current_height:.2f}m ({self.current_height_index + 1}/5级)
  手柄: {self.joystick.get_name() if self.gamepad_connected else "未连接"}
  参数: 最大速度={self.max_speed:.1f}m/s, 转向={self.max_turn_speed:.1f}rad/s, 死区={self.deadzone:.2f}
---"""
        
        # 更新到队列，由主线程处理
        self.message_queue.put(('realtime_status', status_info))
    
    def process_messages(self):
        """处理消息队列"""
        try:
            while True:
                msg_type, msg_data = self.message_queue.get_nowait()
                
                if msg_type == 'gamepad_status':
                    self.gamepad_status_label.configure(text=msg_data)
                    self.update_gamepad_indicator(self.gamepad_connected)
                    
                    # 更新开始按钮状态
                    if self.gamepad_connected and self.connected:
                        self.start_btn.configure(state="normal")
                    else:
                        self.start_btn.configure(state="disabled")
                        
                elif msg_type == 'realtime_status':
                    # 插入实时状态到状态文本框顶部  
                    self.status_text.configure(state='normal')
                    current_content = self.status_text.get(1.0, 'end')
                    self.status_text.delete(1.0, 'end')
                    self.status_text.insert(1.0, msg_data + '\n' + current_content)
                    
                    # 限制文本长度
                    lines = self.status_text.get(1.0, 'end').split('\n')
                    if len(lines) > 50:  # 保持最近50行
                        self.status_text.delete(1.0, 'end')
                        self.status_text.insert(1.0, '\n'.join(lines[:50]))
                    
                    self.status_text.configure(state='disabled')
                    
        except queue.Empty:
            pass
        
        # 定期检查消息
        self.root.after(100, self.process_messages)
    
    def on_closing(self):
        """窗口关闭事件"""
        self.stop_control()
        if self.connected:
            self.disconnect_from_dog()
        
        # 清理pygame
        try:
            pygame.quit()
        except:
            pass
            
        self.root.destroy()
    
    def run(self):
        """运行GUI"""
        # 启动消息处理
        self.process_messages()
        
        # 初始状态检查
        self.root.after(100, self.initial_status_check)
        
        # 运行主循环
        self.root.mainloop()
    
    def initial_status_check(self):
        """初始状态检查"""
        if self.gamepad_connected:
            self.log_message(f"✓ 检测到手柄: {self.joystick.get_name()}")
        else:
            self.log_message("✗ 未检测到游戏手柄，请连接手柄后点击'刷新手柄'")

if __name__ == '__main__':
    try:
        app = GamepadControllerGUI()
        app.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        messagebox.showerror("启动失败", f"程序无法启动:\n{e}")
