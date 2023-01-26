import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##########################################
# SETTING THE HEIGHT AND WIDTH OF CAMERA
width_camera, height_camera = 640, 480
##########################################


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume_range = volume.GetVolumeRange()
min_volume = volume_range[0]
max_volume = volume_range[1]

cap = cv2.VideoCapture(0)
cap.set(3, width_camera)
cap.set(4, height_camera)

detector = htm.handDetector(detection_confidence=0.7)
previous_time = 0
current_time = 0
vol = 0
volBar = 0
volpercentage = 0
while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    landmark = detector.find_position(img, draw=False)
    if len(landmark) != 0:
        thumb_x, thumb_y = landmark[4][1], landmark[4][2]                                                   # x and y  co-ordinates of Thumb
        finger_x, finder_y = landmark[8][1], landmark[8][2]                                                 # x and y co-ordinates of Finger
        center_line_x, center_line_y = (thumb_x + finger_x)//2, (thumb_y + finder_y)//2                     # Center of the line
        cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)                                  # Cordinates of thumb
        cv2.circle(img, (finger_x, finder_y), 10, (255, 0, 255), cv2.FILLED)                                # Cordinates of finger
        cv2.line(img, (thumb_x, thumb_y), (finger_x, finder_y), (255, 0, 255), 3)                           # Drawing a line between thumb and finger
        cv2.circle(img, (center_line_x, center_line_y), 5, (0, 255, 255), cv2.FILLED)                       # Center of Circle

        length = math.hypot(finger_x - thumb_x, finder_y - thumb_y)

        if length < 10:
            cv2.circle(img, (center_line_x, center_line_y), 5, (0, 0, 0), cv2.FILLED)                       # Center of Circle

##################################
# VOLUME RANGE = -65 to 0
# HAND RANGE = 50 to 300
##################################

        vol = np.interp(length, [10, 300], [min_volume, max_volume])
        volBar = np.interp(length, [50, 300], [400, 150])
        volpercentage = np.interp(length, [50, 300], [0, 100])

        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (50, 150), (85, 400), (200, 0, 145), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volpercentage)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (127, 54, 98), 1)



    current_time = time.time()                                                                              # Calculating FPS
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)