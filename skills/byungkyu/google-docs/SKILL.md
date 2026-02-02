---
name: google-docs
description: |
  Google Docs API integration with managed OAuth. Create documents, insert text, apply formatting, and manage content. Use this skill when users want to interact with Google Docs.
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
---

# Google Docs

Access the Google Docs API with managed OAuth authentication. Create documents, insert and format text, and manage document content.

## Quick Start

```bash
# Get document
curl -s -X GET 'https://gateway.maton.ai/google-docs/v1/documents/{documentId}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## Base URL

```
https://gateway.maton.ai/google-docs/v1/documents/{documentId}
```

The gateway proxies requests to `docs.googleapis.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Google OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections?app=google-docs&status=ACTIVE' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Create Connection

```bash
curl -s -X POST 'https://ctrl.maton.ai/connections' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{"app": "google-docs"}'
```

### Get Connection

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-docs"
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## API Reference

### Get Document

```bash
GET /google-docs/v1/documents/{documentId}
```

### Create Document

```bash
POST /google-docs/v1/documents
Content-Type: application/json

{
  "title": "New Document"
}
```

### Batch Update Document

```bash
POST /google-docs/v1/documents/{documentId}:batchUpdate
Content-Type: application/json

{
  "requests": [
    {
      "insertText": {
        "location": {"index": 1},
        "text": "Hello, World!"
      }
    }
  ]
}
```

## Common batchUpdate Requests

### Insert Text

```json
{
  "insertText": {
    "location": {"index": 1},
    "text": "Text to insert"
  }
}
```

### Delete Content

```json
{
  "deleteContentRange": {
    "range": {
      "startIndex": 1,
      "endIndex": 10
    }
  }
}
```

### Replace All Text

```json
{
  "replaceAllText": {
    "containsText": {
      "text": "{{placeholder}}",
      "matchCase": true
    },
    "replaceText": "replacement value"
  }
}
```

### Insert Table

```json
{
  "insertTable": {
    "location": {"index": 1},
    "rows": 3,
    "columns": 3
  }
}
```

### Update Text Style

```json
{
  "updateTextStyle": {
    "range": {
      "startIndex": 1,
      "endIndex": 10
    },
    "textStyle": {
      "bold": true,
      "fontSize": {"magnitude": 14, "unit": "PT"}
    },
    "fields": "bold,fontSize"
  }
}
```

### Insert Page Break

```json
{
  "insertPageBreak": {
    "location": {"index": 1}
  }
}
```

## Code Examples

### JavaScript

```javascript
// Create document
const response = await fetch(
  'https://gateway.maton.ai/google-docs/v1/documents',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({ title: 'New Document' })
  }
);

// Insert text
await fetch(
  `https://gateway.maton.ai/google-docs/v1/documents/${docId}:batchUpdate`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      requests: [{ insertText: { location: { index: 1 }, text: 'Hello!' } }]
    })
  }
);
```

### Python

```python
import os
import requests

# Create document
response = requests.post(
    'https://gateway.maton.ai/google-docs/v1/documents',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'title': 'New Document'}
)
```

## Notes

- Index positions are 1-based (document starts at index 1)
- Use `endOfSegmentLocation` to append at end
- Multiple requests in batchUpdate are applied atomically
- Get document first to find correct indices for updates
- The `fields` parameter in style updates uses field mask syntax

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Google Docs connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Google Docs API |

## Resources

- [Docs API Overview](https://developers.google.com/docs/api/how-tos/overview)
- [Get Document](https://developers.google.com/docs/api/reference/rest/v1/documents/get)
- [Create Document](https://developers.google.com/docs/api/reference/rest/v1/documents/create)
- [Batch Update](https://developers.google.com/docs/api/reference/rest/v1/documents/batchUpdate)
- [Request Types](https://developers.google.com/docs/api/reference/rest/v1/documents/request)
- [Document Structure](https://developers.google.com/docs/api/concepts/structure)
