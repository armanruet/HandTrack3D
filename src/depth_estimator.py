"""
Depth estimation module using DepthAnything model.
"""

import cv2
import torch
import torch.nn.functional as F
from torchvision.transforms import Compose
from depth_anything.dpt import DepthAnything
from depth_anything.util.transform import (
    Resize,
    NormalizeImage,
    PrepareForNet
)
from config import MODEL_NAME


class DepthEstimator:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        """Initialize the depth estimator with the DepthAnything model."""
        self.device = device
        self.model = self._initialize_model()
        self.transform = self._create_transform()

    def _initialize_model(self):
        """Initialize and prepare the DepthAnything model."""
        model = DepthAnything.from_pretrained(MODEL_NAME).to(self.device)
        model.eval()
        return model

    def _create_transform(self):
        """Create the image transformation pipeline."""
        return Compose([
            Resize(
                width=150,
                height=150,
                resize_target=False,
                keep_aspect_ratio=True,
                ensure_multiple_of=14,
                resize_method="lower_bound",
                image_interpolation_method=cv2.INTER_CUBIC,
            ),
            NormalizeImage(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225]),
            PrepareForNet(),
        ])

    @torch.no_grad()
    def estimate_depth(self, frame):
        """
        Estimate depth from input frame.

        Args:
            frame: BGR image (OpenCV format)

        Returns:
            numpy array: Depth map normalized to 0-255 range
        """
        # Convert BGR to RGB and normalize
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) / 255.0
        h, w = image.shape[:2]

        # Transform image
        transformed = self.transform({"image": image})["image"]
        transformed = torch.from_numpy(
            transformed).unsqueeze(0).to(self.device)

        # Get depth prediction
        depth = self.model(transformed)

        # Resize to original dimensions
        depth = F.interpolate(depth[None], (h, w),
                              mode="bilinear",
                              align_corners=False)[0, 0]

        # Normalize depth map
        depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
        depth_map = depth.cpu().numpy().astype('uint8')

        return depth_map

    def get_depth_at_point(self, depth_map, x, y):
        """
        Get normalized depth value at specific point.

        Args:
            depth_map: Generated depth map
            x, y: Coordinates

        Returns:
            float: Normalized depth value (0-1)
        """
        return depth_map[y, x] / 255.0
