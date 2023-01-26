import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, max_hands = 2, detection_confidence = 0.5, track_confidence = 0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.detectionConfidence = detection_confidence
        self.trackConfidence = track_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, int(self.maxHands), int(self.detectionConfidence), int(self.trackConfidence))
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_num=0, draw = True):

        landmark_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_num]
            for id,lm in enumerate(my_hand.landmark):
                height, width, channels = img.shape
                channel_x, channel_y = int(lm.x*width), int(lm.y*height)
                landmark_list.append([id, channel_x, channel_y])
                if draw:
                    if id == 4:
                        cv2.circle(img, (channel_x,channel_y),10,(255,0,255), cv2.FILLED)

        return landmark_list


def main():
    cap = cv2.VideoCapture(0)
    previous_time = 0
    current_time = 0
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        landmarks = detector.find_position(img)
        if len(landmarks) != 0:
            print(landmarks[4])

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()