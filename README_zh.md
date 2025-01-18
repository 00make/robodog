# RoboDog SDK

[English](README.md) | [中文](README_zh.md)

AlphaDog 机器狗 Python SDK，提供简单直观的编程接口。

## 安装

```bash
pip install robodog
```

## 快速开始

1. 确保您的电脑与机器狗在同一网络下
2. 记录机器狗的 IP 地址（默认：10.10.10.10）

### 基本示例

```python
from robodog import Dog

with Dog() as dog:
    # 调整站立高度
    dog.body_height = 0.25
    time.sleep(2)
    
    # 恢复默认高度
    dog.set_parameters({'body_height': 0.23})
```

## 参数控制功能

SDK 提供全面的参数控制功能，具体包括：

### 1. 基本运动参数

```python
dog.vx = 0.2    # 前进速度 (-1.0 到 1.0)
dog.vy = 0.1    # 左右移动速度 (-1.0 到 1.0)
dog.wz = 0.1    # 旋转速度 (-1.0 到 1.0)
```

### 2. 姿态控制

```python
dog.roll = 0.1          # 横滚角 (-0.5 到 0.5)
dog.pitch = 0.1         # 俯仰角 (-0.5 到 0.5)
dog.yaw = 0.1           # 偏航角 (-0.5 到 0.5)
dog.body_height = 0.25  # 身体高度 (0.1 到 0.35)
```

### 3. 步态参数

```python
dog.foot_height = 0.08     # 抬脚高度 (0.0 到 0.15)
dog.swing_duration = 0.3   # 摆动周期 (0.1 到 1.0)
dog.friction = 0.6         # 摩擦系数 (0.1 到 1.0)
```

### 4. 高级控制功能

组合参数设置：

```python
# 设置步态参数
dog.set_gait_params(
    friction=0.6,  # 摩擦系数
    scale_x=1.2,   # 支撑面X方向缩放
    scale_y=1.0    # 支撑面Y方向缩放
)

# 设置运动参数
dog.set_motion_params(
    swaying_duration=2.0,  # 摇摆周期
    jump_distance=0.3,     # 跳跃距离
    jump_angle=0.1         # 跳跃旋转角度
)

# 设置控制参数
dog.set_control_params(
    velocity_decay=0.8,        # 速度衰减
    collision_protect=1,       # 碰撞保护
    decelerate_time=2.0,      # 减速延迟
    decelerate_duration=1.0    # 减速时间
)
```

## 示例程序

完整的演示程序请查看 `examples`，其中包含：

- 基础运动控制演示
- 高级运动参数调整
- 完整参数配置展示
- 用户模式切换演示

运行示例：

```bash
python examples/demo_basic_movement.py
```

### 贡献代码

欢迎提交 Issue 和 Pull Request。如需重大变更，请先开 Issue 讨论您的建议。

### 许可证

本项目采用 MIT 许可证 - 详见 `LICENSE` 文件。

### 联系方式

如有问题或建议：

- 提交 GitHub Issues
- 电子邮件：<towardsrwby@gmail.com>
