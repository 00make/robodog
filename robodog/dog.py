from dataclasses import dataclass
from typing import Dict, Any, Optional, TypedDict, Union
import time
from .states import CtrlState, BodyStatus
from .client import ROSClient
from .controller import DogController, UserMode
from .subscriber import DogStateSubscriber

# 参数范围常量定义 - 整理分组并添加详细注释
PARAM_RANGES = {
    # 基础运动参数组
    'vx': (-4.0, 4.0),             # 前后移动速度(m/s)，向前为正
    'vy': (-1.0, 1.0),             # 左右移动速度(m/s)，向左为正
    'wz': (-2.0, 2.0),             # 旋转速度(rad/s)，顺时针为正
    
    # 姿态参数组
    'roll': (-1, 1),           # 横滚角(rad)
    'pitch': (-1, 1),          # 俯仰角(rad)
    'yaw': (-1, 1),            # 偏航角(rad)
    'body_height': (0.09, 0.35),    # 机体高度(m)
    'body_tilt_x': (-0.2, 0.2),    # 身体前后偏移(m)
    'body_tilt_y': (-0.2, 0.2),    # 身体左右偏移(m)
    
    # 步态参数组
    'foot_height': (0.01, 0.26),    # 抬脚高度(m)
    'swing_duration': (0.1, 5.0),   # 摆动周期(s)
    'friction': (0.01, 1.0),        # 足底摩擦系数
    'scale_x': (0.2, 1.8),         # 支撑面X方向缩放比例
    'scale_y': (0.2, 1.8),         # 支撑面Y方向缩放比例
    
    # 特殊动作参数组
    'swaying_duration': (0.5, 5.0), # 左右摇摆周期(s)
    'jump_distance': (0.0, 1.0),    # 跳跃距离(m)
    'jump_angle': (-3.14, 3.14),    # 跳跃旋转角度(rad)
    
    # 控制参数组
    'velocity_decay': (0.0, 1.0),   # 速度衰减比例
    'decelerate_time': (0.0, 86400.0),      # 减速延迟时间(s)
    'decelerate_duration': (0.0, 86400.0),   # 减速持续时间(s)
}

def param_property(param_name: str, doc: str = None, get_attr: str = None, type_convert=None):
    """创建参数属性的装饰器工厂
    
    Args:
        param_name: 参数名称
        doc: 文档字符串
        get_attr: 获取值时使用的属性名(默认与param_name相同)
        type_convert: 设置值时的类型转换函数
    """
    def getter(self):
        """获取参数值"""
        status = self.body_status if not param_name.startswith('user_') else self.ctrl_state
        return getattr(status, get_attr or param_name)
        
    def setter(self, value):
        """设置参数值"""
        if type_convert:
            value = type_convert(value)
        self.set_parameters({param_name: value})
        
    return property(getter, setter, doc=doc)

class Dog:
    """机器狗统一管理类"""

    def __init__(self, host='10.10.10.10', port=9090):
        self._client = ROSClient(host, port)
        self._controller = None
        self._subscriber = None
        self._ctrl_state = CtrlState()
        self._body_status = BodyStatus()

    # 基础连接和状态管理方法
    def connect(self): 
        """连接到机器狗"""
        self._client.connect()
        self._controller = DogController(self._client)
        self._subscriber = DogStateSubscriber(self)
        self._subscriber.subscribe_ctrl_state()
        self._subscriber.subscribe_body_status()
        return self

    def disconnect(self):
        """断开连接"""
        if self._subscriber:
            self._subscriber.unsubscribe_all()
        self._client.disconnect()

    def update_ctrl_state(self, state: Dict[str, Any]) -> None:
        """更新控制状态"""
        self._ctrl_state.update(state)

    def update_body_status(self, status: Dict[str, Any]) -> None:
        """更新机体状态"""
        self._body_status.update(status)

    def is_state_valid(self) -> bool:
        """检查状态是否有效（未超时）"""
        return self._ctrl_state.is_valid or self._body_status.is_valid

    @property
    def ctrl_state(self):
        """获取控制状态"""
        return self._ctrl_state

    @property
    def body_status(self):
        """获取机体状态"""
        return self._body_status

    # 参数验证和设置
    def _validate_param(self, name: str, value: Union[int, float]) -> None:
        """验证单个参数是否合法"""
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} value must be a number")
        
        if name in PARAM_RANGES:
            min_val, max_val = PARAM_RANGES[name]
            if not min_val <= value <= max_val:
                raise ValueError(f"{name} must be between {min_val} and {max_val}")

    def set_parameters(self, params: Dict[str, float]) -> bool:
        """设置运动参数"""
        # 验证所有参数
        for name, value in params.items():
            if name in PARAM_RANGES:
                self._validate_param(name, value)
        # 调用控制器
        return self._controller.set_parameters(params)

    # 基础运动属性
    vx = param_property('vx', '前后移动速度(m/s)')
    vy = param_property('vy', '左右移动速度(m/s)')
    wz = param_property('wz', '旋转速度(rad/s)')

    # 姿态控制属性
    body_height = param_property('body_height', '机体高度(m)', 'z')
    roll = param_property('roll', '横滚角(rad)')
    pitch = param_property('pitch', '俯仰角(rad)')
    yaw = param_property('yaw', '偏航角(rad)')
    body_tilt_x = param_property('body_tilt_x', '身体前后偏移(m)')
    body_tilt_y = param_property('body_tilt_y', '身体左右偏移(m)')

    # 步态参数
    foot_height = param_property('foot_height', '抬脚高度(m)')
    swing_duration = param_property('swing_duration', '摆动周期(s)')
    friction = param_property('friction', '足底摩擦系数')
    scale_x = param_property('scale_x', '支撑面X方向缩放比例')
    scale_y = param_property('scale_y', '支撑面Y方向缩放比例')

    # 特殊动作参数
    swaying_duration = param_property('swaying_duration', '左右摇摆周期(s)')
    jump_distance = param_property('jump_distance', '跳跃距离(m)')
    jump_angle = param_property('jump_angle', '跳跃旋转角度(rad)')

    # 控制参数
    velocity_decay = param_property('velocity_decay', '速度衰减比例')
    collision_protect = param_property('collision_protect', '碰撞保护状态(0:关闭,1:开启)', type_convert=int)
    decelerate_time = param_property('decelerate_time', '减速延迟时间(s)')
    decelerate_duration = param_property('decelerate_duration', '减速持续时间(s)')
    free_leg = param_property('free_leg', '自由腿序号', type_convert=int)

    # 只读状态属性
    @property
    def x(self): """X位置(只读)"""; return self.body_status.x

    @property
    def y(self): """Y位置(只读)"""; return self.body_status.y

    @property
    def z(self): """Z位置(只读)"""; return self.body_status.z

    # 组合参数设置方法
    def set_gait_params(self, friction: float = None, scale_x: float = None, scale_y: float = None):
        """设置步态相关参数"""
        params = {}
        if friction is not None: params['friction'] = friction
        if scale_x is not None: params['scale_x'] = scale_x
        if scale_y is not None: params['scale_y'] = scale_y
        if params: self.set_parameters(params)

    def set_motion_params(self, swaying_duration: float = None, jump_distance: float = None, 
                         jump_angle: float = None):
        """设置运动相关参数"""
        params = {}
        if swaying_duration is not None: params['swaying_duration'] = swaying_duration
        if jump_distance is not None: params['jump_distance'] = jump_distance
        if jump_angle is not None: params['jump_angle'] = jump_angle
        if params: self.set_parameters(params)

    def set_control_params(self, velocity_decay: float = None, collision_protect: int = None,
                          decelerate_time: float = None, decelerate_duration: float = None):
        """设置控制相关参数"""
        params = {}
        if velocity_decay is not None: params['velocity_decay'] = velocity_decay
        if collision_protect is not None: params['collision_protect'] = collision_protect
        if decelerate_time is not None: params['decelerate_time'] = decelerate_time
        if decelerate_duration is not None: params['decelerate_duration'] = decelerate_duration
        if params: self.set_parameters(params)

    # 用户模式控制
    def set_user_mode(self, mode: UserMode):
        """设置用户模式"""
        return self._controller.set_user_mode(mode)

    # 上下文管理
    def __enter__(self): return self.connect()
    def __exit__(self, exc_type, exc_val, exc_tb): self.disconnect()
