"""
Configuration settings for the HandTrack3D system.
"""

# MQTT Settings
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# UI Parameters
BOX_LINE_THICKNESS = 3
TARGET_BOX_COLOR = (0, 255, 0)     # Green
NON_TARGET_BOX_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255)        # White
FONT_SCALE = 1

# System Parameters
MAX_BOXES = 3
FPS_WINDOW_SIZE = 30

# Depth Thresholds
DEPTH_THRESHOLD_NEAR = 0.20
DEPTH_THRESHOLD_FAR = 0.63

# Font Settings
FONT_PATHS = {
    'default': "/System/Library/Fonts/HelveticaNeue.ttc",
}
FONT_SIZES = {
    'box': 24,
    'instruction': 30
}

# Model Settings
ENCODER = "vits"
MODEL_NAME = f"LiheYoung/depth_anything_{ENCODER}14"

# Box to Step Mapping
BOX_TO_STEP_MAPPING = {
    "Box_1": 1,
    "Box_2": 3,
    "Box_3": 5
}

# Asset Paths
SOUND_PATHS = {
    'target': 'assets/sounds/ring_2.mp3',
    'non_target': 'assets/sounds/ring_1.mp3'
}

IMAGE_PATHS = {
    'thumbs_up': 'assets/images/thumbs_up.png',
    'thumbs_down': 'assets/images/thumbs_down.png'
}

# Camera Settings
CAMERA_INDEX = 0
