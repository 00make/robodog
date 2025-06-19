"""
机器狗跳舞系统

这个模块提供了机器狗跳舞功能的核心实现，包括：
- 简单的舞蹈动作定义
- 动作插值和执行
- 基础的动作库管理

用法示例:
    from dance.core.simple_actions import DanceExecutor
    
    executor = DanceExecutor()
    executor.start_action("点头")
"""

__version__ = "0.1.0"
__author__ = "GitHub Copilot"

# 导入核心模块
from .core.simple_actions import (
    SimplePose,
    SimpleAction, 
    DanceExecutor,
    create_basic_dance_actions
)

__all__ = [
    'SimplePose',
    'SimpleAction',
    'DanceExecutor', 
    'create_basic_dance_actions'
]
