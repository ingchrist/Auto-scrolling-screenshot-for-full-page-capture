"""
Image Stitcher Module

Responsible for:
- Combining image strips into one final image
- Handling different scroll directions
- Maintaining pixel-perfect alignment
"""

from typing import List
from PIL import Image
from core.image_buffer import ImageStrip


class ImageStitcher:
    """Stitches multiple image strips into a single image."""
    
    @staticmethod
    def stitch_vertical(strips: List[ImageStrip]) -> Image.Image:
        """
        Stitch image strips vertically (for up/down scrolling).
        
        Args:
            strips: List of ImageStrip objects
        
        Returns:
            PIL.Image: Stitched image
        
        Raises:
            ValueError: If strips list is empty or invalid
        """
        if not strips:
            raise ValueError("Cannot stitch empty strip list")
        
        # Get width from first strip (all should be same width)
        width = strips[0].get_width()
        
        # Calculate total height
        total_height = sum(strip.get_height() for strip in strips)
        
        # Create new image
        result = Image.new('RGB', (width, total_height))
        
        # Paste each strip
        y_offset = 0
        for strip in strips:
            result.paste(strip.image, (0, y_offset))
            y_offset += strip.get_height()
        
        return result
    
    @staticmethod
    def stitch_horizontal(strips: List[ImageStrip]) -> Image.Image:
        """
        Stitch image strips horizontally (for left/right scrolling).
        
        Args:
            strips: List of ImageStrip objects
        
        Returns:
            PIL.Image: Stitched image
        
        Raises:
            ValueError: If strips list is empty or invalid
        """
        if not strips:
            raise ValueError("Cannot stitch empty strip list")
        
        # Get height from first strip (all should be same height)
        height = strips[0].get_height()
        
        # Calculate total width
        total_width = sum(strip.get_width() for strip in strips)
        
        # Create new image
        result = Image.new('RGB', (total_width, height))
        
        # Paste each strip
        x_offset = 0
        for strip in strips:
            result.paste(strip.image, (x_offset, 0))
            x_offset += strip.get_width()
        
        return result
    
    @staticmethod
    def stitch_mixed(strips: List[ImageStrip]) -> Image.Image:
        """
        Stitch strips captured from mixed directions.
        
        Groups strips by direction and stitches appropriately.
        
        Args:
            strips: List of ImageStrip objects with direction info
        
        Returns:
            PIL.Image: Stitched image
        
        Raises:
            ValueError: If strips list is empty
        """
        if not strips:
            raise ValueError("Cannot stitch empty strip list")
        
        # For simplicity, vertical stitch is default
        # In a more complex scenario, could analyze directions
        return ImageStitcher.stitch_vertical(strips)
    
    @staticmethod
    def validate_strips_compatible(
        strips: List[ImageStrip],
        mode: str = 'vertical'
    ) -> bool:
        """
        Check if strips are compatible for stitching.
        
        Args:
            strips: List of strips to validate
            mode: 'vertical' or 'horizontal'
        
        Returns:
            bool: True if compatible
        """
        if not strips:
            return False
        
        if mode == 'vertical':
            # All strips should have same width
            width = strips[0].get_width()
            return all(strip.get_width() == width for strip in strips)
        
        elif mode == 'horizontal':
            # All strips should have same height
            height = strips[0].get_height()
            return all(strip.get_height() == height for strip in strips)
        
        return False


if __name__ == "__main__":
    # Test the module
    from PIL import Image
    
    print("Testing ImageStitcher...")
    
    # Create test strips
    strips = []
    for i in range(3):
        img = Image.new('RGB', (800, 100), color=(255, 0, 0))  # Red strips
        strip = ImageStrip(img, direction='down')
        strips.append(strip)
    
    print(f"Created {len(strips)} strips of {strips[0].get_size()}")
    
    # Test vertical stitching
    print("\nTesting vertical stitch...")
    stitched = ImageStitcher.stitch_vertical(strips)
    print(f"Stitched image size: {stitched.size}")
    expected_height = 300  # 3 strips * 100 pixels
    print(f"Expected height: {expected_height}, Got: {stitched.height}")
    assert stitched.height == expected_height, "Height mismatch!"
    
    # Test compatibility check
    print("\nTesting compatibility check...")
    compatible = ImageStitcher.validate_strips_compatible(strips, mode='vertical')
    print(f"Strips compatible for vertical stitch: {compatible}")
    
    # Save test image
    stitched.save("/tmp/test_stitched.png")
    print("Test stitched image saved to /tmp/test_stitched.png")
