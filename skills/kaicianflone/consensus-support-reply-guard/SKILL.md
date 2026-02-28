---
name: consensus-support-reply-guard
description: Risk-aware support response governance with persona-weighted consensus. Detects legal/sensitive/confidentiality issues, applies hard-block policy checks, and writes auditable decision artifacts for customer-facing automation.
homepage: https://github.com/kaicianflone/consensus-support-reply-guard
source: https://github.com/kaicianflone/consensus-support-reply-guard
metadata:
  {"openclaw": {"requires": {"bins": ["node", "tsx"], "env": ["OPENAI_API_KEY"]}}}
---

# consensus-support-reply-guard

`consensus-support-reply-guard` is a customer-trust guard for support workflows.

## What this skill does

- evaluates support drafts before sending
- detects high-risk claim patterns
- blocks or rewrites responses when policy violations appear
- updates persona reputations based on final decision alignment
- preserves decision history in board artifacts

## Why this matters

Support replies are high-frequency and brand-critical. This skill prevents overconfident legal/PII mistakes at scale.

## Ecosystem role

Composes with persona generation + consensus board state so support quality improves through persistent decision memory.

## Ideal scenarios

- automated ticket triage replies
- L1/L2 AI response review gates
- regulated or enterprise support channels


## Runtime, credentials, and network behavior

## Credential declaration (registry + runtime)

- declared env: `OPENAI_API_KEY`
- requirement is **conditional**: only needed when persona generation is configured to use an OpenAI-backed LLM provider
- no API key is required when you pass an existing `persona_set_id` and skip generation


- runtime binaries: `node`, `tsx`
- network calls: none in the guard decision path itself
- conditional network behavior: if a run needs persona generation and your persona-generator backend uses an external LLM, that backend may perform outbound API calls
- credentials: `OPENAI_API_KEY` (or equivalent provider key) may be required **only** for persona generation in LLM-backed setups; if `persona_set_id` is provided, guards can run without LLM credentials
- filesystem writes: board/state artifacts under the configured consensus state path

## Dependency trust model

- `consensus-guard-core` and `consensus-persona-generator` are first-party consensus packages
- versions are semver-pinned in `package.json` for reproducible installs
- this skill does not request host-wide privileges and does not mutate other skills

## Quick start

```bash
node --import tsx run.js --input ./examples/input.json
```

## Tool-call integration

This skill is wired to the consensus-interact contract boundary (via shared consensus-guard-core wrappers where applicable):
- readBoardPolicy
- getLatestPersonaSet / getPersonaSet
- writeArtifact / writeDecision
- idempotent decision lookup

This keeps board orchestration standardized across skills.

## Invoke Contract

This skill exposes a canonical entrypoint:

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` starts the guard flow, which then executes persona evaluation and consensus-interact-contract board operations (via shared guard-core wrappers where applicable).

## external_agent mode

Guards support two modes:
- `mode="persona"` (default): guard loads/generates persona_set and runs internal persona voting.
- `mode="external_agent"`: caller supplies `external_votes[]` from real agents; guard performs deterministic aggregation, policy checks, and board decision writes without requiring persona harness.
