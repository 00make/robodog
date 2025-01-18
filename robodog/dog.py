from dataclasses import dataclass
from typing import Dict, Any, Optional, TypedDict, Union
import time
from .states import CtrlState, BodyStatus
from .client import ROSClient
from .controller import DogController, UserMode
from .subscriber import DogStateSubscriber

# 参数范围常量定义
PARAM_RANGES = {
    'body_height': (0.1, 0.35),  # 机体高度范围
    'roll': (-0.5, 0.5),        # 横滚角范围
    'pitch': (-0.5, 0.5),       # 俯仰角范围
    'yaw': (-0.5, 0.5),         # 偏航角范围
    'vx': (-1.0, 1.0),          # 前进速度范围
    'vy': (-1.0, 1.0),          # 侧向速度范围
}


class Dog:
    """机器狗统一管理类"""

    def __init__(self, host='10.10.10.10', port=9090):
        self._client = ROSClient(host, port)
        self._controller = None
        self._subscriber = None
        self._ctrl_state = CtrlState()
        self._body_status = BodyStatus()

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

    def _validate_param(self, name: str, value: Union[int, float]) -> None:
        """验证参数是否合法"""
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} value must be a number")

        if name in PARAM_RANGES:
            min_val, max_val = PARAM_RANGES[name]
            if not min_val <= value <= max_val:
                raise ValueError(f"{name} value must be between {
                                 min_val} and {max_val}")

    def _validate_param_change(self, name: str, value: float, timeout: float = 2.0) -> bool:
        """验证参数是否成功改变"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.is_state_valid():
                time.sleep(0.1)
                continue

            current_value = None
            if name == 'body_height':
                current_value = self.body_status.z
            elif name in ('roll', 'pitch', 'yaw', 'vx', 'vy'):
                current_value = getattr(self.body_status, name)

            if current_value is not None and abs(current_value - value) < 0.01:
                return True
            time.sleep(0.1)
        return False

    def set_parameters(self, params: Dict[str, float]) -> bool:
        """设置运动参数"""
        # 只保留基本的参数验证
        for name, value in params.items():
            if name in PARAM_RANGES:
                self._validate_param(name, value)

        # 直接调用控制器设置参数
        return self._controller.set_parameters(params)

    def _set_param_safe(self, name: str, value: Union[int, float]) -> None:
        """安全设置参数"""
        try:
            self._validate_param(name, value)
            self.set_parameters({name: value})
        except Exception as e:
            raise RuntimeError(f"Error setting {name}: {str(e)}")

    # 核心控制属性
    @property
    def body_height(self):
        """获取机体高度"""
        return self.body_status.z

    @body_height.setter
    def body_height(self, value):
        """设置机体高度"""
        self.set_parameters({'body_height': value})

    @property
    def roll(self):
        """获取横滚角"""
        return self.body_status.roll

    @roll.setter
    def roll(self, value):
        """设置横滚角"""
        self.set_parameters({'roll': value})

    @property
    def pitch(self):
        """获取俯仰角"""
        return self.body_status.pitch

    @pitch.setter
    def pitch(self, value):
        """设置俯仰角"""
        self.set_parameters({'pitch': value})

    @property
    def yaw(self):
        """获取偏航角"""
        return self.body_status.yaw

    @yaw.setter
    def yaw(self, value):
        self.set_parameters({'yaw': value})

    # 速度控制属性
    @property
    def vx(self):
        """获取前进速度"""
        return self.body_status.vx

    @vx.setter
    def vx(self, value):
        """设置前进速度"""
        self.set_parameters({'vx': value})

    @property
    def vy(self):
        """获取侧向速度"""
        return self.body_status.vy

    @vy.setter
    def vy(self, value):
        """设置侧向速度"""
        self.set_parameters({'vy': value})

    # 只读状态属性
    @property
    def x(self):
        """获取X位置(只读)"""
        return self.body_status.x

    @property
    def y(self):
        """获取Y位置(只读)"""
        return self.body_status.y

    @property
    def z(self):
        """获取Z位置(只读)"""
        return self.body_status.z

    def set_user_mode(self, mode: UserMode):
        """设置用户模式"""
        return self._controller.set_user_mode(mode)

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
