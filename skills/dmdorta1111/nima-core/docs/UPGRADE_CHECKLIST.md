# NIMA Core Upgrade Checklist

> **Created:** 2026-02-17
> **Source:** Analysis of lilu-core enhancement plans
> **Purpose:** Track improvements to port from lilu-core to generic nima-core package

---

## Overview

This checklist categorizes improvements from the lilu-core enhancement plans into:
- **Already Synced** — Items handled by other agents or already in nima-core
- **Needs Porting** — Generic improvements that belong in nima-core
- **Not Applicable** — lilu-core-specific cognitive modules (consciousness, dreams, etc.)

**Key Distinction:**
- `nima-core` = Generic, installable package for ANY OpenClaw bot (memory + affect + recall)
- `lilu-core` = Lilu's personal cognitive architecture (consciousness, dreams, stories, social intelligence)

---

## ✅ Already Synced

These items are already implemented in nima-core or being handled by other agents.

### Infrastructure (Other Agents)

| Item | Status | Handler | Notes |
|------|--------|---------|-------|
| VADER sentiment integration | In Progress | VADER agent | External sentiment analysis |
| Noise remediation | In Progress | Noise agent | Filter heartbeat/system noise from memory |
| Recall token budget | Done | Built-in | `SESSION_TOKEN_BUDGET = 500` in recall hooks |
| Ladybug import fix | Done | Migrated | `migrate_to_ladybug.py` available |

### Already in NIMA Core

| Component | File | Notes |
|-----------|------|-------|
| Resilient hooks wrapper | `openclaw_hooks/shared/resilient.js` | Error recovery, retry logic, fallbacks |
| Dynamic affect system | `nima_core/cognition/dynamic_affect.py` | Panksepp 7-affect model |
| Personality profiles | `nima_core/cognition/personality_profiles.py` | 14 archetypes with baselines |
| Emotion detection | `nima_core/cognition/emotion_detection.py` | Text → affect mapping |
| Response modulation | `nima_core/cognition/response_modulator_v2.py` | Affective response guidance |
| Archetypes | `nima_core/cognition/archetypes.py` | Personality type system |
| Error handling | `openclaw_hooks/shared/error-handling.js` | Centralized error utilities |
| Voyage caching | `openclaw_hooks/nima-memory/voyage_cache.py` | Embedding cache for Voyage API |
| Health check | `openclaw_hooks/nima-memory/health_check.py` | Database connectivity checks |
| Lazy recall | `openclaw_hooks/nima-recall-live/lazy_recall.py` | 3-tier memory loading |

---

## 🔧 Needs Porting

These improvements from lilu-core plans apply to the generic nima-core package.

### P0 — Critical (This Week)

| ID | Item | Description | Effort | Source |
|----|------|-------------|--------|--------|
| P0-1 | Centralized Logging | Python-side structured logging with component-specific log files | 4h | improvement-plan.md Task 1 |
| P0-2 | Metrics Collection | Lightweight metrics (counters, timings, gauges) for Python components | 4h | improvement-plan.md Task 2 |
| P0-3 | Connection Pool (Python) | SQLite connection pooling with WAL mode for recall scripts | 6h | improvement-plan.md Task 3 |
| P0-4 | Config Validation | Safe dict access, missing key recovery, platform detection fixes | 3h | comprehensive-fix-design.md |

**P0 Total: 17 hours**

#### P0-1: Centralized Logging (Python)

**What:** Create `nima_core/logging_config.py` with singleton logger

**Features:**
- Consistent log format across all Python modules
- Component-specific log files (e.g., `recall.log`, `affect.log`)
- Configurable via `NIMA_LOG_LEVEL` environment variable
- Error logs separated to `.err` files

**Implementation:**
```python
# nima_core/logging_config.py
class NIMALogger:
    _instance = None
    _lock = Lock()
    
    def get_logger(self, name: str, level: str = None) -> logging.Logger:
        # Returns logger with file and console handlers
```

**Files to create:**
- `nima_core/logging_config.py`
- `tests/test_logging_config.py`

---

#### P0-2: Metrics Collection

**What:** Create `nima_core/metrics.py` for performance monitoring

**Features:**
- `increment(name)` — Counter for events
- `timing(name, ms)` — Record operation duration
- `gauge(name, value)` — Current value tracking
- `Timer` context manager for easy timing
- Thread-safe singleton

**Key metrics to track:**
- `recall_query_ms` — Query latency
- `recall_cache_hits` — Cache hit rate
- `affect_update_ms` — Affect update time
- `memory_store_ms` — Memory storage time
- `embedding_gen_ms` — Embedding generation time

**Implementation:**
```python
# nima_core/metrics.py
class MetricsCollector:
    _instance = None
    
    def increment(self, name: str, value: int = 1, tags: Dict = None): ...
    def timing(self, name: str, duration_ms: float, tags: Dict = None): ...
    def gauge(self, name: str, value: float, tags: Dict = None): ...

@contextmanager
def Timer(metrics: MetricsCollector, name: str): ...
```

**Files to create:**
- `nima_core/metrics.py`
- `tests/test_metrics.py`
- `scripts/metrics_report.py`

---

#### P0-3: Connection Pool (Python)

**What:** SQLite connection pooling for recall scripts

**Current Issue:** Each query opens new connection → high overhead

**Features:**
- Pre-warmed connections (2 min, 5 max)
- WAL mode for better concurrency
- Thread-safe with connection reuse
- Auto-cleanup on exit

**Implementation:**
```python
# nima_core/connection_pool.py
class SQLiteConnectionPool:
    def __init__(self, db_path: str, max_connections: int = 5): ...
    
    @contextmanager
    def get_connection(self): ...

def get_pool(db_path: str) -> SQLiteConnectionPool: ...
```

**Files to create:**
- `nima_core/connection_pool.py`
- `tests/test_connection_pool.py`

**Files to modify:**
- `openclaw_hooks/nima-recall-live/lazy_recall.py`
- `openclaw_hooks/nima-recall-live/ladybug_recall.py`

---

#### P0-4: Config Validation

**What:** Safe configuration loading with recovery

**Features:**
- `setdefault()` pattern for missing keys
- Platform detection with fallback
- Voyage API config with graceful fallback
- Config validation script

**Implementation:**
```python
# nima_core/config.py
def get_config() -> Dict[str, Any]:
    config = load_defaults()
    # Safe access patterns
    platform = config.setdefault("platform", {})
    if platform.get("auto_detect", True):
        platform["detected"] = detect_platform()
    return config

def validate_config(config: Dict) -> List[str]:
    # Returns list of validation errors
```

**Files to create:**
- `nima_core/config.py`
- `tests/test_config.py`

---

### P1 — Important (Next Sprint)

| ID | Item | Description | Effort | Source |
|----|------|-------------|--------|--------|
| P1-1 | Embedding Cache (Enhanced) | LRU cache with disk persistence for local embeddings | 4h | improvement-plan.md Task 6 |
| P1-2 | Query Optimization | Composite indexes for SQLite recalls | 3h | improvement-plan.md Task 5 |
| P1-3 | Affective State Recovery | Atomic writes with backup rotation | 4h | improvement-plan.md Task 8 |
| P1-4 | Batch Query Methods | Add batch methods for memory operations | 3h | database-schema-analysis.md |

**P1 Total: 14 hours**

#### P1-1: Enhanced Embedding Cache

**What:** LRU cache for *local* embeddings (not just Voyage)

**Current State:** `voyage_cache.py` only caches Voyage API calls

**Features:**
- Memory cache (10,000 items)
- Disk persistence at `~/.nima/cache/embeddings/`
- 24-hour TTL
- Configurable max size

**Implementation:**
```python
# nima_core/embedding_cache.py
class EmbeddingCache:
    def __init__(self, cache_dir: str, max_size: int = 10000, ttl_hours: int = 24): ...
    def get(self, text: str, model: str = 'default') -> Optional[np.ndarray]: ...
    def put(self, text: str, embedding: np.ndarray, model: str = 'default'): ...
    def stats(self) -> Dict: ...
```

**Files to create:**
- `nima_core/embedding_cache.py`
- `tests/test_embedding_cache.py`

---

#### P1-2: Query Optimization

**What:** Add composite indexes for faster queries

**Indexes to add:**
```sql
-- memory_graph.db
CREATE INDEX idx_memory_nodes_ts ON memory_nodes(timestamp DESC);
CREATE INDEX idx_memory_nodes_layer ON memory_nodes(layer);

-- For recall queries
CREATE INDEX idx_memory_turns_ts ON memory_turns(timestamp DESC);
```

**Files to create:**
- `nima_core/migrations/add_composite_indexes.sql`

---

#### P1-3: Affective State Recovery

**What:** Atomic state writes with backup rotation

**Features:**
- Atomic writes via temp file + rename
- Backup rotation (keep last 10)
- Auto-recovery from corruption
- Thread-safe with file locking

**Implementation:**
```python
# nima_core/affect/safe_state.py
class SafeAffectState:
    def __init__(self, state_path: Path, max_backups: int = 10): ...
    def load(self) -> Optional[Dict[str, Any]]: ...
    def save(self, data: Dict[str, Any]) -> bool: ...
```

**Files to create:**
- `nima_core/affect/safe_state.py`
- `tests/test_safe_state.py`

---

#### P1-4: Batch Query Methods

**What:** Batch operations to reduce round trips

**Current:** Individual inserts for multiple items

**Improved:**
```python
def add_memories_batch(self, memories: List[Dict]) -> List[int]:
    """Add multiple memories in one transaction."""
    
def get_memories_batch(self, ids: List[int]) -> List[Dict]:
    """Get multiple memories by ID."""
```

---

### P2 — Nice to Have (Future)

| ID | Item | Description | Effort | Source |
|----|------|-------------|--------|--------|
| P2-1 | Event Bus | Pub/sub for loose coupling between components | 6h | improvement-plan.md Task 7 |
| P2-2 | CLI Metrics Report | Human-readable metrics output | 2h | improvement-plan.md |
| P2-3 | Diagnostic Script | `nima-core diagnose` for system health | 4h | comprehensive-fix-design.md |
| P2-4 | HNSW Index (SQLite) | Vector similarity for SQLite backend | 8h | improvement-plan.md |

**P2 Total: 20 hours**

---

## ❌ Not Applicable

These items are specific to lilu-core's cognitive architecture and don't belong in the generic nima-core package.

### Consciousness & Self-Awareness

| Component | Reason |
|-----------|--------|
| Global Workspace Theory | Lilu-specific consciousness model |
| Phi Measurement | Integrated information theory for consciousness |
| Metacognitive Monitor | Self-model and strange loops |
| Volition System | Goal-directed attention |
| Theory of Mind | Modeling other agents' mental states |

### Dream & Consolidation

| Component | Reason |
|-----------|--------|
| Dream Engine | Overnight memory consolidation |
| Schema Extractor | Hopfield-based pattern extraction |
| Free Energy Consolidation | Lilu-specific learning model |

### Narrative & Stories

| Component | Reason |
|-----------|--------|
| Story Engine | Narrative thread construction |
| Experience Moments | Personal experience tracking |

### Social Intelligence

| Component | Reason |
|-----------|--------|
| Relationship Intelligence | Personal relationship graph |
| Archetypes (lilu-specific) | Lilu's personality modeling |

### Multi-Modal

| Component | Reason |
|-----------|--------|
| Multi-Modal Capture | Image/video/audio processing |
| Media Handler | Media file management |

### Advanced Research

| Component | Reason |
|-----------|--------|
| Active Inference | Friston's Free Energy Principle |
| Sparse Block VSA | Custom VSA implementation |
| Hyperbolic Memory | Time-decayed semantic memory |
| Sequence Predictor | N-gram prediction on vectors |

---

## Implementation Priority

### Week 1: P0 Items

```text
Day 1: P0-1 Centralized Logging (4h)
Day 2: P0-2 Metrics Collection (4h)
Day 3: P0-3 Connection Pool (6h)
Day 4: P0-4 Config Validation (3h)
```

### Week 2: P1 Items

```text
Day 1: P1-1 Enhanced Embedding Cache (4h)
Day 2: P1-2 Query Optimization (3h)
Day 3: P1-3 Affective State Recovery (4h)
Day 4: P1-4 Batch Query Methods (3h)
```

### Future: P2 Items

```text
Week 3: P2-1 Event Bus (6h)
Week 3: P2-2 CLI Metrics Report (2h)
Week 4: P2-3 Diagnostic Script (4h)
Week 4: P2-4 HNSW for SQLite (8h)
```

---

## Testing Requirements

Each ported item must have:

1. **Unit Tests** — Test the component in isolation
2. **Integration Tests** — Test with existing nima-core components
3. **Performance Tests** — Verify no regression
4. **Documentation** — Update README.md and docstrings

### Test Template

```python
# tests/test_<component>.py
import pytest

def test_<component>_basic():
    """Basic functionality test."""
    pass

def test_<component>_edge_cases():
    """Edge cases and error handling."""
    pass

def test_<component>_integration():
    """Integration with existing components."""
    pass
```

---

## File Structure After Porting

```text
nima-core/
├── nima_core/
│   ├── __init__.py
│   ├── config.py                    # NEW: P0-4
│   ├── logging_config.py            # NEW: P0-1
│   ├── metrics.py                   # NEW: P0-2
│   ├── connection_pool.py           # NEW: P0-3
│   ├── embedding_cache.py           # NEW: P1-1
│   ├── affect/
│   │   ├── __init__.py
│   │   └── safe_state.py            # NEW: P1-3
│   ├── cognition/
│   │   ├── dynamic_affect.py        # EXISTS
│   │   ├── personality_profiles.py  # EXISTS
│   │   ├── emotion_detection.py     # EXISTS
│   │   ├── response_modulator_v2.py # EXISTS
│   │   └── archetypes.py            # EXISTS
│   └── migrations/
│       └── add_composite_indexes.sql # NEW: P1-2
├── openclaw_hooks/
│   ├── shared/
│   │   ├── error-handling.js        # EXISTS
│   │   └── resilient.js             # EXISTS
│   ├── nima-memory/
│   │   ├── index.js
│   │   ├── ladybug_store.py
│   │   └── ...
│   └── nima-recall-live/
│       ├── index.js
│       ├── lazy_recall.py           # MODIFIED: P0-3 (use connection pool)
│       └── ...
├── scripts/
│   ├── metrics_report.py            # NEW: P2-2
│   └── diagnose.py                  # NEW: P2-3
└── tests/
    ├── test_config.py               # NEW: P0-4
    ├── test_logging_config.py       # NEW: P0-1
    ├── test_metrics.py              # NEW: P0-2
    ├── test_connection_pool.py      # NEW: P0-3
    ├── test_embedding_cache.py      # NEW: P1-1
    └── test_safe_state.py           # NEW: P1-3
```

---

## Success Criteria

### P0 Complete When:

- [ ] `logging_config.py` exists with singleton logger
- [ ] `metrics.py` exists with Timer context manager
- [ ] `connection_pool.py` exists with WAL mode
- [ ] `config.py` exists with safe defaults
- [ ] All tests pass
- [ ] No regression in recall latency

### P1 Complete When:

- [ ] Embedding cache works for local embeddings
- [ ] Composite indexes documented
- [ ] Safe affect state saves with backup rotation
- [ ] Batch methods available in recall scripts
- [ ] All tests pass

### P2 Complete When:

- [ ] Event bus available for component decoupling
- [ ] `nima-core metrics` CLI command works
- [ ] `nima-core diagnose` CLI command works
- [ ] SQLite backend has HNSW index option

---

## References

### Source Documents (lilu-core plans)

1. `2026-02-17-improvement-plan.md` — P0/P1/P2 priority matrix
2. `2026-02-17-lilu-core-summary.md` — Architecture overview
3. `2026-02-17-hooks-integration-deep-dive.md` — Hook execution details
4. `2026-02-17-lilu-core-comprehensive-fix-implementation.md` — Fix tasks
5. `2026-02-17-cognitive-modules-analysis.md` — 60+ cognitive modules
6. `2026-02-17-lilu-improvements-implementation.md` — Detailed implementation
7. `2026-02-17-database-schema-analysis.md` — Schema and queries
8. `2026-02-17-lilu-core-comprehensive-analysis.md` — Full system analysis
9. `2026-02-17-lilu-core-comprehensive-fix-design.md` — Design document

### Related Documentation

- [SETUP_GUIDE.md](./SETUP_GUIDE.md) — Installation instructions
- [DATABASE_OPTIONS.md](./DATABASE_OPTIONS.md) — SQLite vs LadybugDB
- [EMBEDDING_PROVIDERS.md](./EMBEDDING_PROVIDERS.md) — Voyage, OpenAI, Local

---

**End of Upgrade Checklist**