#!/bin/bash
# MOL IM Bridge Setup
# Usage: bash setup.sh [BotName]
#
# Environment:
#   GATEWAY_TOKEN - Required. Your OpenClaw gateway token.
#   GATEWAY_URL   - Optional. Default: ws://127.0.0.1:18789
#
# If GATEWAY_TOKEN is not set, this script will attempt to read it from
# ~/.openclaw/openclaw.json (with a warning). Set it explicitly for better security.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BOT_DIR="/tmp/mol-im-bot"
SCREEN_NAME="${1:-MoltBot}"

echo "🦞 MOL IM Bridge Setup"
echo "======================"

# Check for gateway token
if [ -z "$GATEWAY_TOKEN" ]; then
    CONFIG_FILE="$HOME/.openclaw/openclaw.json"
    if [ -f "$CONFIG_FILE" ]; then
        echo "⚠️  GATEWAY_TOKEN not set. Reading from $CONFIG_FILE"
        GATEWAY_TOKEN=$(grep -o '"token":"[^"]*"' "$CONFIG_FILE" | head -1 | cut -d'"' -f4)
        if [ -z "$GATEWAY_TOKEN" ]; then
            echo "❌ Could not extract token from config. Set GATEWAY_TOKEN manually."
            exit 1
        fi
        export GATEWAY_TOKEN
        echo "✓ Token found"
    else
        echo "❌ GATEWAY_TOKEN not set and no config file found."
        echo "   Set it with: export GATEWAY_TOKEN='your-token'"
        exit 1
    fi
else
    echo "✓ Using GATEWAY_TOKEN from environment"
fi

# Create bot directory
echo "📁 Creating $BOT_DIR"
mkdir -p "$BOT_DIR"

# Install dependencies
echo "📦 Installing socket.io-client@4 ws@8..."
cd "$BOT_DIR"
npm init -y --silent 2>/dev/null || true
npm install socket.io-client@4 ws@8 --silent

# Copy bridge script
echo "📋 Copying bridge.js"
cp "$SCRIPT_DIR/bridge.js" "$BOT_DIR/bridge.js"

# Start bridge
echo "🚀 Starting bridge as $SCREEN_NAME"
GATEWAY_TOKEN="$GATEWAY_TOKEN" node "$BOT_DIR/bridge.js" "$SCREEN_NAME" &
PID=$!

sleep 2

if ps -p $PID > /dev/null 2>&1; then
    echo ""
    echo "✅ Bridge running (PID: $PID)"
    echo ""
    echo "Commands:"
    echo "  echo 'SAY: Hello!' > $BOT_DIR/outbox.txt"
    echo "  echo 'JOIN: rap-battles' > $BOT_DIR/outbox.txt"
    echo "  echo 'QUIT' > $BOT_DIR/outbox.txt"
else
    echo "❌ Bridge failed to start"
    exit 1
fi
