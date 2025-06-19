# 机器狗跳舞功能 - 快速原型开发指南

## 🎯 MVP (最小可行产品) 设计

### 核心目标
在2周内实现一个基础的机器狗跳舞原型，验证核心概念的可行性。

### MVP功能范围
- ✅ 基础动作定义和存储
- ✅ 简单的动作序列播放
- ✅ 基本的时间轴编辑器
- ✅ 单机器狗动作执行
- ✅ 音乐文件导入和节拍检测
- ✅ 简单的GUI界面

## 🚀 开发阶段规划

### 第1周：核心基础建设

#### Day 1-2: 数据结构和动作引擎
```python
# 文件: dance_mvp/core/action_types.py
from dataclasses import dataclass
from typing import List, Dict
import json
import time

@dataclass
class SimplePose:
    """简化的姿态数据"""
    body_height: float = 0.25
    pitch: float = 0.0
    roll: float = 0.0
    yaw: float = 0.0
    x: float = 0.0
    y: float = 0.0

@dataclass
class SimpleKeyframe:
    """简化的关键帧"""
    time: float  # 相对时间(秒)
    pose: SimplePose

@dataclass
class SimpleAction:
    """简化的动作定义"""
    name: str
    duration: float
    keyframes: List[SimpleKeyframe]
    
    def to_dict(self):
        return {
            'name': self.name,
            'duration': self.duration,
            'keyframes': [
                {
                    'time': kf.time,
                    'pose': {
                        'body_height': kf.pose.body_height,
                        'pitch': kf.pose.pitch,
                        'roll': kf.pose.roll,
                        'yaw': kf.pose.yaw,
                        'x': kf.pose.x,
                        'y': kf.pose.y
                    }
                } for kf in self.keyframes
            ]
        }
    
    @classmethod
    def from_dict(cls, data):
        keyframes = []
        for kf_data in data['keyframes']:
            pose = SimplePose(**kf_data['pose'])
            keyframe = SimpleKeyframe(kf_data['time'], pose)
            keyframes.append(keyframe)
        
        return cls(data['name'], data['duration'], keyframes)

# 文件: dance_mvp/core/action_engine.py
class SimpleActionEngine:
    """简化的动作执行引擎"""
    
    def __init__(self):
        self.is_playing = False
        self.current_time = 0.0
        self.start_time = None
        
    def linear_interpolate(self, pose1: SimplePose, pose2: SimplePose, t: float) -> SimplePose:
        """线性插值计算姿态"""
        return SimplePose(
            body_height=pose1.body_height + (pose2.body_height - pose1.body_height) * t,
            pitch=pose1.pitch + (pose2.pitch - pose1.pitch) * t,
            roll=pose1.roll + (pose2.roll - pose1.roll) * t,
            yaw=pose1.yaw + (pose2.yaw - pose1.yaw) * t,
            x=pose1.x + (pose2.x - pose1.x) * t,
            y=pose1.y + (pose2.y - pose1.y) * t
        )
    
    def get_pose_at_time(self, action: SimpleAction, time: float) -> SimplePose:
        """获取动作在指定时间的姿态"""
        if time >= action.duration:
            return action.keyframes[-1].pose
        if time <= 0:
            return action.keyframes[0].pose
        
        # 找到前后两个关键帧
        for i in range(len(action.keyframes) - 1):
            kf1 = action.keyframes[i]
            kf2 = action.keyframes[i + 1]
            
            if kf1.time <= time <= kf2.time:
                # 计算插值比例
                duration = kf2.time - kf1.time
                if duration == 0:
                    return kf1.pose
                
                t = (time - kf1.time) / duration
                return self.linear_interpolate(kf1.pose, kf2.pose, t)
        
        return action.keyframes[-1].pose
    
    def start_action(self, action: SimpleAction):
        """开始播放动作"""
        self.is_playing = True
        self.start_time = time.time()
        self.current_action = action
    
    def stop_action(self):
        """停止播放动作"""
        self.is_playing = False
        self.start_time = None
    
    def update(self) -> SimplePose:
        """更新并返回当前姿态"""
        if not self.is_playing or not self.start_time:
            return SimplePose()
        
        elapsed = time.time() - self.start_time
        if elapsed >= self.current_action.duration:
            self.stop_action()
            return self.current_action.keyframes[-1].pose
        
        return self.get_pose_at_time(self.current_action, elapsed)
```

#### Day 3-4: 基础动作库
```python
# 文件: dance_mvp/data/create_basic_actions.py
from core.action_types import SimpleAction, SimpleKeyframe, SimplePose
import json
import os

def create_basic_dance_moves():
    """创建基础舞蹈动作库"""
    
    actions = []
    
    # 1. 点头动作
    nod = SimpleAction(
        name="点头",
        duration=2.0,
        keyframes=[
            SimpleKeyframe(0.0, SimplePose(body_height=0.25, pitch=0.0)),
            SimpleKeyframe(0.5, SimplePose(body_height=0.25, pitch=-0.3)),
            SimpleKeyframe(1.0, SimplePose(body_height=0.25, pitch=0.0)),
            SimpleKeyframe(1.5, SimplePose(body_height=0.25, pitch=-0.3)),
            SimpleKeyframe(2.0, SimplePose(body_height=0.25, pitch=0.0))
        ]
    )
    actions.append(nod)
    
    # 2. 摇头动作
    shake_head = SimpleAction(
        name="摇头",
        duration=2.0,
        keyframes=[
            SimpleKeyframe(0.0, SimplePose(body_height=0.25, yaw=0.0)),
            SimpleKeyframe(0.5, SimplePose(body_height=0.25, yaw=0.5)),
            SimpleKeyframe(1.0, SimplePose(body_height=0.25, yaw=0.0)),
            SimpleKeyframe(1.5, SimplePose(body_height=0.25, yaw=-0.5)),
            SimpleKeyframe(2.0, SimplePose(body_height=0.25, yaw=0.0))
        ]
    )
    actions.append(shake_head)
    
    # 3. 跳跃动作
    jump = SimpleAction(
        name="跳跃",
        duration=1.5,
        keyframes=[
            SimpleKeyframe(0.0, SimplePose(body_height=0.25)),
            SimpleKeyframe(0.3, SimplePose(body_height=0.15)),  # 下蹲
            SimpleKeyframe(0.6, SimplePose(body_height=0.35)),  # 跳起
            SimpleKeyframe(1.0, SimplePose(body_height=0.15)),  # 落地
            SimpleKeyframe(1.5, SimplePose(body_height=0.25))   # 恢复
        ]
    )
    actions.append(jump)
    
    # 4. 侧摆动作
    sway = SimpleAction(
        name="侧摆",
        duration=3.0,
        keyframes=[
            SimpleKeyframe(0.0, SimplePose(body_height=0.25, roll=0.0)),
            SimpleKeyframe(0.75, SimplePose(body_height=0.25, roll=0.3)),
            SimpleKeyframe(1.5, SimplePose(body_height=0.25, roll=0.0)),
            SimpleKeyframe(2.25, SimplePose(body_height=0.25, roll=-0.3)),
            SimpleKeyframe(3.0, SimplePose(body_height=0.25, roll=0.0))
        ]
    )
    actions.append(sway)
    
    # 5. 圆周运动
    circle = SimpleAction(
        name="圆周运动",
        duration=4.0,
        keyframes=[
            SimpleKeyframe(0.0, SimplePose(x=0.0, y=0.0)),
            SimpleKeyframe(1.0, SimplePose(x=0.5, y=0.0)),
            SimpleKeyframe(2.0, SimplePose(x=0.0, y=0.5)),
            SimpleKeyframe(3.0, SimplePose(x=-0.5, y=0.0)),
            SimpleKeyframe(4.0, SimplePose(x=0.0, y=0.0))
        ]
    )
    actions.append(circle)
    
    # 保存到文件
    os.makedirs('data/actions', exist_ok=True)
    for action in actions:
        filename = f"data/actions/{action.name}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(action.to_dict(), f, indent=2, ensure_ascii=False)
    
    print(f"已创建 {len(actions)} 个基础动作")
    return actions

if __name__ == "__main__":
    create_basic_dance_moves()
```

#### Day 5-6: 动作序列管理
```python
# 文件: dance_mvp/core/sequence_manager.py
from typing import List, Tuple
from .action_types import SimpleAction
import json
import os

class ActionSequence:
    """动作序列管理类"""
    
    def __init__(self, name: str = "Untitled Sequence"):
        self.name = name
        self.sequence: List[Tuple[float, SimpleAction]] = []  # (start_time, action)
        self.total_duration = 0.0
    
    def add_action(self, start_time: float, action: SimpleAction):
        """添加动作到序列"""
        self.sequence.append((start_time, action))
        self.sequence.sort(key=lambda x: x[0])  # 按时间排序
        
        # 更新总时长
        end_time = start_time + action.duration
        self.total_duration = max(self.total_duration, end_time)
    
    def remove_action(self, index: int):
        """移除动作"""
        if 0 <= index < len(self.sequence):
            self.sequence.pop(index)
            self._recalculate_duration()
    
    def get_active_actions_at_time(self, time: float) -> List[Tuple[SimpleAction, float]]:
        """获取指定时间正在执行的动作"""
        active_actions = []
        
        for start_time, action in self.sequence:
            end_time = start_time + action.duration
            
            if start_time <= time <= end_time:
                relative_time = time - start_time
                active_actions.append((action, relative_time))
        
        return active_actions
    
    def _recalculate_duration(self):
        """重新计算总时长"""
        self.total_duration = 0.0
        for start_time, action in self.sequence:
            end_time = start_time + action.duration
            self.total_duration = max(self.total_duration, end_time)
    
    def to_dict(self):
        """序列化为字典"""
        return {
            'name': self.name,
            'total_duration': self.total_duration,
            'sequence': [
                {
                    'start_time': start_time,
                    'action': action.to_dict()
                }
                for start_time, action in self.sequence
            ]
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典反序列化"""
        sequence = cls(data['name'])
        
        for item in data['sequence']:
            action = SimpleAction.from_dict(item['action'])
            sequence.add_action(item['start_time'], action)
        
        return sequence
    
    def save_to_file(self, filepath: str):
        """保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str):
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

class ActionLibrary:
    """动作库管理类"""
    
    def __init__(self, actions_dir: str = "data/actions"):
        self.actions_dir = actions_dir
        self.actions: Dict[str, SimpleAction] = {}
        self.load_all_actions()
    
    def load_all_actions(self):
        """加载所有动作文件"""
        if not os.path.exists(self.actions_dir):
            return
        
        for filename in os.listdir(self.actions_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.actions_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    action = SimpleAction.from_dict(data)
                    self.actions[action.name] = action
                except Exception as e:
                    print(f"加载动作文件失败 {filename}: {e}")
    
    def get_action(self, name: str) -> SimpleAction:
        """获取指定名称的动作"""
        return self.actions.get(name)
    
    def get_all_action_names(self) -> List[str]:
        """获取所有动作名称"""
        return list(self.actions.keys())
    
    def add_action(self, action: SimpleAction):
        """添加新动作"""
        self.actions[action.name] = action
        
        # 保存到文件
        filepath = os.path.join(self.actions_dir, f"{action.name}.json")
        os.makedirs(self.actions_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(action.to_dict(), f, indent=2, ensure_ascii=False)
```

#### Day 7: 简单音频支持
```python
# 文件: dance_mvp/audio/simple_audio.py
import pygame
import librosa
import numpy as np
from typing import List, Optional

class SimpleAudioManager:
    """简化的音频管理器"""
    
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.current_music = None
        self.is_playing = False
        self.beats = []
        self.tempo = 120.0
        
    def load_music(self, filepath: str) -> bool:
        """加载音乐文件"""
        try:
            pygame.mixer.music.load(filepath)
            self.current_music = filepath
            
            # 简单的节拍检测
            self._analyze_beats(filepath)
            return True
        except Exception as e:
            print(f"加载音乐失败: {e}")
            return False
    
    def _analyze_beats(self, filepath: str):
        """分析音乐节拍"""
        try:
            # 使用librosa进行节拍检测
            y, sr = librosa.load(filepath, sr=22050)
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            self.tempo = tempo
            self.beats = librosa.frames_to_time(beats, sr=sr).tolist()
            
            print(f"检测到节拍: BPM={tempo:.1f}, 节拍点数={len(self.beats)}")
        except Exception as e:
            print(f"节拍分析失败: {e}")
            # 使用默认值
            self.tempo = 120.0
            self.beats = []
    
    def play_music(self):
        """播放音乐"""
        if self.current_music:
            pygame.mixer.music.play()
            self.is_playing = True
    
    def stop_music(self):
        """停止音乐"""
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def pause_music(self):
        """暂停音乐"""
        pygame.mixer.music.pause()
        self.is_playing = False
    
    def resume_music(self):
        """恢复播放"""
        pygame.mixer.music.unpause()
        self.is_playing = True
    
    def get_nearest_beat(self, time: float) -> float:
        """获取最近的节拍点"""
        if not self.beats:
            return time
        
        nearest_beat = min(self.beats, key=lambda x: abs(x - time))
        return nearest_beat
    
    def get_beat_times(self) -> List[float]:
        """获取所有节拍时间点"""
        return self.beats.copy()
```

### 第2周：GUI界面和集成

#### Day 8-10: 基础GUI界面
```python
# 文件: dance_mvp/ui/main_window.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from core.action_engine import SimpleActionEngine
from core.sequence_manager import ActionLibrary, ActionSequence
from audio.simple_audio import SimpleAudioManager
from robodog import Dog, UserMode

class SimpleDanceGUI:
    """简化的跳舞GUI界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("机器狗跳舞 MVP v1.0")
        self.root.geometry("1000x700")
        
        # 核心组件
        self.action_engine = SimpleActionEngine()
        self.action_library = ActionLibrary()
        self.audio_manager = SimpleAudioManager()
        self.current_sequence = ActionSequence("新建序列")
        
        # 机器狗连接
        self.dog = None
        self.connected = False
        self.is_performing = False
        
        # 界面组件
        self.setup_ui()
        
        # 控制线程
        self.control_thread = None
        self.running = False
    
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 左侧面板
        self.setup_left_panel(main_frame)
        
        # 右侧面板
        self.setup_right_panel(main_frame)
        
        # 底部控制面板
        self.setup_bottom_panel(main_frame)
    
    def setup_left_panel(self, parent):
        """设置左侧面板"""
        left_frame = ttk.Frame(parent, width=300)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 机器狗连接
        conn_frame = ttk.LabelFrame(left_frame, text="机器狗连接", padding="10")
        conn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(conn_frame, text="IP地址:").grid(row=0, column=0, sticky="w")
        self.ip_var = tk.StringVar(value="192.168.118.29")
        ttk.Entry(conn_frame, textvariable=self.ip_var, width=20).grid(row=0, column=1, padx=(5, 10))
        
        self.connect_btn = ttk.Button(conn_frame, text="连接", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=2)
        
        self.status_label = ttk.Label(conn_frame, text="未连接", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        # 动作库
        library_frame = ttk.LabelFrame(left_frame, text="动作库", padding="10")
        library_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # 动作列表
        self.action_listbox = tk.Listbox(library_frame, height=8)
        self.action_listbox.pack(fill="both", expand=True, pady=(0, 10))
        
        # 刷新动作库
        self.refresh_action_library()
        
        # 动作控制按钮
        action_btn_frame = ttk.Frame(library_frame)
        action_btn_frame.pack(fill="x")
        
        ttk.Button(action_btn_frame, text="预览动作", 
                  command=self.preview_selected_action).pack(side="left", padx=(0, 5))
        ttk.Button(action_btn_frame, text="添加到序列", 
                  command=self.add_action_to_sequence).pack(side="left")
        
        # 音乐控制
        music_frame = ttk.LabelFrame(left_frame, text="音乐控制", padding="10")
        music_frame.pack(fill="x")
        
        ttk.Button(music_frame, text="加载音乐", 
                  command=self.load_music).pack(side="left", padx=(0, 5))
        ttk.Button(music_frame, text="播放", 
                  command=self.play_music).pack(side="left", padx=(0, 5))
        ttk.Button(music_frame, text="停止", 
                  command=self.stop_music).pack(side="left")
    
    def setup_right_panel(self, parent):
        """设置右侧面板"""
        right_frame = ttk.Frame(parent)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # 序列编辑器
        sequence_frame = ttk.LabelFrame(right_frame, text="动作序列编辑", padding="10")
        sequence_frame.pack(fill="both", expand=True)
        sequence_frame.columnconfigure(0, weight=1)
        sequence_frame.rowconfigure(1, weight=1)
        
        # 序列信息
        info_frame = ttk.Frame(sequence_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(info_frame, text="序列名称:").grid(row=0, column=0, sticky="w")
        self.sequence_name_var = tk.StringVar(value=self.current_sequence.name)
        ttk.Entry(info_frame, textvariable=self.sequence_name_var, width=30).grid(row=0, column=1, padx=(5, 10))
        
        self.duration_label = ttk.Label(info_frame, text="总时长: 0.0s")
        self.duration_label.grid(row=0, column=2)
        
        # 序列列表
        sequence_list_frame = ttk.Frame(sequence_frame)
        sequence_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        sequence_list_frame.columnconfigure(0, weight=1)
        sequence_list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview显示序列
        columns = ("开始时间", "动作名称", "持续时间")
        self.sequence_tree = ttk.Treeview(sequence_list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.sequence_tree.heading(col, text=col)
            self.sequence_tree.column(col, width=100)
        
        self.sequence_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(sequence_list_frame, orient="vertical", command=self.sequence_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.sequence_tree.configure(yscrollcommand=scrollbar.set)
        
        # 序列控制按钮
        seq_btn_frame = ttk.Frame(sequence_frame)
        seq_btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(seq_btn_frame, text="删除选中", 
                  command=self.remove_selected_from_sequence).pack(side="left", padx=(0, 5))
        ttk.Button(seq_btn_frame, text="清空序列", 
                  command=self.clear_sequence).pack(side="left", padx=(0, 5))
        ttk.Button(seq_btn_frame, text="保存序列", 
                  command=self.save_sequence).pack(side="left", padx=(0, 5))
        ttk.Button(seq_btn_frame, text="加载序列", 
                  command=self.load_sequence).pack(side="left")
    
    def setup_bottom_panel(self, parent):
        """设置底部控制面板"""
        bottom_frame = ttk.Frame(parent)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 演出控制
        performance_frame = ttk.LabelFrame(bottom_frame, text="演出控制", padding="10")
        performance_frame.pack(fill="x")
        
        self.start_btn = ttk.Button(performance_frame, text="开始演出", 
                                   command=self.start_performance, state="disabled")
        self.start_btn.pack(side="left", padx=(0, 10))
        
        self.stop_btn = ttk.Button(performance_frame, text="停止演出", 
                                  command=self.stop_performance, state="disabled")
        self.stop_btn.pack(side="left", padx=(0, 10))
        
        ttk.Button(performance_frame, text="紧急停止", 
                  command=self.emergency_stop).pack(side="left", padx=(0, 10))
        
        # 状态显示
        self.performance_status = ttk.Label(performance_frame, text="状态: 待机")
        self.performance_status.pack(side="right")
    
    # 事件处理方法
    def toggle_connection(self):
        """切换机器狗连接状态"""
        if not self.connected:
            self.connect_to_dog()
        else:
            self.disconnect_from_dog()
    
    def connect_to_dog(self):
        """连接到机器狗"""
        try:
            ip = self.ip_var.get()
            self.dog = Dog(host=ip)
            self.dog.__enter__()
            self.dog.set_user_mode(UserMode.NORMAL)
            
            self.connected = True
            self.connect_btn.configure(text="断开连接")
            self.status_label.configure(text="已连接", foreground="green")
            self.start_btn.configure(state="normal")
            
            messagebox.showinfo("连接成功", f"已成功连接到机器狗 {ip}")
            
        except Exception as e:
            messagebox.showerror("连接失败", f"无法连接到机器狗: {e}")
    
    def disconnect_from_dog(self):
        """断开机器狗连接"""
        if self.is_performing:
            self.stop_performance()
        
        if self.dog:
            try:
                self.dog.vx = 0.0
                self.dog.vy = 0.0
                self.dog.wz = 0.0
                self.dog.body_height = 0.25
                self.dog.__exit__(None, None, None)
            except:
                pass
            finally:
                self.dog = None
        
        self.connected = False
        self.connect_btn.configure(text="连接")
        self.status_label.configure(text="未连接", foreground="red")
        self.start_btn.configure(state="disabled")
    
    def refresh_action_library(self):
        """刷新动作库列表"""
        self.action_listbox.delete(0, tk.END)
        for action_name in self.action_library.get_all_action_names():
            self.action_listbox.insert(tk.END, action_name)
    
    def preview_selected_action(self):
        """预览选中的动作"""
        selection = self.action_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个动作")
            return
        
        action_name = self.action_listbox.get(selection[0])
        action = self.action_library.get_action(action_name)
        
        if action and self.connected and not self.is_performing:
            # 启动预览线程
            thread = threading.Thread(target=self._preview_action_thread, args=(action,))
            thread.daemon = True
            thread.start()
    
    def _preview_action_thread(self, action):
        """预览动作的线程函数"""
        self.action_engine.start_action(action)
        
        while self.action_engine.is_playing:
            pose = self.action_engine.update()
            
            if self.dog and self.connected:
                try:
                    self.dog.body_height = pose.body_height
                    self.dog.roll = pose.roll
                    self.dog.pitch = pose.pitch
                    self.dog.yaw = pose.yaw
                    self.dog.vx = pose.x * 0.1  # 降低移动速度
                    self.dog.vy = pose.y * 0.1
                except:
                    break
            
            time.sleep(0.05)  # 20Hz更新频率
        
        # 重置姿态
        if self.dog and self.connected:
            try:
                self.dog.body_height = 0.25
                self.dog.roll = 0.0
                self.dog.pitch = 0.0
                self.dog.yaw = 0.0
                self.dog.vx = 0.0
                self.dog.vy = 0.0
                self.dog.wz = 0.0
            except:
                pass
    
    def add_action_to_sequence(self):
        """将选中的动作添加到序列"""
        selection = self.action_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个动作")
            return
        
        action_name = self.action_listbox.get(selection[0])
        action = self.action_library.get_action(action_name)
        
        if action:
            # 添加到序列末尾
            start_time = self.current_sequence.total_duration
            self.current_sequence.add_action(start_time, action)
            self.refresh_sequence_display()
    
    def refresh_sequence_display(self):
        """刷新序列显示"""
        # 清空现有项目
        for item in self.sequence_tree.get_children():
            self.sequence_tree.delete(item)
        
        # 添加序列项目
        for start_time, action in self.current_sequence.sequence:
            self.sequence_tree.insert("", "end", values=(
                f"{start_time:.1f}s",
                action.name,
                f"{action.duration:.1f}s"
            ))
        
        # 更新总时长
        self.duration_label.configure(text=f"总时长: {self.current_sequence.total_duration:.1f}s")
    
    def remove_selected_from_sequence(self):
        """从序列中删除选中项"""
        selection = self.sequence_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的项目")
            return
        
        # 获取选中项的索引
        item = selection[0]
        index = self.sequence_tree.index(item)
        
        self.current_sequence.remove_action(index)
        self.refresh_sequence_display()
    
    def clear_sequence(self):
        """清空序列"""
        if messagebox.askyesno("确认", "确定要清空整个序列吗？"):
            self.current_sequence = ActionSequence("新建序列")
            self.sequence_name_var.set("新建序列")
            self.refresh_sequence_display()
    
    def save_sequence(self):
        """保存序列到文件"""
        filename = filedialog.asksaveasfilename(
            title="保存动作序列",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_sequence.name = self.sequence_name_var.get()
                self.current_sequence.save_to_file(filename)
                messagebox.showinfo("保存成功", f"序列已保存到 {filename}")
            except Exception as e:
                messagebox.showerror("保存失败", f"无法保存序列: {e}")
    
    def load_sequence(self):
        """从文件加载序列"""
        filename = filedialog.askopenfilename(
            title="加载动作序列",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_sequence = ActionSequence.load_from_file(filename)
                self.sequence_name_var.set(self.current_sequence.name)
                self.refresh_sequence_display()
                messagebox.showinfo("加载成功", f"序列已从 {filename} 加载")
            except Exception as e:
                messagebox.showerror("加载失败", f"无法加载序列: {e}")
    
    def load_music(self):
        """加载音乐文件"""
        filename = filedialog.askopenfilename(
            title="选择音乐文件",
            filetypes=[
                ("音频文件", "*.mp3 *.wav *.ogg"),
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("OGG files", "*.ogg"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            if self.audio_manager.load_music(filename):
                messagebox.showinfo("加载成功", f"音乐文件已加载\nBPM: {self.audio_manager.tempo:.1f}")
            else:
                messagebox.showerror("加载失败", "无法加载音乐文件")
    
    def play_music(self):
        """播放音乐"""
        self.audio_manager.play_music()
    
    def stop_music(self):
        """停止音乐"""
        self.audio_manager.stop_music()
    
    def start_performance(self):
        """开始演出"""
        if not self.connected:
            messagebox.showwarning("警告", "请先连接机器狗")
            return
        
        if not self.current_sequence.sequence:
            messagebox.showwarning("警告", "序列为空，请先添加动作")
            return
        
        self.is_performing = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.performance_status.configure(text="状态: 演出中")
        
        # 启动演出线程
        self.running = True
        self.control_thread = threading.Thread(target=self._performance_thread)
        self.control_thread.daemon = True
        self.control_thread.start()
    
    def _performance_thread(self):
        """演出控制线程"""
        start_time = time.time()
        
        while self.running and self.is_performing:
            current_time = time.time() - start_time
            
            # 检查是否演出结束
            if current_time >= self.current_sequence.total_duration:
                break
            
            # 获取当前时间的活跃动作
            active_actions = self.current_sequence.get_active_actions_at_time(current_time)
            
            if active_actions and self.dog and self.connected:
                # 简单合并多个动作（取平均值）
                total_height = 0.0
                total_roll = 0.0
                total_pitch = 0.0
                total_yaw = 0.0
                total_x = 0.0
                total_y = 0.0
                count = len(active_actions)
                
                for action, relative_time in active_actions:
                    pose = self.action_engine.get_pose_at_time(action, relative_time)
                    total_height += pose.body_height
                    total_roll += pose.roll
                    total_pitch += pose.pitch
                    total_yaw += pose.yaw
                    total_x += pose.x
                    total_y += pose.y
                
                if count > 0:
                    avg_pose = SimplePose(
                        body_height=total_height / count,
                        roll=total_roll / count,
                        pitch=total_pitch / count,
                        yaw=total_yaw / count,
                        x=total_x / count,
                        y=total_y / count
                    )
                    
                    try:
                        self.dog.body_height = avg_pose.body_height
                        self.dog.roll = avg_pose.roll
                        self.dog.pitch = avg_pose.pitch
                        self.dog.yaw = avg_pose.yaw
                        self.dog.vx = avg_pose.x * 0.1
                        self.dog.vy = avg_pose.y * 0.1
                    except Exception as e:
                        print(f"控制错误: {e}")
                        break
            
            time.sleep(0.05)  # 20Hz更新频率
        
        # 演出结束，重置状态
        self.stop_performance()
    
    def stop_performance(self):
        """停止演出"""
        self.running = False
        self.is_performing = False
        
        # 重置机器狗姿态
        if self.dog and self.connected:
            try:
                self.dog.body_height = 0.25
                self.dog.roll = 0.0
                self.dog.pitch = 0.0
                self.dog.yaw = 0.0
                self.dog.vx = 0.0
                self.dog.vy = 0.0
                self.dog.wz = 0.0
            except:
                pass
        
        # 更新界面状态
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.performance_status.configure(text="状态: 待机")
    
    def emergency_stop(self):
        """紧急停止"""
        self.stop_performance()
        self.stop_music()
        
        if self.dog and self.connected:
            try:
                self.dog.vx = 0.0
                self.dog.vy = 0.0
                self.dog.wz = 0.0
            except:
                pass
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()
    
    def __del__(self):
        """析构函数"""
        if self.connected:
            self.disconnect_from_dog()

# 主入口
if __name__ == "__main__":
    app = SimpleDanceGUI()
    app.run()
```

#### Day 11-12: 测试和优化
- 创建测试用例
- 修复发现的bug
- 优化性能和用户体验

#### Day 13-14: 文档和演示
- 编写用户手册
- 录制演示视频
- 准备展示材料

## 🎯 MVP期望成果

### 功能演示场景
1. **基础动作演示**: 机器狗执行点头、摇头、跳跃等基本动作
2. **序列编排**: 用户可以拖拽创建一个包含3-5个动作的序列
3. **音乐同步**: 播放音乐并让机器狗按节拍执行动作
4. **完整演出**: 机器狗执行一段30秒的完整舞蹈表演

### 技术验证目标
- ✅ 动作定义和插值算法可行性
- ✅ 时间轴编辑的用户体验
- ✅ 音乐节拍检测的准确性
- ✅ 机器狗控制的稳定性

### 用户反馈收集
- 界面易用性评估
- 动作编排效率测试
- 系统稳定性验证
- 功能扩展需求调研

## 🚀 后续迭代方向

### 根据MVP反馈的可能改进方向

#### 短期改进 (1-2周)
- 增加更多预设动作
- 改进动作过渡的平滑度
- 优化时间轴编辑器的交互
- 添加动作预览的3D可视化

#### 中期扩展 (1-2个月)
- 实现多机器狗同步控制
- 添加更复杂的编排功能
- 集成更高级的音频分析
- 开发动作自动生成算法

#### 长期目标 (3-6个月)
- 商业化的完整跳舞系统
- 云端动作库和分享平台
- AI驱动的个性化编排
- 与其他表演设备的集成

## 📋 开发检查清单

### Week 1 完成标准
- [ ] 动作数据结构定义完成
- [ ] 基础动作执行引擎工作正常
- [ ] 5个以上预设动作创建完成
- [ ] 动作序列管理功能实现
- [ ] 简单音频加载和节拍检测

### Week 2 完成标准
- [ ] GUI界面基本功能完整
- [ ] 机器狗连接和控制正常
- [ ] 动作预览功能工作正常
- [ ] 序列编排和保存功能
- [ ] 完整演出流程测试通过

### MVP演示标准
- [ ] 能够流畅演示完整的工作流程
- [ ] 机器狗能够执行流畅的舞蹈动作
- [ ] 系统运行稳定，无重大bug
- [ ] 用户能够在10分钟内学会基本操作
- [ ] 具备足够的扩展性以支持后续开发

这个MVP开发指南为你提供了一个快速实现机器狗跳舞功能的路径。建议严格按照时间计划执行，优先保证核心功能的完整性，然后再考虑细节优化。

你觉得这个开发计划怎么样？有哪些地方需要调整或者你想先从哪个部分开始实现？
