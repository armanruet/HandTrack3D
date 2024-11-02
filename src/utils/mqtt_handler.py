"""
MQTT communication handler for the HandTrack3D system.
"""

import paho.mqtt.client as mqtt
from config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_KEEPALIVE,
    BOX_TO_STEP_MAPPING
)


class MQTTHandler:
    def __init__(self, interaction_system):
        """
        Initialize MQTT handler.

        Args:
            interaction_system: Reference to the interaction system
        """
        self.interaction_system = interaction_system
        self.client = mqtt.Client()
        self.setup_callbacks()

    def setup_callbacks(self):
        """Setup MQTT callback functions."""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker."""
        print(f"Connected with result code {rc}")
        client.subscribe("step_click")

    def on_message(self, client, userdata, msg):
        """Callback for when a message is received."""
        if msg.topic == "step_click":
            self.handle_step_click(msg.payload.decode())

    def handle_step_click(self, payload):
        """Handle step click messages."""
        try:
            step_number = int(payload)
            # Find corresponding box for the step
            for box, step in BOX_TO_STEP_MAPPING.items():
                if step == step_number:
                    self.interaction_system.set_target_box(box)
                    print(f"Target box updated: {box}")
                    break
        except ValueError:
            print(f"Invalid step number received: {payload}")

    def publish_completion(self):
        """Publish completion message."""
        self.client.publish("conf_mes", "All targeted boxes touched.")

    def connect(self):
        """Connect to MQTT broker."""
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()
