# Changelog

All notable changes to NIMA Core will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2026-02-19

### Added
- **Memory Pruner** (`nima_core/memory_pruner.py`) — Episodic distillation engine. Distills old conversation turns into semantic gists via LLM, suppresses raw noise in 30-day limbo. Configurable: `NIMA_DISTILL_MODEL`, `NIMA_DB_PATH`, `NIMA_DATA_DIR`, `NIMA_CAPTURE_CLI`. Pure stdlib (no `anthropic` package needed).
- **Logging** (`nima_core/logging_config.py`) — Singleton logger with file + console handlers. `NIMA_LOG_LEVEL` env var.
- **Metrics** (`nima_core/metrics.py`) — Thread-safe counters, timings, gauges. `Timer` context manager. Tagged metric support.
- **Connection Pool** (`nima_core/connection_pool.py`) — SQLite connection pool with WAL mode, max 5 connections, thread-safe.
- **Ollama embedding support** — `NIMA_EMBEDDER=ollama` with `NIMA_OLLAMA_MODEL` configuration.

### Fixed
- `__init__.py` — `__all__` NameError (used before definition)
- Memory pruner — Cypher injection prevention via layer whitelist
- Connection pool — Thread-safe `_waiters` counter, no double-decrement
- Logging — Correct log directory path (`NIMA_DATA_DIR/logs`, not parent)
- Metrics — Tagged metrics no longer overwrite each other in `get_summary()`

### Changed
- Version bump: 2.2.0 → 2.3.0
- Python requirement: 3.8+ (was 3.11+)
- All hardcoded paths replaced with env vars for portability

## [2.2.0] - 2026-02-19

### Added
- **VADER Affect Analyzer** — Contextual sentiment replacing lexicon-based detection
- **4-Phase Noise Remediation** — Empty validation → heartbeat filter → dedup → metrics
- **Resilient hook wrappers** — Auto-retry with exponential backoff and jitter
- **Ecology scoring** — Memory strength, decay, recency, surprise, dismissal in recall
- **Suppression registry** — File-based memory suppression with 30-day limbo

### Fixed
- Null contemplation layer crash
- Duplicate VADER/emotion lexicon keys
- Negation logic (proper 2-word window)
- Hardcoded venv paths → dynamic `os.homedir()`
- `--who` CLI filter (was a no-op)
- `maxRetries` clamped ≥ 1 in resilient wrapper
- Debug logging gated behind `NIMA_DEBUG_RECALL`
- Division by zero in cleanup script
- Ruff E701 lint issues

### Changed
- Recall token budget: 500 → 3000
- Shebang: hardcoded path → `#!/usr/bin/env python3`
- Turn IDs: full millisecond timestamps

## [2.1.0] - 2026-02-17

### Added
- Pre-release of VADER and noise remediation (shipped in v2.2.0)

## [2.0.3] - 2026-02-15

### Security
- Fixed path traversal vulnerability in affect_history.py (CRITICAL)
- Fixed temp file resource leaks in 3 files (HIGH)

### Fixed
- Corrected non-existent `json.JSONEncodeError` → `TypeError`/`ValueError`
- Improved exception handling — replaced 5 generic catches with specific types

### Improved
- Better error visibility and debugging throughout

## [2.0.1] - 2026-02-14

### Fixed
- Thread-safe singleton with double-checked locking

### Security
- Clarified metadata requirements (Node.js, env vars)
- Added security disclosure for API key usage

## [2.0.0] - 2026-02-13

### Added
- **LadybugDB backend** with HNSW vector search (18ms query time)
- **Native graph traversal** with Cypher queries
- **nima-query CLI** for unified database queries
- SQL/FTS5 injection prevention
- Path traversal protection
- Temp file cleanup
- API timeouts (Voyage 30s, LadybugDB 10s)
- 348 unit tests with full coverage

### Performance
- 3.4x faster text search (9ms vs 31ms)
- 44% smaller database (50MB vs 91MB)
- 6x smaller context tokens (~30 vs ~180)

### Fixed
- Thread-safe singleton initialization

## [1.2.1] - 2026-02-10

### Added
- 8 consciousness systems (Φ, Global Workspace, self-awareness)
- Sparse Block VSA memory
- ConsciousnessCore unified interface

## [1.2.0] - 2026-02-08

### Added
- 4 Layer-2 composite affect engines
- Async affective processing
- Voyage AI embedding support

## [1.1.9] - 2026-02-05

### Fixed
- nima-recall hook spawning new Python process every bootstrap
- Performance: ~50-250x faster hook recall

---

## Release Notes Format

Each release includes:
- **Added** — New features
- **Changed** — Changes to existing functionality
- **Deprecated** — Soon-to-be removed features
- **Removed** — Removed features
- **Fixed** — Bug fixes
- **Security** — Security improvements
