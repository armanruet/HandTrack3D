"""
Visualization utilities for the HandTrack3D system.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw
import time
from config import (
    BOX_LINE_THICKNESS,
    TARGET_BOX_COLOR,
    NON_TARGET_BOX_COLOR,
    TEXT_COLOR
)


class Visualizer:
    def __init__(self, fonts):
        """Initialize visualizer with fonts dictionary."""
        self.fonts = fonts
        self.frame_times = []
        self.fps = 0

    def get_text_dimensions(self, text, font):
        """Get width and height of text with given font."""
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def draw_fps(self, frame):
        """Draw FPS counter on frame."""
        current_time = time.time()
        self.frame_times.append(current_time)

        # Keep only the last 30 frame times
        if len(self.frame_times) > 30:
            self.frame_times.pop(0)

        if len(self.frame_times) > 1:
            self.fps = len(self.frame_times) / \
                (self.frame_times[-1] - self.frame_times[0])

        cv2.putText(frame, f"FPS: {self.fps:.2f}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def draw_depth_visualization(self, frame, depth_map):
        """Draw depth map visualization in corner of frame."""
        normalized_depth = cv2.normalize(
            depth_map, None, 0, 255, cv2.NORM_MINMAX)
        colored_depth = cv2.applyColorMap(normalized_depth.astype(np.uint8),
                                          cv2.COLORMAP_JET)

        small_depth = cv2.resize(colored_depth,
                                 (frame.shape[1] // 4, frame.shape[0] // 4))

        # Overlay in top-right corner
        frame[10:10+small_depth.shape[0],
              -10-small_depth.shape[1]:-10] = small_depth

    def draw_hand_detection_indicator(self, frame, hand_detected):
        """Draw hand detection status indicator."""
        color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.circle(frame, (frame.shape[1] - 30, 30), 10, color, -1)
        cv2.putText(frame, "Hand", (frame.shape[1] - 80, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    def draw_boxes(self, frame, box_coords, target_box):
        """Draw all interaction boxes with labels."""
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        for box_name, box_info in box_coords.items():
            coords = box_info["coords"]
            color = TARGET_BOX_COLOR if box_name == target_box else NON_TARGET_BOX_COLOR

            # Draw box with gradient outline
            for i in range(BOX_LINE_THICKNESS):
                alpha = 1 - (i / BOX_LINE_THICKNESS)
                current_color = tuple(int(c * alpha) for c in color)
                cv2.rectangle(frame,
                              (coords[0]-i, coords[1]-i),
                              (coords[2]+i, coords[3]+i),
                              current_color,
                              1)

            # Add text label
            text_width, text_height = self.get_text_dimensions(box_name,
                                                               self.fonts['box'])
            text_position = (coords[0], coords[1] - text_height - 5)

            # Draw text background
            draw.rectangle([
                text_position[0] - 2,
                text_position[1] - 2,
                text_position[0] + text_width + 2,
                text_position[1] + text_height + 2
            ], fill=(0, 0, 0, 180))

            # Draw text
            draw.text(text_position, box_name,
                      font=self.fonts['box'],
                      fill=(255, 255, 255, 255))

        frame[:] = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def draw_progress_bar(self, frame, progress):
        """Draw progress bar at bottom of frame."""
        h, w = frame.shape[:2]

        # Background
        cv2.rectangle(frame, (10, h-40), (w-10, h-10), (0, 0, 0), -1)

        # Progress bar
        progress_width = int((progress / 100) * (w - 30))
        cv2.rectangle(frame, (15, h-35), (15 + progress_width, h-15),
                      (0, 255, 0), -1)

        # Progress text
        cv2.putText(frame, f"Progress: {int(progress)}%",
                    (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, TEXT_COLOR, 2)

    def draw_status_message(self, frame, message):
        """Draw status message at bottom of frame."""
        h = frame.shape[0]
        cv2.rectangle(frame, (0, h-40), (frame.shape[1], h), (0, 0, 0), -1)
        cv2.putText(frame, message, (10, h-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, TEXT_COLOR, 2)

    def draw_instructions(self, frame):
        """Draw instruction text for users."""
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        instruction_text = "Draw interaction zones by clicking and dragging"
        text_width, text_height = self.get_text_dimensions(
            instruction_text,
            self.fonts['instruction']
        )

        # Center text position
        text_position = ((frame.shape[1] - text_width) // 2, 20)

        # Draw semi-transparent background
        draw.rectangle([
            text_position[0] - 10,
            text_position[1] - 5,
            text_position[0] + text_width + 10,
            text_position[1] + text_height + 5
        ], fill=(0, 0, 0, 180))

        # Draw text
        draw.text(text_position, instruction_text,
                  font=self.fonts['instruction'],
                  fill=(255, 255, 255, 255))

        frame[:] = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
