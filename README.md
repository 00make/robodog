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

# Connect to the dog using default IP
with Dog() as dog:

    # Adjust standing height
    dog.body_height=0.25
    time.sleep(2)
    
    # Restore default height
    dog.set_parameters({'body_height': 0.23})
```

## Core Features

* Switch between user modes (normal, quiet, kids, etc.)
* Adjust body posture (height, tilt, etc.)
* Real-time status monitoring

Check the `examples` directory for more examples.

### Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Contact

For questions or suggestions:

* Submit GitHub Issues
* Email: <towardsrwby@gmail.com>
