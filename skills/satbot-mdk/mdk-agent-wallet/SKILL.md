---
name: agent-wallet
description: Self-custodial Bitcoin Lightning wallet for AI agents. Use when the agent needs to send or receive bitcoin payments, check its balance, generate invoices, or manage its wallet. Supports bolt11, bolt12, LNURL, and lightning addresses. Zero config — one command to initialize.
homepage: https://docs.moneydevkit.com/agent-wallet
repository: https://github.com/anthropics/moneydevkit
metadata:
  {
    "openclaw":
      {
        "emoji": "₿",
        "requires": { "bins": ["node", "npx"] },
        "install":
          [
            {
              "id": "agent-wallet-npm",
              "kind": "npm",
              "package": "@moneydevkit/agent-wallet",
              "bins": ["agent-wallet"],
              "label": "Install @moneydevkit/agent-wallet (npm)",
            },
          ],
        "security":
          {
            "secrets": ["~/.mdk-wallet/config.json (BIP39 mnemonic)"],
            "network": ["localhost:3456 (daemon HTTP server)", "MDK Lightning infrastructure via outbound connections"],
            "persistence": ["~/.mdk-wallet/ (config, payment history)"],
            "notes": "The wallet stores a BIP39 mnemonic to disk and runs a local daemon. The mnemonic controls real funds on mainnet. Back it up and restrict file permissions on ~/.mdk-wallet/."
          }
      },
  }
---

# agent-wallet

Self-custodial Lightning wallet for AI agents, built by [MoneyDevKit](https://moneydevkit.com). One command to init. All output is JSON.

**Source:** [@moneydevkit/agent-wallet on npm](https://www.npmjs.com/package/@moneydevkit/agent-wallet) · [GitHub](https://github.com/anthropics/moneydevkit)

## Security & Transparency

This skill runs `@moneydevkit/agent-wallet` — an npm package published by MoneyDevKit. What it does:

- **Generates and stores a BIP39 mnemonic** at `~/.mdk-wallet/config.json` — this IS your private key. Treat it like a password.
- **Runs a local daemon** on `localhost:3456` — HTTP server for wallet operations. Binds to localhost only (not externally accessible).
- **Connects outbound** to MDK's Lightning infrastructure.
- **Persists payment history** to `~/.mdk-wallet/`.

No data is sent to external servers beyond standard Lightning protocol operations. You can verify this by inspecting the [source code](https://github.com/anthropics/moneydevkit) or the published npm tarball.

### Security Guardrails

- **Localhost-only binding**: The daemon HTTP server binds exclusively to `127.0.0.1:3456` — it is not accessible from the network or other machines.
- **File permissions**: Config and payment files are written with mode `0600` (owner-read/write only). The config directory uses mode `0700`.
- **No external data exfiltration**: The daemon communicates only with MDK Lightning infrastructure via standard Lightning protocol. No telemetry, no analytics, no third-party reporting.
- **Webhook URLs are user-configured**: Payment notification webhooks only fire to URLs explicitly set by the user via `config-webhook`. They are never set automatically and default to off.
- **Mnemonic stays local**: The BIP39 mnemonic never leaves the local filesystem. It is not transmitted, logged, or included in webhook payloads.
- **Pin versions in production**: Use `npx @moneydevkit/agent-wallet@0.12.0` to lock to a specific version and avoid supply chain risk from unpinned `@latest` resolution.

## Quick Start

```bash
# Initialize wallet (generates mnemonic)
npx @moneydevkit/agent-wallet@0.12.0 init

# Get balance
npx @moneydevkit/agent-wallet@0.12.0 balance

# Create invoice
npx @moneydevkit/agent-wallet@0.12.0 receive 1000

# Pay someone
npx @moneydevkit/agent-wallet@0.12.0 send user@getalby.com 500
```

## How It Works

The CLI automatically starts a daemon on first command. The daemon:
- Runs a local HTTP server on `localhost:3456`
- Connects to MDK's Lightning infrastructure
- Polls for incoming payments every 30 seconds
- Persists payment history to `~/.mdk-wallet/`

Optionally, configure a webhook to get notified instantly when payments arrive.

## Setup

### First-time initialization

```bash
npx @moneydevkit/agent-wallet@0.12.0 init
```

This command:
1. **Generates a BIP39 mnemonic** — 12-word seed phrase that IS your wallet
2. **Creates config** at `~/.mdk-wallet/config.json`
3. **Derives a walletId** — deterministic 8-char hex ID from your mnemonic
4. **Starts the daemon** — local Lightning node on port 3456

The wallet is ready immediately. No API keys, no signup, no accounts. The agent holds its own keys.

### View existing config

```bash
npx @moneydevkit/agent-wallet@0.12.0 init --show
```

Returns `{ "mnemonic": "...", "network": "mainnet", "walletId": "..." }`.

**Note:** `init` will refuse to overwrite an existing wallet. To reinitialize:

```bash
npx @moneydevkit/agent-wallet@0.12.0 stop
rm -rf ~/.mdk-wallet  # WARNING: backup mnemonic first!
npx @moneydevkit/agent-wallet@0.12.0 init
```

## Commands

All commands return JSON on stdout. Exit 0 on success, 1 on error.

| Command | Description |
|---------|-------------|
| `init` | Generate mnemonic, create config |
| `init --show` | Show config (mnemonic redacted) |
| `start` | Start the daemon |
| `balance` | Get balance in sats |
| `receive <amount>` | Generate invoice |
| `receive` | Generate variable-amount invoice |
| `receive <amount> --description "..."` | Invoice with custom description |
| `receive-bolt12` | Generate a BOLT12 offer (variable amount, reusable) |
| `send <destination> [amount]` | Pay bolt11, bolt12, lnurl, or lightning address |
| `payments` | List payment history |
| `status` | Check if daemon is running |
| `config-webhook <url>` | Set webhook URL for payment notifications |
| `config-webhook <url> --secret <token>` | Set webhook URL with auth token |
| `config-webhook --clear` | Remove webhook URL and secret |
| `stop` | Stop the daemon |
| `restart` | Restart the daemon |

### Balance

```bash
npx @moneydevkit/agent-wallet@0.12.0 balance
```
→ `{ "balance_sats": 3825 }`

### Receive (generate invoice)

```bash
# Fixed amount
npx @moneydevkit/agent-wallet@0.12.0 receive 1000

# Variable amount (payer chooses)
npx @moneydevkit/agent-wallet@0.12.0 receive

# With description
npx @moneydevkit/agent-wallet@0.12.0 receive 1000 --description "payment for service"
```
→ `{ "invoice": "lnbc...", "payment_hash": "...", "expires_at": "..." }`

### Receive BOLT12 Offer

```bash
npx @moneydevkit/agent-wallet@0.12.0 receive-bolt12
```
→ `{ "offer": "lno1..." }`

BOLT12 offers are reusable and don't expire — share one offer and receive unlimited payments to it. Unlike BOLT11 invoices, the payer chooses the amount.

### Send

```bash
npx @moneydevkit/agent-wallet@0.12.0 send <destination> [amount_sats]
```

Destination auto-detection:
- **bolt11 invoice**: `lnbc10n1...` (amount encoded, no arg needed)
- **bolt12 offer**: `lno1...`
- **lightning address**: `user@example.com`
- **LNURL**: `lnurl1...`

For lightning addresses and LNURL, amount is required:
```bash
npx @moneydevkit/agent-wallet@0.12.0 send user@getalby.com 500
```

### Payment History

```bash
npx @moneydevkit/agent-wallet@0.12.0 payments
```
→ `{ "payments": [{ "paymentHash": "...", "amountSats": 1000, "direction": "inbound"|"outbound", "timestamp": ..., "destination": "..." }] }`

## Upgrading

```bash
# Stop the running daemon
npx @moneydevkit/agent-wallet@0.12.0 stop

# Run with @latest to pull the newest version
npx @moneydevkit/agent-wallet@0.12.0 start
```

Your wallet config and payment history in `~/.mdk-wallet/` are preserved across upgrades.

## Webhooks

Get notified instantly when payments arrive — no polling, no manual confirmation.

### Setup

```bash
# Set webhook URL (persisted in ~/.mdk-wallet/config.json)
npx @moneydevkit/agent-wallet@0.12.0 config-webhook <url>

# With auth token (for endpoints that require Bearer auth)
npx @moneydevkit/agent-wallet@0.12.0 config-webhook <url> --secret <token>

# Check current webhook config
npx @moneydevkit/agent-wallet@0.12.0 config-webhook

# Remove webhook
npx @moneydevkit/agent-wallet@0.12.0 config-webhook --clear
```

**Restart the daemon after setting the webhook** for it to take effect:

```bash
npx @moneydevkit/agent-wallet@0.12.0 restart
```

### Webhook Payload

When a payment is received, the daemon POSTs to the configured URL:

```json
{
  "message": "Lightning payment received: 1000 sats (payment_hash: abc123...). Your new wallet balance is 50000 sats.",
  "name": "agent-wallet",
  "deliver": true,
  "event": "payment_received",
  "payment_hash": "abc123...",
  "amount_sats": 1000,
  "payer_note": "optional note from sender",
  "new_balance_sats": 50000,
  "timestamp": 1709123456789
}
```

The webhook is fire-and-forget (5s timeout, async) — never blocks payment processing. Duplicate events from daemon restarts are automatically skipped.

### Advanced: `webhookBody` Overrides

For routing to specific channels, you can add a `webhookBody` object to `~/.mdk-wallet/config.json`. These fields merge into every webhook POST, letting you control delivery without changing the wallet code:

```json
{
  "webhookBody": {
    "channel": "signal",
    "to": "group:your-group-id-here"
  }
}
```

### OpenClaw Integration

To get payment notifications delivered to a chat, use OpenClaw's webhook hooks:

**1. Enable OpenClaw hooks** (one-time):

```bash
openclaw config set hooks.enabled true
openclaw config set hooks.token "$(openssl rand -hex 16)"
openclaw gateway restart
```

**2. Point agent-wallet at `/hooks/agent`:**

```bash
# Get your hooks token
openclaw config get hooks.token

# Configure agent-wallet
npx @moneydevkit/agent-wallet@0.12.0 config-webhook http://127.0.0.1:18789/hooks/agent --secret <your-hooks-token>
```

**3. Set delivery target** in `~/.mdk-wallet/config.json`:

Add a `webhookBody` with your desired channel and recipient:

```json
{
  "webhookBody": {
    "channel": "signal",
    "to": "group:your-signal-group-id"
  }
}
```

Other channel options: `telegram`, `discord`, `slack`, `whatsapp`, `imessage`.
The `to` field is the recipient ID for that channel (group ID, chat ID, phone number, etc.).

**4. Restart the daemon:**

```bash
npx @moneydevkit/agent-wallet@0.12.0 restart
```

Now when a payment arrives, OpenClaw spawns an isolated agent turn that announces it to your chat. The agent sees the payment details and sends a confirmation message — no polling, no "did you pay?" back-and-forth.

**How it works under the hood:**
- agent-wallet POSTs to `/hooks/agent` with `deliver: true`
- OpenClaw runs an isolated agent session with the payment message
- The agent's response is delivered to the configured channel/recipient
- The whole flow takes ~5 seconds from payment to chat notification

### Environment Variables

- `MDK_WALLET_WEBHOOK_URL` — override webhook URL
- `MDK_WALLET_WEBHOOK_SECRET` — override webhook auth token

## Usage Notes

- **Denomination**: use ₿ prefix with sats (e.g. ₿1,000 not "1,000 sats")
- **Self-custodial**: the mnemonic IS the wallet. Back it up. Lose it, lose funds.
- **Daemon**: runs a local Lightning node on `:3456`. Auto-starts, persists to disk.
- **Agent-to-agent payments**: any agent with this wallet can pay any other agent's invoice or lightning address.

## What's Next?

**Want to accept payments from customers?** Use the [moneydevkit skill](https://clawhub.ai/satbot-mdk/moneydevkit) to add checkouts to any website. Agent-wallet handles agent-to-agent payments; moneydevkit handles customer-to-agent payments. Together they give your agent full payment superpowers.
