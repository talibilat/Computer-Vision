"""
python run.pySimple Hand Wave Detection for Chrome Tab Control
Detects left-right and right-left hand waves only
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple
import time

# Global variables for wave tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand_positions = []
last_gesture_time = 0

# Configuration constants - Balanced for one wave = one change
MAX_POSITIONS = 8  # Enough positions for reliable detection
GESTURE_COOLDOWN = 0.5  # Longer cooldown to prevent multiple triggers
MOVEMENT_THRESHOLD = 60  # Higher threshold for deliberate movements
MIN_MOVEMENT = 40  # Require more substantial movement


def initialize_hands(detection_confidence: float = 0.7, tracking_confidence: float = 0.6):
    """
    Initialize MediaPipe hands detection with higher sensitivity
    
    Args:
        detection_confidence: Minimum confidence for hand detection
        tracking_confidence: Minimum confidence for hand tracking
        
    Returns:
        MediaPipe hands object
    """
    return mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,  # Only track one hand
        min_detection_confidence=detection_confidence,
        min_tracking_confidence=tracking_confidence
    )


def detect_hands_in_frame(frame: np.ndarray, hands_detector) -> Tuple[np.ndarray, Optional[str]]:
    """
    Detect hands in the frame and determine wave gesture
    
    Args:
        frame: Input video frame
        hands_detector: MediaPipe hands object
        
    Returns:
        Tuple of (annotated_frame, detected_gesture)
    """
    global hand_positions
    
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(rgb_frame)
    
    gesture = None
    annotated_frame = frame.copy()
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                annotated_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get wrist position for wave tracking
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            wrist_x = int(wrist.x * frame.shape[1])
            
            # Track hand positions
            hand_positions.append(wrist_x)
            
            if len(hand_positions) > MAX_POSITIONS:
                hand_positions.pop(0)
            
            # Detect wave gesture if we have enough positions
            if len(hand_positions) >= MAX_POSITIONS:
                gesture = detect_wave_gesture()
    
    # Add gesture status to frame
    if gesture:
        cv2.putText(annotated_frame, f"Gesture: {gesture}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return annotated_frame, gesture


def detect_wave_gesture() -> Optional[str]:
    """
    Detect horizontal wave gesture for tab switching
    
    Returns:
        'wave_left' (previous tab), 'wave_right' (next tab), or None
    """
    global last_gesture_time, hand_positions
    
    current_time = time.time()
    
    # Check cooldown
    if current_time - last_gesture_time < GESTURE_COOLDOWN:
        return None
    
    if len(hand_positions) < MAX_POSITIONS:
        return None
    
    # Calculate movement direction using all positions
    positions = np.array(hand_positions)
    
    # Check for significant movement
    movement_range = np.max(positions) - np.min(positions)
    if movement_range < MOVEMENT_THRESHOLD:
        return None
    
    # Calculate overall movement trend
    start_pos = positions[0]
    end_pos = positions[-1]
    movement = end_pos - start_pos
    
    # Check for consistent directional movement (at least 70% of movements in same direction)
    differences = np.diff(positions)
    if movement > 0:  # Right movement
        consistent_moves = np.sum(differences > 0) / len(differences)
    else:  # Left movement
        consistent_moves = np.sum(differences < 0) / len(differences)
    
    # Require strong overall movement AND consistent direction
    if abs(movement) > MIN_MOVEMENT and consistent_moves >= 0.7:
        if movement > 0:  # Moving right
            last_gesture_time = current_time
            print(f"Wave detected: RIGHT (movement: {movement:.1f}, consistency: {consistent_moves:.2f})")
            return 'wave_right'
        else:  # Moving left
            last_gesture_time = current_time
            print(f"Wave detected: LEFT (movement: {movement:.1f}, consistency: {consistent_moves:.2f})")
            return 'wave_left'
    
    return None


def reset_gesture_tracking():
    """Reset gesture tracking variables"""
    global hand_positions, last_gesture_time
    hand_positions = []
    last_gesture_time = 0


def cleanup_hands(hands_detector):
    """Clean up MediaPipe resources"""
    if hands_detector:
        hands_detector.close() 