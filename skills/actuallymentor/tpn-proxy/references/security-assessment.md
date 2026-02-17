# Security Assessment: tpn-proxy Skill

This document addresses potential security concerns identified in the tpn-proxy skill and explains the mitigations in place.

---

## 1. Shell Command Construction with User Input

**Concern:** The skill instructs an AI agent to construct shell commands (e.g. `curl`) using values derived from user input — specifically `geo` (country code), `minutes` (duration), `connection_type`, and target URLs. Without validation, a malicious input like `DE"; rm -rf / #` could escape the intended JSON payload and execute arbitrary commands.

**Mitigation:** The skill enforces mandatory input validation before any shell command is constructed:

- `geo` — must match exactly 2 uppercase ASCII letters (ISO 3166-1 alpha-2)
- `minutes` — must be a positive integer between 1 and 1440
- `connection_type` — must be one of the enum values `any`, `datacenter`, `residential`
- `format` — must be one of `text` or `json`

The skill explicitly prohibits string concatenation of raw user input into JSON payloads or shell commands. Only validated, type-checked values may be inserted into static single-quoted command templates.

---

## 2. Arbitrary URL Fetching via Proxy (SSRF)

**Concern:** The skill can fetch user-specified URLs through a SOCKS5 proxy, which could be abused for Server-Side Request Forgery (SSRF) — probing internal networks, accessing metadata endpoints, or scanning private infrastructure.

**Mitigation:** The skill uses an **allowlist model** — every check must pass before a URL is fetched:

1. Scheme must be `http://` or `https://`
2. No shell metacharacters allowed
3. Raw IP addresses rejected — domain names only
4. Internal hostname patterns rejected (`*.internal`, `*.local`, `*.localhost`, `*.localdomain`, `*.corp`, `*.lan`, `metadata.*`, single-label hostnames)
5. Hostname must resolve via local DNS — **unresolvable hostnames are rejected** (they may only exist in the proxy's internal DNS, bypassing SSRF protections)
6. Resolved IP must be publicly routable — private ranges (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1`, `fd00::/8`) and cloud metadata addresses are rejected

The skill prefers the agent's built-in HTTP tools (e.g. `WebFetch`) over `curl`, avoiding shell command construction entirely. When `curl` is used, all URL and proxy URI arguments must be double-quoted.

**Dual-scheme approach:** The skill uses two SOCKS5 schemes depending on context. For agent-side fetching (Step 5), it uses `socks5://` — DNS resolves locally, so the IP validated by checks 5–6 is the IP the proxy connects to. This eliminates the DNS rebinding vector entirely. For user-facing credentials (Step 4), it uses `socks5h://` to preserve user DNS privacy.

**SOCKS5 DNS (eliminated for agent-side fetching):** Because the agent uses `socks5://`, local DNS resolution is authoritative — there is no proxy-side DNS gap to exploit. The resolved IP is the connected IP. User-facing credentials continue using `socks5h://` for DNS privacy, where the proxy-side DNS trade-off is acceptable (the user controls the target URL).

---

## 3. JSON Parsing Fallback Chain

**Concern:** Earlier versions of the skill suggested using `python3 -c` with inline code and `grep | cut` pipelines as fallbacks for parsing JSON responses. These patterns create additional attack surface if any part of the parsed data is attacker-controlled.

**Mitigation:** The fallback chain has been removed entirely. The skill now supports only two parsing approaches:

1. `jq` — a dedicated JSON processor with no shell evaluation risk
2. `format=text` — returns a plain URI string that requires no parsing at all

The skill explicitly prohibits `python -c`, `grep`, `cut`, and other shell-based JSON parsing.

---

## 4. Cryptographic Material (x402)

**Concern:** The x402 payment flow requires cryptographic signing of USDC transactions on Base.

**Mitigation:** This skill does not access, store, or manage any signing keys or cryptographic material. Its role is limited to:

- Providing the x402 endpoint URL (`/api/v1/x402/proxy/generate`)
- Documenting the request/response format
- Referencing external libraries (`@x402/core`, `@x402/evm`) that handle signing

The code examples in `x402-examples.md` use only browser-based signing (`window.ethereum` / MetaMask popup) and references to external npm packages. No environment variable access patterns for signing credentials appear in any skill file.

---

## 5. API Key Handling

**Concern:** The skill reads `$TPN_API_KEY` from the environment to authenticate with the TPN API.

**Mitigation:** This follows standard practice for API key management:

- The key is read from an environment variable, never hardcoded
- The key's existence is checked via `[ -n "$TPN_API_KEY" ]` — never echoed, logged, or displayed
- It is passed via the `X-API-Key` HTTP header over HTTPS — not exposed in URLs or logs
- The key is injected by the agent runtime (OpenClaw config), not by the skill itself
- The skill never logs, displays, or transmits the API key beyond the authenticated API call

---

## 6. Proxy Credential Exposure

**Concern:** The skill displays proxy credentials (username, password, host, port) in the agent's response.

**Mitigation:** These credentials are:

- **Short-lived** — scoped to the lease duration (1–1440 minutes), then automatically invalidated
- **Single-purpose** — valid only for SOCKS5 proxy connections to the assigned exit node
- **Non-reusable** — each proxy generation creates a fresh credential set
- **Not linked to the user's API key** — compromising a proxy credential does not expose the user's TPN account

Displaying them is intentional and necessary for the skill's purpose.

---

## 7. Runtime-Dependent Protections

**Concern:** The SSRF allowlist (DNS resolution, IP-range checks) and input validation are procedural requirements that the agent must implement at runtime. Because this is a declarative skill (markdown instructions, not executable code), the protections are not enforced by code — they depend on the agent following the instructions correctly.

**Mitigation:** This is an inherent architectural property of declarative skills. The following measures reduce the risk of agent non-compliance:

- **Validation rules are explicit and enumerated** — not vague guidelines but specific regex patterns, enum values, and CIDR ranges that leave no room for interpretation
- **The dual-scheme approach (`socks5://` vs `socks5h://`) is structurally enforced** — the skill uses different schemes in different contexts (Step 4 vs Step 5), making it harder for the agent to accidentally use the wrong one
- **The allowlist model is fail-closed** — the instructions say "every check must pass; reject the URL if any check fails," so an agent that skips a check will still block on the remaining checks
- **Reference examples model correct behavior** — all code examples in the skill and its reference files demonstrate the validated patterns, giving the agent concrete templates to follow rather than abstract rules

**Residual risk:** An agent that ignores or misinterprets the instructions could bypass SSRF protections. This risk is shared by all declarative agent skills and is best addressed at the agent framework level (e.g. runtime URL validation middleware). The skill's layered checks (scheme, hostname pattern, DNS resolution, IP range) provide defense-in-depth even if one layer is imperfectly implemented.

---

## Summary

| Concern | Risk Level | Status |
|---------|-----------|--------|
| Shell injection via user input | Mitigated | Mandatory input validation, no raw interpolation |
| SSRF via arbitrary URL fetching | Eliminated | Allowlist model + dual-scheme: `socks5://` for agent fetching makes local DNS authoritative, eliminating proxy-side DNS rebinding; `socks5h://` for user-facing DNS privacy |
| Unsafe JSON parsing fallbacks | Eliminated | Removed; jq or format=text only — all reference examples also comply |
| Cryptographic material (x402) | Not applicable | Skill provides endpoint URLs only; signing handled by external libraries |
| API key handling | Standard practice | Environment variable, existence-checked only (never echoed), HTTPS header |
| Proxy credential exposure | By design | Short-lived, single-purpose, non-reusable |
| Runtime-dependent protections | Acknowledged | Explicit validation rules, fail-closed allowlist, defense-in-depth; residual risk shared by all declarative skills |
