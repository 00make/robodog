# robodog

A Python library for controlling AlphaDog robotic dogs.

## Features

* Automated ROS connection management
* Multiple control modes (standing, walking, dancing, etc.)
* Real-time status monitoring
* Dynamic parameter configuration
* Elegant context manager support
* Comprehensive error handling
* Type annotation support

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
from robodog.config import UserMode
import time

# Connect to the dog using default IP
with Dog() as dog:
    # Switch to normal mode
    dog.set_user_mode(UserMode.NORMAL)
    
    # Adjust standing height
    dog.set_parameters({'body_height': 0.25})
    time.sleep(2)
    
    # Restore default height
    dog.set_parameters({'body_height': 0.23})
```

## Core Features

* Switch between user modes (normal, quiet, kids, etc.)
* Adjust body posture (height, tilt, etc.)
* Real-time status monitoring

Check the `examples` directory for more examples.

### User Modes

Available user modes:

* `UserMode.NORMAL`: Normal mode
* `UserMode.QUIET`: Quiet mode
* `UserMode.KIDS`: Kids mode
* `UserMode.EXTREME`: Extreme mode
* `UserMode.DANCE`: Dance mode
* `UserMode.MUTE`: Mute mode
* `UserMode.LONG_ENDURANCE`: Long endurance mode

Basic parameters:

* `body_height`: Body height (default 0.23)
* `roll`: Roll angle
* `pitch`: Pitch angle
* `yaw`: Yaw angle

### Contributing

Issues and pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Contact

For questions or suggestions:

* Submit GitHub Issues
* Email: <towardsrwby@gmail.com>
