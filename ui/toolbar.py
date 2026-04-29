"""
Toolbar Module

Responsible for:
- Creating and managing the toolbar window
- Start/Stop button
- Simple UI for user to trigger capture
"""

import tkinter as tk
from typing import Callable, Optional


class Toolbar:
    """Simple toolbar with start capture button."""
    
    def __init__(self, on_start_callback: Callable = None):
        """
        Initialize toolbar.
        
        Args:
            on_start_callback: Function to call when "Start Capture" is clicked
        """
        self.on_start_callback = on_start_callback
        self.root = None
        self.is_running = False
    
    def create(self, x: int = 100, y: int = 100) -> None:
        """
        Create and show toolbar window.
        
        Args:
            x, y: Window position
        """
        self.root = tk.Tk()
        self.root.title("ScrollSnip")
        self.root.geometry("150x50+{}+{}".format(x, y))
        self.root.resizable(False, False)
        
        # Make always on top
        self.root.attributes('-topmost', True)
        
        # Start button
        self.start_button = tk.Button(
            self.root,
            text="Start Capture",
            command=self._on_start_clicked,
            width=18,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        self.start_button.pack(pady=10, padx=5)
        
        # Info label
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 8),
            fg="gray"
        )
        self.status_label.pack(pady=5)
    
    def _on_start_clicked(self) -> None:
        """Internal callback for start button click."""
        self.is_running = True
        self.start_button.config(state=tk.DISABLED, bg="#999999", text="Capturing...")
        self.update_status("Waiting for selection...")
        
        if self.on_start_callback:
            self.on_start_callback()
    
    def on_capture_complete(self) -> None:
        """Called when capture is complete."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL, bg="#4CAF50", text="Start Capture")
        self.update_status("Ready")
    
    def on_capture_cancelled(self) -> None:
        """Called when capture is cancelled."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL, bg="#4CAF50", text="Start Capture")
        self.update_status("Cancelled")
    
    def update_status(self, status_text: str) -> None:
        """
        Update status label.
        
        Args:
            status_text: Status message
        """
        if self.status_label:
            self.status_label.config(text=status_text)
            self.root.update()
    
    def show(self) -> None:
        """Show toolbar window."""
        if self.root:
            self.root.deiconify()
            self.root.mainloop()
    
    def hide(self) -> None:
        """Hide toolbar window."""
        if self.root:
            self.root.withdraw()
    
    def close(self) -> None:
        """Close toolbar window."""
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None
    
    def is_visible(self) -> bool:
        """Check if toolbar is visible."""
        return self.root is not None and self.root.winfo_exists()


if __name__ == "__main__":
    # Test the module
    print("Testing Toolbar...")
    
    def on_start():
        print("Start Capture clicked!")
    
    toolbar = Toolbar(on_start_callback=on_start)
    toolbar.create(x=100, y=100)
    
    # Simulate some updates
    import time
    toolbar.root.after(2000, lambda: toolbar.update_status("Capturing..."))
    toolbar.root.after(4000, lambda: toolbar.update_status("Waiting..."))
    toolbar.root.after(6000, lambda: toolbar.on_capture_complete())
    
    toolbar.show()
