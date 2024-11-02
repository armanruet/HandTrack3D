"""
Hand tracking module using MediaPipe.
"""

import cv2
import mediapipe as mp
from config import DEPTH_THRESHOLD_NEAR, DEPTH_THRESHOLD_FAR


class HandTracker:
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        """Initialize the hand tracker with MediaPipe Hands."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        """
        Detect hands in the frame.

        Args:
            frame: BGR image (OpenCV format)

        Returns:
            results: MediaPipe hand detection results
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(frame_rgb)

    def draw_landmarks(self, frame, results):
        """
        Draw hand landmarks on the frame.

        Args:
            frame: BGR image
            results: MediaPipe detection results
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

    def get_hand_center(self, landmarks, frame_shape):
        """
        Get the center point of the hand.

        Args:
            landmarks: Hand landmarks
            frame_shape: Shape of the frame

        Returns:
            tuple: (x, y) coordinates of hand center
        """
        h, w = frame_shape[:2]
        lm = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        return int(lm.x * w), int(lm.y * h)

    def check_hand_in_box(self, landmarks, box_coords, depth_value, frame_shape):
        """
        Check if hand is inside a box and at correct depth.

        Args:
            landmarks: Hand landmarks
            box_coords: (x1, y1, x2, y2) box coordinates
            depth_value: Normalized depth value
            frame_shape: Shape of the frame

        Returns:
            bool: True if hand is in box at correct depth
        """
        x, y = self.get_hand_center(landmarks, frame_shape)
        x1, y1, x2, y2 = box_coords

        in_box = (x1 < x < x2) and (y1 < y < y2)
        correct_depth = DEPTH_THRESHOLD_NEAR < depth_value < DEPTH_THRESHOLD_FAR

        return in_box and correct_depth

    def release(self):
        """Release resources."""
        self.hands.close()
