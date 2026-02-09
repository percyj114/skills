# safe-multisig-skill

Operate a Safe multisig smart account from the CLI:
- read Safe state (owners/threshold/nonce)
- list queued/executed multisig transactions
- propose transactions (off-chain signatures via Transaction Service)
- add confirmations
- execute transactions onchain

## Requirements

- Node.js 18+ (this machine: Node 22)
- Internet access to the Safe Transaction Service endpoint for your chain
- For propose/confirm/execute: a signer private key for an **owner** of the Safe

## Install

```bash
./scripts/bootstrap.sh
```

## Smoke test

```bash
bash tests/smoke.sh
```

## Usage

### Check tx service connectivity

```bash
./scripts/safe_about.sh --chain base
# or
./scripts/safe_about.sh --tx-service-url https://api.safe.global/tx-service/base
```

### Get Safe info

```bash
node scripts/safe_info.mjs --chain base --safe 0xYourSafe
```

### List multisig txs

```bash
node scripts/safe_txs_list.mjs --chain base --safe 0xYourSafe --limit 20
```

### Propose tx (single-call)

1) Create a tx file based on `references/example.tx.json`
2) Propose:

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."
export BASE_RPC_URL="https://mainnet.base.org"

node scripts/safe_tx_propose.mjs \
  --chain base \
  --rpc-url "$BASE_RPC_URL" \
  --tx-file references/example.tx.json
```

### Confirm tx

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."

node scripts/safe_tx_confirm.mjs \
  --chain base \
  --safe 0xYourSafe \
  --safe-tx-hash 0x...
```

### Execute tx

```bash
export SAFE_SIGNER_PRIVATE_KEY="..."

node scripts/safe_tx_execute.mjs \
  --chain base \
  --rpc-url "$BASE_RPC_URL" \
  --safe 0xYourSafe \
  --safe-tx-hash 0x...
```

## Notes

- The Safe Transaction Service uses per-chain base URLs like:
  - Base: `https://api.safe.global/tx-service/base`
  - Base Sepolia: `https://api.safe.global/tx-service/base-sepolia`

See `references/tx_service_slugs.md`.
