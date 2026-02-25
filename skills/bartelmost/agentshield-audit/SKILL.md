---
name: agentshield-audit
description: Initiate and manage AgentShield security audits for AI agents. Use when a user wants to audit their agent's security posture, generate cryptographic identity keys, obtain security certificates, or verify other agents' trustworthiness. Triggers on phrases like "audit my agent", "get security certificate", "verify agent", or "activate AgentShield".
---

# AgentShield Audit Skill

🔒 **Audit your agent's security and obtain verifiable trust certificates for inter-agent communication.**

No API key required. No registration. Just install and run.

---

## 🚀 One-Line Quick Start

```bash
clawhub install agentshield-audit && python -m agentshield_audit
```

That's it. Your agent will be audited in ~30 seconds.

---

## 📋 The Complete Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1️⃣  INSTALL                                            │
│     clawhub install agentshield-audit                   │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2️⃣  AUTO-DETECT                                        │
│     Skill detects your agent name & platform            │
│     (reads IDENTITY.md, SOUL.md, channel config)        │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  3️⃣  GENERATE KEYS                                      │
│     Ed25519 keypair created locally                     │
│     Stored in: ~/.agentshield/agent.key                 │
│     🔐 Private keys NEVER leave your workspace          │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  4️⃣  RUN AUDIT (~30 seconds)                            │
│     ✓ System Prompt Extraction Test                     │
│     ✓ Instruction Override Test                         │
│     ✓ Tool Permission Check                             │
│     ✓ Memory Isolation Test                             │
│     ✓ Secret Leakage Detection                          │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  5️⃣  RECEIVE CERTIFICATE                                │
│     90 days validity • Verifiable by anyone             │
│     Show with: python scripts/show_certificate.py       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 When to Use

- ✅ User wants to audit their agent's security
- ✅ User wants a trust certificate for their agent
- ✅ User wants to verify another agent's certificate
- ✅ Setting up inter-agent secure communication
- ✅ Before installing untrusted skills

---

## 🛠️ Installation Methods

### Method A: One-Line (Recommended)
```bash
clawhub install agentshield-audit && python -m agentshield_audit
```

### Method B: Step by Step
```bash
# Install the skill
clawhub install agentshield-audit

# Run with auto-detection (detects name, platform automatically)
cd ~/.openclaw/workspace/skills/agentshield-audit
python scripts/initiate_audit.py --auto

# Or specify manually
python scripts/initiate_audit.py --name "MyAgent" --platform telegram
```

---

## 📊 Understanding Your Results

### Security Score (0-100)
| Score | Tier | Description |
|-------|------|-------------|
| 90-100 | 🛡️ HARDENED | Passed all critical tests. Top-tier security. |
| 75-89 | ✅ PROTECTED | Passed most tests. Minor issues found. |
| 50-74 | ⚠️ BASIC | Minimum requirements met. Room for improvement. |
| <50 | 🔴 VULNERABLE | Failed critical tests. Immediate action recommended. |

### Your Certificate
- **Valid for:** 90 days
- **Format:** Ed25519-signed JWT
- **Storage:** `~/.openclaw/workspace/.agentshield/certificate.json`
- **Verification URL:** `https://agentshield.live/verify/YOUR_AGENT_ID`

---

## 🔐 Security Model

- **Private keys** never leave the agent's workspace
- **Challenge-response** authentication prevents replay attacks
- **Certificates** are signed by AgentShield and verifiable by anyone
- **90-day validity** encourages regular re-auditing
- **Rate limiting:** 1 audit per hour per IP (prevents abuse)

---

## 🧰 Script Reference

| Script | Purpose | Example |
|--------|---------|---------|
| `initiate_audit.py` | Start new audit | `python scripts/initiate_audit.py --auto` |
| `verify_peer.py` | Verify another agent | `python scripts/verify_peer.py --agent-id "agent_xyz789"` |
| `show_certificate.py` | Display your certificate | `python scripts/show_certificate.py` |
| `audit_client.py` | Low-level API client | Import for custom integrations |

---

## 🆓 Demo Mode / Free Usage

**First 3 audits are completely free.** No registration, no API key.

After that:
- Rate limit: 1 audit per hour per IP
- No payment required for basic usage
- Enterprise/high-volume: Contact us

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No certificate found" | Run `initiate_audit.py` first |
| "Challenge failed" | Check system clock (NTP sync required) |
| "API unreachable" | Verify internet connection |
| "Rate limited" | Wait 1 hour between audits |
| Auto-detection failed | Use `--name` and `--platform` manually |

---

## 📚 Additional Documentation

- [Quick Start Guide](QUICKSTART.md) - Step-by-step for first-time users
- [API Reference](references/api.md) - Technical API documentation
- [GitHub Repo](https://github.com/bartelmost/agentshield) - Source code & issues

---

## 💬 Questions?

Open an issue on GitHub or ping @Kalle-OC on Moltbook.

**Secure yourself. Verify others. Trust nothing by default.** 🛡️
