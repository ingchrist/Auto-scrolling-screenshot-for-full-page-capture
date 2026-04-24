# ScrollSnip Development Guide

Complete technical documentation for developers working on or extending ScrollSnip.

## Project Structure Deep Dive

### Data Flow Architecture

```
User Interface Layer (UI)
    ↓
    └→ toolbar.py        (Start button)
    └→ notifications.py  (Popups)
    
Orchestration Layer
    ↓
    └→ orchestrator.py   (State machine & workflow)
    
Core Capture Layer
    ├→ mouse_listener.py (Global events)
    ├→ overlay_window.py (Visual feedback)
    ├→ capture_region.py (Rectangle tracking)
    └→ scroll_detector.py (Edge detection)
    
Capture Execution Layer
    ├→ screenshot_capturer.py (Screenshot logic)
    ├→ image_buffer.py        (Strip storage)
    └→ screen_utils.py        (Screen info)
    
Processing Layer
    ├→ image_stitcher.py (Strip combining)
    └→ file_saver.py     (File I/O)
    
Configuration Layer
    └→ config.py (Constants)
```

### State Machine

```
┌─────────────────────────────────────────────────────┐
│                     CaptureState                     │
└─────────────────────────────────────────────────────┘

    IDLE
      ↓
      ├─→ User clicks "Start Capture"
      ↓
    SELECTING
      │
      ├─→ Overlay shown
      ├─→ Waiting for right-click press
      │
      └─→ Right-click press detected
      ↓
    CAPTURING
      │
      ├─→ Initial screenshot taken
      ├─→ Region tracking active
      ├─→ Auto-scroll triggered on edge
      │
      └─→ Right-click released OR User cancels
      ↓
    PROCESSING
      │
      ├─→ Strips stitched together
      ├─→ Image saved to disk
      │
      └─→ Popup shown
      ↓
    COMPLETE / CANCELLED → IDLE
```

## Key Modules Explained

### 1. Orchestrator (`orchestrator.py`)

**Responsibility**: Coordinates all components, manages state transitions

**Key Methods**:
- `start_toolbar()` - Show UI
- `start_capture_session()` - Initialize capture
- `_on_mouse_move()` - Handle mouse movement
- `_on_right_press()` - Start capture
- `_on_right_release()` - End capture
- `_auto_scroll_loop()` - Background scroll thread
- `_process_and_save()` - Finalize capture

**State Transitions**:
```python
IDLE → SELECTING (on start button click)
SELECTING → CAPTURING (on right-click press)
CAPTURING → PROCESSING (on right-click release)
PROCESSING → COMPLETE (on successful save)
Any → CANCELLED (on error)
COMPLETE/CANCELLED → IDLE (reset)
```

### 2. Mouse Listener (`core/mouse_listener.py`)

**Responsibility**: Global mouse event handling (works outside window focus)

**Key Features**:
- Uses `pynput.mouse.Listener` for global events
- Thread-safe with locks
- Three callback types: move, press, release
- Doesn't block application

**Usage**:
```python
listener = GlobalMouseListener()
listener.set_on_mouse_move(callback_func)
listener.set_on_right_press(callback_func)
listener.set_on_right_release(callback_func)
listener.start()
```

### 3. Capture Region Tracker (`core/capture_region.py`)

**Responsibility**: Track and manage the selection rectangle

**Key Data Class**:
```python
@dataclass
class CaptureRegion:
    x1, y1, x2, y2  # Raw coordinates (may not be normalized)
    
    Methods:
    - get_normalized() → (x1, y1, x2, y2)  # Ensure top-left/bottom-right
    - get_size() → (width, height)
    - is_valid(min_size) → bool
    - expand_bottom/top/left/right(pixels)  # Used for auto-scroll
```

**Tracker Usage**:
```python
tracker = CaptureRegionTracker()
tracker.start_selection(100, 100)           # Right-click point
tracker.update_selection(300, 250)          # Mouse moved to
tracker.get_current_region()                # Get live region
final = tracker.end_selection()             # Finalize on release
```

### 4. Scroll Detector (`core/scroll_detector.py`)

**Responsibility**: Determine if mouse is in edge trigger zones

**Algorithm**:
```python
# For each edge:
# 1. Check if mouse is in trigger zone (60px from edge)
# 2. Check if mouse is within the capture region bounds
# 3. Priority order: DOWN > UP > RIGHT > LEFT

# If mouse in bottom 60px AND within region width → SCROLL DOWN
# If mouse in top 60px AND within region width → SCROLL UP
# If mouse in right 60px AND within region height → SCROLL RIGHT
# If mouse in left 60px AND within region height → SCROLL LEFT
```

**Usage**:
```python
detector = ScrollDetector(trigger_zone=60)
direction = detector.detect_scroll_direction(
    mouse_x, mouse_y,
    region,
    screen_width, screen_height
)
# Returns: 'up', 'down', 'left', 'right', or None
```

### 5. Screenshot Capturer (`core/screenshot_capturer.py`)

**Responsibility**: Simple screenshot capture logic

**Key Methods**:
```python
capturer.capture_region(region)      # Capture CaptureRegion
capturer.capture_full_screen()       # Full screenshot
capturer.capture_strip(x, y, w, h)   # Specific rectangle
```

**Implementation**:
- Uses `pyautogui.screenshot(region=(x, y, w, h))`
- Returns PIL Image objects
- Thread-safe (each call is independent)

### 6. Image Buffer (`core/image_buffer.py`)

**Responsibility**: Thread-safe storage of captured image strips

**Key Methods**:
```python
buffer.add_strip(strip)              # Add to buffer
buffer.get_all_strips()              # Get copy of all
buffer.get_strip_count()             # Number of strips
buffer.is_full()                     # Check if at max capacity
buffer.clear()                       # Clear all
buffer.get_buffer_memory_mb()        # Memory usage estimate
```

**Thread Safety**: Uses `threading.Lock()` for all operations

### 7. Image Stitcher (`processing/image_stitcher.py`)

**Responsibility**: Combine image strips into final image

**Key Methods**:
```python
ImageStitcher.stitch_vertical(strips)     # Stack vertically
ImageStitcher.stitch_horizontal(strips)   # Stack horizontally
ImageStitcher.validate_strips_compatible(strips, mode)
```

**Algorithm for Vertical Stitching**:
```
1. Get width from first strip (all must match)
2. Sum all heights
3. Create new image(width, total_height)
4. For each strip, paste at y_offset
5. Increment y_offset by strip height
6. Return combined image
```

### 8. File Saver (`processing/file_saver.py`)

**Responsibility**: Save PNG with timestamp

**Key Methods**:
```python
saver.save_image(image)                   # Auto-generate filename
saver.save_image(image, filename)         # Custom filename
saver.generate_filename()                 # Get timestamp-based name
saver.get_latest_file()                   # Most recent file
saver.get_file_list()                     # All captured files
```

**Filename Format**: `scrollsnip_YYYYMMDD_HHMMSS.png`

## Common Patterns

### Thread-Safe Callbacks

```python
# Pattern used in mouse_listener.py
def set_on_mouse_move(self, callback: Callable):
    self.on_mouse_move_callback = callback

# Called from listener thread:
def _on_move(self, x, y):
    with self._lock:
        self.current_pos = (x, y)
    
    if self.on_mouse_move_callback:
        self.on_mouse_move_callback(x, y)
```

### Data Class Pattern

```python
# Used throughout for clean data passing
@dataclass
class ImageStrip:
    image: Image.Image
    direction: str
    
    def get_width(self) -> int:
        return self.image.width
```

### Single-Threaded Main, Background Workers

```python
# Main thread (GUI):
orchestrator = ScrollSnipOrchestrator()
orchestrator.start_toolbar()  # Blocks in mainloop

# Background thread (scroll):
def start_auto_scroll(direction):
    thread = threading.Thread(
        target=self._auto_scroll_loop,
        args=(direction,),
        daemon=True
    )
    thread.start()
```

## Extending ScrollSnip

### Adding a New Feature

**Example: Save to Clipboard**

1. **Create module** in appropriate folder:
   ```python
   # processing/clipboard_saver.py
   import pyperclip
   
   class ClipboardSaver:
       def copy_image_to_clipboard(self, image):
           # Implementation
   ```

2. **Update orchestrator** to use it:
   ```python
   from processing.clipboard_saver import ClipboardSaver
   
   self.clipboard_saver = ClipboardSaver()
   # In _process_and_save():
   self.clipboard_saver.copy_image_to_clipboard(final_image)
   ```

3. **Update config** for options:
   ```python
   COPY_TO_CLIPBOARD = True
   ```

### Adding Cloud Upload

1. Create `processing/cloud_uploader.py`
2. Implement upload logic
3. Add config for credentials
4. Call from orchestrator after save

**Structure remains clean** - new module doesn't affect existing code!

## Testing Strategies

### Unit Testing Individual Modules

```python
# test_capture_region.py
def test_region_normalize():
    region = CaptureRegion(500, 200, 100, 300)
    assert region.get_normalized() == (100, 200, 500, 300)

def test_region_expand():
    region = CaptureRegion(100, 100, 300, 300)
    region.expand_bottom(50)
    assert region.y2 == 350
```

### Running Module Tests

Each module has `__main__` for testing:

```bash
python core/screen_utils.py
python core/capture_region.py
python processing/image_stitcher.py
```

### Integration Testing

```python
# Test full workflow without UI
def test_full_capture():
    orch = ScrollSnipOrchestrator()
    
    # Simulate user actions
    orch._on_right_press(100, 100)
    orch._on_right_release(500, 400)
    
    # Check file was created
    assert os.path.exists(orch.file_saver.get_latest_file())
```

## Performance Considerations

### Memory Usage

- Each screenshot strip ≈ width × height × 4 bytes
- Example: 1920×1080 = ~8MB per strip
- 500-strip limit ≈ 4GB max buffer

### CPU Usage

- Mouse listener runs in background thread
- Scroll loop has 120ms sleep between captures
- Screenshot capture is blocking (pyautogui limitation)

### Optimization Tips

1. **Reduce scroll interval** in config for faster capture
2. **Increase trigger zone** to catch edge scrolls earlier
3. **Limit buffer size** to prevent memory issues on large captures
4. **Use smaller regions** to reduce strip size

## Debugging Tips

### Enable Verbose Logging

```python
# In orchestrator.py
print(f"[{self.state}] Event: {event_name}")
```

### Capture State at Each Step

```python
print(f"Region: {region}")
print(f"Buffer size: {image_buffer.get_strip_count()}")
print(f"Memory: {image_buffer.get_buffer_memory_mb()}MB")
```

### Test Individual Components

```python
# Test overlay independently
overlay = OverlayWindow()
overlay.create()
overlay.show()
overlay.draw_selection_rect(100, 100, 500, 400)

# Test capture without full workflow
capturer = ScreenshotCapturer()
img = capturer.capture_region(CaptureRegion(0, 0, 400, 300))
img.save("/tmp/test.png")
```

## Code Style Guidelines

- **Module names**: `snake_case`
- **Class names**: `PascalCase`
- **Function names**: `snake_case`
- **Constants**: `UPPER_CASE`
- **Private methods**: `_leading_underscore`

**Docstring format**:
```python
def function(param1: Type1, param2: Type2) -> ReturnType:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        ReturnType: Description
    
    Raises:
        ExceptionType: When this happens
    """
```

## Troubleshooting Development

### Import Circular Dependencies

- Keep dependencies unidirectional (core → processing → ui)
- Don't import orchestrator into core modules
- Use simple data types (dicts, tuples) for passing between modules

### Thread Safety Issues

- Always use `threading.Lock()` for shared state
- Never access `self.state` from multiple threads without lock
- Test with concurrent operations

### Performance Problems

1. Profile with `cProfile`:
   ```python
   import cProfile
   cProfile.run('orchestrator.start_capture_session()')
   ```

2. Check memory with `tracemalloc`:
   ```python
   import tracemalloc
   tracemalloc.start()
   # ... code ...
   current, peak = tracemalloc.get_traced_memory()
   print(f"Memory: {peak / 1024 / 1024}MB")
   ```

---

**Happy coding! 🚀**
