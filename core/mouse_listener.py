"""
Mouse Listener Module

Responsible for:
- Capturing global mouse events (right-click, mouse move)
- Thread-safe event handling
- No dependency on tkinter window focus
"""

from typing import Callable, Optional
from pynput import mouse
from pynput.mouse import Listener, Button
import threading


class MouseState:
    """Data class for mouse information."""
    
    def __init__(self, x: int, y: int, is_right_clicked: bool = False):
        self.x = x
        self.y = y
        self.is_right_clicked = is_right_clicked
    
    def __repr__(self) -> str:
        return f"MouseState(x={self.x}, y={self.y}, right_clicked={self.is_right_clicked})"


class GlobalMouseListener:
    """
    Listens for global mouse events using pynput.
    
    This works even when the tkinter window is not focused.
    """
    
    def __init__(self):
        """Initialize the mouse listener."""
        self.current_pos = (0, 0)
        self.is_right_pressed = False
        
        # Callbacks
        self.on_mouse_move_callback: Optional[Callable[[int, int], None]] = None
        self.on_right_press_callback: Optional[Callable[[int, int], None]] = None
        self.on_right_release_callback: Optional[Callable[[int, int], None]] = None
        
        # Thread management
        self._listener: Optional[Listener] = None
        self._listener_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._lock = threading.Lock()
    
    def start(self) -> None:
        """Start listening for global mouse events."""
        if self._is_running:
            return
        
        self._is_running = True
        self._listener = Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll
        )
        self._listener.start()
    
    def stop(self) -> None:
        """Stop listening for global mouse events."""
        if not self._is_running:
            return
        
        self._is_running = False
        if self._listener:
            self._listener.stop()
            self._listener = None
    
    def _on_move(self, x: int, y: int) -> None:
        """Internal callback for mouse move events."""
        with self._lock:
            self.current_pos = (x, y)
        
        if self.on_mouse_move_callback:
            self.on_mouse_move_callback(x, y)
    
    def _on_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        """Internal callback for mouse click events."""
        if button != Button.right:
            return
        
        with self._lock:
            self.is_right_pressed = pressed
        
        if pressed and self.on_right_press_callback:
            self.on_right_press_callback(x, y)
        elif not pressed and self.on_right_release_callback:
            self.on_right_release_callback(x, y)
    
    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """Internal callback for scroll events (not used currently)."""
        pass
    
    def set_on_mouse_move(self, callback: Callable[[int, int], None]) -> None:
        """
        Set callback for mouse move events.
        
        Args:
            callback: Function(x, y) called on mouse move
        """
        self.on_mouse_move_callback = callback
    
    def set_on_right_press(self, callback: Callable[[int, int], None]) -> None:
        """
        Set callback for right-click press.
        
        Args:
            callback: Function(x, y) called on right-click press
        """
        self.on_right_press_callback = callback
    
    def set_on_right_release(self, callback: Callable[[int, int], None]) -> None:
        """
        Set callback for right-click release.
        
        Args:
            callback: Function(x, y) called on right-click release
        """
        self.on_right_release_callback = callback
    
    def get_current_position(self) -> tuple:
        """
        Get current mouse position (thread-safe).
        
        Returns:
            tuple: (x, y)
        """
        with self._lock:
            return self.current_pos
    
    def is_right_button_pressed(self) -> bool:
        """
        Check if right button is currently pressed (thread-safe).
        
        Returns:
            bool: True if right button pressed
        """
        with self._lock:
            return self.is_right_pressed
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


if __name__ == "__main__":
    # Test the module
    import time
    
    print("Testing GlobalMouseListener...")
    print("Move your mouse and press right-click (will exit after 5 seconds)")
    
    listener = GlobalMouseListener()
    
    def on_move(x, y):
        print(f"Mouse moved to ({x}, {y})")
    
    def on_right_press(x, y):
        print(f"Right-click pressed at ({x}, {y})")
    
    def on_right_release(x, y):
        print(f"Right-click released at ({x}, {y})")
    
    listener.set_on_mouse_move(on_move)
    listener.set_on_right_press(on_right_press)
    listener.set_on_right_release(on_right_release)
    
    listener.start()
    
    try:
        time.sleep(5)
    finally:
        listener.stop()
        print("Listener stopped")
