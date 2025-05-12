#!/bin/bash

# Set the path to the application directory
APP_DIR="/Users/kian/Desktop/Software/nikimonitorscreen"

# Change to the application directory
cd "$APP_DIR"

# Print a message to indicate the application is starting
echo "Starting OVERSIGHT application..."
echo "-------------------------------------"
echo "Running from: $APP_DIR"
echo "Current date and time: $(date)"
echo "Version: 1.5.3 (Tab Indicator Fix)"
echo "-------------------------------------"

# Determine the Python command to use
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found. Please install Python 3 to run this application."
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"
echo "Python version: $($PYTHON_CMD --version)"
echo "-------------------------------------"

# Run the application
$PYTHON_CMD nikimonitorscreenADMIN.py

exit 0 