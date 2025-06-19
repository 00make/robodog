# RoboDog SDK

[English](README.md) | [中文](README_zh.md)

A comprehensive Python SDK for AlphaDog robotic dog control, providing intuitive programming interfaces for robot motion control, parameter adjustment, and real-time interaction.

## System Requirements

**⚠️ Important: This SDK requires Python 3.9 specifically**

- **Python Version**: Python 3.9 (Required - other versions are not supported)
- **Operating System**: Windows, macOS, Linux
- **Network**: Robot and computer must be on the same network

## Installation

### Prerequisites

First, ensure you have Python 3.9 installed:

```bash
# Check Python version
python --version  # Should show Python 3.9.x

# If you don't have Python 3.9, install it from python.org

# Quick version check using our tool
python check_python_version.py
```

### Install RoboDog SDK

```bash
# Install from PyPI
pip install robodog

# Or install from source
git clone https://github.com/00make/robodog.git
cd robodog
pip install -e .
```

## Quick Start

1. **Network Setup**: Ensure your computer is on the same network as the robotic dog
2. **IP Configuration**: Note the IP address of the robotic dog (default: 10.10.10.10)
3. **Python Environment**: Verify Python 3.9 is active in your environment

### Basic Example

```python
from robodog import Dog
import time

# Connect to the robot dog
with Dog() as dog:
    print("Connected to RoboDog!")
    
    # Adjust standing height
    dog.body_height = 0.25
    time.sleep(2)
    
    # Move forward slowly
    dog.vx = 0.2
    time.sleep(3)
    
    # Stop movement
    dog.vx = 0.0
    
    # Restore default height
    dog.set_parameters({'body_height': 0.23})
```

### Advanced Connection Options

```python
from robodog import Dog

# Connect with custom IP
dog = Dog(host="192.168.1.100")

# Connect with custom port
dog = Dog(host="10.10.10.10", port=9090)
    
# Use context manager for automatic cleanup
with Dog(host="10.10.10.10") as dog:
    # Your robot control code here
    pass
```

## Parameter Control Features

The SDK provides comprehensive parameter control capabilities:

### 1. Basic Motion Parameters

```python
dog.vx = 0.2    # Forward velocity (-1.0 to 1.0)
dog.vy = 0.1    # Lateral velocity (-1.0 to 1.0)
dog.wz = 0.1    # Rotational velocity (-1.0 to 1.0)
```

### 2. Posture Control

```python
dog.roll = 0.1          # Roll angle (-0.5 to 0.5)
dog.pitch = 0.1         # Pitch angle (-0.5 to 0.5)
dog.yaw = 0.1           # Yaw angle (-0.5 to 0.5)
dog.body_height = 0.25  # Body height (0.1 to 0.35)
```

### 3. Gait Parameters

```python
dog.foot_height = 0.08     # Foot lift height (0.0 to 0.15)
dog.swing_duration = 0.3   # Swing period (0.1 to 1.0)
dog.friction = 0.6         # Friction coefficient (0.1 to 1.0)
```

### 4. Advanced Control Features

Combined parameter settings:

```python
# Set gait parameters
dog.set_gait_params(
    friction=0.6,  # Friction coefficient
    scale_x=1.2,   # Support surface X scaling
    scale_y=1.0    # Support surface Y scaling
)

# Set motion parameters
dog.set_motion_params(
    swaying_duration=2.0,  # Swaying period
    jump_distance=0.3,     # Jump distance
    jump_angle=0.1         # Jump rotation angle
)

# Set control parameters
dog.set_control_params(
    velocity_decay=0.8,        # Velocity decay
    collision_protect=1,       # Collision protection
    decelerate_time=2.0,      # Deceleration delay
    decelerate_duration=1.0    # Deceleration duration
)
```

## Example Programs

The `examples` directory contains comprehensive demonstrations:

### Available Examples

1. **`demo_basic_movement.py`** - Basic motion control and posture adjustment
2. **`demo_advanced_movement.py`** - Advanced motion parameters and gait control
3. **`demo_modes.py`** - User mode switching and state management
4. **`keyboard_control.py`** - Real-time keyboard control interface
5. **`test.py`** - System testing and validation

### Running Examples

```bash
# Navigate to the examples directory
cd examples

# Run basic movement demo
python demo_basic_movement.py

# Run keyboard control (requires pynput)
pip install pynput
python keyboard_control.py

# Run advanced movement demo
python demo_advanced_movement.py
```

### Keyboard Control

The keyboard control example provides real-time control:

- **W/S**: Forward/Backward movement
- **A/D**: Left/Right movement  
- **Q/E**: Rotate left/right
- **R/F**: Increase/Decrease body height
- **SPACE**: Emergency stop
- **ESC**: Exit program

## API Reference

### Core Classes

- **`Dog`**: Main robot control interface
- **`UserMode`**: Robot operation modes (IDLE, TROT, etc.)
- **`DogController`**: Low-level parameter control
- **`ROSClient`**: ROS communication handler

### Key Methods

```python
# Robot connection
dog = Dog(host="10.10.10.10", port=9090)
dog.connect()
dog.disconnect()

# Parameter control
dog.set_parameters(params_dict)
dog.set_gait_params(friction=0.6, scale_x=1.2)
dog.set_motion_params(jump_distance=0.3)
dog.set_control_params(velocity_decay=0.8)

# State queries
current_state = dog.get_state()
position = (dog.x, dog.y, dog.z)
```

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check network connectivity
   - Verify robot IP address
   - Ensure robot is powered on and ready

2. **Python Version Error**
   - This SDK requires Python 3.9 specifically
   - Install Python 3.9 from [python.org](https://www.python.org/downloads/)

3. **Import Errors**
   - Install required dependencies: `pip install -r requirements.txt`
   - For keyboard control: `pip install pynput`

4. **Performance Issues**
   - Reduce control frequency if network is slow
   - Check robot battery level
   - Minimize network interference

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from robodog import Dog
# Debug information will be printed
```

### Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Contact

For questions or suggestions:

- Submit GitHub Issues
- Email: <towardsrwby@gmail.com>
