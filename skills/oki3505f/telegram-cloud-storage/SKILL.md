---
name: telegram-cloud-storage
description: Setup and manage an unlimited cloud storage pool using Telegram as the backend. Provides high-level commands to upload, download, list, and delete files. Use when you need a persistent, large-scale storage solution for system state, datasets, or long-term memory that bypasses local disk limits.
---

# Telegram Cloud Storage

This skill enables an agent to use Telegram as a distributed, unlimited cloud storage backend. It uses a local instance of the Pentaract engine to handle chunking, encryption, and multi-bot scheduling.

## Core Capabilities

1. **Unlimited Storage**: Leverages Telegram's cloud for file storage.
2. **Auto-Chunking**: Large files are split into 20MB chunks to bypass Telegram limits.
3. **Private Backend**: All metadata is stored in a local Postgres database.
4. **Agent-Friendly CLI**: Python-based CLI for easy integration into agent workflows.

## Initial Setup

Before using the storage, you must perform a one-time setup:

1. **Install Dependencies**: Ensure `postgresql@15`, `rust`, and `pnpm` are available.
2. **Build Engine**: Run `python scripts/cli.py setup` to clone and build the backend.
3. **Initialize**: Run `python scripts/cli.py init <bot_token> <chat_id> <admin_email> <admin_password>`.
4. **Start Server**: Run `python scripts/cli.py start`.

## Common Workflows

### 1. Authenticate
```bash
python scripts/cli.py login <email> <password>
```

### 2. List Storages
Identify the storage ID where you want to save data.
```bash
python scripts/cli.py list
```

### 3. Save a File
```bash
python scripts/cli.py upload <storage_id> <local_file_path> <remote_path>
```

### 4. Retrieve a File
```bash
python scripts/cli.py download <storage_id> <remote_path> <local_save_path>
```

## Maintenance

- **Stopping the server**: `python scripts/cli.py stop`
- **Checking logs**: View `app/server.log` for backend activity.

## Important Notes

- **Database**: The skill requires a running Postgres instance.
- **Privacy**: No data is sent to external servers other than Telegram's API.
- **Limits**: While storage is unlimited, respect Telegram's rate limits. The scheduler automatically handles basic throttling.
