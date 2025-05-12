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

# Launch the main application
echo "Launching OVERSIGHT application..."
$PYTHON_CMD "$APP_DIR/nikimonitorscreenADMIN.py" 2>&1

# Capture the exit code
EXIT_CODE=$?

# If there was an error, display it
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "-------------------------------------"
    echo "Application exited with error code: $EXIT_CODE"
    echo "Please check the error messages above."
else
    echo ""
    echo "-------------------------------------"
    echo "Application closed normally."
fi

# Keep the terminal open for a while to read the error messages
echo ""
echo "This window will close in 30 seconds..."
sleep 30 