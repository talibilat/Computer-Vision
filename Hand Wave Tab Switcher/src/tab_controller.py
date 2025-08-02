"""
Chrome Tab Controller Module
Handles switching between Chrome tabs using keyboard shortcuts
"""

import pyautogui
import time

# Configuration
ACTION_DELAY = 0.1

# Initialize pyautogui settings
pyautogui.FAILSAFE = True  # Enable failsafe (move mouse to corner to stop)


def switch_tab_right() -> bool:
    """
    Switch to the next tab (right direction)
    
    Returns:
        True if action was performed successfully
    """
    try:
        # Ctrl+Tab switches to next tab
        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(ACTION_DELAY)
        return True
    except Exception as e:
        print(f"Error switching to next tab: {e}")
        return False


def switch_tab_left() -> bool:
    """
    Switch to the previous tab (left direction)
    
    Returns:
        True if action was performed successfully
    """
    try:
        # Ctrl+Shift+Tab switches to previous tab
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        time.sleep(ACTION_DELAY)
        return True
    except Exception as e:
        print(f"Error switching to previous tab: {e}")
        return False


def handle_gesture(gesture: str) -> bool:
    """
    Handle a detected gesture by performing the appropriate tab action
    
    Args:
        gesture: The detected gesture ('wave_left' or 'wave_right')
        
    Returns:
        True if action was performed successfully
    """
    if gesture == 'wave_right':
        print("🔀 Gesture detected: Wave Right → Next Tab")
        return switch_tab_right()
    elif gesture == 'wave_left':
        print("🔀 Gesture detected: Wave Left → Previous Tab")
        return switch_tab_left()
    else:
        return False


def set_action_delay(delay: float):
    """Set the delay between keyboard actions"""
    global ACTION_DELAY
    ACTION_DELAY = delay 