"""
Scroll Detector Module

Responsible for:
- Detecting if mouse is in edge trigger zones
- Determining which direction to scroll
- Simple, testable logic
"""

from typing import Optional


class ScrollDirection:
    """Constants for scroll directions."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class ScrollDetector:
    """Detects when mouse enters edge zones and determines scroll direction."""
    
    def __init__(self, trigger_zone: int = 60):
        """
        Initialize scroll detector.
        
        Args:
            trigger_zone: Number of pixels from edge that trigger scrolling
        """
        self.trigger_zone = trigger_zone
    
    def detect_scroll_direction(
        self,
        mouse_x: int,
        mouse_y: int,
        region: CaptureRegion,
        screen_width: int,
        screen_height: int
    ) -> Optional[str]:
        """
        Detect if mouse is in a scroll trigger zone and return direction.
        
        Priority order (if multiple zones active, returns in order):
        1. Bottom edge (highest priority)
        2. Top edge
        3. Right edge
        4. Left edge
        
        Args:
            mouse_x, mouse_y: Current mouse position
            region: Current capture region
            screen_width, screen_height: Screen dimensions
        
        Returns:
            str: ScrollDirection (UP, DOWN, LEFT, RIGHT) or None if not in zone
        """
        # Get normalized region bounds
        x1, y1, x2, y2 = region.get_normalized()
        
        # Check if mouse is within the region horizontally and vertically
        in_region_x = x1 <= mouse_x <= x2
        in_region_y = y1 <= mouse_y <= y2
        
        # Bottom edge: mouse within region and near screen bottom
        if in_region_x and (screen_height - mouse_y) <= self.trigger_zone:
            return ScrollDirection.DOWN
        
        # Top edge: mouse within region and near screen top
        if in_region_x and mouse_y <= self.trigger_zone:
            return ScrollDirection.UP
        
        # Right edge: mouse within region and near screen right
        if in_region_y and (screen_width - mouse_x) <= self.trigger_zone:
            return ScrollDirection.RIGHT
        
        # Left edge: mouse within region and near screen left
        if in_region_y and mouse_x <= self.trigger_zone:
            return ScrollDirection.LEFT
        
        return None
    
    def is_in_trigger_zone(
        self,
        mouse_x: int,
        mouse_y: int,
        region: CaptureRegion,
        screen_width: int,
        screen_height: int
    ) -> bool:
        """
        Check if mouse is in any trigger zone.
        
        Args:
            mouse_x, mouse_y: Current mouse position
            region: Current capture region
            screen_width, screen_height: Screen dimensions
        
        Returns:
            bool: True if in any trigger zone
        """
        direction = self.detect_scroll_direction(
            mouse_x, mouse_y, region, screen_width, screen_height
        )
        return direction is not None
    
    def set_trigger_zone(self, pixels: int) -> None:
        """
        Update trigger zone size.
        
        Args:
            pixels: New trigger zone size in pixels
        """
        if pixels < 1:
            raise ValueError("Trigger zone must be at least 1 pixel")
        self.trigger_zone = pixels


if __name__ == "__main__":
    # Test the module
    from .screen_utils import get_screen_size
    from .capture_region import CaptureRegion
    
    print("Testing ScrollDetector...")
    
    detector = ScrollDetector(trigger_zone=60)
    
    # Create a test region
    region = CaptureRegion(x1=200, y1=200, x2=800, y2=600)
    
    screen_w, screen_h = 1920, 1080
    
    # Test cases
    test_cases = [
        # (mouse_x, mouse_y, expected_direction, description)
        (500, 1020, ScrollDirection.DOWN, "Mouse near bottom edge"),
        (500, 30, ScrollDirection.UP, "Mouse near top edge"),
        (1900, 400, ScrollDirection.RIGHT, "Mouse near right edge"),
        (20, 400, ScrollDirection.LEFT, "Mouse near left edge"),
        (500, 400, None, "Mouse in center - no scroll"),
        (100, 400, None, "Mouse outside region - no scroll"),
    ]
    
    for mouse_x, mouse_y, expected, desc in test_cases:
        result = detector.detect_scroll_direction(
            mouse_x, mouse_y, region, screen_w, screen_h
        )
        status = "✓" if result == expected else "✗"
        print(f"{status} {desc}: {result} (expected: {expected})")
