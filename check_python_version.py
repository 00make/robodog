#!/usr/bin/env python3
"""
Python Version Checker for RoboDog SDK

This script checks if the current Python version is compatible with RoboDog SDK.
RoboDog SDK supports Python 3.10, 3.11, and 3.12.
"""

import sys
import platform

SUPPORTED_VERSIONS = [(3, 10), (3, 11), (3, 12)]

def check_python_version():
    """Check if Python version is 3.10, 3.11, or 3.12"""
    current_version = sys.version_info
    
    print("=" * 50)
    print("RoboDog SDK - Python Version Checker")
    print("=" * 50)
    
    print(f"Current Python version: {platform.python_version()}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    
    if (current_version.major, current_version.minor) in SUPPORTED_VERSIONS:
        print(f"✅ SUCCESS: Python {current_version.major}.{current_version.minor} detected - RoboDog SDK is supported!")
        return True
    else:
        print("❌ ERROR: Incompatible Python version!")
        supported_str = ", ".join(f"{major}.{minor}" for major, minor in SUPPORTED_VERSIONS)
        print(f"Required: Python {supported_str}")
        print(f"Current:  Python {current_version.major}.{current_version.minor}.{current_version.micro}")
        print("\nPlease install a compatible Python version from https://www.python.org/downloads/")
        print("RoboDog SDK will not work with other Python versions.")
        return False

def main():
    """Main function"""
    is_compatible = check_python_version()
    
    if is_compatible:
        print("\nYou can now install RoboDog SDK:")
        print("pip install robodog")
    else:
        print("\nPlease install a supported Python version before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
