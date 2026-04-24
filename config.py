"""
ScrollSnip Configuration & Constants

All configurable parameters are defined here for easy modification.
"""

# Scrolling Configuration
SCROLL_STEP = 3                    # Pixels to scroll per trigger
TRIGGER_ZONE = 60                  # Edge pixels that trigger auto-scroll (pixels from edge)
SCROLL_INTERVAL = 120              # Milliseconds between scroll repeats

# Screen Configuration
MIN_CAPTURE_SIZE = 50              # Minimum width/height for valid capture region (pixels)

# Overlay Configuration
OVERLAY_ALPHA = 0.1                # Transparency of overlay (0.0 = transparent, 1.0 = opaque)
SELECTION_RECT_COLOR = "blue"      # Color of selection rectangle
SELECTION_RECT_WIDTH = 2           # Width of selection rectangle border (pixels)
CROSSHAIR_COLOR = "red"            # Color of crosshair cursor

# File Configuration
OUTPUT_FORMAT = "PNG"              # Output image format
OUTPUT_DIR = "~/Pictures/ScrollSnip"  # Default save directory

# Logging Configuration
DEBUG_MODE = False                 # Enable debug logging
LOG_LEVEL = "INFO"                 # Logging level: DEBUG, INFO, WARNING, ERROR

# UI Configuration
TOOLBAR_WIDTH = 150                # Width of toolbar window (pixels)
TOOLBAR_HEIGHT = 50                # Height of toolbar window (pixels)
BUTTON_FONT_SIZE = 10              # Font size for buttons
CONFIRMATION_POPUP_WIDTH = 400     # Width of confirmation popup (pixels)
CONFIRMATION_POPUP_HEIGHT = 150    # Height of confirmation popup (pixels)

# Performance Configuration
SCREENSHOT_QUALITY = 95            # Quality level for image capture (1-100)
MAX_IMAGE_BUFFER_SIZE = 500        # Maximum number of strips to buffer (prevents memory issues)

# Mouse Configuration
MOUSE_BUTTON = "right"             # Which mouse button triggers capture (left/right/middle)
MODIFIER_KEY = None                # Optional modifier key (shift, ctrl, alt) - None means no modifier required

# Timing Configuration
INITIAL_SCREENSHOT_DELAY = 0       # Delay after right-click press before first capture (ms)
STRIP_CAPTURE_DELAY = 0            # Delay before capturing each strip (ms)
