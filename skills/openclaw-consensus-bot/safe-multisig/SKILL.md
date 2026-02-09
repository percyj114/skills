---
name: safe-multisig-skill
description: Propose, confirm, and execute Safe multisig transactions using the Safe Transaction Service API and Safe{Core} SDK (protocol-kit/api-kit). Use when an agent needs to operate a Safe smart account: (1) fetch Safe owners/threshold/nonce, (2) list queued/executed multisig txs, (3) build + propose a tx, (4) add confirmations, (5) execute a tx onchain, or (6) troubleshoot Safe nonce/signature/service-url issues across chains (Base/Ethereum/etc.).
---

# Safe Multisig Skill

This skill packages a small, reliable set of scripts for interacting with Safe multisig accounts via:
- **Safe Transaction Service** (read state, propose txs, submit confirmations)
- **Safe{Core} SDK** (create txs, compute hashes, sign, execute)

The scripts are designed to be used from the command line by an agent.

## Quick start

```bash
cd <this-skill>
./scripts/bootstrap.sh

# sanity check network + service
./scripts/safe_about.sh --chain base
```

## Common tasks

### 1) Get Safe info (owners / threshold / nonce)

```bash
node scripts/safe_info.mjs \
  --chain base \
  --safe 0xYourSafe
```

### 2) List multisig transactions (queued + executed)

```bash
node scripts/safe_txs_list.mjs \
  --chain base \
  --safe 0xYourSafe \
  --limit 10
```

### 3) Propose a new transaction

Create a tx request JSON (see `references/tx_request.schema.json` and `references/examples.md`).

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."   # never paste keys into chat logs

node scripts/safe_tx_propose.mjs \
  --chain base \
  --rpc-url "$BASE_RPC_URL" \
  --tx-file ./references/example.tx.json
```

### 4) Confirm a proposed transaction

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."

node scripts/safe_tx_confirm.mjs \
  --chain base \
  --safe 0xYourSafe \
  --safe-tx-hash 0x...
```

### 5) Execute a confirmed transaction (onchain)

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."

node scripts/safe_tx_execute.mjs \
  --chain base \
  --rpc-url "$BASE_RPC_URL" \
  --safe 0xYourSafe \
  --safe-tx-hash 0x...
```

## Configuration

All scripts accept either:
- `--chain <slug>` (recommended) where slug matches Safe’s tx-service slugs (e.g. `base`, `base-sepolia`, `mainnet`, `arbitrum`, `optimism`), OR
- explicit `--tx-service-url <url>`.

You can verify the correct per-chain base URL from Safe docs. Example for Base:
`https://api.safe.global/tx-service/base`.

## Security rules

- **Never paste private keys into chat.** Use env vars or files.
- Prefer low-privilege signers and spending limits when possible.
- Always verify:
  - Safe address
  - chainId / RPC
  - nonce (mismatch is the #1 cause of failures)

## References

- `references/examples.md` — example requests + workflows
- `references/tx_request.schema.json` — tx request JSON shape used by scripts
- `references/tx_service_slugs.md` — common chain slugs + notes
