# AgentShield Security Audit

**Privacy-first security auditing for AI agents with human oversight.**

## Overview

AgentShield enables AI agents to audit their own security posture—but only with **explicit human permission** at every step. This skill guides agents through a comprehensive security assessment while ensuring sensitive data is handled responsibly.

⚠️ **Important:** This skill requires human-in-the-loop approval for all sensitive operations. Your agent **cannot** and **will not** transmit system prompts, code, or configuration data without your explicit consent.

---

## 🔒 Security & Privacy First

### Data Handling
- **Explicit Consent:** Your agent asks for permission before sending ANY sensitive data
- **Transient Processing:** System prompts and code are analyzed in memory and not stored permanently
- **30-Day Logs:** Debugging logs retained for 30 days only, then auto-deleted
- **Encrypted Transmission:** All data sent via HTTPS with TLS 1.3

### Key Management
- **Local Generation:** Ed25519 key pairs are generated locally on your system
- **Private Key Security:** The private key NEVER leaves your device
- **Public Key Only:** Only the public key is shared with AgentShield for certificate issuance
- **No Key Storage:** AgentShield does not store agent private keys

### Authentication
- **API Key Required:** Human administrator must configure `AGENTSHIELD_API_KEY`
- **Endpoint Configuration:** Self-hosted or managed endpoint must be explicitly set
- **No Blind Trust:** Agent cannot connect to unknown endpoints

---

## 📋 Requirements

- Python 3.12+
- `cryptography` library (`pip install cryptography`)
- Configured AgentShield API endpoint
- Valid API key (obtained from agentshield.live)

---

## ⚙️ Configuration

Before using this skill, the human administrator must configure:

```bash
export AGENTSHIELD_API_KEY="your-api-key-here"
export AGENTSHIELD_ENDPOINT="https://agentshield-api-bartel-fe94823ceeea.herokuapp.com"
```

**Note:** The agent **cannot** proceed without these environment variables set.

---

## 🚀 Usage (Human-in-the-Loop)

### Step 1: Agent Requests Permission
Your agent will ask:
> "I can run a comprehensive security audit on myself using AgentShield. This will check:"
> - Input sanitization (prompt injection resistance)
> - Output data loss prevention
> - Tool sandbox validation
> - Prompt leak detection
> - Supply chain security
> 
> **Do you want me to proceed with the audit?** (Yes/No)

### Step 2: Granular Consent
For each security module, your agent asks for specific permission:

**Input Sanitizer Check:**
> "To test prompt injection resistance, I need to send my system prompt to the AgentShield API. **Allow me to send my system prompt?** (Yes/No)"

**Code Security Scan:**
> "To check for vulnerabilities, I need to send my skill code for analysis. **Allow me to send my code?** (Yes/No)"

**Tool Sandbox Test:**
> "I will test my tool execution permissions locally first, then report results. **Proceed with local sandbox test?** (Yes/No)"

### Step 3: Local Processing (Where Possible)
Some tests run entirely locally:
- Tool Sandbox validation
- EchoLeak basic checks
- Supply Chain pattern matching

Data is only sent to external APIs when:
1. You explicitly approve it
2. It's necessary for the specific test
3. The data is encrypted in transit

### Step 4: Results & Certificate
After completion (with your approval at each step):
- Security score presented to you
- Ed25519-signed certificate generated (optional)
- PDF report available for download (optional)

---

## 🛡️ What This Skill Does NOT Do

❌ **Never sends data without permission**  
❌ **Never stores your private keys**  
❌ **Never connects to unknown endpoints**  
❌ **Never runs without API key**  
❌ **Never retains sensitive data permanently**  

---

## 🔐 The Agent Audit Flow

With your explicit approval at each step:

1. **Initiate:** Agent requests audit session (requires your API key)
2. **Challenge:** Agent proves identity via Ed25519 signature (local operation)
3. **Test:** For each security module, agent asks your permission before sending data
4. **Certificate:** Optional Ed25519 certificate issued (public key only)

**Your agent controls:**
- What data to share (you decide)
- Which tests to run (you approve each)
- Whether to get a certificate (optional)

**You control:**
- API endpoint configuration
- API key management
- Data sharing permissions
- Audit scope

---

## 📊 Security Tiers

| Tier | Score | Description |
|------|-------|-------------|
| 🛡️ HARDENED | 90-100 | All tests passed with high scores |
| ✅ PROTECTED | 75-89 | Good security, minor improvements |
| ⚡ BASIC | 50-74 | Standard security, some issues |
| ⚠️ UNVERIFIED | 0-49 | Critical issues found |

---

## 🏠 Self-Hosted Option

For maximum privacy, you can self-host the AgentShield backend:

```bash
# Clone and deploy your own instance
git clone https://github.com/bartelmost/agentshield.git
cd agentshield
pip install -r requirements.txt
python main.py

# Configure agent to use your endpoint
export AGENTSHIELD_ENDPOINT="http://localhost:5000"
```

This ensures NO data leaves your infrastructure.

---

## ⚠️ Scope Limitations

This skill is **instruction-only** and provides:
- Guidelines for secure self-auditing
- API endpoint documentation
- Security best practices
- Certificate verification protocols

**This skill does NOT:**
- Install server components automatically
- Handle key storage
- Process data without consent
- Connect to endpoints without configuration

---

## 🔗 Additional Resources

- **Full Documentation:** https://agentshield.live/docs
- **API Reference:** https://github.com/bartelmost/agentshield/blob/main/AGENTSHIELD_API_DOCUMENTATION_v6.0.md
- **GitHub Repository:** https://github.com/bartelmost/agentshield
- **Privacy Policy:** https://agentshield.live/privacy

---

## 📝 Changelog

### v6.0.0 (2026-02-21)
- Added explicit human-in-the-loop requirements
- Enhanced privacy controls
- Granular consent for each security module
- Self-hosted deployment option
- Improved key management documentation

### v1.0.0 (2026-02-20)
- Initial release
- Basic audit functionality
- Ed25519 certificate issuance

---

## 📞 Support

- **Issues:** https://github.com/bartelmost/agentshield/issues
- **Email:** support@agentshield.io
- **Security:** security@agentshield.io

---

**Built with 🔒 privacy and 🛡️ security as core principles.**

*Your agent works for you—not the other way around.*
