"""
Notifications Module

Responsible for:
- Showing popup notifications
- Displaying confirmation dialogs
- User feedback
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable


class ConfirmationPopup:
    """Shows a confirmation popup for saved files."""
    
    def __init__(self, title: str = "ScrollSnip", auto_close_ms: int = None):
        """
        Initialize confirmation popup.
        
        Args:
            title: Window title
            auto_close_ms: Auto-close after N milliseconds (None = manual close)
        """
        self.title = title
        self.auto_close_ms = auto_close_ms
        self.result = None
        self.root = None
    
    def show_success(self, filepath: str, on_close: Callable = None) -> Optional[str]:
        """
        Show success popup for saved file.
        
        Args:
            filepath: Path to saved file
            on_close: Callback when popup closes
        
        Returns:
            str: Selected option ('copy', 'open', 'close') or None
        """
        message = f"Screenshot saved successfully!\n\n{filepath}"
        
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry("450x150")
        self.root.resizable(False, False)
        
        # Make it always on top
        self.root.attributes('-topmost', True)
        
        # Message label
        label = tk.Label(self.root, text=message, wraplength=400, justify=tk.LEFT)
        label.pack(pady=10, padx=10)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        def on_copy():
            self.result = 'copy'
            # Copy filepath to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(filepath)
            self.root.destroy()
            if on_close:
                on_close()
        
        def on_open():
            self.result = 'open'
            import subprocess
            import platform
            
            # Open file location
            if platform.system() == 'Windows':
                subprocess.Popen(f'explorer /select, "{filepath}"')
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', '-R', filepath])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(filepath)])
            
            self.root.destroy()
            if on_close:
                on_close()
        
        def on_close_click():
            self.result = 'close'
            self.root.destroy()
            if on_close:
                on_close()
        
        tk.Button(button_frame, text="Copy Path", command=on_copy, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Open", command=on_open, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=on_close_click, width=12).pack(side=tk.LEFT, padx=5)
        
        # Auto-close if specified
        if self.auto_close_ms:
            self.root.after(self.auto_close_ms, on_close_click)
        
        self.root.mainloop()
        
        return self.result
    
    def show_error(self, error_message: str) -> None:
        """
        Show error popup.
        
        Args:
            error_message: Error message to display
        """
        messagebox.showerror(self.title, f"Error: {error_message}")
    
    def show_info(self, message: str) -> None:
        """
        Show info popup.
        
        Args:
            message: Info message to display
        """
        messagebox.showinfo(self.title, message)
    
    def ask_yes_no(self, question: str) -> bool:
        """
        Show yes/no confirmation popup.
        
        Args:
            question: Question to ask
        
        Returns:
            bool: True if yes, False if no
        """
        return messagebox.askyesno(self.title, question)


class Toast:
    """Simple toast notification (doesn't block execution)."""
    
    def __init__(self, message: str, duration_ms: int = 2000):
        """
        Show a toast notification.
        
        Args:
            message: Message to display
            duration_ms: Duration in milliseconds
        """
        self.message = message
        self.duration_ms = duration_ms
        self.root = None
    
    def show(self) -> None:
        """Display the toast."""
        self.root = tk.Tk()
        self.root.geometry("300x80")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.8)
        
        label = tk.Label(self.root, text=self.message, wraplength=280, justify=tk.CENTER)
        label.pack(expand=True)
        
        self.root.after(self.duration_ms, self.root.destroy)


if __name__ == "__main__":
    # Test the module
    print("Testing Notifications...")
    
    popup = ConfirmationPopup()
    
    # Test success popup (with auto-close)
    print("Showing success popup...")
    result = popup.show_success(
        "/home/user/Pictures/ScrollSnip/scrollsnip_20260424_143022.png",
        auto_close_ms=3000
    )
    print(f"Result: {result}")
    
    # Test error popup
    # popup.show_error("Failed to capture screenshot")
    
    # Test info popup
    # popup.show_info("Capture session ended")
