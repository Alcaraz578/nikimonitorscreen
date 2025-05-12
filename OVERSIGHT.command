#!/bin/bash

# Set the path to your desktop
DESKTOP_PATH="/Users/kian/Desktop"

# Change to the desktop directory
cd "$DESKTOP_PATH"

# Launch the main application
python3 "$DESKTOP_PATH/nikimonitorscreenADMIN.py"

# If the application exits, keep the terminal open
echo "Application has closed. Press Enter to exit this window."
read -p "" 