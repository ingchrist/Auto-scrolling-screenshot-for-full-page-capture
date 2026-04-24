"""
Screen Utilities Module

Responsible for:
- Getting screen dimensions
- DPI awareness
- Multi-monitor support detection
"""

import pyautogui
from typing import Tuple, Dict, Any


class ScreenMetrics:
    """Data class for screen information."""
    
    def __init__(self, width: int, height: int, dpi: int = 96):
        self.width = width
        self.height = height
        self.dpi = dpi
    
    def __repr__(self) -> str:
        return f"ScreenMetrics(width={self.width}, height={self.height}, dpi={self.dpi})"


def get_screen_size() -> Tuple[int, int]:
    """
    Get the primary screen dimensions.
    
    Returns:
        Tuple[int, int]: (width, height) in pixels
    """
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height


def get_screen_metrics() -> ScreenMetrics:
    """
    Get complete screen metrics including DPI.
    
    Returns:
        ScreenMetrics: Object containing width, height, and DPI
    """
    width, height = get_screen_size()
    # Standard DPI is 96 (can be extended for DPI detection if needed)
    dpi = 96
    
    return ScreenMetrics(width=width, height=height, dpi=dpi)


def get_mouse_position() -> Tuple[int, int]:
    """
    Get current mouse position on screen.
    
    Returns:
        Tuple[int, int]: (x, y) coordinates
    """
    return pyautogui.position()


def is_valid_region(x1: int, y1: int, x2: int, y2: int, min_size: int = 50) -> bool:
    """
    Check if a capture region is valid.
    
    Args:
        x1, y1: Top-left corner
        x2, y2: Bottom-right corner
        min_size: Minimum width/height required (pixels)
    
    Returns:
        bool: True if region is valid, False otherwise
    """
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    
    return width >= min_size and height >= min_size


def clamp_to_screen(x: int, y: int) -> Tuple[int, int]:
    """
    Clamp coordinates to screen bounds.
    
    Args:
        x, y: Coordinates to clamp
    
    Returns:
        Tuple[int, int]: Clamped (x, y)
    """
    width, height = get_screen_size()
    x = max(0, min(x, width))
    y = max(0, min(y, height))
    return x, y


def normalize_region(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
    """
    Normalize region coordinates so (x1, y1) is always top-left.
    
    Args:
        x1, y1, x2, y2: Raw region coordinates
    
    Returns:
        Tuple[int, int, int, int]: Normalized (x1, y1, x2, y2)
    """
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    
    return left, top, right, bottom


if __name__ == "__main__":
    # Test the module
    print("Screen Metrics:", get_screen_metrics())
    print("Mouse Position:", get_mouse_position())
    print("Is valid region (100x100)?", is_valid_region(0, 0, 100, 100))
    print("Is valid region (30x30)?", is_valid_region(0, 0, 30, 30, min_size=50))
    print("Clamped position:", clamp_to_screen(2000, 2000))
    print("Normalized region:", normalize_region(500, 200, 100, 300))
