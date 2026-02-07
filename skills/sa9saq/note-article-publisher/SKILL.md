---
name: note-article-publisher
description: Publish articles to note.com from markdown. Convert markdown drafts to note.com format, manage drafts, and publish. Use when user says "publish to note", "note.com article", "create note draft", or "note記事".
---

# Note Article Publisher

Create and publish articles to note.com from markdown files. Automate your content pipeline from draft to publication.

## Features

- **Markdown to note.com**: Convert markdown files to note.com compatible format
- **Draft management**: Create, edit, and preview drafts before publishing
- **Image upload**: Attach cover images and inline images
- **Tag management**: Auto-suggest and apply tags
- **Headless browser automation**: Publish via Playwright automation
- **Template support**: Reusable article templates

## Quick Start

```bash
cd {skill_dir}
npm install
npx playwright install chromium

# Create draft from markdown
node dist/cli.js draft --input ./article.md --title "記事タイトル"

# Preview draft
node dist/cli.js preview --draft-id <id>

# Publish draft
node dist/cli.js publish --draft-id <id> --tags "AI,テクノロジー"

# Full pipeline: markdown → note.com
node dist/cli.js pipeline \
  --input ./article.md \
  --title "AIエージェントの作り方" \
  --tags "AI,プログラミング,自動化" \
  --cover-image ./cover.png
```

## Article Pipeline

```
Markdown file → Parse & Format → Upload images → Create draft → Review → Publish
```

## Markdown Format

Standard markdown with frontmatter:

```markdown
---
title: 記事タイトル
tags: [AI, テクノロジー]
cover: ./cover.png
---

# 見出し

本文テキスト...

## セクション

- リスト項目
- リスト項目

![画像の説明](./image.png)
```

## Configuration

Environment variables:
- `NOTE_EMAIL` — note.com login email (required)
- `NOTE_PASSWORD` — note.com login password (required)
- `NOTE_SESSION` — Session cookie (alternative to email/password)

## Requirements

- Node.js 18+
- Playwright (chromium)
- note.com account
