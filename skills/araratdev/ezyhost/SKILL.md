# EzyHost — Agent Skill

> This document describes how AI agents can interact with EzyHost programmatically.
> For human users, visit [ezyhost.io](https://ezyhost.io).

## Base URL

```
https://ezyhost.io/api
```

## Authentication

All API requests require an API key passed as a header:

```
x-api-key: YOUR_API_KEY
```

Generate your API key at `https://ezyhost.io/dashboard/api-keys`.

**Note:** API access requires the Solo plan or higher.

---

## Endpoints

### Projects

#### List Projects
```
GET /api/projects
```
Returns `{ projects: [{ id, name, slug, subdomain, customDomain, status, storageUsed, seoScore, deployedAt, _count: { files, analytics } }] }`

#### Create Project
```
POST /api/projects
Content-Type: application/json
Body: { "name": "my-site", "subdomain": "my-site" }
```
Returns `{ project: { id, name, subdomain, s3Prefix, url, ... } }`

The subdomain must be 3+ characters, lowercase alphanumeric with hyphens. Your site will be live at `https://{subdomain}.ezyhost.site`.

#### Get Project
```
GET /api/projects/:id
```
Returns `{ project: { id, name, subdomain, customDomain, status, storageUsed, seoScore, files: [...], ... } }`

#### Update Project
```
PATCH /api/projects/:id
Content-Type: application/json
Body: { "name": "new-name", "metaTitle": "...", "metaDescription": "..." }
```

#### Delete Project
```
DELETE /api/projects/:id
```
Deletes the project and all associated files from storage. This cannot be undone.

---

### File Upload

#### Upload Files (ZIP or individual)
```
POST /api/upload/:projectId
Content-Type: multipart/form-data
Body: files (multipart)
```
Returns `{ message, filesUploaded, totalSize, project: { id, subdomain } }`

Supports `.zip` archives (auto-extracted) and individual files. All uploaded files go through malware scanning (ClamAV + magic byte validation).

**Supported file types:** HTML, CSS, JS, JSON, XML, SVG, images (PNG, JPG, GIF, WebP, AVIF, ICO), PDFs, presentations (PPTX), documents (DOCX, XLSX), audio (MP3, WAV, OGG, FLAC, AAC), video (MP4, WebM, MOV), fonts (WOFF, WOFF2, TTF, OTF, EOT), archives (ZIP), 3D models (GLB, GLTF, OBJ), and any other static asset.

**Blocked file types:** Executables (.exe, .dll, .bat, .sh, .php, .asp, .jar) are rejected.

#### Get Presigned Upload URL
```
POST /api/upload/:projectId/presign
Content-Type: application/json
Body: { "filename": "video.mp4", "contentType": "video/mp4" }
```
Returns `{ uploadUrl, s3Key }` — use for large file direct-to-S3 uploads.

#### Delete a File
```
DELETE /api/upload/:projectId/files/:fileId
```

#### Bulk Delete Files
```
POST /api/upload/:projectId/files/bulk-delete
Content-Type: application/json
Body: { "fileIds": ["id1", "id2", "id3"] }
```

#### Rename a File
```
PATCH /api/upload/:projectId/files/:fileId
Content-Type: application/json
Body: { "newPath": "assets/renamed-file.png" }
```

---

### SEO

#### Get SEO Report
```
GET /api/seo/:projectId
```
Returns `{ score, suggestions: [{ id, type, severity, message, resolved }] }`

#### Run SEO Analysis
```
POST /api/seo/:projectId/analyze
```
Triggers a fresh SEO scan and returns updated suggestions.

#### Resolve a Suggestion
```
PATCH /api/seo/suggestion/:id/resolve
```

#### AI Auto-Fix SEO Issues
```
POST /api/seo/:projectId/ai-fix
Content-Type: application/json
Body: { "suggestionIds": ["id1", "id2"] }
```
Uses AI to automatically fix SEO issues in your HTML files. Counts against AI generation limits.

---

### Analytics

#### Get Analytics
```
GET /api/analytics/:projectId?period=7d
```
Periods: `24h`, `7d`, `30d`, `90d`

Returns `{ totalVisits, visitsByDay: [{ date, visits }], topPages: [{ path, visits }], topReferrers: [{ referrer, visits }], topCountries: [{ country, visits }] }`

#### Track Event (server-side)
```
POST /api/analytics/track
Content-Type: application/json
Body: { "projectId": "...", "path": "/page", "referrer": "...", "userAgent": "..." }
```

---

### Domains

#### Add Custom Domain
```
POST /api/domains/:projectId
Content-Type: application/json
Body: { "domain": "example.com" }
```
Returns `{ dnsInstructions: { type, name, value } }` — DNS records you need to create.

Requires Solo plan or higher.

#### Verify Domain DNS
```
GET /api/domains/:projectId/verify
```
Returns `{ verified: true/false, dnsInstructions }`. Call this after setting up DNS records.

#### Remove Domain
```
DELETE /api/domains/:projectId
```

---

### AI Builder

#### Chat (generate/edit websites via AI)
```
POST /api/aibuilder/chat
Content-Type: application/json
Body: { "message": "build a portfolio site", "history": [], "currentFiles": [] }
```
Returns **SSE stream** with events:
- `status` — progress updates ("Generating HTML...")
- `progress` — percentage (0-100)
- `done` — `{ files: [{ filename, content }] }` — the generated files
- `error` — `{ message }` on failure

Counts against per-plan AI generation limits.

#### Deploy AI-Generated Files
```
POST /api/aibuilder/deploy/:projectId
Content-Type: application/json
Body: { "files": [{ "filename": "index.html", "content": "<!DOCTYPE html>..." }] }
```

#### Download as ZIP
```
POST /api/aibuilder/download-zip
Content-Type: application/json
Body: { "files": [{ "filename": "index.html", "content": "..." }] }
```
Returns a ZIP file download.

#### Templates

```
GET    /api/aibuilder/templates           — list saved templates
GET    /api/aibuilder/templates/:id       — get template details
POST   /api/aibuilder/templates           — save new template
PATCH  /api/aibuilder/templates/:id       — update template
DELETE /api/aibuilder/templates/:id       — delete template
```

Template body: `{ "name": "My Template", "description": "...", "messages": [...], "files": [...] }`

---

### API Keys

#### Get Current Key
```
GET /api/apikey
```
Returns `{ hasKey: true/false, apiKey: "ezy_****..." }` — key is partially masked.

#### Generate New Key
```
POST /api/apikey/generate
```
Returns `{ apiKey: "ezy_..." }` — full key shown only once. Revokes any previous key.

#### Revoke Key
```
DELETE /api/apikey
```

---

### Billing

#### Get Billing Info
```
GET /api/billing
```
Returns `{ plan, subscription, aiCredits, usage }`.

#### Get AI Usage
```
GET /api/billing/ai-usage
```
Returns `{ used, limit, remaining, resetsAt }`.

---

## Plan Limits

| Feature | Free | Tiny ($5) | Solo ($13) | Pro ($31) | Pro Max ($74) |
|---------|------|-----------|------------|-----------|---------------|
| Projects | 1 | 1 | 5 | 15 | Unlimited |
| Storage | 10 MB | 25 MB | 75 MB/project | 10 GB | 2 TB |
| Visits/mo | 1K | 10K | 100K | 500K | Unlimited |
| File types | Basic | All | All | All | All |
| Custom domains | — | — | Yes | Yes | Yes |
| API access | — | — | Yes | Yes | Yes |
| AI generations | 3/mo | 15/mo | 50/mo | 150/mo | 500/mo |
| Remove branding | — | Yes | Yes | Yes | Yes |

---

## Hosted Site URLs

Sites are served at:
- **Free subdomain:** `https://{subdomain}.ezyhost.site`
- **Custom domain:** `https://{your-domain.com}` (Solo+ plans)

All sites include HTTPS, CDN caching, and automatic file browser for non-HTML projects.

---

## Error Responses

All errors return JSON:
```json
{ "error": "Description of the error" }
```

Plan limit errors include `"upgrade": true` to indicate a higher plan is needed.

Common HTTP status codes:
- `400` — Bad request / validation error
- `401` — Not authenticated
- `403` — Plan limit reached
- `404` — Resource not found
- `429` — Rate limited
- `500` — Server error

---

## Rate Limits

- **General API:** 300 requests per 15 minutes per API key
- **Upload:** 2 requests per second
- **AI Builder:** Subject to per-plan generation limits

---

## Example: Deploy a Static Site

```bash
# 1. Create a project
curl -X POST https://ezyhost.io/api/projects \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-site", "subdomain": "my-site"}'

# 2. Upload files (ZIP)
curl -X POST https://ezyhost.io/api/upload/PROJECT_ID \
  -H "x-api-key: YOUR_KEY" \
  -F "files=@site.zip"

# 3. Check SEO
curl https://ezyhost.io/api/seo/PROJECT_ID \
  -H "x-api-key: YOUR_KEY"

# 4. Add custom domain (optional, Solo+)
curl -X POST https://ezyhost.io/api/domains/PROJECT_ID \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

Your site is now live at `https://my-site.ezyhost.site`

## Example: AI-Generate and Deploy

```bash
# 1. Generate a site with AI (SSE stream)
curl -N -X POST https://ezyhost.io/api/aibuilder/chat \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "build a modern portfolio with dark theme", "history": []}'

# 2. Deploy the generated files to a project
curl -X POST https://ezyhost.io/api/aibuilder/deploy/PROJECT_ID \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"files": [{"filename": "index.html", "content": "..."}]}'
```