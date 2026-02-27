---
name: payclaw-io
description: "Give your AI agent a virtual card to make real purchases. Intent-based authorization, post-purchase audit, $500 max balance. Uses the PayClaw MCP server (@payclaw/mcp-server)."
metadata:
  {
    "openclaw":
      {
        "emoji": "💳",
        "requires": { "bins": ["npx"], "env": ["PAYCLAW_API_KEY"] },
        "mcp":
          {
            "name": "payclaw",
            "command": "npx",
            "args": ["@payclaw/mcp-server"],
            "env": { "PAYCLAW_API_KEY": "${PAYCLAW_API_KEY}", "PAYCLAW_API_URL": "https://payclaw.io" },
          },
      },
  }
---

# PayClaw — Virtual Cards for AI Agents

Give your agent a funded virtual card so it can buy things for you — without ever touching your real credit card.

## Setup

### 1. Create a PayClaw account

Sign up at [payclaw.io](https://payclaw.io) and set up MFA (required).

### 2. Fund your wallet

Add funds from your dashboard (up to $500). This is what your agent can spend.

### 3. Generate an API key

Go to Settings → Create API Key. Copy the `pk_live_...` key (shown once).

### 4. Set the environment variable

```bash
export PAYCLAW_API_KEY="pk_live_your_key_here"
```

Or add it to your OpenClaw config.

## What Your Agent Can Do

### Buy something

> "Order me two large pizzas from Domino's, keep it under $30"

The agent will:
1. Declare what it wants to buy (merchant, amount, description)
2. PayClaw checks your balance and spending rules
3. If approved, agent gets a virtual card
4. Agent completes checkout
5. Agent reports what it actually bought
6. PayClaw auto-audits: did the purchase match the intent?

### Tools available

| Tool | What it does |
|------|-------------|
| `payclaw_getCard` | Declare purchase intent → get a virtual card |
| `payclaw_reportPurchase` | Report what was bought → auto-audit against intent |

## Security

- **Intent-based:** Agent must declare what it's buying before getting card access
- **Auto-audit:** Every purchase is compared against the declared intent
- **$500 ceiling:** Hard cap on total balance
- **Mandatory MFA:** Every account requires authenticator app
- **API keys hashed:** Same security model as Stripe
- **Instant kill:** Revoke your API key from the dashboard at any time

## Example

```
You: "Buy me a new mechanical keyboard from Amazon, budget $75"

Agent: I'll help you purchase a mechanical keyboard. Let me get a card...
       [calls payclaw_getCard: merchant=amazon.com, amount=$75, desc="mechanical keyboard"]
       
       ✅ Card approved. Completing purchase on Amazon...
       
       [completes checkout for $67.99]
       [calls payclaw_reportPurchase: intent matched ✅, $67.99 vs $75 estimate]
       
       Done! Ordered a Keychron K6 mechanical keyboard for $67.99.
       Your remaining PayClaw balance is $432.01.
```

## Pricing

- **1.5% fee** on wallet deposits (e.g., $1.50 on a $100 deposit)
- No per-transaction fees
- No monthly subscription

## Links

- [Dashboard](https://payclaw.io/dashboard)
- [Documentation](https://payclaw.io/docs)
- [Security](https://payclaw.io/docs/security)
- [GitHub](https://github.com/payclaw/mcp-server)
