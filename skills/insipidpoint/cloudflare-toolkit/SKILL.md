---
name: cloudflare
description: Manage Cloudflare domains, DNS records, SSL settings, zone configuration, firewall rules, tunnels, and analytics via the Cloudflare API. Use when the user asks to set up a domain, add/edit/delete DNS records, configure SSL, check zone settings, manage Cloudflare Tunnels, view analytics, or any Cloudflare account management task.
---

# Cloudflare

Manage Cloudflare zones, DNS, SSL, tunnels, and settings via the `cf` CLI wrapper.

## Setup

Requires environment variables:
- `CLOUDFLARE_API_TOKEN` — API token (create at dash.cloudflare.com/profile/api-tokens)
- `CLOUDFLARE_ACCOUNT_ID` — Account ID (needed for tunnel operations only; find in dashboard sidebar)

## CLI: `scripts/cf`

All operations go through the `cf` bash script. Run from skill directory or add to PATH.

```bash
CF="$(dirname "$0")/../skills/cloudflare/scripts/cf"
# or if on PATH:
cf <command> [args...]
```

### Commands

| Command | Args | Description |
|---------|------|-------------|
| `verify` | | Verify API token is valid |
| `zones` | `[domain]` | List zones (optionally filter by domain name) |
| `zone-get` | `<zone_id>` | Get zone details |
| `dns-list` | `<zone_id> [type] [name]` | List DNS records |
| `dns-create` | `<zone_id> <type> <name> <content> [proxied] [ttl]` | Create DNS record |
| `dns-update` | `<zone_id> <record_id> <type> <name> <content> [proxied] [ttl]` | Update DNS record |
| `dns-delete` | `<zone_id> <record_id>` | Delete DNS record |
| `settings-list` | `<zone_id>` | List all zone settings |
| `setting-get` | `<zone_id> <setting>` | Get specific setting |
| `setting-set` | `<zone_id> <setting> <value>` | Update a setting |
| `ssl-get` | `<zone_id>` | Get current SSL mode |
| `ssl-set` | `<zone_id> <mode>` | Set SSL mode (off/flexible/full/strict) |
| `pagerules-list` | `<zone_id>` | List page rules |
| `firewall-list` | `<zone_id>` | List firewall rules |
| `tunnels-list` | | List Cloudflare Tunnels (needs ACCOUNT_ID) |
| `tunnel-get` | `<tunnel_id>` | Get tunnel details |
| `analytics` | `<zone_id> [since_minutes]` | Zone analytics (default: last 24h) |

### Proxied flag

- `true` — orange cloud, traffic through Cloudflare (CDN, WAF, DDoS)
- `false` — grey cloud, DNS-only (use for MX, non-HTTP services)

### TTL

- `1` = automatic (Cloudflare-managed)
- Set explicit seconds for DNS-only records (e.g., `3600`)

## Typical workflows

### Point domain to server
```bash
# Find zone ID
cf zones example.com
# Create A record (proxied)
cf dns-create <zone_id> A example.com 1.2.3.4 true
# Create www CNAME
cf dns-create <zone_id> CNAME www.example.com example.com true
```

### Set up email (MX + SPF)
```bash
cf dns-create <zone_id> MX example.com "mx.provider.com" false 1
cf dns-create <zone_id> TXT example.com "v=spf1 include:provider.com ~all" false
```

### Enable strict SSL
```bash
cf ssl-set <zone_id> strict
```

## Safety rules

**Always confirm with the user before:**
- Deleting DNS records (`dns-delete`)
- Changing SSL mode
- Modifying firewall rules
- Any destructive operation

**Safe to do freely:**
- Listing/reading zones, records, settings, analytics
- Verifying token

## Reference

For DNS record types, SSL modes, and API details: see `references/api-guide.md`
