#!/bin/bash
# Quick setup and run script for ScrollSnip

set -e  # Exit on error

echo "================================"
echo "ScrollSnip - Quick Setup"
echo "================================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if Python 3.8+
major=$(echo $python_version | cut -d. -f1)
minor=$(echo $python_version | cut -d. -f2)
if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
    echo "✗ Python 3.8+ required (you have $python_version)"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Display next steps
echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To run ScrollSnip:"
echo ""
echo "  1. Activate environment (if not already active):"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python main.py"
echo ""
echo "================================"
echo ""
