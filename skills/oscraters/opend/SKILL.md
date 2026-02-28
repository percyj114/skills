---
name: opend
description: Agentic trading and market-data workflows for Futu OpenD (MooMoo/Futu OpenAPI), including secure credential handling, account discovery, position queries, and order placement. Use when tasks require calling local OpenD through Python/Bash automation, especially with repeatable CLI-driven flows and structured JSON output.
---

# OpenD Skill

Use this skill to execute local OpenD operations through a single CLI surface.

## Quick Start

- Ensure OpenD is running (default `127.0.0.1:11111`).
- Install one provider SDK: `moomoo` or `futu`.
- Optional credential helpers: `pip install keyring cryptography`.
- Set password source:
  - `env`: `export MOOMOO_PASSWORD='...'`
  - `config`: `setup_config.py` then `export MOOMOO_CONFIG_KEY='...'`
  - `keyring`: first call prompts and stores in system keyring.

## Primary Interface

Use Bash CLI `./openclaw` for all routine operations.

Examples:
- Snapshot:
  - `./openclaw snapshot --codes HK.00700,US.AAPL`
- Accounts:
  - `./openclaw accounts`
- Positions:
  - `./openclaw --trd-env SIMULATE positions`
- Place simulated order:
  - `./openclaw --market HK --trd-env SIMULATE place-order --code HK.00700 --price 100 --qty 100 --side BUY`
- Cancel order:
  - `./openclaw --market HK --trd-env SIMULATE cancel-order --order-id <ORDER_ID>`

## Agentic Defaults

- Prefer `--output json` (default) so downstream steps can parse results.
- Prefer `SIMULATE` unless user explicitly requests live trading.
- Query `accounts` first for unknown environments; then pass explicit `--acc-id` when needed.
- For live trading, unlock is required; simulated accounts skip unlock automatically.

## Environment Overrides

`openclaw` reads these defaults when present:
- `OPEND_HOST`
- `OPEND_PORT`
- `OPEND_MARKET`
- `OPEND_SECURITY_FIRM`
- `OPEND_TRD_ENV`
- `OPEND_CREDENTIAL_METHOD`
- `OPEND_OUTPUT`
- `OPEND_SDK_PATH` (optional SDK path override)

## Files

- `openclaw`: Bash CLI entrypoint.
- `opend_cli.py`: structured command interface.
- `opend_core.py`: shared OpenD logic (SDK load, context, account resolution).
- `credentials.py`: env/keyring/encrypted-config password loading.
- `references/api_docs.md`: official API links and key limits.

## Legacy Compatibility

Older scripts now delegate to `opend_cli.py`:
- `get_market_snapshot.py`
- `query_positions.py`
- `place_order.py`
- `place_order_env.py`
- `place_order_keyring.py`
- `place_order_config.py`
