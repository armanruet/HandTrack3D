"""
Interaction system managing boxes and user interaction.
"""

import string
import pygame
import cv2
from PIL import Image, ImageDraw, ImageFont
from config import (
    MAX_BOXES,
    SOUND_PATHS,
    IMAGE_PATHS,
    FONT_PATHS,
    FONT_SIZES
)


class InteractionSystem:
    def __init__(self):
        """Initialize the interaction system."""
        self.box_coords = {}  # Dictionary to store box coordinates
        self.target_box = None
        self.completion_published = False
        self.box_count = 0
        self.drawing = False
        self.start_pos = (-1, -1)

        # Initialize sounds
        pygame.mixer.init()
        self.sounds = {
            'target': pygame.mixer.Sound(SOUND_PATHS['target']),
            'non_target': pygame.mixer.Sound(SOUND_PATHS['non_target'])
        }

        # Load images
        self.images = {
            'thumbs_up': cv2.imread(IMAGE_PATHS['thumbs_up']),
            'thumbs_down': cv2.imread(IMAGE_PATHS['thumbs_down'])
        }

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

    def generate_box_name(self):
        """Generate a name for a new box."""
        return f"Box {string.ascii_uppercase[self.box_count]}"

    def start_box_drawing(self, x, y):
        """Start drawing a new box."""
        if self.box_count < MAX_BOXES:
            self.drawing = True
            self.start_pos = (x, y)

    def update_box_drawing(self, x, y):
        """Update box being drawn."""
        if self.drawing:
            return self.start_pos + (x, y)
        return None

    def finish_box_drawing(self, x, y):
        """Finish drawing a box."""
        if self.drawing and self.box_count < MAX_BOXES:
            self.drawing = False
            box_name = self.generate_box_name()
            self.box_coords[box_name] = {
                "coords": self.start_pos + (x, y),
                "touched": False
            }
            self.box_count += 1

    def handle_box_interaction(self, box_name, correct=True):
        """Handle interaction with a box."""
        if not self.box_coords[box_name]["touched"]:
            self.box_coords[box_name]["touched"] = True
            if correct:
                self.sounds['target'].play()
            else:
                self.sounds['non_target'].play()

    def is_interaction_complete(self):
        """Check if all boxes have been interacted with."""
        return all(box["touched"] for box in self.box_coords.values())

    def reset(self):
        """Reset the interaction system."""
        self.box_coords.clear()
        self.target_box = None
        self.completion_published = False
        self.box_count = 0
        self.drawing = False
        self.start_pos = (-1, -1)

    def get_box_at_position(self, x, y):
        """Get box name at given position."""
        for name, box in self.box_coords.items():
            x1, y1, x2, y2 = box["coords"]
            if x1 < x < x2 and y1 < y < y2:
                return name
        return None

    def set_target_box(self, box_name):
        """Set the target box."""
        if box_name in self.box_coords:
            self.target_box = box_name
            return True
        return False

    def get_progress(self):
        """Get interaction progress percentage."""
        if not self.box_coords:
            return 0
        touched = sum(1 for box in self.box_coords.values() if box["touched"])
        return (touched / len(self.box_coords)) * 100
