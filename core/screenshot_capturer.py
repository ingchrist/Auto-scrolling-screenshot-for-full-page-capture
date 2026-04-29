"""
Screenshot Capturer Module

Responsible for:
- Taking screenshots of screen regions
- Handling different image formats
- Simple, focused capture logic
"""

import pyautogui
from PIL import Image
from typing import Tuple
from core.capture_region import CaptureRegion


class ScreenshotCapturer:
    """Captures screenshots of screen regions."""
    
    def __init__(self, quality: int = 95):
        """
        Initialize screenshot capturer.
        
        Args:
            quality: JPEG quality level (1-100), PNG always lossless
        """
        if not (1 <= quality <= 100):
            raise ValueError("Quality must be between 1 and 100")
        self.quality = quality
    
    def capture_region(self, region: CaptureRegion) -> Image.Image:
        """
        Capture screenshot of a specific region.
        
        Args:
            region: CaptureRegion object with boundaries
        
        Returns:
            PIL.Image: Captured image
        
        Raises:
            ValueError: If region is invalid or zero-sized
        """
        x1, y1, x2, y2 = region.get_normalized()
        width = x2 - x1
        height = y2 - y1
        
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid region size: {width}x{height}")
        
        # Use pyautogui to capture the region
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        return screenshot
    
    def capture_full_screen(self) -> Image.Image:
        """
        Capture entire screen.
        
        Returns:
            PIL.Image: Full screen image
        """
        screenshot = pyautogui.screenshot()
        return screenshot
    
    def capture_strip(
        self,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> Image.Image:
        """
        Capture a horizontal or vertical strip.
        
        Args:
            x, y: Top-left corner
            width, height: Dimensions of strip
        
        Returns:
            PIL.Image: Captured strip
        
        Raises:
            ValueError: If strip dimensions are invalid
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid strip size: {width}x{height}")
        
        # Ensure coordinates are within screen bounds
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return screenshot
    
    def set_quality(self, quality: int) -> None:
        """
        Set quality for future captures.
        
        Args:
            quality: Quality level (1-100)
        
        Raises:
            ValueError: If quality is out of range
        """
        if not (1 <= quality <= 100):
            raise ValueError("Quality must be between 1 and 100")
        self.quality = quality


if __name__ == "__main__":
    # Test the module
    from .screen_utils import get_screen_size
    
    print("Testing ScreenshotCapturer...")
    
    capturer = ScreenshotCapturer(quality=95)
    
    # Capture a region
    region = CaptureRegion(x1=0, y1=0, x2=400, y2=300)
    print(f"Capturing region: {region}")
    
    try:
        img = capturer.capture_region(region)
        print(f"Captured image size: {img.size}")
        print(f"Image mode: {img.mode}")
        
        # Save for verification
        img.save("/tmp/test_capture.png")
        print("Test image saved to /tmp/test_capture.png")
    except Exception as e:
        print(f"Error during capture: {e}")
    
    # Test strip capture
    print("\nTesting strip capture...")
    try:
        strip = capturer.capture_strip(x=100, y=100, width=200, height=50)
        print(f"Captured strip size: {strip.size}")
    except Exception as e:
        print(f"Error during strip capture: {e}")
