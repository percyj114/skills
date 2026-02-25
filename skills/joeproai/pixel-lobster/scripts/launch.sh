#!/bin/bash
# Pixel Lobster launch helper
# Usage: bash launch.sh <path-to-pixel-lobster-repo> [--system|--tts]
#
# Clone the app first if you haven't already:
#   git clone https://github.com/JoeProAI/pixel-lobster.git

APP_DIR="${1:-./pixel-lobster}"
MODE_FLAG="${2:-}"

if [ ! -d "$APP_DIR" ]; then
  echo "App not found at: $APP_DIR"
  echo "Clone it first: git clone https://github.com/JoeProAI/pixel-lobster.git"
  exit 1
fi

cd "$APP_DIR" || exit 1

if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

case "$MODE_FLAG" in
  --system)
    echo "Starting in system audio mode..."
    npx electron . --audio-mode=system
    ;;
  --tts)
    echo "Starting in TTS mode..."
    npx electron . --audio-mode=tts
    ;;
  *)
    echo "Starting pixel lobster..."
    npx electron .
    ;;
esac
