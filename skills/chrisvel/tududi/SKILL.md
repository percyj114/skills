---
name: tududi
description: Manage tasks, projects, and notes in tududi (self-hosted task manager). Use for todo lists, task management, project organization.
---

# tududi Task Management

## Configuration

Uses environment variables (set in `openclaw.json` under `skills.entries.tududi.env`):
- `TUDUDI_URL` - Base URL (e.g., `http://localhost:3004`)
- `TUDUDI_API_TOKEN` - API token from tududi Settings → API Tokens

## Authentication

All API calls require the header:
```
Authorization: Bearer $TUDUDI_API_TOKEN
```

## Common Operations

### List tasks
```bash
curl -s $TUDUDI_URL/api/v1/tasks \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"
```

### Create a task
```bash
curl -s -X POST $TUDUDI_URL/api/v1/tasks \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Task title", "due_date": "2026-02-10", "priority": 2}'
```

Priority: 1 (low) to 4 (urgent)

### Update a task
```bash
curl -s -X PUT $TUDUDI_URL/api/v1/tasks/{id} \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": 1}'
```

Status: 0=not_started, 1=in_progress, 2=completed, 6=archived

### List projects
```bash
curl -s $TUDUDI_URL/api/v1/projects \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN"
```

### Create project
```bash
curl -s -X POST $TUDUDI_URL/api/v1/projects \
  -H "Authorization: Bearer $TUDUDI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Project name"}'
```

## Task Statuses
- `not_started`
- `in_progress`
- `completed`
- `archived`

## Filters
- `$TUDUDI_URL/api/v1/tasks?filter=today` - Due today
- `$TUDUDI_URL/api/v1/tasks?filter=upcoming` - Future tasks
- `$TUDUDI_URL/api/v1/tasks?filter=someday` - No due date
- `$TUDUDI_URL/api/v1/tasks?project_id={id}` - By project

## API Docs
Swagger UI available at `$TUDUDI_URL/swagger` (requires login)
