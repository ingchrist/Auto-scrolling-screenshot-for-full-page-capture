"""
File Saver Module

Responsible for:
- Saving PNG files with timestamp
- Creating output directory
- Generating filenames
"""

import os
from datetime import datetime
from pathlib import Path
from PIL import Image
from typing import Optional


class FileSaver:
    """Saves screenshots to disk."""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize file saver.
        
        Args:
            output_dir: Directory to save files to (defaults to ~/Pictures/ScrollSnip)
        """
        if output_dir is None:
            output_dir = os.path.expanduser("~/Pictures/ScrollSnip")
        
        self.output_dir = Path(output_dir)
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_filename(self) -> str:
        """
        Generate filename with timestamp.
        
        Format: scrollsnip_YYYYMMDD_HHMMSS.png
        
        Returns:
            str: Filename without path
        """
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        return f"scrollsnip_{timestamp}.png"
    
    def save_image(self, image: Image.Image, filename: str = None) -> str:
        """
        Save image to disk.
        
        Args:
            image: PIL Image to save
            filename: Optional custom filename (if None, uses generated name)
        
        Returns:
            str: Full path to saved file
        
        Raises:
            ValueError: If image is invalid
            IOError: If file cannot be written
        """
        if image is None:
            raise ValueError("Image cannot be None")
        
        if filename is None:
            filename = self.generate_filename()
        
        filepath = self.output_dir / filename
        
        try:
            image.save(str(filepath), format='PNG')
            return str(filepath)
        except Exception as e:
            raise IOError(f"Failed to save image to {filepath}: {e}")
    
    def get_output_directory(self) -> str:
        """
        Get output directory path.
        
        Returns:
            str: Directory path
        """
        return str(self.output_dir)
    
    def get_file_list(self) -> list:
        """
        Get list of all saved screenshots.
        
        Returns:
            list: List of file paths
        """
        return list(self.output_dir.glob("scrollsnip_*.png"))
    
    def get_latest_file(self) -> Optional[str]:
        """
        Get path to most recently saved file.
        
        Returns:
            str: File path or None if no files exist
        """
        files = self.get_file_list()
        if not files:
            return None
        
        # Sort by modification time
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        return str(files[0])
    
    def set_output_directory(self, directory: str) -> None:
        """
        Change output directory.
        
        Args:
            directory: New output directory path
        """
        self.output_dir = Path(directory)
        self._ensure_output_dir()


if __name__ == "__main__":
    # Test the module
    from PIL import Image
    
    print("Testing FileSaver...")
    
    saver = FileSaver()
    print(f"Output directory: {saver.get_output_directory()}")
    
    # Create a test image
    test_image = Image.new('RGB', (800, 600), color=(0, 255, 0))
    
    # Save it
    print("\nSaving test image...")
    filepath = saver.save_image(test_image)
    print(f"Saved to: {filepath}")
    
    # Verify it exists
    if os.path.exists(filepath):
        print("✓ File successfully created")
    else:
        print("✗ File was not created")
    
    # Get latest file
    latest = saver.get_latest_file()
    print(f"Latest file: {latest}")
    
    # List all files
    files = saver.get_file_list()
    print(f"Total saved files: {len(files)}")
