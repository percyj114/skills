# HyperStack — Typed Graph Memory for AI Agents

**Your agents forget everything between sessions. HyperStack fixes that.**

Persistent memory built on a typed knowledge graph. Store decisions, blockers, dependencies, and findings as cards with explicit typed relations. Query with exact answers — not fuzzy similarity. Branch memory like Git. Track provenance on every card.

## Why this instead of vector memory?

- **"What blocks deploy?"** → exact typed blockers, not 17 similar tasks
- **"What breaks if auth changes?"** → full reverse impact chain, instantly
- **Git-style branching** — fork memory, experiment, diff, merge or discard
- **Agent identity + trust** — SHA256 fingerprints, trust scores per agent
- **$0 per operation** — Mem0/Zep charge ~$0.002/op (LLM extraction). This: $0
- **Works everywhere** — Cursor, Claude Desktop, LangGraph, any MCP client simultaneously
- **60-second setup** — one API key, one env var
- **94% token savings** — ~350 tokens per retrieval vs ~6,000 tokens stuffing full context
- **Self-hostable** — one Docker command, point at your own Postgres

## Quick Start

1. Get free API key: https://cascadeai.dev/hyperstack
2. Add to your MCP config:
```json
{
  "mcpServers": {
    "hyperstack": {
      "command": "npx",
      "args": ["-y", "hyperstack-mcp"],
      "env": {
        "HYPERSTACK_API_KEY": "hs_your_key",
        "HYPERSTACK_WORKSPACE": "my-project",
        "HYPERSTACK_AGENT_SLUG": "cursor-agent"
      }
    }
  }
}
```
3. Register your agent and start storing:
```
hs_identify({ agentSlug: "cursor-agent" })
hs_store({ slug: "use-clerk", title: "Use Clerk for auth",
  body: "Better DX, lower cost", type: "decision",
  confidence: 0.95, truthStratum: "confirmed", verifiedBy: "human:deeq" })
```

## Eight Graph Modes

| Mode | Tool | Question answered |
|------|------|-------------------|
| Smart | `hs_smart_search` | Ask anything — auto-routes to right mode |
| Forward | `hs_graph` | What does this card connect to? |
| Impact | `hs_impact` | What depends on this? What breaks if it changes? |
| Recommend | `hs_recommend` | What's topically related? |
| Time-travel | `hs_graph` with `at=` | What did the graph look like at any past moment? |
| Prune | `hs_prune` | What stale memory is safe to remove? |
| Branch diff | `hs_diff` | What changed in this branch vs parent? |
| Trust | `hs_profile` | How trustworthy is this agent? |

## Git-Style Memory Branching (NEW in v1.0.23)

```
hs_fork({ branchName: "experiment-v2" })      # Fork — parent untouched
hs_store({ slug: "new-approach", ... })        # Make changes in branch
hs_diff({ branchWorkspaceId: "clx..." })       # See what changed
hs_merge({ branchWorkspaceId: "clx...", strategy: "ours" })  # Merge if it worked
hs_discard({ branchWorkspaceId: "clx..." })    # Or discard if it didn't
```

## Agent Identity + Trust (NEW in v1.0.23)

```
hs_identify({ agentSlug: "research-agent" })   # Register with SHA256 fingerprint
hs_profile({ agentSlug: "research-agent" })    # trustScore: 0.84
```

## Trust & Provenance

Every card carries epistemic metadata:
- `confidence` — float 0.0–1.0, writer's self-reported certainty
- `truthStratum` — `draft` | `hypothesis` | `confirmed`
- `verifiedBy` — who/what confirmed this card
- `verifiedAt` — server-set automatically
- `sourceAgent` — immutable, set on creation

## Full Memory Lifecycle

```
Store facts      → hs_store (permanent, graph-linked)
Working memory   → hs_store with ttl= + type=scratchpad (auto-expires)
Commit outcomes  → hs_commit (what worked, as a decided card)
Clean up stale   → hs_prune dry=true → inspect → execute
Protect forever  → hs_store with pinned=true
Branch safely    → hs_fork → experiment → hs_merge or hs_discard
```

## How it compares

| | HyperStack | Mem0 | Engram | Cognee |
|--|---|---|---|---|
| "What blocks deploy?" | **Exact: typed blockers** | Fuzzy: similar tasks | Generic | Cypher required |
| Cost per op | **$0** | ~$0.002 LLM | Usage-based | ~$0.002 LLM |
| Memory branching | **✅ fork/diff/merge** | ❌ | ❌ | ❌ |
| Agent trust scores | **✅ Built-in** | ❌ | ❌ | ❌ |
| Provenance layer | **✅ Built-in** | ❌ | ❌ | ❌ |
| Time-travel | **✅ Any timestamp** | ❌ | ❌ | ❌ |
| Works in Cursor | **✅ MCP** | ❌ | ❌ | ❌ |
| Self-hostable | **✅ One Docker command** | ✅ Complex | ✅ | ✅ |
| Setup | **60 seconds** | 5-10min | 5min | 5min + Neo4j |

## Self-Hosting

```bash
docker run -d -p 3000:3000 \
  -e DATABASE_URL=postgresql://... \
  -e JWT_SECRET=your-secret \
  -e OPENAI_API_KEY=sk-... \
  ghcr.io/deeqyaqub1-cmd/hyperstack:latest
```

Full guide: https://github.com/deeqyaqub1-cmd/hyperstack-core/blob/main/SELF_HOSTING.md

## Available as

- **MCP Server**: `npx hyperstack-mcp` (v1.9.0) — 14 tools
- **Python SDK**: `pip install hyperstack-py` (v1.4.0)
- **LangGraph**: `pip install hyperstack-langgraph` (v1.4.0)
- **JavaScript SDK**: `npm install hyperstack-core` (v1.3.0)
- **Docker**: `ghcr.io/deeqyaqub1-cmd/hyperstack:latest`
- **REST API**: https://hyperstack-cloud.vercel.app

## Pricing

| Plan | Price | Cards | Features |
|------|-------|-------|---------|
| Free | $0 | 10 | Search only |
| Pro | $9/mo | 100 | All 8 modes + branching + agent identity |
| Team | $19/mo | 500 | All modes + webhooks + agent tokens |
| Business | $29/mo | 2,000 | All modes + SSO + 20 members |
| Self-hosted | $0 | Unlimited | Full feature parity |

## Links

- Website: https://cascadeai.dev/hyperstack
- GitHub: https://github.com/deeqyaqub1-cmd/hyperstack-core
- Discord: https://discord.gg/tdnXaV6e
