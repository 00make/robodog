#!/usr/bin/env python3
"""
Python Version Checker for RoboDog SDK

This script checks if the current Python version is compatible with RoboDog SDK.
RoboDog SDK requires Python 3.9 specifically.
"""

import sys
import platform

def check_python_version():
    """Check if Python version is 3.9"""
    current_version = sys.version_info
    required_major = 3
    required_minor = 9
    
    print("=" * 50)
    print("RoboDog SDK - Python Version Checker")
    print("=" * 50)
    
    print(f"Current Python version: {platform.python_version()}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    
    if current_version.major == required_major and current_version.minor == required_minor:
        print("✅ SUCCESS: Python 3.9 detected - RoboDog SDK is supported!")
        return True
    else:
        print("❌ ERROR: Incompatible Python version!")
        print(f"Required: Python {required_major}.{required_minor}.x")
        print(f"Current:  Python {current_version.major}.{current_version.minor}.{current_version.micro}")
        print("\nPlease install Python 3.9 from https://www.python.org/downloads/")
        print("RoboDog SDK will not work with other Python versions.")
        return False

def main():
    """Main function"""
    is_compatible = check_python_version()
    
    if is_compatible:
        print("\nYou can now install RoboDog SDK:")
        print("pip install robodog")
    else:
        print("\nPlease install Python 3.9 before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
