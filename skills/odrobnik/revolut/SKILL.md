---
name: revolut
description: "Revolut web automation via Playwright: login/logout, list accounts, and fetch transactions."
summary: "Revolut banking automation: login, accounts, transactions, portfolio."
version: 1.2.2
homepage: "https://github.com/odrobnik/revolut-skill"
metadata: {"openclaw": {"emoji": "💳", "requires": {"bins": ["python3", "playwright"], "python": ["playwright"]}}}
---

# Revolut Banking Automation

Fetch current account balances, investment portfolio holdings, and transactions for all wallet currencies and depots in JSON format for automatic processing. Uses Playwright to automate Revolut web banking.

**Entry point:** `{baseDir}/scripts/revolut.py`

## Authentication

Requires **2FA via the Revolut app** on your iPhone. When the script initiates login, a QR code and approval link are generated. Either open the link on the device where you have your Revolut app installed, or scan the QR code with the device you use for authorization.

The QR code image is saved to `/tmp/openclaw/revolut/revolut_qr.png` and the path is output as `QR_IMAGE:<path>` for the agent to send.

## Configuration

Create `{workspace}/revolut/config.json`:

```json
{
  "users": {
    "oliver": {},
    "sylvia": { "pin": "123456" }
  }
}
```

- **Single user**: auto-selected, no `--user` needed.
- **Multiple users**: `--user` is required.
- **pin**: optional 6-digit app pin for auto-entry.

## Commands

```bash
python3 {baseDir}/scripts/revolut.py --user oliver login
python3 {baseDir}/scripts/revolut.py --user oliver accounts
python3 {baseDir}/scripts/revolut.py --user oliver transactions --from YYYY-MM-DD --until YYYY-MM-DD
python3 {baseDir}/scripts/revolut.py --user sylvia portfolio
python3 {baseDir}/scripts/revolut.py --user oliver invest-transactions --from YYYY-MM-DD --until YYYY-MM-DD
```

## Recommended Flow

```
login → accounts → transactions → portfolio → logout
```

Always call `logout` after completing all operations to delete the stored browser session (cookies, local storage, Playwright profile). This minimizes persistent auth state on disk.

Per-user state stored in `{workspace}/revolut/`:
- `state_{user}.json` + `.pw-state_{user}-profile/` (deleted by `logout`)

## Notes
- Output paths (`--out`) are sandboxed to workspace or `/tmp`.
- No `.env` file loading — credentials in config.json only.
- The `pin` field in config.json is a non-secret personal identification number used to start the Revolut auth flow, not a credential.
