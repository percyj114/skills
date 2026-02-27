---
name: cortex
description: >-
  Local-first agent memory with Ebbinghaus decay, hybrid search, and MCP tools.
  Import files, extract facts, search with BM25 + semantic, track confidence over time.
  Zero dependencies, single Go binary, SQLite storage. Use when you need persistent
  memory beyond OpenClaw's built-in MEMORY.md — especially for multi-agent setups,
  large knowledge bases, or when compaction keeps losing your important context.
  Don't use for: conversation history (use memory_search), exact string matching
  (use ripgrep), or web lookups.
homepage: https://github.com/hurttlocker/cortex
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      files: ["scripts/*"]
---

# Cortex — Local-First Agent Memory

**The memory layer OpenClaw should have built in.**

Cortex is an open-source, import-first memory system for AI agents. Single Go binary, SQLite storage, zero cloud dependencies. It solves the #1 complaint about OpenClaw: agents forget everything after compaction.

**GitHub:** https://github.com/hurttlocker/cortex
**Install:** `brew install hurttlocker/cortex/cortex` or download from [Releases](https://github.com/hurttlocker/cortex/releases)

## Why Cortex?

OpenClaw's default memory is Markdown files. When context fills up, compaction summarizes and **destroys specifics**. Cortex fixes this:

| Problem | Cortex Solution |
|---|---|
| Compaction loses details | Persistent SQLite DB survives any session |
| No search — just dump files into context | Hybrid BM25 + semantic search (~16ms keyword, ~52ms semantic) |
| Everything has equal weight | Ebbinghaus decay — important facts stay, noise fades naturally |
| Can't import existing files | Import-first: Markdown, text, any file. 8 connectors (GitHub, Gmail, Calendar, Drive, Slack, Notion, Discord, Telegram) |
| Multi-agent memory leaks | Per-agent scoping built in |
| Expensive cloud memory services | $0/month. Forever. Local SQLite. |

## Quick Start

### 1. Install Cortex

```bash
# macOS/Linux (Homebrew)
brew install hurttlocker/cortex/cortex

# Or download binary directly
# https://github.com/hurttlocker/cortex/releases/latest
```

### 2. Import Your Memory

```bash
# Import OpenClaw's memory files
cortex import ~/clawd/memory/ --extract

# Import specific files
cortex import ~/clawd/MEMORY.md --extract
cortex import ~/clawd/USER.md --extract
```

### 3. Search

```bash
# Fast keyword search
cortex search "wedding venue" --limit 5

# Semantic search (requires ollama with nomic-embed-text)
cortex search "what decisions did I make about the project" --mode semantic

# Hybrid (recommended)
cortex search "trading strategy" --mode hybrid
```

### 4. Use as MCP Server (recommended for OpenClaw)

```bash
# Add to your MCP config — Cortex exposes 17 tools + 4 resources
cortex mcp              # stdio mode
cortex mcp --port 8080  # HTTP+SSE mode
```

## Key Features

### Ebbinghaus Forgetting Curve
Facts decay at different rates based on type. Identity facts (names, roles) last ~2 years. Temporal facts (events, dates) fade in ~1 week. State facts (status, mood) fade in ~2 weeks. This means search results naturally prioritize what matters — without manual curation.

### Hybrid Search
- **BM25** — instant keyword matching via SQLite FTS5 (~16ms)
- **Semantic** — meaning-based via local embeddings (~52ms)
- **Hybrid** — combines both with reciprocal rank fusion

### Fact Extraction
Every imported file gets facts extracted automatically:
- Rule-based extraction (zero cost, instant)
- Optional LLM enrichment (Grok, Gemini, or any provider — finds facts rules miss)
- Auto-classification into 9 types: identity, relationship, preference, decision, temporal, location, state, config, kv

### Connectors (Beta)
Pull memory from external sources:
```bash
cortex connect sync --provider github --extract
cortex connect sync --provider gmail --extract
cortex connect sync --all --extract
```

### Knowledge Graph
Explore your memory visually:
```bash
cortex graph --serve --port 8090
# Opens interactive 2D graph explorer in browser
```

### Self-Cleaning
```bash
cortex cleanup --purge-noise  # Remove garbage + duplicates
cortex stale 30               # Find facts not accessed in 30 days
cortex conflicts               # Detect contradictions
cortex conflicts --resolve llm # Auto-resolve with LLM
```

## Integration with OpenClaw

### Recommended Search Chain
```
memory_search → Cortex → QMD → ripgrep → web search
```

Use OpenClaw's built-in `memory_search` for conversation history, then Cortex for deep knowledge retrieval.

### Wrapper Script
The included `scripts/cortex.sh` provides shortcuts:

```bash
scripts/cortex.sh search "query" 5       # Hybrid search
scripts/cortex.sh stats                    # Memory health
scripts/cortex.sh stale 30                # Stale fact detection
scripts/cortex.sh conflicts               # Contradiction detection
scripts/cortex.sh sync                    # Incremental import
scripts/cortex.sh reimport                # Full wipe + re-import
scripts/cortex.sh compaction              # Pre-compaction state brief
```

### Automated Sync (launchd/systemd)
```bash
# Auto-import sessions + sync connectors every 30 min
cortex connect schedule --every 30m --install
```

## Architecture

- **Language:** Go (62,300+ lines, 1,081 tests)
- **Storage:** SQLite + FTS5 + WAL mode
- **Binary:** 19MB, pure Go, zero CGO, zero runtime dependencies
- **Platforms:** macOS (arm64/amd64), Linux (arm64/amd64), Windows (amd64)
- **MCP:** 17 tools + 4 resources (stdio or HTTP+SSE)
- **Embeddings:** Local via Ollama (nomic-embed-text), or OpenAI/DeepSeek/custom
- **LLM:** Optional enrichment via any provider (Grok, Gemini, DeepSeek, OpenRouter)
- **Scale:** Tested to 100K+ memories. At ~20-50/day, won't hit ceiling for 5+ years.
- **License:** MIT

## vs Other Memory Tools

| | Cortex | Mem0 | Zep | LangMem |
|---|---|---|---|---|
| **Deploy** | Single binary | Cloud or K8s | Cloud | Python lib |
| **Cost** | $0 | $19-249/mo | $25/mo+ | Infra costs |
| **Privacy** | 100% local | Cloud by default | Cloud | Depends |
| **Decay** | Ebbinghaus (7 rates) | TTL only | Temporal | None |
| **Import** | Files + 8 connectors | Chat extraction | Chat/docs | Chat extraction |
| **Search** | BM25 + semantic | Vector + graph | Temporal KG | JSON docs |
| **MCP** | 17 tools native | No | No | No |
| **Dependencies** | Zero | Python + cloud | Cloud + credits | Python + LangGraph |

## Requirements

- **Cortex binary** — install via Homebrew or download from GitHub Releases
- **Optional:** Ollama with `nomic-embed-text` for semantic search
- **Optional:** LLM API key for enrichment (Grok, Gemini, etc.)
- No Python. No Node. No Docker. No cloud account. Just the binary.
