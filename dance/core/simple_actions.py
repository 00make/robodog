"""
机器狗跳舞系统 - 简单动作定义
用于概念验证阶段的基础动作实现
"""

import time
import math
from typing import Dict, List, Tuple, Any

class SimplePose:
    """简化的机器狗姿态"""
    
    def __init__(self, 
                 body_height: float = 0.25,
                 pitch: float = 0.0,
                 roll: float = 0.0,
                 yaw: float = 0.0,
                 x: float = 0.0,
                 y: float = 0.0):
        self.body_height = body_height
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Pose(h={self.body_height:.2f}, p={self.pitch:.2f}, r={self.roll:.2f}, y={self.yaw:.2f})"

class SimpleAction:
    """简单的舞蹈动作"""
    
    def __init__(self, name: str, keyframes: List[Tuple[float, SimplePose]], description: str = ""):
        self.name = name
        self.keyframes = keyframes  # [(time, pose), ...]
        self.description = description
        self.duration = max(kf[0] for kf in keyframes) if keyframes else 0
    
    def get_pose_at_time(self, t: float) -> SimplePose:
        """获取指定时间的姿态（线性插值）"""
        if not self.keyframes:
            return SimplePose()
        
        if t <= 0:
            return self.keyframes[0][1]
        if t >= self.duration:
            return self.keyframes[-1][1]
        
        # 找到前后两个关键帧进行线性插值
        for i in range(len(self.keyframes) - 1):
            t1, pose1 = self.keyframes[i]
            t2, pose2 = self.keyframes[i + 1]
            
            if t1 <= t <= t2:
                if t2 - t1 == 0:
                    return pose1
                
                # 线性插值
                ratio = (t - t1) / (t2 - t1)
                return self._interpolate_poses(pose1, pose2, ratio)
        
        return self.keyframes[-1][1]
    
    def _interpolate_poses(self, pose1: SimplePose, pose2: SimplePose, ratio: float) -> SimplePose:
        """线性插值两个姿态"""
        return SimplePose(
            body_height=pose1.body_height + (pose2.body_height - pose1.body_height) * ratio,
            pitch=pose1.pitch + (pose2.pitch - pose1.pitch) * ratio,
            roll=pose1.roll + (pose2.roll - pose1.roll) * ratio,
            yaw=pose1.yaw + (pose2.yaw - pose1.yaw) * ratio,
            x=pose1.x + (pose2.x - pose1.x) * ratio,
            y=pose1.y + (pose2.y - pose1.y) * ratio
        )

def create_basic_dance_actions() -> Dict[str, SimpleAction]:
    """创建基础舞蹈动作库"""
    
    actions = {}
    
    # 1. 点头动作
    actions["点头"] = SimpleAction(
        name="点头",
        description="机器狗向前点头致意",
        keyframes=[
            (0.0, SimplePose(body_height=0.25, pitch=0.0)),
            (0.4, SimplePose(body_height=0.25, pitch=-0.3)),
            (0.8, SimplePose(body_height=0.25, pitch=0.0)),
            (1.2, SimplePose(body_height=0.25, pitch=-0.3)),
            (1.6, SimplePose(body_height=0.25, pitch=0.0))
        ]
    )
    
    # 2. 摇头动作
    actions["摇头"] = SimpleAction(
        name="摇头",
        description="机器狗左右摇头",
        keyframes=[
            (0.0, SimplePose(body_height=0.25, yaw=0.0)),
            (0.5, SimplePose(body_height=0.25, yaw=0.4)),
            (1.0, SimplePose(body_height=0.25, yaw=0.0)),
            (1.5, SimplePose(body_height=0.25, yaw=-0.4)),
            (2.0, SimplePose(body_height=0.25, yaw=0.0))
        ]
    )
    
    # 3. 跳跃动作
    actions["跳跃"] = SimpleAction(
        name="跳跃",
        description="机器狗下蹲后跳起",
        keyframes=[
            (0.0, SimplePose(body_height=0.25)),
            (0.3, SimplePose(body_height=0.15)),  # 下蹲准备
            (0.6, SimplePose(body_height=0.35)),  # 跳起
            (0.9, SimplePose(body_height=0.15)),  # 落地缓冲
            (1.2, SimplePose(body_height=0.25))   # 恢复正常
        ]
    )
    
    # 4. 侧摆动作
    actions["侧摆"] = SimpleAction(
        name="侧摆",
        description="机器狗身体左右摆动",
        keyframes=[
            (0.0, SimplePose(body_height=0.25, roll=0.0)),
            (0.6, SimplePose(body_height=0.25, roll=0.3)),
            (1.2, SimplePose(body_height=0.25, roll=0.0)),
            (1.8, SimplePose(body_height=0.25, roll=-0.3)),
            (2.4, SimplePose(body_height=0.25, roll=0.0))
        ]
    )
    
    # 5. 鞠躬动作
    actions["鞠躬"] = SimpleAction(
        name="鞠躬",
        description="机器狗鞠躬致敬",
        keyframes=[
            (0.0, SimplePose(body_height=0.25, pitch=0.0)),
            (0.8, SimplePose(body_height=0.20, pitch=-0.5)),  # 深度鞠躬
            (1.6, SimplePose(body_height=0.25, pitch=0.0))    # 起身
        ]
    )
    
    # 6. 小跳舞组合
    actions["小跳舞"] = SimpleAction(
        name="小跳舞",
        description="简单的跳舞组合动作",
        keyframes=[
            # 开始姿态
            (0.0, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.0)),
            
            # 点头问候
            (0.5, SimplePose(body_height=0.25, pitch=-0.2, roll=0.0, yaw=0.0)),
            (1.0, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.0)),
            
            # 侧摆开始
            (1.5, SimplePose(body_height=0.25, pitch=0.0, roll=0.3, yaw=0.0)),
            (2.0, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.0)),
            (2.5, SimplePose(body_height=0.25, pitch=0.0, roll=-0.3, yaw=0.0)),
            (3.0, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.0)),
            
            # 转圈
            (3.5, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.5)),
            (4.0, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=1.0)),
            (4.5, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.5)),
            (5.0, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.0)),
            
            # 跳跃结束
            (5.3, SimplePose(body_height=0.15, pitch=0.0, roll=0.0, yaw=0.0)),
            (5.6, SimplePose(body_height=0.35, pitch=0.0, roll=0.0, yaw=0.0)),
            (5.9, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.0)),
            
            # 最终鞠躬
            (6.5, SimplePose(body_height=0.20, pitch=-0.4, roll=0.0, yaw=0.0)),
            (7.0, SimplePose(body_height=0.25, pitch=0.0, roll=0.0, yaw=0.0))
        ]
    )
    
    return actions

class DanceExecutor:
    """舞蹈动作执行器"""
    
    def __init__(self):
        self.is_dancing = False
        self.current_action = None
        self.start_time = None
        self.dance_actions = create_basic_dance_actions()
    
    def get_available_actions(self) -> List[str]:
        """获取可用的动作列表"""
        return list(self.dance_actions.keys())
    
    def get_action(self, name: str) -> SimpleAction:
        """获取指定名称的动作"""
        return self.dance_actions.get(name)
    
    def start_action(self, action_name: str) -> bool:
        """开始执行动作"""
        if action_name not in self.dance_actions:
            return False
        
        self.current_action = self.dance_actions[action_name]
        self.start_time = time.time()
        self.is_dancing = True
        return True
    
    def stop_action(self):
        """停止当前动作"""
        self.is_dancing = False
        self.current_action = None
        self.start_time = None
    
    def get_current_pose(self) -> SimplePose:
        """获取当前应该执行的姿态"""
        if not self.is_dancing or not self.current_action or not self.start_time:
            return SimplePose()  # 默认姿态
        
        elapsed_time = time.time() - self.start_time
        
        # 检查动作是否结束
        if elapsed_time >= self.current_action.duration:
            self.stop_action()
            return SimplePose()  # 返回默认姿态
        
        return self.current_action.get_pose_at_time(elapsed_time)
    
    def is_action_finished(self) -> bool:
        """检查当前动作是否已完成"""
        if not self.is_dancing or not self.current_action or not self.start_time:
            return True
        
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.current_action.duration

if __name__ == "__main__":
    # 测试代码
    executor = DanceExecutor()
    print("可用动作:", executor.get_available_actions())
    
    # 测试点头动作
    action = executor.get_action("点头")
    if action:
        print(f"\n测试动作: {action.name}")
        print(f"动作描述: {action.description}")
        print(f"动作时长: {action.duration}秒")
        
        # 模拟动作执行
        for t in [0, 0.4, 0.8, 1.2, 1.6]:
            pose = action.get_pose_at_time(t)
            print(f"时间 {t}s: {pose}")
