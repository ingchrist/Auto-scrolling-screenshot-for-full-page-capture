"""
Overlay Window Module

Responsible for:
- Creating fullscreen transparent overlay
- Drawing selection rectangle
- Rendering crosshair cursor
"""

import tkinter as tk
from core.screen_utils import get_screen_size


class OverlayWindow:
    """Fullscreen transparent overlay for selection."""
    
    def __init__(self, alpha: float = 0.1):
        """
        Initialize overlay window.
        
        Args:
            alpha: Window transparency (0.0 = transparent, 1.0 = opaque)
        """
        self.alpha = alpha
        self.root = None
        self.canvas = None
        self.selection_rect_id = None
        
        # Drawing configuration
        self.rect_color = "blue"
        self.rect_width = 2
        self.crosshair_color = "red"
        self.crosshair_size = 20
    
    def create(self) -> tk.Tk:
        """
        Create the overlay window.
        
        Returns:
            tk.Tk: Root window object
        """
        screen_width, screen_height = get_screen_size()
        
        self.root = tk.Tk()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.attributes('-alpha', self.alpha)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='gray')
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            bg='gray',
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        return self.root
    
    def show(self) -> None:
        """Display the overlay."""
        if self.root:
            self.root.deiconify()
    
    def hide(self) -> None:
        """Hide the overlay."""
        if self.root:
            self.root.withdraw()
    
    def close(self) -> None:
        """Close the overlay."""
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None
            self.canvas = None
    
    def draw_selection_rect(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Draw or update selection rectangle.
        
        Args:
            x1, y1: Top-left corner
            x2, y2: Bottom-right corner
        """
        if not self.canvas:
            return
        
        # Delete previous rectangle
        if self.selection_rect_id:
            self.canvas.delete(self.selection_rect_id)
        
        # Draw new rectangle
        self.selection_rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=self.rect_color,
            width=self.rect_width,
            fill=""
        )
        
        self.canvas.update()
    
    def draw_crosshair(self, x: int, y: int) -> None:
        """
        Draw crosshair at position (for visual feedback).
        
        Args:
            x, y: Center position
        """
        if not self.canvas:
            return
        
        size = self.crosshair_size
        
        # Clear previous crosshairs
        self.canvas.delete("crosshair")
        
        # Draw horizontal line
        self.canvas.create_line(
            x - size, y, x + size, y,
            fill=self.crosshair_color,
            tags="crosshair"
        )
        
        # Draw vertical line
        self.canvas.create_line(
            x, y - size, x, y + size,
            fill=self.crosshair_color,
            tags="crosshair"
        )
        
        self.canvas.update()
    
    def clear_drawing(self) -> None:
        """Clear all drawings (rectangle and crosshair)."""
        if self.canvas:
            self.canvas.delete("all")
            self.selection_rect_id = None
            self.canvas.update()
    
    def set_alpha(self, alpha: float) -> None:
        """
        Update window transparency.
        
        Args:
            alpha: New transparency value (0.0-1.0)
        """
        if not (0.0 <= alpha <= 1.0):
            raise ValueError("Alpha must be between 0.0 and 1.0")
        
        self.alpha = alpha
        if self.root:
            self.root.attributes('-alpha', alpha)
    
    def is_visible(self) -> bool:
        """Check if overlay is visible."""
        return self.root is not None and self.root.winfo_exists()
    
    def update(self) -> None:
        """Process pending events."""
        if self.root:
            self.root.update()


if __name__ == "__main__":
    # Test the module
    print("Testing OverlayWindow...")
    print("Window will show for 5 seconds with a rectangle")
    
    overlay = OverlayWindow(alpha=0.2)
    overlay.create()
    overlay.show()
    
    # Draw a test rectangle
    overlay.draw_selection_rect(100, 100, 500, 400)
    
    # Draw crosshair at different positions
    for x in [200, 300, 400]:
        overlay.root.after(1000, lambda x=x: overlay.draw_crosshair(x, 250))
    
    # Close after 5 seconds
    overlay.root.after(5000, overlay.close)
    
    try:
        overlay.root.mainloop()
    except:
        pass
