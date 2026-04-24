"""
Capture Region Tracker Module

Responsible for:
- Tracking the selection rectangle (x1, y1, x2, y2)
- Updating region based on mouse movement
- Normalizing region coordinates
"""

from dataclasses import dataclass
from typing import Tuple
from .screen_utils import normalize_region, clamp_to_screen


@dataclass
class CaptureRegion:
    """Represents a rectangular capture area."""
    
    x1: int
    y1: int
    x2: int
    y2: int
    
    def get_normalized(self) -> Tuple[int, int, int, int]:
        """
        Get normalized region where (x1, y1) is always top-left.
        
        Returns:
            Tuple[int, int, int, int]: (x1, y1, x2, y2)
        """
        return normalize_region(self.x1, self.y1, self.x2, self.y2)
    
    def get_width(self) -> int:
        """Get width of region."""
        x1, _, x2, _ = self.get_normalized()
        return x2 - x1
    
    def get_height(self) -> int:
        """Get height of region."""
        _, y1, _, y2 = self.get_normalized()
        return y2 - y1
    
    def get_size(self) -> Tuple[int, int]:
        """Get (width, height) of region."""
        return self.get_width(), self.get_height()
    
    def get_area(self) -> int:
        """Get area in square pixels."""
        return self.get_width() * self.get_height()
    
    def is_valid(self, min_size: int = 50) -> bool:
        """
        Check if region is valid (meets minimum size).
        
        Args:
            min_size: Minimum width/height required
        
        Returns:
            bool: True if valid
        """
        width, height = self.get_size()
        return width >= min_size and height >= min_size
    
    def expand_bottom(self, pixels: int) -> None:
        """
        Expand region downward (used for auto-scroll).
        
        Args:
            pixels: Number of pixels to expand downward
        """
        self.y2 += pixels
    
    def expand_top(self, pixels: int) -> None:
        """
        Expand region upward (used for auto-scroll).
        
        Args:
            pixels: Number of pixels to expand upward
        """
        self.y1 -= pixels
    
    def expand_right(self, pixels: int) -> None:
        """
        Expand region rightward (used for auto-scroll).
        
        Args:
            pixels: Number of pixels to expand rightward
        """
        self.x2 += pixels
    
    def expand_left(self, pixels: int) -> None:
        """
        Expand region leftward (used for auto-scroll).
        
        Args:
            pixels: Number of pixels to expand leftward
        """
        self.x1 -= pixels
    
    def __repr__(self) -> str:
        x1, y1, x2, y2 = self.get_normalized()
        return f"CaptureRegion({x1}, {y1}, {x2}, {y2}) - Size: {self.get_width()}x{self.get_height()}"


class CaptureRegionTracker:
    """Tracks and manages the capture region during selection."""
    
    def __init__(self):
        """Initialize tracker with no region."""
        self.region: CaptureRegion = None
        self.start_x: int = None
        self.start_y: int = None
    
    def start_selection(self, x: int, y: int) -> None:
        """
        Start a new selection from the given point.
        
        Args:
            x, y: Starting position
        """
        x, y = clamp_to_screen(x, y)
        self.start_x = x
        self.start_y = y
        self.region = CaptureRegion(x1=x, y1=y, x2=x, y2=y)
    
    def update_selection(self, x: int, y: int) -> None:
        """
        Update selection to current mouse position.
        
        Args:
            x, y: Current mouse position
        """
        if self.region is None:
            return
        
        x, y = clamp_to_screen(x, y)
        self.region.x2 = x
        self.region.y2 = y
    
    def get_current_region(self) -> CaptureRegion:
        """
        Get the current capture region.
        
        Returns:
            CaptureRegion: Current region or None if not started
        """
        return self.region
    
    def end_selection(self) -> CaptureRegion:
        """
        End selection and return final region.
        
        Returns:
            CaptureRegion: Final selected region or None if invalid
        """
        if self.region is None or not self.region.is_valid():
            self.region = None
            return None
        
        region = self.region
        self.region = None
        self.start_x = None
        self.start_y = None
        
        return region
    
    def reset(self) -> None:
        """Reset tracker to initial state."""
        self.region = None
        self.start_x = None
        self.start_y = None
    
    def is_active(self) -> bool:
        """Check if selection is active."""
        return self.region is not None


if __name__ == "__main__":
    # Test the module
    print("Testing CaptureRegion...")
    region = CaptureRegion(x1=100, y1=100, x2=500, y2=400)
    print(f"Region: {region}")
    print(f"Size: {region.get_size()}")
    print(f"Area: {region.get_area()}")
    print(f"Valid: {region.is_valid()}")
    
    region.expand_bottom(100)
    print(f"After expanding bottom 100px: {region}")
    
    print("\nTesting CaptureRegionTracker...")
    tracker = CaptureRegionTracker()
    tracker.start_selection(100, 100)
    print(f"Started at (100, 100): {tracker.get_current_region()}")
    
    tracker.update_selection(300, 250)
    print(f"Updated to (300, 250): {tracker.get_current_region()}")
    
    final = tracker.end_selection()
    print(f"Final region: {final}")
