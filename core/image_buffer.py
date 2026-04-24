"""
Image Buffer Module

Responsible for:
- Managing a queue/buffer of captured image strips
- Thread-safe operations
- Memory management
"""

from typing import List, Optional
from PIL import Image
import threading


class ImageStrip:
    """Represents a captured image strip."""
    
    def __init__(self, image: Image.Image, direction: str = None):
        """
        Initialize image strip.
        
        Args:
            image: PIL Image object
            direction: Direction strip came from ('up', 'down', 'left', 'right', 'initial')
        """
        self.image = image
        self.direction = direction
        self.timestamp = None
    
    def get_width(self) -> int:
        """Get width in pixels."""
        return self.image.width
    
    def get_height(self) -> int:
        """Get height in pixels."""
        return self.image.height
    
    def get_size(self) -> tuple:
        """Get (width, height)."""
        return self.image.size
    
    def __repr__(self) -> str:
        return f"ImageStrip({self.image.size}, direction={self.direction})"


class ImageBuffer:
    """Thread-safe buffer for storing captured image strips."""
    
    def __init__(self, max_size: int = 500):
        """
        Initialize image buffer.
        
        Args:
            max_size: Maximum number of strips to store
        """
        if max_size < 1:
            raise ValueError("Max size must be at least 1")
        
        self.max_size = max_size
        self.strips: List[ImageStrip] = []
        self._lock = threading.Lock()
    
    def add_strip(self, strip: ImageStrip) -> bool:
        """
        Add an image strip to buffer.
        
        Args:
            strip: ImageStrip to add
        
        Returns:
            bool: True if added, False if buffer full
        """
        with self._lock:
            if len(self.strips) >= self.max_size:
                return False
            
            self.strips.append(strip)
            return True
    
    def get_all_strips(self) -> List[ImageStrip]:
        """
        Get copy of all strips in buffer.
        
        Returns:
            List[ImageStrip]: All strips in order
        """
        with self._lock:
            return self.strips.copy()
    
    def get_strip_count(self) -> int:
        """
        Get number of strips in buffer.
        
        Returns:
            int: Number of strips
        """
        with self._lock:
            return len(self.strips)
    
    def is_full(self) -> bool:
        """
        Check if buffer is at capacity.
        
        Returns:
            bool: True if full
        """
        with self._lock:
            return len(self.strips) >= self.max_size
    
    def clear(self) -> None:
        """Clear all strips from buffer."""
        with self._lock:
            self.strips.clear()
    
    def get_total_pixels(self) -> int:
        """
        Calculate total pixels in all strips (for memory estimation).
        
        Returns:
            int: Total pixel count
        """
        with self._lock:
            total = 0
            for strip in self.strips:
                width, height = strip.get_size()
                total += width * height
            return total
    
    def get_buffer_memory_mb(self) -> float:
        """
        Estimate memory usage of all strips in MB.
        
        Assumes RGBA format (4 bytes per pixel).
        
        Returns:
            float: Estimated memory in MB
        """
        total_pixels = self.get_total_pixels()
        bytes_per_pixel = 4  # RGBA
        total_bytes = total_pixels * bytes_per_pixel
        return total_bytes / (1024 * 1024)
    
    def get_first_strip(self) -> Optional[ImageStrip]:
        """
        Get first strip without removing it.
        
        Returns:
            ImageStrip or None if buffer empty
        """
        with self._lock:
            return self.strips[0] if self.strips else None
    
    def get_last_strip(self) -> Optional[ImageStrip]:
        """
        Get last strip without removing it.
        
        Returns:
            ImageStrip or None if buffer empty
        """
        with self._lock:
            return self.strips[-1] if self.strips else None
    
    def __len__(self) -> int:
        """Get number of strips."""
        with self._lock:
            return len(self.strips)


if __name__ == "__main__":
    # Test the module
    from PIL import Image
    
    print("Testing ImageBuffer...")
    
    buffer = ImageBuffer(max_size=10)
    
    # Create test strips
    for i in range(5):
        img = Image.new('RGB', (800, 100))
        strip = ImageStrip(img, direction='down' if i > 0 else 'initial')
        success = buffer.add_strip(strip)
        print(f"Added strip {i+1}: {success}, Buffer size: {buffer.get_strip_count()}")
    
    print(f"\nBuffer memory usage: {buffer.get_buffer_memory_mb():.2f} MB")
    print(f"Is full: {buffer.is_full()}")
    
    # Test retrieval
    strips = buffer.get_all_strips()
    print(f"\nTotal strips: {len(strips)}")
    for i, strip in enumerate(strips):
        print(f"Strip {i}: {strip}")
    
    # Test clearing
    buffer.clear()
    print(f"\nAfter clear - Buffer size: {buffer.get_strip_count()}")
