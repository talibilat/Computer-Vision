#!/usr/bin/env python3
"""
Simple entry point for Hand Gesture Chrome Tab Switcher
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import run_gesture_detection

if __name__ == "__main__":
    run_gesture_detection() 