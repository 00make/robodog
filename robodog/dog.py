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
        """设置偏航角"""
        self.set_parameters({'yaw': value})
    
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

    # 位置相关属性
    @property
    def x(self):
        return self.body_status.x
    
    @x.setter 
    def x(self, value):
        self.set_parameters({'x': value})
    
    @property
    def y(self):
        return self.body_status.y
    
    @y.setter
    def y(self, value):
        self.set_parameters({'y': value})
    
    @property
    def z(self):
        return self.body_status.z
    
    @z.setter
    def z(self, value):
        self.set_parameters({'z': value})

    # 姿态角属性
    @property
    def roll(self):
        return self.body_status.roll
    
    @roll.setter
    def roll(self, value):
        self.set_parameters({'roll': value})
    
    @property
    def pitch(self):
        return self.body_status.pitch
    
    @pitch.setter
    def pitch(self, value):
        self.set_parameters({'pitch': value})
    
    @property
    def yaw(self):
        return self.body_status.yaw
    
    @yaw.setter
    def yaw(self, value):
        self.set_parameters({'yaw': value})

    # 线速度属性
    @property
    def vx(self):
        return self.body_status.vx
    
    @vx.setter
    def vx(self, value):
        self.set_parameters({'vx': value})
    
    @property
    def vy(self):
        return self.body_status.vy
    
    @vy.setter
    def vy(self, value):
        self.set_parameters({'vy': value})
    
    @property
    def vz(self):
        return self.body_status.vz
    
    @vz.setter
    def vz(self, value):
        self.set_parameters({'vz': value})

    # 角速度属性
    @property
    def wx(self):
        return self.body_status.wx
    
    @wx.setter
    def wx(self, value):
        self.set_parameters({'wx': value})
    
    @property
    def wy(self):
        return self.body_status.wy
    
    @wy.setter
    def wy(self, value):
        self.set_parameters({'wy': value})
    
    @property
    def wz(self):
        return self.body_status.wz
    
    @wz.setter
    def wz(self, value):
        self.set_parameters({'wz': value})

    # 加速度属性
    @property
    def ax(self):
        return self.body_status.ax
    
    @ax.setter
    def ax(self, value):
        self.set_parameters({'ax': value})
    
    @property
    def ay(self):
        return self.body_status.ay
    
    @ay.setter
    def ay(self, value):
        self.set_parameters({'ay': value})
    
    @property
    def az(self):
        return self.body_status.az
    
    @az.setter
    def az(self, value):
        self.set_parameters({'az': value})
