from dataclasses import dataclass
from typing import Dict, Any, Optional, TypedDict
import time
from .states import CtrlState, BodyStatus
from .client import ROSClient
from .controller import DogController, UserMode
from .subscriber import DogStateSubscriber

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
    
    def set_parameters(self, params):
        """设置运动参数"""
        return self._controller.set_parameters(params)
    
    def set_user_mode(self, mode: UserMode):
        """设置用户模式"""
        return self._controller.set_user_mode(mode)
        
    def __enter__(self):
        return self.connect()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
