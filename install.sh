#!/bin/bash

# =====================================
# ProjGen Installer (Linux / macOS)
# pipx + PyInstaller + rich (PEP 668 safe)
# =====================================

set -e

echo "====================================="
echo "ProjGen Installer"
echo "====================================="
echo

# ---- Resolve paths ----
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$ROOT_DIR/app"
BUILD_APP="$ROOT_DIR/run.py"
INSTALL_BIN="$HOME/.local/bin"

# ---- Sanity check ----
if [ ! -f "$BUILD_APP" ]; then
    echo "ERROR: run.py not found in project root."
    exit 1
fi

# ---- Check Python ----
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python3 is not installed or not in PATH."
    exit 1
fi

# ---- Check pipx ----
if ! command -v pipx >/dev/null 2>&1; then
    echo "pipx not found. Installing..."

    if command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --noconfirm python-pipx
    elif command -v brew >/dev/null 2>&1; then
        brew install pipx
    else
        python3 -m pip install --user pipx
    fi

    pipx ensurepath
fi

# ---- Install PyInstaller via pipx ----
if ! pipx list | grep -q pyinstaller; then
    echo "Installing PyInstaller via pipx..."
    pipx install pyinstaller
fi

# ---- Ensure rich is available to PyInstaller ----
if ! pipx run python -c "import rich" >/dev/null 2>&1; then
    echo "Injecting rich into PyInstaller environment..."
    pipx inject pyinstaller rich
fi

# ---- Build executable ----
echo
echo "Building projgen executable..."
echo

pipx run pyinstaller \
    --clean \
    --onefile \
    --name projgen \
    --paths "$APP_DIR" \
    --hidden-import app.TemplateFunctions \
    --hidden-import app.Utils \
    --collect-all rich \
    --add-data "$APP_DIR/TemplateOptions.json:app" \
    --add-data "$APP_DIR/templates:app/templates" \
    "$BUILD_APP"

# ---- Install binary ----
mkdir -p "$INSTALL_BIN"
cp "$ROOT_DIR/dist/projgen" "$INSTALL_BIN/projgen"
chmod +x "$INSTALL_BIN/projgen"

# ---- Warn if PATH is missing ~/.local/bin ----
if [[ ":$PATH:" != *":$INSTALL_BIN:"* ]]; then
    echo
    echo "WARNING: $INSTALL_BIN is not in your PATH."
    echo "Add this line to your shell config:"
    echo
    echo "  export PATH=\"\$PATH:$INSTALL_BIN\""
    echo
fi

# ---- Cleanup ----
rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist" "$ROOT_DIR/projgen.spec"

echo
echo "====================================="
echo "Installation Completed Successfully"
echo "Run: projgen"
echo "====================================="
\
