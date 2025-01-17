from dataclasses import dataclass
from typing import Dict, Any
import time

class StateManager:
    """Base class for state management"""
    def __init__(self, timeout: float = 5.0):
        self._timeout = timeout
        self.reset()

    def update(self, data: Dict[str, Any]) -> None:
        self._last_update = time.time()
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def reset(self) -> None:
        """Reset state data"""
        for key in self.__annotations__.keys():
            setattr(self, key, self.__annotations__[key]())
        self._last_update = 0.0
        
    @property
    def is_valid(self) -> bool:
        """Check if state is valid (not timed out)"""
        return (time.time() - self._last_update) < self._timeout

@dataclass
class CtrlState(StateManager):
    """Control state data class"""
    error: bool = False
    warning: bool = False
    estop: bool = False
    user_mode: int = 0
    controller_type: int = 0
    action: int = 0
    motion_mode: int = 0
    velocity_controller: int = 0
    gait: int = 0
    standing: bool = False

@dataclass
class BodyStatus(StateManager):
    """Body status data class"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    wx: float = 0.0
    wy: float = 0.0
    wz: float = 0.0
    ax: float = 0.0
    ay: float = 0.0
    az: float = 0.0
