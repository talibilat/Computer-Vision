"""
Main Application Entry Point
Simple Hand Wave Chrome Tab Switcher using MediaPipe
"""

import cv2
import sys
import signal
from gesture_detector import (
    initialize_hands, 
    detect_hands_in_frame, 
    cleanup_hands, 
    reset_gesture_tracking
)
from tab_controller import handle_gesture


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down gracefully...")
    sys.exit(0)


def print_instructions():
    """Print usage instructions"""
    print("=" * 60)
    print("🖐️  SIMPLE HAND WAVE CHROME TAB SWITCHER")
    print("=" * 60)
    print("📋 Wave Gestures:")
    print("   • Wave LEFT  ← → Switch to PREVIOUS tab")
    print("   • Wave RIGHT → ← Switch to NEXT tab")
    print()
    print("💡 Tips:")
    print("   • Make deliberate left-right hand movements")
    print("   • Keep your hand visible to the camera")
    print("   • Make sure Chrome is the active window")
    print("   • Wait briefly between gestures")
    print()
    print("🎮 Controls:")
    print("   • Press 'q' or Ctrl+C → Quit application")
    print("   • Move mouse to corner → Emergency stop")
    print("=" * 60)
    print()


def initialize_camera(camera_index: int = 0) -> cv2.VideoCapture:
    """
    Initialize camera capture
    
    Args:
        camera_index: Index of camera to use (usually 0 for default)
        
    Returns:
        OpenCV VideoCapture object
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise ValueError(f"Cannot open camera {camera_index}")
    
    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    return cap


def run_gesture_detection():
    """Main application loop"""
    print_instructions()
    
    # Initialize components
    hands_detector = None
    cap = None
    
    try:
        # Initialize camera
        print("📷 Initializing camera...")
        cap = initialize_camera()
        
        # Initialize MediaPipe hands
        print("🤖 Initializing hand detection (balanced sensitivity)...")
        hands_detector = initialize_hands()
        
        print("✅ Ready! Start waving your hand left or right...")
        print("   (Press 'q' to quit)\n")
        
        while True:
            # Read frame from camera
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect hands and gestures
            annotated_frame, gesture = detect_hands_in_frame(frame, hands_detector)
            
            # Handle detected gesture
            if gesture:
                handle_gesture(gesture)
            
            # Add simple text overlay
            cv2.putText(annotated_frame, "Wave Left/Right to Switch Tabs", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(annotated_frame, "Press 'q' to quit", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display frame
            cv2.imshow('Hand Wave Tab Switcher', annotated_frame)
            
            # Check for quit key
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC key
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        if cap:
            cap.release()
        if hands_detector:
            cleanup_hands(hands_detector)
        cv2.destroyAllWindows()
        reset_gesture_tracking()
        print("✅ Cleanup complete!")


if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run the application
    run_gesture_detection() 