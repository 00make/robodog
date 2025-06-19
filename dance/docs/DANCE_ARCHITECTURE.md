# 机器狗跳舞系统技术架构详细设计

## 🏗️ 系统架构概览

### 分层架构设计

```
┌─────────────────────────────────────────────────────────┐
│                  用户界面层 (UI Layer)                    │
├─────────────────────────────────────────────────────────┤
│    跳舞编排界面  │  多机控制台  │  实时监控  │  动作预览   │
├─────────────────────────────────────────────────────────┤
│                 应用服务层 (Service Layer)                │
├─────────────────────────────────────────────────────────┤
│ 编排服务 │ 同步服务 │ 音频服务 │ 动作库服务 │ 网络服务    │
├─────────────────────────────────────────────────────────┤
│                 核心业务层 (Core Layer)                   │
├─────────────────────────────────────────────────────────┤
│ 动作引擎 │ 时间轴  │ 插值器  │ 同步器    │ 编队管理      │
├─────────────────────────────────────────────────────────┤
│                 数据访问层 (Data Layer)                   │
├─────────────────────────────────────────────────────────┤
│ 动作文件 │ 配置文件 │ 音乐文件 │ 日志文件 │ 缓存数据     │
├─────────────────────────────────────────────────────────┤
│                 硬件抽象层 (HAL)                          │
└─────────────────────────────────────────────────────────┘
│  机器狗A  │  机器狗B  │  机器狗C  │  音响设备  │  输入设备   │
```

## 🎯 核心组件详细设计

### 1. 动作执行引擎 (ActionEngine)

#### 1.1 设计目标
- 高精度姿态控制 (±1mm精度)
- 平滑动作过渡 (60Hz更新频率)
- 实时动作调整能力
- 多机器狗并发执行

#### 1.2 核心类设计

```python
class ActionEngine:
    """动作执行引擎核心类"""
    
    def __init__(self):
        self.interpolator = PoseInterpolator()
        self.executor = MotionExecutor()
        self.timeline = Timeline()
        self.sync_manager = SyncManager()
    
    async def execute_sequence(self, sequence: ActionSequence, dogs: List[RoboDog]):
        """执行动作序列"""
        # 预处理和验证
        validated_sequence = self.validate_sequence(sequence)
        
        # 多机器狗并发执行
        tasks = []
        for dog in dogs:
            task = self.execute_for_dog(validated_sequence, dog)
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    
    def calculate_pose_at_time(self, time: float, action: Action) -> Pose:
        """计算指定时间的姿态"""
        return self.interpolator.interpolate(action, time)
```

#### 1.3 插值算法设计

**支持的插值类型**:
- **线性插值**: 简单直线过渡
- **贝塞尔曲线**: 平滑曲线运动  
- **样条插值**: 高阶平滑过渡
- **物理模拟**: 重力和惯性考虑

```python
class PoseInterpolator:
    def interpolate(self, action: Action, time: float) -> Pose:
        # 找到时间点前后的关键帧
        prev_frame, next_frame = self.find_keyframes(action, time)
        
        # 根据插值类型计算姿态
        if action.interpolation_type == "linear":
            return self.linear_interpolate(prev_frame, next_frame, time)
        elif action.interpolation_type == "bezier":
            return self.bezier_interpolate(prev_frame, next_frame, time)
        # ... 其他插值类型
```

### 2. 时间轴管理系统 (Timeline)

#### 2.1 时间轴数据结构

```python
class Timeline:
    """时间轴管理类"""
    
    def __init__(self, duration: float = 60.0):
        self.duration = duration  # 总时长
        self.tracks = {}  # 多轨道字典
        self.current_time = 0.0
        self.is_playing = False
        self.loop_enabled = False
    
    def add_track(self, track_id: str, track_type: TrackType):
        """添加轨道"""
        self.tracks[track_id] = Track(track_id, track_type)
    
    def add_action_to_track(self, track_id: str, start_time: float, action: Action):
        """在指定轨道添加动作"""
        if track_id in self.tracks:
            self.tracks[track_id].add_action(start_time, action)
```

#### 2.2 多轨道支持

**轨道类型**:
- **主体轨道**: 整体移动和姿态
- **头部轨道**: 头部独立动作
- **尾部轨道**: 尾巴摆动
- **腿部轨道**: 步态和姿势
- **音频轨道**: 音乐和音效

### 3. 多机器狗同步系统

#### 3.1 网络架构设计

```
指挥中心 (Master Node)
    ├── 同步时钟服务器
    ├── 动作分发服务器  
    ├── 状态监控服务器
    └── 应急控制服务器
         │
    WebSocket连接
         │
┌────────┴────────┐
│  机器狗节点群组  │
├─────────────────┤
│ Dog_A │ Dog_B  │
│ Dog_C │ Dog_D  │
└─────────────────┘
```

#### 3.2 同步协议设计

**时间同步机制**:
```python
class SyncProtocol:
    def __init__(self):
        self.master_clock = MasterClock()
        self.sync_offset = 0.0  # 时间偏移
        self.latency_compensation = 0.0  # 延迟补偿
    
    async def sync_time_with_master(self):
        """与主节点同步时间"""
        start_time = time.time()
        response = await self.send_sync_request()
        end_time = time.time()
        
        # 计算网络延迟
        latency = (end_time - start_time) / 2
        
        # 计算时间偏移
        master_time = response['timestamp']
        local_time = (start_time + end_time) / 2
        self.sync_offset = master_time - local_time
        self.latency_compensation = latency
```

#### 3.3 编队管理系统

```python
class FormationManager:
    """编队管理器"""
    
    def __init__(self):
        self.formation_config = FormationConfig()
        self.dog_positions = {}  # 机器狗位置映射
        self.collision_detector = CollisionDetector()
    
    def setup_formation(self, formation_type: str, dogs: List[RoboDog]):
        """设置编队"""
        if formation_type == "line":
            self.setup_line_formation(dogs)
        elif formation_type == "circle":
            self.setup_circle_formation(dogs)
        elif formation_type == "square":
            self.setup_square_formation(dogs)
    
    def check_collisions(self) -> List[CollisionWarning]:
        """检查碰撞风险"""
        warnings = []
        positions = self.get_all_positions()
        
        for i, pos_a in enumerate(positions):
            for j, pos_b in enumerate(positions[i+1:], i+1):
                distance = self.calculate_distance(pos_a, pos_b)
                if distance < self.min_safe_distance:
                    warnings.append(CollisionWarning(i, j, distance))
        
        return warnings
```

### 4. 音乐同步系统

#### 4.1 音频分析组件

```python
import librosa
import numpy as np

class AudioAnalyzer:
    """音频分析器"""
    
    def __init__(self):
        self.sample_rate = 22050
        self.hop_length = 512
    
    def analyze_music(self, audio_file: str) -> MusicAnalysis:
        """分析音乐文件"""
        # 加载音频
        y, sr = librosa.load(audio_file, sr=self.sample_rate)
        
        # 检测节拍
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
        
        # 检测音调变化
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # 检测能量变化
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        
        return MusicAnalysis(
            tempo=tempo,
            beats=beats,
            duration=len(y) / sr,
            chroma=chroma,
            energy=spectral_centroids
        )
    
    def get_beat_times(self, beats: np.ndarray) -> List[float]:
        """获取节拍时间点"""
        return librosa.frames_to_time(beats, sr=self.sample_rate, hop_length=self.hop_length)
```

#### 4.2 节拍同步算法

```python
class BeatSyncManager:
    """节拍同步管理器"""
    
    def __init__(self):
        self.audio_analyzer = AudioAnalyzer()
        self.sync_tolerance = 0.05  # 50ms同步容差
    
    def sync_actions_to_beats(self, sequence: ActionSequence, music: MusicAnalysis):
        """将动作同步到音乐节拍"""
        beat_times = music.beat_times
        synced_sequence = ActionSequence()
        
        for action in sequence.actions:
            # 找到最近的节拍点
            closest_beat = self.find_closest_beat(action.start_time, beat_times)
            
            # 调整动作开始时间
            adjusted_action = action.copy()
            adjusted_action.start_time = closest_beat
            
            synced_sequence.add_action(adjusted_action)
        
        return synced_sequence
```

## 🎨 用户界面设计

### 1. 主界面布局

```python
class DanceStudioGUI:
    """跳舞工作室主界面"""
    
    def __init__(self):
        self.setup_layout()
        self.timeline_editor = TimelineEditor()
        self.action_library = ActionLibraryWidget()
        self.multi_dog_panel = MultiDogControlPanel()
        self.preview_window = PreviewWindow()
    
    def setup_layout(self):
        """设置界面布局"""
        # 主要区域布局
        # ┌─────────────┬───────────────┐
        # │  动作库     │   3D预览窗口   │
        # ├─────────────┼───────────────┤  
        # │  时间轴编辑器（跨越两列）      │
        # ├─────────────┬───────────────┤
        # │  多机控制   │   状态监控     │
        # └─────────────┴───────────────┘
```

### 2. 时间轴编辑器界面

**功能特性**:
- 拖拽式动作编排
- 多轨道并行编辑
- 实时预览播放
- 缩放和导航
- 关键帧精确编辑

```python
class TimelineEditor(QWidget):
    """时间轴编辑器组件"""
    
    def __init__(self):
        super().__init__()
        self.zoom_level = 1.0
        self.current_time = 0.0
        self.selection = []
        self.setup_ui()
    
    def paintEvent(self, event):
        """绘制时间轴"""
        painter = QPainter(self)
        
        # 绘制时间刻度
        self.draw_time_ruler(painter)
        
        # 绘制轨道
        for track in self.tracks:
            self.draw_track(painter, track)
        
        # 绘制播放指针
        self.draw_playhead(painter)
```

### 3. 3D预览系统

```python
import open3d as o3d

class Preview3D:
    """3D预览系统"""
    
    def __init__(self):
        self.visualizer = o3d.visualization.Visualizer()
        self.dog_models = {}  # 机器狗3D模型
        self.stage_model = None  # 舞台模型
    
    def load_dog_model(self, dog_id: str, model_path: str):
        """加载机器狗3D模型"""
        mesh = o3d.io.read_triangle_mesh(model_path)
        mesh.paint_uniform_color([0.7, 0.7, 0.7])
        self.dog_models[dog_id] = mesh
    
    def update_dog_pose(self, dog_id: str, pose: Pose):
        """更新机器狗姿态"""
        if dog_id in self.dog_models:
            model = self.dog_models[dog_id]
            # 应用变换矩阵
            transformation = self.pose_to_matrix(pose)
            model.transform(transformation)
    
    def render_frame(self):
        """渲染当前帧"""
        self.visualizer.update_geometry()
        self.visualizer.poll_events()
        self.visualizer.update_renderer()
```

## 📊 数据模型设计

### 1. 核心数据结构

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
import json

@dataclass
class Pose:
    """机器狗姿态数据"""
    body_height: float = 0.25
    roll: float = 0.0
    pitch: float = 0.0  
    yaw: float = 0.0
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    wz: float = 0.0

@dataclass  
class Keyframe:
    """关键帧数据"""
    time: float
    pose: Pose
    interpolation_type: str = "linear"
    ease_in: float = 0.0
    ease_out: float = 0.0

@dataclass
class Action:
    """单个动作定义"""
    name: str
    duration: float
    keyframes: List[Keyframe]
    metadata: Dict = None
    
    def to_json(self) -> str:
        """序列化为JSON"""
        return json.dumps(self, default=lambda o: o.__dict__)
    
    @classmethod
    def from_json(cls, json_str: str):
        """从JSON反序列化"""
        data = json.loads(json_str)
        return cls(**data)

@dataclass
class ActionSequence:
    """动作序列"""
    name: str
    total_duration: float
    actions: List[Tuple[float, Action]]  # (start_time, action)
    music_file: Optional[str] = None
    bpm: Optional[float] = None
```

### 2. 配置管理

```python
class DanceSystemConfig:
    """系统配置管理"""
    
    def __init__(self, config_file: str = "dance_config.yaml"):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)
    
    @property
    def max_dogs(self) -> int:
        return self.config.get('multi_dog', {}).get('max_count', 8)
    
    @property
    def sync_tolerance(self) -> float:
        return self.config.get('sync', {}).get('tolerance', 0.05)
    
    @property
    def default_interpolation(self) -> str:
        return self.config.get('animation', {}).get('interpolation', 'linear')
```

## 🔧 开发工具和环境

### 1. 开发环境配置

**Python依赖**:
```requirements.txt
# 核心依赖
numpy>=1.21.0
scipy>=1.7.0
asyncio>=3.4.3

# GUI开发
PyQt5>=5.15.0
# 或者 tkinter (Python标准库)

# 音频处理  
librosa>=0.8.1
soundfile>=0.10.3
pygame>=2.1.0

# 3D可视化
open3d>=0.13.0
matplotlib>=3.5.0

# 网络通信
websockets>=10.0
aiohttp>=3.8.0

# 数据处理
pyyaml>=6.0
pydantic>=1.8.0

# 机器狗控制
# robodog (项目本地库)
```

### 2. 项目结构建议

```
robodog_dance/
├── core/                    # 核心模块
│   ├── __init__.py
│   ├── action_engine.py     # 动作执行引擎
│   ├── timeline.py          # 时间轴管理
│   ├── interpolator.py      # 插值算法
│   └── sync_manager.py      # 同步管理器
├── choreography/           # 编排模块
│   ├── __init__.py
│   ├── editor.py           # 编排编辑器
│   ├── action_library.py   # 动作库管理
│   └── sequence_builder.py # 序列构建器
├── multi_dog/              # 多机器狗控制
│   ├── __init__.py
│   ├── network_manager.py  # 网络管理
│   ├── formation.py        # 编队控制
│   └── sync_protocol.py    # 同步协议
├── audio/                  # 音频处理
│   ├── __init__.py
│   ├── analyzer.py         # 音频分析
│   ├── beat_detector.py    # 节拍检测
│   └── player.py           # 音频播放
├── ui/                     # 用户界面
│   ├── __init__.py
│   ├── main_window.py      # 主窗口
│   ├── timeline_widget.py  # 时间轴组件
│   ├── preview_3d.py       # 3D预览
│   └── control_panel.py    # 控制面板
├── data/                   # 数据文件
│   ├── actions/            # 预设动作
│   │   ├── basic_moves.json
│   │   ├── dance_moves.json
│   │   └── expressions.json
│   ├── sequences/          # 动作序列
│   ├── music/              # 音乐文件
│   └── configs/            # 配置文件
├── tests/                  # 测试代码
│   ├── test_action_engine.py
│   ├── test_sync_manager.py
│   └── test_multi_dog.py
├── docs/                   # 文档
│   ├── api_reference.md
│   ├── user_guide.md
│   └── development.md
├── requirements.txt        # 依赖列表
├── setup.py               # 安装脚本
└── main.py                # 主入口
```

## 🎯 性能优化策略

### 1. 实时性能优化

**关键性能指标**:
- 控制循环延迟: <10ms
- 同步精度: ±20ms
- 帧率: 60FPS (预览), 20Hz (控制)

**优化技术**:
- 异步I/O (asyncio)
- 多线程并行处理
- 缓存预计算结果
- GPU加速计算 (可选)

### 2. 内存管理

```python
class MemoryManager:
    """内存管理器"""
    
    def __init__(self):
        self.action_cache = LRUCache(maxsize=100)
        self.pose_buffer = CircularBuffer(size=1000)
    
    def cache_action(self, action: Action):
        """缓存动作数据"""
        self.action_cache[action.name] = action
    
    def get_cached_action(self, name: str) -> Optional[Action]:
        """获取缓存的动作"""
        return self.action_cache.get(name)
```

### 3. 网络优化

**策略**:
- 命令压缩和批处理
- 预测性发送和补偿
- 自适应品质调整
- 错误检测和恢复

## 🔒 安全和容错设计

### 1. 安全机制

```python
class SafetyManager:
    """安全管理器"""
    
    def __init__(self):
        self.emergency_stop = False
        self.collision_detector = CollisionDetector()
        self.bounds_checker = BoundsChecker()
    
    def validate_pose(self, pose: Pose) -> bool:
        """验证姿态安全性"""
        # 检查物理限制
        if not self.check_physical_limits(pose):
            return False
        
        # 检查边界限制
        if not self.bounds_checker.is_within_bounds(pose):
            return False
        
        return True
    
    def emergency_stop_all(self):
        """紧急停止所有机器狗"""
        self.emergency_stop = True
        # 发送停止命令到所有机器狗
```

### 2. 容错处理

**容错策略**:
- 网络断线自动重连
- 命令失败重试机制
- 状态不一致自动同步
- 异常情况安全降级

这个技术架构为机器狗跳舞系统提供了完整的设计框架。你可以根据实际需求调整具体的实现细节。建议从核心的动作执行引擎开始开发，然后逐步扩展其他功能模块。

你觉得这个架构设计如何？有哪些部分需要进一步细化或调整吗？
