# RoboDog SDK

[English](README.md) | [中文](README_zh.md)

AlphaDog 机器狗 Python SDK，提供简单直观的编程接口，支持机器人运动控制、参数调整和实时交互。

## 系统要求

**⚠️ 重要提醒：本SDK仅支持Python 3.9版本**

- **Python版本**: Python 3.9（必需 - 不支持其他版本）
- **操作系统**: Windows, macOS, Linux
- **网络环境**: 机器人和电脑必须在同一网络下

## 安装

### 环境准备

首先确保您安装了Python 3.9：

```bash
# 检查Python版本
python --version  # 应显示 Python 3.9.x

# 如果没有Python 3.9，请从 python.org 下载安装

# 使用我们的工具快速检查版本
python check_python_version.py
```

### 安装RoboDog SDK

```bash
# 从PyPI安装
pip install robodog

# 或从源码安装
git clone https://github.com/00make/robodog.git
cd robodog
pip install -e .
```

## 快速开始

1. **网络设置**: 确保您的电脑与机器狗在同一网络下
2. **IP配置**: 记录机器狗的IP地址（默认：10.10.10.10）
3. **Python环境**: 确认Python 3.9环境已激活

### 基本示例

```python
from robodog import Dog
import time

# 连接机器狗
with Dog() as dog:
    print("已连接到机器狗！")
    
    # 调整站立高度
    dog.body_height = 0.25
    time.sleep(2)
    
    # 缓慢前进
    dog.vx = 0.2
    time.sleep(3)
    
    # 停止运动
    dog.vx = 0.0
    
    # 恢复默认高度
    dog.set_parameters({'body_height': 0.23})
```

### 高级连接选项

```python
from robodog import Dog

# 使用自定义IP连接
dog = Dog(host="192.168.1.100")

# 使用自定义端口连接
dog = Dog(host="10.10.10.10", port=9090)
    
# 使用上下文管理器自动清理资源
with Dog(host="10.10.10.10") as dog:
    # 在这里编写机器人控制代码
    pass
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

`examples` 目录包含完整的演示程序：

### 可用示例

1. **`demo_basic_movement.py`** - 基础运动控制和姿态调整
2. **`demo_advanced_movement.py`** - 高级运动参数和步态控制
3. **`demo_modes.py`** - 用户模式切换和状态管理
4. **`keyboard_control.py`** - 实时键盘控制界面
5. **`test.py`** - 系统测试和验证

### 运行示例

```bash
# 进入示例目录
cd examples

# 运行基础运动演示
python demo_basic_movement.py

# 运行键盘控制（需要安装pynput）
pip install pynput
python keyboard_control.py

# 运行高级运动演示
python demo_advanced_movement.py
```

### 键盘控制

键盘控制示例提供实时控制功能：

- **W/S**: 前进/后退
- **A/D**: 左移/右移
- **Q/E**: 左转/右转
- **R/F**: 升高/降低身体高度
- **空格**: 紧急停止
- **ESC**: 退出程序

## API参考

### 核心类

- **`Dog`**: 主要机器人控制接口
- **`UserMode`**: 机器人操作模式（IDLE, TROT等）
- **`DogController`**: 底层参数控制
- **`ROSClient`**: ROS通信处理器

### 主要方法

```python
# 机器人连接
dog = Dog(host="10.10.10.10", port=9090)
dog.connect()
dog.disconnect()

# 参数控制
dog.set_parameters(params_dict)
dog.set_gait_params(friction=0.6, scale_x=1.2)
dog.set_motion_params(jump_distance=0.3)
dog.set_control_params(velocity_decay=0.8)

# 状态查询
current_state = dog.get_state()
position = (dog.x, dog.y, dog.z)
```

## 故障排除

### 常见问题

1. **连接失败**
   - 检查网络连接
   - 验证机器人IP地址
   - 确保机器人已开机并就绪

2. **Python版本错误**
   - 本SDK需要Python 3.9版本
   - 请从 [python.org](https://www.python.org/downloads/) 安装Python 3.9

3. **导入错误**
   - 安装必需依赖：`pip install -r requirements.txt`
   - 键盘控制需要：`pip install pynput`

4. **性能问题**
   - 网络较慢时降低控制频率
   - 检查机器人电池电量
   - 减少网络干扰

### 调试模式

启用调试日志以便故障排除：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from robodog import Dog
# 将打印调试信息
```

### 贡献代码

欢迎提交 Issue 和 Pull Request。如需重大变更，请先开 Issue 讨论您的建议。

### 许可证

本项目采用 MIT 许可证 - 详见 `LICENSE` 文件。

### 联系方式

如有问题或建议：

- 提交 GitHub Issues
- 电子邮件：<towardsrwby@gmail.com>
