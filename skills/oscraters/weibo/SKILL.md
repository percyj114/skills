---
name: weibo
description: Use Weibo Open Platform for OAuth2 authentication, timeline/trend retrieval, and structured social sentiment collection. Trigger this skill when tasks involve Weibo API calls, token setup, endpoint debugging, Chinese social trend monitoring, or fallback Weibo web search when API access is unavailable.
---

# Weibo

Use this skill to collect Weibo signals with reproducible API calls and CLI automation.

## Quick Start

1. Review [references/api_guide.md](references/api_guide.md) for current official endpoints and constraints.
2. Export credentials:
`export WEIBO_APP_KEY=...`
`export WEIBO_APP_SECRET=...`
`export WEIBO_REDIRECT_URI=...`
3. Generate an authorization URL:
`bash scripts/weibo_cli.sh oauth-authorize-url`
4. Exchange `code` for a token:
`bash scripts/weibo_cli.sh oauth-access-token --code "<code>"`
5. Call endpoints:
`bash scripts/weibo_cli.sh public-timeline --count 20`

## Primary Interface

Use the Bash CLI first:
- `scripts/weibo_cli.sh`: OAuth2 + direct API command interface, optimized for agentic runs.

Fallback discovery:
- `scripts/weibo_search.py`: Web search fallback for `site:weibo.com` when API app approval/token is unavailable.

## Recommended Workflow

1. Validate provider requirements in [references/api_guide.md](references/api_guide.md).
2. Run `oauth-authorize-url`, open URL, capture `code`.
3. Run `oauth-access-token --code ...` and store token securely.
4. Use endpoint helpers (`public-timeline`, `user-timeline`, `search-topics`) or `call`.
5. If API access is blocked, use `python3 scripts/weibo_search.py "<keyword>"`.

## CLI Command Surface

- `oauth-authorize-url`
- `oauth-access-token --code <code>`
- `oauth-token-info`
- `public-timeline [--count N] [--page N]`
- `user-timeline --uid <uid> [--count N]`
- `search-topics --q <query>`
- `call --method GET --path /2/... --param key=value`

Run `bash scripts/weibo_cli.sh --help` for details.

## Notes

- Prefer JSON output for downstream automation.
- Keep requests minimal and paginated to reduce rate-limit pressure.
- Use the official docs linked in [references/api_guide.md](references/api_guide.md) as source of truth when endpoint behavior conflicts with old SDK examples.
