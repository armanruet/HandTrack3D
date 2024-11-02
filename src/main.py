"""
Main entry point for the HandTrack3D system.
"""

import cv2
import pygame
from PIL import ImageFont

from config import CAMERA_INDEX, FONT_PATHS, FONT_SIZES
from hand_tracker import HandTracker
from depth_estimator import DepthEstimator
from interaction_system import InteractionSystem
from utils.mqtt_handler import MQTTHandler
from utils.visualization import Visualizer


class HandTrack3D:
    def __init__(self):
        """Initialize the HandTrack3D system."""
        # Initialize fonts
        try:
            self.fonts = {
                'box': ImageFont.truetype(FONT_PATHS['default'], FONT_SIZES['box']),
                'instruction': ImageFont.truetype(FONT_PATHS['default'],
                                                  FONT_SIZES['instruction'])
            }
        except IOError:
            print("Font file not found. Using default font.")
            self.fonts = {
                'box': ImageFont.load_default(),
                'instruction': ImageFont.load_default()
            }

        # Initialize components
        self.hand_tracker = HandTracker()
        self.depth_estimator = DepthEstimator()
        self.interaction_system = InteractionSystem()
        self.mqtt_handler = MQTTHandler(self.interaction_system)
        self.visualizer = Visualizer(self.fonts)

        # Initialize camera
        self.camera = None

        # Initialize pygame for audio
        pygame.init()
        pygame.display.set_mode((1, 1))

    def setup_camera(self):
        """Setup and initialize the camera."""
        self.camera = cv2.VideoCapture(CAMERA_INDEX)
        if not self.camera.isOpened():
            raise RuntimeError("Failed to open camera")

        cv2.namedWindow('HandTrack3D', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('HandTrack3D', self.handle_mouse_event)

    def handle_mouse_event(self, event, x, y, flags, param):
        """Handle mouse events for box drawing."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.interaction_system.start_box_drawing(x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            coords = self.interaction_system.update_box_drawing(x, y)
            if coords:
                ret, frame = self.camera.read()
                if ret:
                    cv2.rectangle(frame, (coords[0], coords[1]),
                                  (coords[2], coords[3]), (0, 255, 0), 2)
                    cv2.imshow('HandTrack3D', frame)
        elif event == cv2.EVENT_LBUTTONUP:
            self.interaction_system.finish_box_drawing(x, y)

    def process_frame(self, frame):
        """Process a single frame."""
        # Get depth map
        depth_map = self.depth_estimator.estimate_depth(frame)

        # Detect hands
        hand_results = self.hand_tracker.detect_hands(frame)
        hand_detected = bool(hand_results.multi_hand_landmarks)

        # Draw visualizations
        self.visualizer.draw_fps(frame)
        self.visualizer.draw_hand_detection_indicator(frame, hand_detected)
        self.visualizer.draw_depth_visualization(frame, depth_map)

        if self.interaction_system.box_coords:
            # Draw boxes and process hand interactions
            self.visualizer.draw_boxes(frame,
                                       self.interaction_system.box_coords,
                                       self.interaction_system.target_box)

            status_message = ""
            if hand_detected:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    self.hand_tracker.draw_landmarks(frame, hand_results)

                    for box_name, box_info in self.interaction_system.box_coords.items():
                        if not box_info["touched"]:
                            hand_center = self.hand_tracker.get_hand_center(
                                hand_landmarks,
                                frame.shape
                            )
                            depth_value = self.depth_estimator.get_depth_at_point(
                                depth_map,
                                hand_center[0],
                                hand_center[1]
                            )

                            if self.hand_tracker.check_hand_in_box(
                                hand_landmarks,
                                box_info["coords"],
                                depth_value,
                                frame.shape
                            ):
                                is_target = box_name == self.interaction_system.target_box
                                self.interaction_system.handle_box_interaction(
                                    box_name,
                                    correct=is_target
                                )
                                status_message = (
                                    f"{box_name} touched "
                                    f"{'correctly!' if is_target else 'incorrectly.'}"
                                )

            # Check completion
            if (self.interaction_system.is_interaction_complete() and
                    not self.interaction_system.completion_published):
                self.mqtt_handler.publish_completion()
                self.interaction_system.completion_published = True
                status_message = "All boxes touched! Task completed!"

            # Update progress and status
            progress = self.interaction_system.get_progress()
            self.visualizer.draw_progress_bar(frame, progress)
            self.visualizer.draw_status_message(frame, status_message)
        else:
            self.visualizer.draw_instructions(frame)

        return frame

    def run(self):
        """Main run loop."""
        try:
            self.setup_camera()
            self.mqtt_handler.connect()

            while True:
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to grab frame")
                    break

                frame = cv2.flip(frame, 1)  # Mirror image
                processed_frame = self.process_frame(frame)
                cv2.imshow('HandTrack3D', processed_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('f'):
                    # Toggle fullscreen
                    cv2.setWindowProperty('HandTrack3D',
                                          cv2.WND_PROP_FULLSCREEN,
                                          cv2.WINDOW_FULLSCREEN)

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources."""
        if self.camera is not None:
            self.camera.release()
        self.mqtt_handler.disconnect()
        self.hand_tracker.release()
        cv2.destroyAllWindows()
        pygame.quit()


if __name__ == "__main__":
    app = HandTrack3D()
    app.run()
