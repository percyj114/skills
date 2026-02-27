# Swaps Intel Skill (ClawHub Launch Pack)

Swaps Intel gives AI agents blockchain risk signals for wallet addresses and transactions.

## What this skill does
- Checks a crypto address using Swaps Intelligence API
- Returns risk score, sanctions/labels, and report link
- Helps users triage potential scam exposure

## What this skill does **not** do
- Does **not** provide legal advice
- Does **not** provide investment advice
- Does **not** guarantee asset recovery
- Does **not** make definitive criminal allegations

## API Endpoint
- Base URL: `https://system.swaps.app/functions/v1/agent-api`
- Operation: `POST /check_address_risk`
- Auth: `Bearer <API_KEY>`

## Minimal request
```json
{
  "address": "0x..."
}
```

## Minimal response (shape)
```json
{
  "markdown_summary": "..."
}
```

## Mandatory output policy for agents using this skill
1. Treat output as **risk analytics**, not final truth.
2. Keep factual data unchanged.
3. Always include source/report link if returned.
4. Include disclaimer text in user-facing response.

## Required disclaimer (copy-paste)
> Swaps Search provides blockchain analytics signals for informational purposes only. Results may include false positives or false negatives and are not legal, compliance, financial, or investigative advice. Swaps does not guarantee asset recovery outcomes. Users are solely responsible for decisions and actions taken based on these outputs.

## Links
- Bot: https://t.me/SwapSearchBot
- Product: https://www.swaps.app/search
- Contact: support@swaps.app
