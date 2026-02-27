# Caravo Agent Skills

Agent Skills for [Caravo](https://caravo.ai) — non-MCP agent integration for OpenClaw, Claude Code, Cursor, Codex, and 40+ other agents.

## Install

```bash
# ClawHub (OpenClaw)
npx clawhub@latest install caravo

# Vercel Skills CLI
npx skills add Caravo-AI/Agent-Skills

# Manual
curl -fsSL https://raw.githubusercontent.com/Caravo-AI/Agent-Skills/main/SKILL.md \
  --create-dirs -o ~/.openclaw/skills/caravo/SKILL.md
```

## What's Inside

`SKILL.md` — A comprehensive agent skill that teaches AI agents how to use Caravo's marketplace via the `caravo` CLI. Supports both API key authentication and x402 USDC payments.

The skill covers:
- Tool search and discovery
- Tool execution with automatic payment
- Review and upvote system
- Favorites management
- Tool request submission
- Raw x402 HTTP mode

## Requirements

- `caravo` CLI (`npm install -g @caravo/cli`)
- Either `CARAVO_API_KEY` env var or USDC on Base for x402 payments

## License

MIT
