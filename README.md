# RoboDog SDK

[English](README.md) | [中文](README_zh.md)

Python SDK for AlphaDog robotic dog control.

## Installation

```bash
pip install robodog
```

## Quick Start

1. Ensure your computer is on the same network as the robotic dog
2. Note the IP address of the robotic dog (default: 10.10.10.10)

### Basic Example

```python
from robodog import Dog
import time

with Dog() as dog:
    # Adjust standing height
    dog.body_height = 0.25
    time.sleep(2)
    
    # Restore default height
    dog.set_parameters({'body_height': 0.23})
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

Check out `examples` for a complete demonstration including:

- Basic motion control demo
- Advanced motion parameter adjustment
- Complete parameter configuration showcase
- User mode switching demonstration

Running the example:

```bash
python examples/demo_basic_movement.py
```

### Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Contact

For questions or suggestions:

- Submit GitHub Issues
- Email: <towardsrwby@gmail.com>
