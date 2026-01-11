#!/usr/bin/env bash
set -e

# ------------------------------
# FlaskProject Installer Script
# ------------------------------
# This script builds your Python package and installs it globally using pipx
# Works on Linux
# ------------------------------

echo "Starting FlaskProject installation..."

# Step 1: Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi
PYTHON=$(command -v python3)
echo "Python found at $PYTHON"

# Step 2: Check pipx, install if missing
if ! command -v pipx &> /dev/null; then
    echo "pipx not found, installing..."
    # Install pipx using Python's ensurepip
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    export PATH="$HOME/.local/bin:$PATH"
    echo "pipx installed successfully."
else
    echo "pipx found."
fi

# Step 3: Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Adding ~/.local/bin to PATH for this session..."
    export PATH="$HOME/.local/bin:$PATH"
fi

if ! python3 -m pip show build &> /dev/null; then
    echo "Installing build module..."
    python3 -m pip install --user build
fi

# Step 4: Build the wheel
echo "Building FlaskProject wheel..."
python3 -m build

# Step 5: Install with pipx
WHEEL_FILE=$(ls dist/flaskproject-*.whl | head -n 1)
if [ -z "$WHEEL_FILE" ]; then
    echo "Error: wheel file not found in dist/"
    exit 1
fi

echo "Installing FlaskProject using pipx..."
pipx install --force "$WHEEL_FILE" || {
    echo "pipx installation failed. Trying pip user install..."
    python3 -m pip install --user "$WHEEL_FILE";
}

echo "FlaskProject installed successfully!"

# Step 6: Test the command
if command -v FlaskProject &> /dev/null; then
    echo "You can now run FlaskProject from any terminal:"
    echo "    FlaskProject"
else
    echo "Warning: FlaskProject command not found. Make sure ~/.local/bin is in your PATH."
fi

echo "Installation complete."
