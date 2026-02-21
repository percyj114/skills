<p align="center">
  <img src="assets/banner.png" alt="NIMA Core" width="700" />
</p>

<h1 align="center">NIMA Core</h1>

<p align="center">
  <strong>Neural Integrated Memory Architecture</strong><br/>
  Persistent memory, emotional intelligence, and semantic recall for AI agents.
</p>

<p align="center">
  <a href="https://nima-core.ai"><b>🌐 nima-core.ai</b></a> · 
  <a href="https://github.com/lilubot/nima-core">GitHub</a> · 
  <a href="https://clawhub.com/skills/nima-core">ClawHub</a> · 
  <a href="./CHANGELOG.md">Changelog</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.3.0-blue" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.8%2B-green" alt="Python" />
  <img src="https://img.shields.io/badge/node-18%2B-green" alt="Node" />
  <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="License" />
</p>

---

> *"Your AI wakes up fresh every session. NIMA gives it a past."*

NIMA Core is the memory system that makes AI agents **remember**. It captures conversations, encodes them as searchable memories with emotional context, and injects relevant history before every response — so your bot sounds like it's been paying attention all along.

**Works with any OpenClaw bot. One install script. Zero config to start.**

---

## ⚡ 30-Second Install

```bash
pip install nima-core && nima-core
```

That's it. The setup wizard handles everything:
- Creates `~/.nima/` directory
- Installs OpenClaw hooks
- Configures your embedding provider
- Restarts the gateway

**Or clone and install manually:**

```bash
git clone https://github.com/lilubot/nima-core.git
cd nima-core
./install.sh
openclaw gateway restart
```

Your bot now has persistent memory. Every conversation is captured, indexed, and recalled automatically.

---

## 🆕 What's New in v2.3.0

### Memory Pruner — Forgetting as a Feature
Old conversations pile up. The new **memory pruner** automatically distills aging transcripts into compact semantic summaries, then suppresses the raw noise. Your bot's memory gets *smarter*, not just *bigger*.

```bash
# Run manually
python -m nima_core.memory_pruner --min-age 14 --live

# Or let the nightly cron handle it
```

- LLM distillation via Anthropic API (stdlib only — no `anthropic` package needed)
- Extractive fallback when no API key
- 30-day suppression limbo (restorable if needed)
- Configurable: `NIMA_DISTILL_MODEL`, `NIMA_DB_PATH`, `NIMA_DATA_DIR`

### Infrastructure Modules
Production-ready internals:
- **`logging_config.py`** — Singleton logger, file + console, `NIMA_LOG_LEVEL` env var
- **`metrics.py`** — Thread-safe counters, timings, gauges with `Timer` context manager
- **`connection_pool.py`** — SQLite connection pool, WAL mode, max 5 connections

### v2.2.0 Highlights
- **VADER Affect Analyzer** — Contextual sentiment with caps boost, negation, idiom recognition
- **4-Phase Noise Remediation** — Empty validation → heartbeat filter → dedup → metrics
- **3000-token recall budget** (was 500) — 6x more context per response
- **Resilient hook wrappers** — Auto-retry with exponential backoff, no more crash loops

---

## 🧠 How It Works

```
  User message arrives
         │
         ▼
  ┌──────────────┐     ┌─────────────────────────┐
  │ nima-memory  │────▶│ Capture → Filter → Store │
  │  (on save)   │     │ 4-phase noise remediation│
  └──────────────┘     └─────────────────────────┘
         │
         ▼
  ┌──────────────┐     ┌─────────────────────────┐
  │ nima-recall  │────▶│ Search → Score → Inject  │
  │ (before LLM) │     │ Text + Vector + Ecology  │
  └──────────────┘     └─────────────────────────┘
         │
         ▼
  ┌──────────────┐     ┌─────────────────────────┐
  │ nima-affect  │────▶│ VADER → Panksepp 7-Affect│
  │ (on message) │     │ Emotional state tracking │
  └──────────────┘     └─────────────────────────┘
         │
         ▼
  Agent responds with memory + emotional awareness
```

**Three hooks, fully automatic:**

| Hook | Fires | Does |
|------|-------|------|
| `nima-memory` | After each message | Captures text → filters noise → stores in graph DB |
| `nima-recall-live` | Before agent responds | Searches relevant memories → injects as context |
| `nima-affect` | On each message | Detects emotion → updates 7-dimensional affect state |

---

## 🔧 Configuration

### Embedding Providers

NIMA needs an embedding model to create searchable memory vectors. **Pick one:**

<table>
<tr><th>Provider</th><th>Setup</th><th>Dims</th><th>Cost</th><th>Quality</th><th>Best For</th></tr>
<tr>
<td><b>🏠 Local (default)</b></td>
<td>

```bash
export NIMA_EMBEDDER=local
pip install sentence-transformers
```

</td>
<td>384</td><td>Free</td><td>Good</td><td>Privacy-first, offline, dev</td>
</tr>
<tr>
<td><b>🚀 Voyage AI</b></td>
<td>

```bash
export NIMA_EMBEDDER=voyage
export VOYAGE_API_KEY=pa-xxx
```

</td>
<td>1024</td><td>$0.12/1M tokens</td><td>Excellent</td><td>Production, best quality/cost</td>
</tr>
<tr>
<td><b>🤖 OpenAI</b></td>
<td>

```bash
export NIMA_EMBEDDER=openai
export OPENAI_API_KEY=sk-xxx
```

</td>
<td>1536</td><td>$0.13/1M tokens</td><td>Excellent</td><td>If you already use OpenAI</td>
</tr>
<tr>
<td><b>🦙 Ollama</b></td>
<td>

```bash
export NIMA_EMBEDDER=ollama
export NIMA_OLLAMA_MODEL=nomic-embed-text
# Ollama must be running locally
```

</td>
<td>768</td><td>Free</td><td>Good</td><td>Local GPU, custom models</td>
</tr>
<tr>
<td><b>💡 Custom Local Model</b></td>
<td>

```bash
export NIMA_EMBEDDER=local
export NIMA_LOCAL_MODEL=all-mpnet-base-v2  # or any sentence-transformers model
pip install sentence-transformers
```

</td>
<td>384-768</td><td>Free</td><td>Good</td><td>Custom embedding model</td>
</tr>
</table>

> **Don't have a preference?** Leave `NIMA_EMBEDDER` unset — it defaults to `local` with `all-MiniLM-L6-v2`. Free, works offline, no API keys. Upgrade to Voyage later when you want better recall quality.

### Database Backend

<table>
<tr><th></th><th>SQLite (default)</th><th>LadybugDB (recommended)</th></tr>
<tr><td><b>Setup</b></td><td>Zero config</td><td><code>pip install real-ladybug</code></td></tr>
<tr><td><b>Text Search</b></td><td>31ms</td><td>9ms (3.4x faster)</td></tr>
<tr><td><b>Vector Search</b></td><td>External only</td><td>Native HNSW (18ms)</td></tr>
<tr><td><b>Graph Queries</b></td><td>SQL JOINs</td><td>Native Cypher</td></tr>
<tr><td><b>DB Size</b></td><td>~91 MB</td><td>~50 MB (44% smaller)</td></tr>
<tr><td><b>Best For</b></td><td>Getting started</td><td>Production</td></tr>
</table>

```bash
# Start with SQLite (automatic, nothing to do)

# Upgrade to LadybugDB when ready:
pip install real-ladybug
python scripts/ladybug_parallel.py --migrate
```

### Full Environment Variables

```bash
# Required: none! Defaults work out of the box.

# Embedding provider (default: local)
NIMA_EMBEDDER=local|voyage|openai|ollama

# Provider-specific keys
VOYAGE_API_KEY=pa-xxx                    # For voyage
OPENAI_API_KEY=sk-xxx                    # For openai
NIMA_OLLAMA_MODEL=nomic-embed-text       # For ollama
NIMA_LOCAL_MODEL=all-MiniLM-L6-v2       # For local/sentence-transformers

# Data paths (defaults shown)
NIMA_DATA_DIR=~/.nima/memory             # Where memories live
NIMA_DB_PATH=~/.nima/memory/ladybug.lbug # LadybugDB path

# Memory pruner
NIMA_DISTILL_MODEL=claude-haiku-4-5      # LLM model for distillation (any Anthropic model)
ANTHROPIC_API_KEY=sk-ant-xxx             # For LLM distillation (optional)
NIMA_CAPTURE_CLI=/path/to/capture        # Custom capture CLI

# Logging
NIMA_LOG_LEVEL=INFO                      # DEBUG, INFO, WARNING, ERROR

# Debug
NIMA_DEBUG_RECALL=1                      # Verbose recall logging
```

---

## 🔌 Hook Setup for Bots

### Automatic (recommended)

```bash
./install.sh
openclaw gateway restart
```

### Manual

**1. Copy hooks to extensions:**
```bash
cp -r openclaw_hooks/nima-memory ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-recall-live ~/.openclaw/extensions/
cp -r openclaw_hooks/nima-affect ~/.openclaw/extensions/
```

**2. Add to `openclaw.json`:**
```json
{
  "plugins": {
    "allow": ["nima-memory", "nima-recall-live", "nima-affect"],
    "entries": {
      "nima-memory": {
        "enabled": true,
        "skip_subagents": true,
        "skip_heartbeats": true,
        "noise_filtering": {
          "filter_heartbeat_mechanics": true,
          "filter_system_noise": true
        }
      },
      "nima-recall-live": {
        "enabled": true,
        "max_results": 7,
        "token_budget": 3000,
        "use_ladybug": true,
        "compressed_format": true
      },
      "nima-affect": {
        "enabled": true,
        "identity_name": "my_bot",
        "baseline": "guardian"
      }
    }
  }
}
```

**3. Restart:**
```bash
openclaw gateway restart
```

### Verify It's Working

```bash
# Check hooks are loaded
openclaw status

# Send a test message and check memory was captured
ls ~/.nima/memory/

# Check affect state
cat ~/.nima/affect/affect_state.json
```

---

## 🎭 Affect System

NIMA tracks emotional state across conversations using **Panksepp's 7 primary affects** — the neurobiological basis of mammalian emotions:

| Affect | What It Feels Like | Triggers |
|--------|-------------------|----------|
| **SEEKING** | Curiosity, excitement, anticipation | Questions, exploration, new topics |
| **RAGE** | Frustration, assertion, boundaries | Conflict, demands, criticism |
| **FEAR** | Caution, vigilance, protection | Threats, uncertainty, risk |
| **LUST** | Desire, attraction, motivation | Goals, wants, enthusiasm |
| **CARE** | Nurturing, empathy, connection | Sharing, vulnerability, support |
| **PANIC** | Separation distress, sensitivity | Loss, rejection, loneliness |
| **PLAY** | Joy, humor, social bonding | Jokes, creativity, fun |

### Archetype Presets

Your bot's emotional personality:

```python
from nima_core import DynamicAffectSystem

# Pick a personality
affect = DynamicAffectSystem(identity_name="my_bot", baseline="guardian")
```

| Archetype | Vibe | High | Low |
|-----------|------|------|-----|
| **Guardian** | Protective, warm | CARE, SEEKING | PLAY |
| **Explorer** | Curious, bold | SEEKING, PLAY | FEAR |
| **Trickster** | Witty, irreverent | PLAY, SEEKING | CARE |
| **Empath** | Deeply feeling | CARE, PANIC | RAGE |
| **Sage** | Balanced, wise | SEEKING | All balanced |

See [docs/AFFECTIVE_CORE_PROFILES_GUIDE.md](./docs/AFFECTIVE_CORE_PROFILES_GUIDE.md) for the full guide.

---

## 🧹 Memory Pruner

Over time, raw conversation transcripts pile up. The pruner distills them into compact summaries:

```
Before: 829 raw turns taking up space
After:  5 semantic summaries + 829 turns suppressed (30-day limbo)
```

### Usage

```bash
# Dry run (preview what would be pruned)
python -m nima_core.memory_pruner --min-age 14

# Live run
python -m nima_core.memory_pruner --min-age 14 --live

# Process up to 10 sessions
python -m nima_core.memory_pruner --min-age 7 --max-sessions 10 --live

# Check suppression status
python -m nima_core.memory_pruner --status

# Restore a memory from suppression
python -m nima_core.memory_pruner --restore 12345
```

### How It Works

1. Finds conversation turns older than `--min-age` days
2. Groups them into sessions (4-hour gap heuristic)
3. Sends each session to Claude Haiku for semantic distillation
4. Stores the compact gist as a new "contemplation" memory
5. Suppresses original turn IDs in a registry (30-day limbo, restorable)
6. Recall automatically surfaces distillates instead of raw turns

**No database writes.** Suppression is file-based — zero risk of LadybugDB issues.

### Automate It

```bash
# Cron job example (nightly at 2 AM)
0 2 * * * cd $HOME/.openclaw/workspace/nima-core && python -m nima_core.memory_pruner --min-age 7 --live --max-sessions 10  # adjust path to your nima-core install
```

Or use OpenClaw cron:
```json
{
  "name": "nima-memory-pruner",
  "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "America/New_York" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run: python -m nima_core.memory_pruner --min-age 7 --live --max-sessions 10"
  },
  "sessionTarget": "isolated"
}
```

---

## 📊 Performance

| Operation | SQLite | LadybugDB |
|-----------|--------|-----------|
| Text search | 31ms | 9ms |
| Vector search | — | 18ms |
| Full recall cycle | ~50ms | ~30ms |
| Recall context overhead | ~180 tokens | ~30 tokens |
| Database size (10K memories) | ~91 MB | ~50 MB |

---

## 🔒 Privacy

**What NIMA accesses:**
- ✅ Conversation transcripts → stored locally in `~/.nima/`
- ✅ Embedding API (only when using Voyage/OpenAI) → sends text for vectorization
- 🔒 **Local embedding mode** → zero external network calls

**What NIMA never does:**
- ❌ Send data to NIMA servers (there are none)
- ❌ Track usage or analytics
- ❌ Phone home

**Your data stays on your machine.** The only external calls are to your chosen embedding provider, and you can avoid even that by using local embeddings.

**Fine-grained controls:**
```json
{
  "nima-memory": {
    "skip_subagents": true,
    "skip_heartbeats": true,
    "noise_filtering": { "filter_system_noise": true }
  }
}
```

---

## 🔄 Upgrading

### From v2.2.x → v2.3.x

```bash
git pull origin main
pip install -e .  # or: pip install nima-core --upgrade

# New modules are automatic — no config changes needed
openclaw gateway restart
```

### From v1.x → v2.x

```bash
# Backup first
cp -r ~/.nima ~/.nima.backup

# Update hooks
rm -rf ~/.openclaw/extensions/nima-*
cp -r openclaw_hooks/* ~/.openclaw/extensions/

# Optional: Migrate to LadybugDB
pip install real-ladybug
python scripts/ladybug_parallel.py --migrate

openclaw gateway restart
```

See [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) for the full guide.

---

## 📚 Documentation

| Guide | What's in it |
|-------|-------------|
| [SETUP_GUIDE.md](./SETUP_GUIDE.md) | Detailed step-by-step installation |
| [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) | Common commands cheat sheet |
| [docs/DATABASE_OPTIONS.md](./docs/DATABASE_OPTIONS.md) | SQLite vs LadybugDB deep dive |
| [docs/EMBEDDING_PROVIDERS.md](./docs/EMBEDDING_PROVIDERS.md) | All embedding options explained |
| [docs/AFFECTIVE_CORE_PROFILES_GUIDE.md](./docs/AFFECTIVE_CORE_PROFILES_GUIDE.md) | Personality archetypes guide |
| [docs/DYNAMIC_AFFECT.md](./docs/DYNAMIC_AFFECT.md) | Full affect system documentation |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

---

## 🤝 Contributing

PRs welcome. The repo uses:
- **CodeRabbit** and **Gemini Code Assist** for automated review
- Python 3.8+ compatibility (no walrus operators)
- Conventional commits

```bash
# Dev setup
git clone https://github.com/lilubot/nima-core.git
cd nima-core
pip install -e ".[vector]"
python -m pytest tests/
```

---

## License

MIT License — free to use for any AI agent, commercial or personal.

---

<p align="center">
  <a href="https://nima-core.ai"><b>🌐 nima-core.ai</b></a><br/>
  Built by the NIMA Core Team
</p>
