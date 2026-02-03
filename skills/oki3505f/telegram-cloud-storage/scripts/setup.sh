#!/bin/bash
# setup.sh - Complete setup for Telegram Cloud Storage

echo "--- Telegram Cloud Storage Setup ---"

# 1. Database Setup
if [ -f "./scripts/setup_db.sh" ]; then
    bash ./scripts/setup_db.sh
else
    echo "Error: scripts/setup_db.sh not found."
    exit 1
fi

# 2. Dependency Check
echo "Checking dependencies..."
for cmd in psql cargo pnpm node openssl
do
    if ! command -v $cmd &> /dev/null
    then
        echo "Error: $cmd is not installed."
        exit 1
    fi
done

# 3. Build Pentaract
python3 ./scripts/cli.py setup

echo "------------------------------------"
echo "Setup complete!"
echo "Next steps:"
echo "1. Run: python3 ./scripts/cli.py init <bot_token> <chat_id> <email> <password>"
echo "2. Run: python3 ./scripts/cli.py start"
echo "3. Run: python3 ./scripts/cli.py login <email> <password>"
echo "------------------------------------"
