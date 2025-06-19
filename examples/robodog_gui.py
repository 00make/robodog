import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from robodog import Dog, UserMode
from pynput import keyboard
import queue

class RobodogGUI:
    def __init__(self):
        # 连接参数
        self.host = '192.168.118.29'
        self.dog = None
        self.connected = False
        
        # 控制参数
        self.speed_levels = [0.2, 0.5, 0.8, 1.2, 1.5, 2.0]
        self.current_speed_index = 2
        self.max_turn_speed = 1.0
        
        self.height_levels = [0.15, 0.20, 0.25, 0.30, 0.35]
        self.current_height_index = 2
        
        # 当前状态
        self.current_vx = 0.0
        self.current_vy = 0.0
        self.current_wz = 0.0
        self.current_height = self.height_levels[self.current_height_index]
        
        # 按键状态
        self.pressed_keys = set()
        self.gui_pressed_keys = set()  # GUI按钮按下状态
        self.keyboard_listener = None
        self.control_thread = None
        self.running = False
        
        # 消息队列用于线程间通信
        self.message_queue = queue.Queue()
        
        # 移动键映射
        self.movement_keys = {
            'w': {'vx': 1.0, 'vy': 0.0, 'wz': 0.0, 'name': '前进'},
            's': {'vx': -1.0, 'vy': 0.0, 'wz': 0.0, 'name': '后退'},
            'a': {'vx': 0.0, 'vy': 1.0, 'wz': 0.0, 'name': '左移'},
            'd': {'vx': 0.0, 'vy': -1.0, 'wz': 0.0, 'name': '右移'},
            'q': {'vx': 0.0, 'vy': 0.0, 'wz': 1.0, 'name': '左转'},
            'e': {'vx': 0.0, 'vy': 0.0, 'wz': -1.0, 'name': '右转'},
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        """设置GUI界面"""
        self.root = tk.Tk()
        self.root.title("机器狗遥控器 v2.0")
        self.root.geometry("800x600")
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
        main_frame.columnconfigure(1, weight=1)
        
        # 连接控制区域
        self.setup_connection_area(main_frame)
        
        # 状态显示区域
        self.setup_status_area(main_frame)
        
        # 控制面板区域
        self.setup_control_area(main_frame)
        
        # 移动控制区域
        self.setup_movement_area(main_frame)
        
        # 设置键盘事件
        self.root.bind('<KeyPress>', self.on_gui_key_press)
        self.root.bind('<KeyRelease>', self.on_gui_key_release)
        self.root.focus_set()
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_connection_area(self, parent):
        """设置连接控制区域"""
        conn_frame = ttk.LabelFrame(parent, text="连接控制", padding="5")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # IP地址输入
        ttk.Label(conn_frame, text="机器狗IP:").grid(row=0, column=0, padx=(0, 5))
        self.ip_var = tk.StringVar(value=self.host)
        ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var, width=20)
        ip_entry.grid(row=0, column=1, padx=(0, 10))
        
        # 连接按钮
        self.connect_btn = ttk.Button(conn_frame, text="连接", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=2, padx=(0, 10))
        
        # 连接状态标签
        self.status_label = ttk.Label(conn_frame, text="未连接")
        self.status_label.grid(row=0, column=3)
        
    def setup_status_area(self, parent):
        """设置状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="当前状态", padding="5")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        # 状态文本
        self.status_text = tk.Text(status_frame, height=6, width=50, state='disabled')
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def setup_control_area(self, parent):
        """设置控制面板区域"""
        control_frame = ttk.LabelFrame(parent, text="控制面板", padding="5")
        control_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 速度控制
        speed_frame = ttk.LabelFrame(control_frame, text="速度控制", padding="5")
        speed_frame.pack(fill="x", pady=(0, 10))
        
        self.speed_var = tk.StringVar(value=f"速度: {self.speed_levels[self.current_speed_index]:.1f} m/s")
        ttk.Label(speed_frame, textvariable=self.speed_var).pack()
        
        speed_scale = ttk.Scale(speed_frame, from_=0, to=len(self.speed_levels)-1, 
                               orient="horizontal", command=self.on_speed_change)
        speed_scale.set(self.current_speed_index)
        speed_scale.pack(fill="x", pady=5)
        
        # 高度控制
        height_frame = ttk.LabelFrame(control_frame, text="身高控制", padding="5")
        height_frame.pack(fill="x", pady=(0, 10))
        
        self.height_var = tk.StringVar(value=f"身高: {self.height_levels[self.current_height_index]:.2f} m")
        ttk.Label(height_frame, textvariable=self.height_var).pack()
        
        height_scale = ttk.Scale(height_frame, from_=0, to=len(self.height_levels)-1,
                                orient="horizontal", command=self.on_height_change)
        height_scale.set(self.current_height_index)
        height_scale.pack(fill="x", pady=5)
        
        # 功能按钮
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="紧急停止", command=self.emergency_stop).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="重置姿态", command=self.reset_posture).pack(side="left")
        
    def setup_movement_area(self, parent):
        """设置移动控制区域"""
        move_frame = ttk.LabelFrame(parent, text="移动控制", padding="5")
        move_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 说明文本
        ttk.Label(move_frame, text="键盘控制: WASD移动, QE转向\n或使用下方按钮控制").pack(pady=(0, 10))
        
        # 按钮控制区域
        button_grid = ttk.Frame(move_frame)
        button_grid.pack()
        
        # 创建移动按钮
        self.move_buttons = {}
        
        # 前进按钮 (W)
        self.move_buttons['w'] = ttk.Button(button_grid, text="前进(W)", width=10)
        self.move_buttons['w'].grid(row=0, column=1, padx=2, pady=2)
        
        # 左移按钮 (A)
        self.move_buttons['a'] = ttk.Button(button_grid, text="左移(A)", width=10)
        self.move_buttons['a'].grid(row=1, column=0, padx=2, pady=2)
        
        # 后退按钮 (S)
        self.move_buttons['s'] = ttk.Button(button_grid, text="后退(S)", width=10)
        self.move_buttons['s'].grid(row=1, column=1, padx=2, pady=2)
        
        # 右移按钮 (D)
        self.move_buttons['d'] = ttk.Button(button_grid, text="右移(D)", width=10)
        self.move_buttons['d'].grid(row=1, column=2, padx=2, pady=2)
        
        # 左转按钮 (Q)
        self.move_buttons['q'] = ttk.Button(button_grid, text="左转(Q)", width=10)
        self.move_buttons['q'].grid(row=2, column=0, padx=2, pady=2)
        
        # 右转按钮 (E)
        self.move_buttons['e'] = ttk.Button(button_grid, text="右转(E)", width=10)
        self.move_buttons['e'].grid(row=2, column=2, padx=2, pady=2)
        
        # 绑定按钮事件
        for key, button in self.move_buttons.items():
            button.bind('<Button-1>', lambda e, k=key: self.on_button_press(k))
            button.bind('<ButtonRelease-1>', lambda e, k=key: self.on_button_release(k))
        
    def on_speed_change(self, value):
        """速度滑块改变事件"""
        self.current_speed_index = int(float(value))
        self.speed_var.set(f"速度: {self.speed_levels[self.current_speed_index]:.1f} m/s")
        
    def on_height_change(self, value):
        """高度滑块改变事件"""
        self.current_height_index = int(float(value))
        self.current_height = self.height_levels[self.current_height_index]
        self.height_var.set(f"身高: {self.current_height:.2f} m")
        
    def on_button_press(self, key):
        """GUI按钮按下"""
        self.gui_pressed_keys.add(key)
        self.move_buttons[key].configure(style='Pressed.TButton')
        
    def on_button_release(self, key):
        """GUI按钮释放"""
        self.gui_pressed_keys.discard(key)
        self.move_buttons[key].configure(style='TButton')
        
    def on_gui_key_press(self, event):
        """GUI键盘按下事件"""
        key = event.keysym.lower()
        if key in self.movement_keys:
            self.pressed_keys.add(key)
            if key in self.move_buttons:
                self.move_buttons[key].configure(style='Pressed.TButton')
        elif key == 'space':
            self.emergency_stop()
        elif key == 'r':
            self.reset_posture()
            
    def on_gui_key_release(self, event):
        """GUI键盘释放事件"""
        key = event.keysym.lower()
        if key in self.movement_keys:
            self.pressed_keys.discard(key)
            if key in self.move_buttons:
                self.move_buttons[key].configure(style='TButton')
    
    def toggle_connection(self):
        """切换连接状态"""
        if not self.connected:
            self.connect_to_dog()
        else:
            self.disconnect_from_dog()
            
    def connect_to_dog(self):
        """连接到机器狗"""
        self.host = self.ip_var.get()
        try:
            self.dog = Dog(host=self.host)
            self.dog.__enter__()
            self.dog.set_user_mode(UserMode.NORMAL)
            
            self.connected = True
            self.running = True
            
            # 更新UI
            self.connect_btn.configure(text="断开连接")
            self.status_label.configure(text="已连接")
            
            # 启动控制线程
            self.start_control_thread()
            
            self.update_status("成功连接到机器狗")
            
        except Exception as e:
            messagebox.showerror("连接错误", f"无法连接到机器狗: {e}")
            self.update_status(f"连接失败: {e}")
            
    def disconnect_from_dog(self):
        """断开机器狗连接"""
        self.running = False
        
        if self.control_thread and self.control_thread.is_alive():
            self.control_thread.join(timeout=1)
            
        if self.dog:
            try:
                # 重置姿态
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
        
        # 更新UI
        self.connect_btn.configure(text="连接")
        self.status_label.configure(text="未连接")
        self.update_status("已断开连接")
        
    def start_control_thread(self):
        """启动控制线程"""
        self.control_thread = threading.Thread(target=self.control_loop)
        self.control_thread.daemon = True
        self.control_thread.start()
        
    def control_loop(self):
        """控制循环"""
        while self.running and self.connected:
            try:
                # 计算移动速度
                vx, vy, wz = self.calculate_movement()
                
                # 更新机器狗状态
                if self.dog:
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
                    
                # 更新状态显示
                self.message_queue.put(('status_update', None))
                
            except Exception as e:
                self.message_queue.put(('error', f"控制错误: {e}"))
                break
                
            time.sleep(0.05)  # 20Hz更新频率
            
    def calculate_movement(self):
        """计算移动速度"""
        vx, vy, wz = 0.0, 0.0, 0.0
        current_speed = self.speed_levels[self.current_speed_index]
        
        # 合并键盘和GUI按钮的输入
        all_pressed = self.pressed_keys | self.gui_pressed_keys
        
        for key in all_pressed:
            if key in self.movement_keys:
                move = self.movement_keys[key]
                vx += move['vx'] * current_speed
                vy += move['vy'] * current_speed
                wz += move['wz'] * self.max_turn_speed
                
        return vx, vy, wz
        
    def emergency_stop(self):
        """紧急停止"""
        if self.dog:
            self.dog.vx = 0.0
            self.dog.vy = 0.0
            self.dog.wz = 0.0
            self.current_vx = 0.0
            self.current_vy = 0.0
            self.current_wz = 0.0
        self.update_status("紧急停止")
        
    def reset_posture(self):
        """重置姿态"""
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
        self.update_status("重置姿态")
        
    def update_status(self, message):
        """更新状态显示"""
        current_time = time.strftime("%H:%M:%S")
        status_info = f"[{current_time}] {message}\n"
        
        if hasattr(self, 'status_text'):
            self.status_text.configure(state='normal')
            self.status_text.insert('end', status_info)
            self.status_text.see('end')
            self.status_text.configure(state='disabled')
            
    def update_current_status(self):
        """更新当前状态信息"""
        if not hasattr(self, 'status_text'):
            return
            
        # 获取当前动作
        all_pressed = self.pressed_keys | self.gui_pressed_keys
        actions = []
        for key in all_pressed:
            if key in self.movement_keys:
                actions.append(self.movement_keys[key]['name'])
        
        action_text = ', '.join(actions) if actions else '静止'
        
        status_info = f"""
当前状态 [{time.strftime("%H:%M:%S")}]:
  速度等级: {self.current_speed_index + 1}/6 ({self.speed_levels[self.current_speed_index]:.1f} m/s)
  身高等级: {self.current_height_index + 1}/5 ({self.current_height:.2f} m)
  当前速度: vx={self.current_vx:.2f}, vy={self.current_vy:.2f}, wz={self.current_wz:.2f}
  当前动作: {action_text}
---
"""
        
        self.status_text.configure(state='normal')
        self.status_text.delete(1.0, 'end')
        self.status_text.insert('end', status_info)
        self.status_text.configure(state='disabled')
        
    def process_messages(self):
        """处理消息队列"""
        try:
            while True:
                msg_type, msg_data = self.message_queue.get_nowait()
                if msg_type == 'status_update':
                    self.update_current_status()
                elif msg_type == 'error':
                    self.update_status(msg_data)
        except queue.Empty:
            pass
            
        # 定期检查消息
        self.root.after(100, self.process_messages)
        
    def on_closing(self):
        """窗口关闭事件"""
        if self.connected:
            self.disconnect_from_dog()
        self.root.destroy()
        
    def run(self):
        """运行GUI"""
        # 创建按钮样式
        style = ttk.Style()
        style.configure('Pressed.TButton', background='lightblue')
        
        # 启动消息处理
        self.process_messages()
        
        # 运行主循环
        self.root.mainloop()

if __name__ == '__main__':
    app = RobodogGUI()
    app.run()
