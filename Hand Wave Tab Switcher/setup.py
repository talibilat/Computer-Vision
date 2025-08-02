#!/usr/bin/env python3
"""
Setup script for Hand Gesture Chrome Tab Switcher
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_camera():
    """Check if camera is accessible"""
    print("📷 Testing camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera is accessible!")
            cap.release()
            return True
        else:
            print("❌ Cannot access camera. Please check camera permissions.")
            return False
    except ImportError:
        print("⚠️  OpenCV not installed yet, skipping camera test.")
        return True

def main():
    """Main setup function"""
    print("🖐️  Hand Gesture Chrome Tab Switcher Setup")
    print("=" * 50)
    
    if not install_requirements():
        sys.exit(1)
    
    if not check_camera():
        print("⚠️  Camera issues detected. You may need to:")
        print("   • Grant camera permissions to your terminal")
        print("   • Check if camera is being used by another app")
        print("   • Try running the app anyway - it might still work")
    
    print()
    print("🚀 Setup complete! You can now run the application:")
    print("   python run.py")
    print()
    print("🐳 Or use Docker:")
    print("   docker-compose up --build")

if __name__ == "__main__":
    main() 