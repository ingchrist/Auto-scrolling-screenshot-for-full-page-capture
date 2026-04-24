# ScrollSnip - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd scrollsnip

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python main.py
```

A toolbar window will appear with a "Start Capture" button.

## Usage (2 minutes)

1. **Click "Start Capture"** button
2. **Right-click and drag** to select capture area
3. **Move mouse to edges** to auto-scroll (60px from edge):
   - Near **bottom** → Scrolls down
   - Near **top** → Scrolls up
   - Near **right** → Scrolls right
   - Near **left** → Scrolls left
4. **Release right-click** when done
5. Choose to **copy path**, **open folder**, or **close**

## Common Issues & Solutions

### Error: `ModuleNotFoundError: No module named 'pyautogui'`

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Error: `ModuleNotFoundError: No module named 'tkinter'`

**Linux**: Install tkinter
```bash
sudo apt-get install python3-tk
```

**macOS**: Usually included; if not:
```bash
brew install python-tk
```

**Windows**: Included with Python; reinstall if missing

### Overlay doesn't appear

- Check that tkinter is installed
- Try running from terminal to see error messages
- Some window managers may not support transparent windows

### Mouse listener not working

- Ensure pynput is installed: `pip install pynput`
- Try running with elevated permissions if needed
- Check that mouse permissions are granted in system settings

## Configuration

Edit `config.py` to customize behavior:

```python
# Adjust scrolling speed (lower = faster, higher = slower)
SCROLL_STEP = 3                    # Pixels per scroll
TRIGGER_ZONE = 60                  # Edge distance to trigger
SCROLL_INTERVAL = 120              # Milliseconds between scrolls

# Change save location
OUTPUT_DIR = "~/Pictures/ScrollSnip"

# Adjust overlay appearance
OVERLAY_ALPHA = 0.1                # 0 = invisible, 1 = opaque
SELECTION_RECT_COLOR = "blue"      # Color of selection box
SELECTION_RECT_WIDTH = 2           # Thickness of border
```

## File Organization

Saved screenshots go to:
```
~/Pictures/ScrollSnip/
├── scrollsnip_20260424_143022.png
├── scrollsnip_20260424_143515.png
├── scrollsnip_20260424_150300.png
└── ...
```

Format: `scrollsnip_YYYYMMDD_HHMMSS.png`

## Keyboard Shortcuts

Currently no keyboard shortcuts. To trigger:
- Click **"Start Capture"** button in toolbar

## Tips & Tricks

### Capture Long Scrollable Pages

1. Start capture on article/page beginning
2. Let ScrollSnip auto-scroll to bottom by hovering near edge
3. Release when done

### Capture Multi-Column Content

Drag horizontally to capture left-to-right scrolling content:
1. Select narrow vertical region
2. Hover near right edge to scroll right
3. Let it capture each column

### Adjust Sensitivity

- **Too fast?** Increase `SCROLL_INTERVAL` in config.py
- **Too slow?** Decrease `SCROLL_INTERVAL`
- **Wrong edge distance?** Adjust `TRIGGER_ZONE`

### Check Memory Usage

For long captures, check buffer status by adding to config:

```python
DEBUG_MODE = True
```

This prints memory usage during capture.

## Next Steps

- Read [README.md](README.md) for full feature list
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for technical details
- Modify `config.py` to suit your workflow

## Getting Help

### Check Existing Modules

Each module has test code at the bottom:

```bash
# Test individual components
python core/screen_utils.py
python core/capture_region.py
python processing/image_stitcher.py
```

### Debug Mode

Enable detailed logging:

```python
# In config.py
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"
```

Then run:
```bash
python main.py
```

Error messages will appear in terminal.

---

**Enjoy capturing scrollable content! 🎉**
