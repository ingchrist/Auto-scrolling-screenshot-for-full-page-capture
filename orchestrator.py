"""
Capture Orchestrator Module

Responsible for:
- Orchestrating the entire capture workflow
- Managing state transitions
- Coordinating between different components
- Main business logic
"""

import time
import threading
from typing import Optional
import pyautogui

from .config import (
    SCROLL_STEP,
    TRIGGER_ZONE,
    SCROLL_INTERVAL,
    MIN_CAPTURE_SIZE,
)

from .core.screen_utils import get_screen_size, get_screen_metrics
from .core.mouse_listener import GlobalMouseListener
from .core.capture_region import CaptureRegion, CaptureRegionTracker
from .core.screenshot_capturer import ScreenshotCapturer
from .core.scroll_detector import ScrollDetector, ScrollDirection
from .core.image_buffer import ImageBuffer, ImageStrip
from .core.overlay_window import OverlayWindow

from .processing.image_stitcher import ImageStitcher
from .processing.file_saver import FileSaver

from .ui.toolbar import Toolbar
from .ui.notifications import ConfirmationPopup


class CaptureState:
    """Constants for capture states."""
    IDLE = "idle"
    SELECTING = "selecting"
    CAPTURING = "capturing"
    PROCESSING = "processing"
    COMPLETE = "complete"
    CANCELLED = "cancelled"


class ScrollSnipOrchestrator:
    """Main orchestrator for the ScrollSnip capture workflow."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.state = CaptureState.IDLE
        
        # Components
        self.screen_metrics = get_screen_metrics()
        self.mouse_listener = GlobalMouseListener()
        self.region_tracker = CaptureRegionTracker()
        self.screenshot_capturer = ScreenshotCapturer()
        self.scroll_detector = ScrollDetector(trigger_zone=TRIGGER_ZONE)
        self.image_buffer = ImageBuffer()
        self.overlay = OverlayWindow()
        self.file_saver = FileSaver()
        self.toolbar = Toolbar(on_start_callback=self.start_capture_session)
        
        # State tracking
        self.capture_thread = None
        self.scroll_thread = None
        self.is_scroll_active = False
        self.last_scroll_time = 0
    
    def start_toolbar(self) -> None:
        """Create and show the toolbar."""
        self.toolbar.create()
        self.toolbar.show()
    
    def start_capture_session(self) -> None:
        """
        Start a capture session.
        
        Shows overlay and waits for user selection.
        """
        if self.state != CaptureState.IDLE:
            return
        
        self.state = CaptureState.SELECTING
        self.image_buffer.clear()
        self.region_tracker.reset()
        
        print(f"[{self.state}] Starting capture session...")
        
        # Create overlay
        self.overlay.create()
        self.overlay.show()
        
        # Setup mouse listener
        self.mouse_listener.set_on_mouse_move(self._on_mouse_move)
        self.mouse_listener.set_on_right_press(self._on_right_press)
        self.mouse_listener.set_on_right_release(self._on_right_release)
        self.mouse_listener.start()
    
    def _on_mouse_move(self, x: int, y: int) -> None:
        """Mouse move callback."""
        if self.state == CaptureState.SELECTING and self.region_tracker.is_active():
            # Update selection rectangle
            self.region_tracker.update_selection(x, y)
            region = self.region_tracker.get_current_region()
            if region:
                x1, y1, x2, y2 = region.get_normalized()
                self.overlay.draw_selection_rect(x1, y1, x2, y2)
        
        elif self.state == CaptureState.CAPTURING:
            # Check for scroll zones
            region = self.region_tracker.get_current_region()
            if region:
                scroll_dir = self.scroll_detector.detect_scroll_direction(
                    x, y, region,
                    self.screen_metrics.width,
                    self.screen_metrics.height
                )
                
                if scroll_dir and not self.is_scroll_active:
                    self.is_scroll_active = True
                    self._start_auto_scroll(scroll_dir)
                elif not scroll_dir:
                    self.is_scroll_active = False
    
    def _on_right_press(self, x: int, y: int) -> None:
        """Right-click press callback."""
        if self.state != CaptureState.SELECTING:
            return
        
        print(f"[{CaptureState.SELECTING}] Right-click pressed at ({x}, {y})")
        
        # Start selection
        self.region_tracker.start_selection(x, y)
        
        # Capture initial screenshot
        time.sleep(0.05)  # Small delay for stability
        
        try:
            # Create a minimal region for first capture
            region = CaptureRegion(x1=x, y1=y, x2=x+1, y2=y+1)
            initial_screenshot = self.screenshot_capturer.capture_full_screen()
            
            strip = ImageStrip(initial_screenshot, direction='initial')
            self.image_buffer.add_strip(strip)
            
            print(f"[{CaptureState.SELECTING}] Initial screenshot captured: {initial_screenshot.size}")
            
            self.state = CaptureState.CAPTURING
        except Exception as e:
            print(f"Error capturing initial screenshot: {e}")
            self._cancel_capture()
    
    def _on_right_release(self, x: int, y: int) -> None:
        """Right-click release callback."""
        if self.state != CaptureState.CAPTURING:
            return
        
        print(f"[{CaptureState.CAPTURING}] Right-click released at ({x}, {y})")
        
        # End selection
        final_region = self.region_tracker.end_selection()
        
        if not final_region or not final_region.is_valid(MIN_CAPTURE_SIZE):
            print(f"Invalid region: {final_region}")
            self._cancel_capture()
            return
        
        print(f"[{CaptureState.CAPTURING}] Selection complete: {final_region}")
        
        # Stop scrolling if active
        self.is_scroll_active = False
        
        # Close overlay
        self.overlay.close()
        self.mouse_listener.stop()
        
        # Process captured images
        self._process_and_save()
    
    def _start_auto_scroll(self, direction: str) -> None:
        """Start auto-scrolling in specified direction."""
        print(f"Auto-scroll triggered: {direction}")
        
        self.scroll_thread = threading.Thread(
            target=self._auto_scroll_loop,
            args=(direction,),
            daemon=True
        )
        self.scroll_thread.start()
    
    def _auto_scroll_loop(self, direction: str) -> None:
        """Loop for auto-scrolling."""
        while self.is_scroll_active and self.state == CaptureState.CAPTURING:
            try:
                # Scroll
                if direction == ScrollDirection.DOWN:
                    pyautogui.scroll(-SCROLL_STEP)
                elif direction == ScrollDirection.UP:
                    pyautogui.scroll(SCROLL_STEP)
                elif direction == ScrollDirection.RIGHT:
                    pyautogui.scroll(-SCROLL_STEP, x=0)  # Horizontal scroll
                elif direction == ScrollDirection.LEFT:
                    pyautogui.scroll(SCROLL_STEP, x=0)
                
                # Wait for render
                time.sleep(SCROLL_INTERVAL / 1000.0)
                
                # Capture strip
                region = self.region_tracker.get_current_region()
                if region and region.is_valid():
                    try:
                        strip_image = self.screenshot_capturer.capture_region(region)
                        strip = ImageStrip(strip_image, direction=direction)
                        
                        if self.image_buffer.add_strip(strip):
                            # Expand region
                            if direction == ScrollDirection.DOWN:
                                region.expand_bottom(SCROLL_STEP)
                            elif direction == ScrollDirection.UP:
                                region.expand_top(SCROLL_STEP)
                            elif direction == ScrollDirection.RIGHT:
                                region.expand_right(SCROLL_STEP)
                            elif direction == ScrollDirection.LEFT:
                                region.expand_left(SCROLL_STEP)
                            
                            # Update overlay
                            x1, y1, x2, y2 = region.get_normalized()
                            self.overlay.draw_selection_rect(x1, y1, x2, y2)
                        else:
                            print("Image buffer full")
                            break
                    except Exception as e:
                        print(f"Error capturing strip: {e}")
                        break
                
                # Check if still in trigger zone
                if not self.is_scroll_active:
                    break
                
            except Exception as e:
                print(f"Error in auto-scroll loop: {e}")
                break
    
    def _process_and_save(self) -> None:
        """Process captured strips and save final image."""
        print(f"[{CaptureState.PROCESSING}] Processing {len(self.image_buffer)} strips...")
        
        self.state = CaptureState.PROCESSING
        self.toolbar.update_status("Processing...")
        
        try:
            # Get all strips
            strips = self.image_buffer.get_all_strips()
            
            if not strips:
                raise ValueError("No strips captured")
            
            print(f"Stitching {len(strips)} strips...")
            
            # Stitch strips
            final_image = ImageStitcher.stitch_vertical(strips)
            print(f"Stitched image size: {final_image.size}")
            
            # Save
            filepath = self.file_saver.save_image(final_image)
            print(f"[{CaptureState.COMPLETE}] Saved to: {filepath}")
            
            self.state = CaptureState.COMPLETE
            self.toolbar.on_capture_complete()
            
            # Show confirmation popup
            popup = ConfirmationPopup()
            popup.show_success(filepath)
            
        except Exception as e:
            print(f"Error processing capture: {e}")
            popup = ConfirmationPopup()
            popup.show_error(str(e))
            self._cancel_capture()
    
    def _cancel_capture(self) -> None:
        """Cancel current capture session."""
        print(f"[{CaptureState.CANCELLED}] Capture cancelled")
        
        self.state = CaptureState.CANCELLED
        self.is_scroll_active = False
        
        if self.overlay.is_visible():
            self.overlay.close()
        
        self.mouse_listener.stop()
        self.region_tracker.reset()
        self.image_buffer.clear()
        
        self.toolbar.on_capture_cancelled()
        
        # Reset to idle
        time.sleep(0.5)
        self.state = CaptureState.IDLE


if __name__ == "__main__":
    # Test the module
    print("Testing CaptureOrchestrator...")
    
    orchestrator = ScrollSnipOrchestrator()
    print("Created orchestrator")
    print(f"Screen: {orchestrator.screen_metrics}")
