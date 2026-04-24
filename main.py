"""
ScrollSnip - Main Entry Point

A desktop application for capturing scrollable content beyond the visible screen area.

Usage:
    python main.py
"""

import sys
from orchestrator import ScrollSnipOrchestrator


def main():
    """Main entry point."""
    print("=" * 60)
    print("ScrollSnip - Scrollable Content Capture Tool")
    print("=" * 60)
    print()
    print("Starting application...")
    print()
    print("Instructions:")
    print("1. Click 'Start Capture' button")
    print("2. Right-click and drag to select area")
    print("3. Move mouse to screen edges to auto-scroll")
    print("4. Release right-click to finish")
    print("5. Image will be saved and displayed")
    print()
    print("-" * 60)
    print()
    
    try:
        # Create and start orchestrator
        orchestrator = ScrollSnipOrchestrator()
        orchestrator.start_toolbar()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
