# ScrollSnip - Scrollable Content Capture Tool

A Python desktop application that captures content beyond the visible screen area using smart auto-scrolling.

## Features

✨ **Smart Capture**: Select any area on screen with right-click and drag
🔄 **Auto-Scroll**: Automatically scrolls content when you drag toward screen edges  
📸 **Seamless Stitching**: Combines all captured strips into one tall image
💾 **Easy Save**: Saves as PNG with timestamp in your Pictures folder
🎯 **Precise**: Pixel-perfect alignment of scrolled content

## How It Works

1. Click **"Start Capture"** button
2. **Right-click and drag** to select a capture area
3. Move mouse **toward screen edges** (within 60px) to trigger auto-scroll
4. The tool automatically:
   - Scrolls the window
   - Captures new content strips
   - Expands your selection area
5. **Release right-click** to finish capturing
6. Image is stitched and saved automatically

## Technical Architecture

### Modular Design

The project is organized into independent, testable modules:

```
scrollsnip/
├── config.py                    # All configuration constants
├── main.py                      # Entry point
├── orchestrator.py              # Main workflow orchestration
│
├── core/                        # Core functionality modules
│   ├── screen_utils.py          # Screen dimensions and positioning
│   ├── mouse_listener.py        # Global mouse event handling
│   ├── overlay_window.py        # Fullscreen transparent overlay
│   ├── capture_region.py        # Selection rectangle tracking
│   ├── screenshot_capturer.py   # Screenshot capture logic
│   ├── scroll_detector.py       # Edge proximity detection
│   └── image_buffer.py          # Image strip management
│
├── processing/                  # Image processing
│   ├── image_stitcher.py        # Strip stitching logic
│   └── file_saver.py            # PNG file saving
│
└── ui/                          # User interface
    ├── toolbar.py               # Start capture button
    └── notifications.py         # Save confirmation popups
```

### Each Module Has Single Responsibility

| Module | Responsibility |
|--------|-----------------|
| `config.py` | Constants & configuration |
| `screen_utils.py` | Screen dimensions, DPI |
| `mouse_listener.py` | Global mouse events only |
| `overlay_window.py` | Window rendering |
| `capture_region.py` | Rectangle tracking |
| `screenshot_capturer.py` | Screenshot capture |
| `scroll_detector.py` | Edge zone detection |
| `image_buffer.py` | Strip buffer management |
| `image_stitcher.py` | Image combination |
| `file_saver.py` | File I/O |
| `notifications.py` | User notifications |
| `toolbar.py` | Toolbar UI |
| `orchestrator.py` | Workflow coordination |

## Installation

### Prerequisites

- Python 3.8+
- Linux, macOS, or Windows

### Setup

```bash
# Clone or navigate to scrollsnip directory
cd scrollsnip

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

- **pyautogui** (3.0.0) - Control mouse and keyboard
- **Pillow** (10.1.0) - Image processing
- **pynput** (1.7.6) - Global mouse listener
- **numpy** (1.24.3) - Numerical operations (used by Pillow)

## Usage

### Run the Application

```bash
python main.py
```

### Capture Process

1. **Start Button**: Click "Start Capture" in the toolbar
2. **Select Area**: Right-click and drag to define capture region
3. **Auto-Scroll**: Move mouse near screen edges to scroll:
   - **Bottom edge** (60px): Scrolls down
   - **Top edge** (60px): Scrolls up
   - **Right edge** (60px): Scrolls right
   - **Left edge** (60px): Scrolls left
4. **Release**: Release right-click to finish
5. **Save**: Choose to copy path, open folder, or close

### Configuration

Edit [config.py](config.py) to customize:

```python
# Scrolling
SCROLL_STEP = 3                # Pixels per scroll
TRIGGER_ZONE = 60              # Edge trigger distance
SCROLL_INTERVAL = 120          # ms between scrolls

# Output
OUTPUT_DIR = "~/Pictures/ScrollSnip"
OUTPUT_FORMAT = "PNG"

# UI
OVERLAY_ALPHA = 0.1            # Overlay transparency
SELECTION_RECT_COLOR = "blue"  # Selection color
```

## Troubleshooting

### Module Not Found Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Mouse Listener Not Working

- Check that pynput is installed
- On Linux, you may need additional system packages:
  ```bash
  sudo apt-get install python3-tk python3-dev
  ```

### Screenshots Not Capturing

- Verify pyautogui is installed correctly
- Some desktop environments may restrict screenshot access
- Try running with elevated permissions (if needed)

### Overlay Not Appearing

- Check that tkinter is installed
- Try running from a terminal to see error messages
- Some window managers may not support fullscreen transparent windows

## Development

### Running Tests

Each module has a `__main__` block for testing:

```bash
python core/screen_utils.py
python core/mouse_listener.py
python core/capture_region.py
python processing/image_stitcher.py
```

### Debugging

Enable debug mode in [config.py](config.py):

```python
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"
```

### Code Quality

The project uses modular design for easy maintenance:

- **Single Responsibility**: Each module does one thing
- **Low Coupling**: Modules use simple data types (dicts, objects)
- **High Cohesion**: Related logic is grouped together
- **Testable**: Each module can be tested independently
- **Scalable**: Easy to add features without modifying core logic

## Advanced Usage

### Custom Output Directory

```python
from processing.file_saver import FileSaver

saver = FileSaver(output_dir="/path/to/your/folder")
filepath = saver.save_image(image)
```

### Programmatic Usage

```python
from orchestrator import ScrollSnipOrchestrator

orchestrator = ScrollSnipOrchestrator()
orchestrator.start_toolbar()
```

### Batch Processing

Extend the orchestrator to process multiple captures:

```python
# Capture multiple times, processing each automatically
for i in range(num_captures):
    orchestrator.start_capture_session()
    # Results saved automatically
```

## Performance Notes

- **Memory**: Strips are stored in memory during capture
  - Each strip = width × height × 4 bytes (RGBA)
  - Buffer limited to 500 strips by default
- **Timing**: 120ms scroll interval allows window render time
- **Quality**: PNG format preserves full quality (no compression loss)

## Known Limitations

- Works best with vertically scrollable content
- Horizontal scrolling works but requires precise edge positioning
- Some applications may not respond to programmatic scrolling
- Overlay may not work on some specialized window managers

## Future Enhancements

Possible improvements (maintain modular structure):

- [ ] Video capture (mp4 encoding module)
- [ ] Cloud upload (cloud_saver.py module)
- [ ] OCR text recognition (ocr_module.py)
- [ ] Batch processing UI
- [ ] Custom scroll intervals per window
- [ ] Format options (JPG, WebP, PDF)

## License

MIT License - Feel free to use and modify

## Contributing

Issues and pull requests welcome!

---

**Made with ❤️ for easy screenshot capturing**
