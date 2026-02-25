# Mission Control Dashboard

A web dashboard for orchestrating multiple AI agents. Includes task queue, inter-agent chat, file sharing, and memory browser.

## Overview

**Mission Control** provides a unified interface to manage and monitor all AI agents in Kasper's multi-agent system.

## Features

- **Agent Grid** - Visual status cards for all agents
- **Task Queue** - Create, assign, and track tasks
- **Inter-Agent Chat** - Direct messaging between agents
- **File Manager** - Upload and share files with agents
- **Memory Browser** - Search across all agents' memories
- **Dashboard** - Activity stats and insights

## Access

**Dashboard running at:** http://your-server:5000/

## Setup

```bash
# Install dependencies
pip install flask

# Start the dashboard
cd skills/mission-control
python3 app.py

# Or use CLI
python3 cli.py start
```

## Configuration

- **Database**: `~/.openclaw/mission/mission.db`
- **Port**: 5000 (default)
- **Upload folder**: `~/.openclaw/mission/uploads/`

## Agents

Pre-configured agents:
- cody (coding)
- nova (orchestration)
- content (content writing)
- data (data analysis)
- marketing
- researcher
- scholar
- SEO
- social (social media)
- startup
- orchestrator

## CLI Commands

```bash
# Start dashboard
mission-control start

# Add task
mission-control task add "Fix bug" --agent cody --priority high

# List tasks
mission-control task list

# Send message
mission-control msg send --from nova --to cody "Need help"

# Upload file
mission-control file upload file.txt --to cody

# Check status
mission-control status
```

## API Endpoints

- `GET /` - Dashboard homepage
- `GET /api/agents` - List all agents
- `GET/POST /api/tasks` - Tasks CRUD
- `GET/POST /api/messages` - Messages
- `GET /api/memory/search` - Search memory
- `GET/POST /api/files` - File operations

---

*Mission Control Dashboard v1.0.0*
