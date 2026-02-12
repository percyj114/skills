#!/bin/bash
# Setup script for a2a-agent-signup CLI command
# Run this after installing the skill: bash setup.sh

SKILL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR="$HOME/bin"

# Create ~/bin if it doesn't exist
mkdir -p "$BIN_DIR"

# Create symlink
ln -sf "$SKILL_DIR/index.js" "$BIN_DIR/a2a-agent-signup"
chmod +x "$SKILL_DIR/index.js"

echo "✓ a2a-agent-signup linked to $BIN_DIR/a2a-agent-signup"
echo ""
echo "Make sure $BIN_DIR is in your PATH:"
echo "  export PATH=\"\$HOME/bin:\$PATH\""
echo ""
echo "Add to ~/.bashrc if not already there:"
echo "  echo 'export PATH=\"\$HOME/bin:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
echo ""
echo "Then test it:"
echo "  a2a-agent-signup"
