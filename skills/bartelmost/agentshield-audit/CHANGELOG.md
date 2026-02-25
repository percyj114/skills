# Changelog

All notable changes to AgentShield Audit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-02-24

### Added - Critical Security Fixes & Cryptographic Verification

#### 1. Real Cryptographic Certificate Verification
- ✅ **Implemented Ed25519 signature verification** in `verify_peer.py`.
- ✅ Certificates are now cryptographically validated against AgentShield's public key (not just trusting the API).
- ✅ Added `verify_certificate_signature()` function using the `cryptography` library.
- ✅ Implemented canonical JSON serialization for signature consistency.

#### 2. Interactive Peer Challenge
- ✅ **Added manual challenge-response verification** in `verify_peer.py`.
- ✅ User can now input an agent's signature to prove ownership of the private key associated with a certificate.
- ✅ Uses Ed25519 verification to cross-check signatures against the certificate's public key.

#### 3. Privacy-First Consent Flow
- ✅ **Redesigned `initiate_audit.py` for explicit consent**.
- ✅ Identity files (`IDENTITY.md`, `SOUL.md`, etc.) are now only read *after* user approves the scan.
- ✅ Auto-detection now follows a strict hierarchy: Consent → Scan → Verification.
- ✅ Added "Manual Mode" fallback: if consent is denied, the script prompts for manual input instead of crashing or reading files anyway.

#### 4. Safe Sensitive Environment Access
- ✅ **Restricted environment variable reading**.
- ✅ `TELEGRAM_TOKEN`, `DISCORD_TOKEN`, etc. are now only accessed for platform detection if the user grants explicit permission.
- ✅ Removed silent auto-probing of sensitive tokens.

### Changed
- **Version bumped from 1.1.0 → 1.2.0** due to critical security and privacy improvements.
- Updated `initiate_audit.py` to be more interactive and transparent.
- Internal developer notes updated regarding backend infrastructure (Heroku development status).
- Improved CLI UX for audit initiation.

### Technical Details
- **Dependency Update:** `cryptography` is now strictly required for verification (not just key generation).
- **Crypto:** Ed25519 (RFC 8032) for all identity and certificate operations.
- **Serialization:** Canonical JSON (separators `(`,`:`) for deterministic signing.

### Security Note
"Backend runs currently on Heroku (Development), will be replaced by production server (Q2 2026)."

## [1.1.0] - 2025-02-24

### Added - Real Security Tests Implementation

#### New Security Tests
- ✅ **System Prompt Extraction Test** (`system_prompt_extraction.py`)
  - Tests 12 different prompt injection attack vectors
  - Detects if adversaries can extract system prompts
  - Attack vectors include: direct override, repetition attacks, translation tricks, Unicode injection, developer mode exploitation
  - Realistic scoring: 100 (perfect) to 0 (full leakage)
  - Pattern-based detection with confidence scoring
  
- ✅ **Instruction Override Test** (`instruction_override.py`)
  - Tests 14 different instruction override attack vectors
  - Detects if adversaries can hijack agent behavior or goals
  - Attack vectors include: DAN jailbreaks, role hijacking, goal manipulation, privilege escalation, Base64 obfuscation, multi-language attacks, token injection
  - Realistic scoring: 100 (all blocked) to 0 (easily overridable)
  - Comprehensive behavioral analysis

#### Test Integration
- ✅ Updated `initiate_audit.py` to use real tests instead of placeholders
- ✅ Replaced placeholder scores with actual test execution
- ✅ Added proper error handling for test failures
- ✅ Updated imports in `__init__.py` to export new test functions

#### Security Improvements
- Real threat simulations instead of hardcoded pass/fail
- Pattern-based detection algorithms
- Severity-weighted scoring
- Actionable security recommendations based on findings
- Support for CLI testing of individual modules

### Changed
- **Version bumped from 1.0.0 → 1.1.0**
- Test suite now includes 3 real tests (Secret Leakage, System Prompt Extraction, Instruction Override)
- 2 placeholder tests remain (Tool Permission Check, Memory Isolation) for future implementation

### Technical Details
- **New modules:** `system_prompt_extraction.py`, `instruction_override.py`
- **Total attack vectors tested:** 26 (12 prompt extraction + 14 instruction override)
- **Pattern matching:** 13 leakage patterns + 12 override indicators
- **Python compatibility:** Maintained 3.8+
- **No new dependencies:** Uses standard library only

### Testing
```bash
# Test individual modules
python3 -m agentshield_security.system_prompt_extraction
python3 -m agentshield_security.instruction_override

# Full audit with real tests
python scripts/initiate_audit.py --auto
```

### Security Research
These tests are based on real-world AI security research:
- OWASP Top 10 for LLM Applications
- Prompt injection research (Riley Goodside, Simon Willison)
- Jailbreak taxonomy (Anthropic, OpenAI red teaming)
- Unicode steganography attacks
- Multi-language prompt injection vectors

---

## [1.0.0] - 2025-02-24

### Added - ClawHub Compliance Release

#### Core Bundle Structure
- ✅ Created `clawhub.json` manifest with full ClawHub compliance
  - Installation method: "bundle" (no git clone required)
  - Complete privacy & security documentation
  - Platform compatibility declarations
  - Proper dependency specification
  
- ✅ Created comprehensive `README.md`
  - Installation instructions
  - Usage examples
  - Privacy & security model explanation
  - Troubleshooting guide
  - Development setup
  
- ✅ Created `setup.py` for pip installation
  - Console script entry points (`agentshield-audit`, `agentshield-verify`, `agentshield-cert`)
  - Proper package discovery
  - Metadata for PyPI compatibility
  
- ✅ Created `MANIFEST.in` for bundle packaging
  - Includes all necessary files
  - Excludes build artifacts and cache files
  
- ✅ Added `LICENSE` file (MIT)

- ✅ Added `scripts/__init__.py` to make scripts importable as a package

- ✅ Added `.gitignore` for development cleanliness

#### Documentation Improvements
- Enhanced `SKILL.md` with ClawHub-compliant frontmatter
- Existing `QUICKSTART.md` verified for compatibility
- API documentation in `references/api.md` preserved

#### Security & Privacy
- **No hardcoded API keys** - All authentication uses locally-generated Ed25519 keypairs
- **Private keys stay local** - Never transmitted to AgentShield API
- **Clear data handling** - Documented what gets stored locally vs. sent to API
- **Human-in-the-loop** - Audit initiation requires explicit user action
- **Rate limiting** - 1 audit/hour enforced server-side to prevent abuse

#### Installation Experience
Users can now:
```bash
clawhub install agentshield-audit
cd ~/.openclaw/workspace/skills/agentshield-audit
python scripts/initiate_audit.py --auto
```

Or via pip (future):
```bash
pip install agentshield-audit
agentshield-audit --auto
```

### Changed
- Reorganized bundle structure for ClawHub compliance
- Updated documentation to emphasize zero-config auto-detection

### Technical Details
- **Bundle size:** 49KB (compressed)
- **Python compatibility:** 3.8+
- **Dependencies:** cryptography>=41.0.0, requests>=2.31.0
- **Platforms supported:** Discord, Telegram, Slack, Signal, WhatsApp, CLI

### Bundle Contents
```
agentshield-audit-v1.0.0-clawhub.tar.gz
└── agentshield-audit/
    ├── clawhub.json
    ├── setup.py
    ├── MANIFEST.in
    ├── LICENSE
    ├── README.md
    ├── SKILL.md
    ├── QUICKSTART.md
    ├── CHANGELOG.md
    ├── .gitignore
    ├── sandbox_config.yaml
    ├── scripts/
    │   ├── __init__.py
    │   ├── requirements.txt
    │   ├── initiate_audit.py
    │   ├── verify_peer.py
    │   ├── show_certificate.py
    │   └── audit_client.py
    ├── src/
    │   └── agentshield_security/
    │       ├── __init__.py
    │       ├── input_sanitizer.py
    │       ├── output_dlp.py
    │       ├── tool_sandbox.py
    │       ├── echoleak_test.py
    │       ├── secret_scanner.py
    │       └── supply_chain_scanner.py
    ├── references/
    │   └── api.md
    ├── docs/
    │   ├── BACKEND_CERTIFICATE_STORE.md
    │   └── RATE_LIMITING.md
    └── tests/
        ├── test_security_modules.py
        ├── test_input_sanitizer.py
        └── test_quick.py
```

### Verification
- ✅ JSON schema validated (`clawhub.json`)
- ✅ Bundle structure verified
- ✅ Dependencies specified correctly
- ✅ Privacy/security requirements documented
- ✅ Installation experience tested conceptually

### Next Steps (Future Releases)
- [ ] Submit to official ClawHub registry
- [ ] Add automated integration tests
- [ ] Create video tutorial
- [ ] Add more security test modules
- [ ] Support for custom audit profiles

---

## [0.9.0] - Pre-ClawHub Release

Initial development version with:
- Security audit framework
- Ed25519 cryptographic identity
- Certificate signing via AgentShield API
- Auto-detection capabilities
- Peer verification

---

**Made with 🔐 by the AgentShield team**
