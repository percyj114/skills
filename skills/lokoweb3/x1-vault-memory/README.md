# 🦞 X1 Vault Memory

**Decentralized, encrypted memory backup for OpenClaw AI agents — powered by X1 blockchain and IPFS.**

---

## What Is This?

An OpenClaw skill that backs up your AI agent's identity and memory files to IPFS with encrypted storage and on-chain CID references on the X1 blockchain.

Your agent's brain — personality, knowledge, memories — encrypted with your wallet key, stored on decentralized infrastructure, and recoverable from anywhere.

**No more losing your agent when a server dies.**

---

## How It Works
```
Agent Files → tar.gz → Encrypt (AES-256-GCM) → Upload (IPFS/Pinata) → Record CID (X1 Blockchain)
```

1. **Bundle** — Compresses agent files (IDENTITY.md, SOUL.md, USER.md, TOOLS.md, memory/) into a tar.gz
2. **Encrypt** — Encrypts the archive with your wallet's secret key using AES-256-GCM
3. **Upload** — Pushes the encrypted blob to IPFS via Pinata's API
4. **Record** — Stores the IPFS CID on the X1 blockchain via Memo Program
5. **Track** — Logs the CID and timestamp to vault-log.json

Only your wallet keypair can decrypt. Even if someone finds the CID, your data stays private.

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **Node.js** | v18+ |
| **Pinata Account** | Free at [app.pinata.cloud](https://app.pinata.cloud) |
| **Solana/X1 Wallet** | Keypair JSON file |
| **X1 Tokens** | Mainnet XN for transaction fees |
| **OpenClaw** | Running instance with workspace access |

---

## Installation

### For OpenClaw Agents

1. Clone into your OpenClaw workspace:
``````````bash
cd /home/node/.openclaw/workspace
git clone https://github.com/Lokoweb3/x1-vault-memory.git
cd x1-vault-memory
npm install
`````````

2. Add environment variables to your docker-compose.yml:
````````yaml
environment:
  PINATA_JWT: ${PINATA_JWT}
  X1_RPC_URL: https://rpc.mainnet.x1.xyz
```````

3. Add PINATA_JWT to your .env file:
``````bash
echo "PINATA_JWT=your_token_here" >> ~/openclaw/.env
`````

4. Restart the container:
````bash
cd ~/openclaw
docker compose down && docker compose up -d
```

5. Tell your agent about the skill:
> "You have a new skill called x1-vault-memory. You can backup your memory with node x1-vault-memory/src/backup.js and restore with node x1-vault-memory/src/restore.js CID. Save this to your memory."

---

## Setup

### 0. Configure for X1 Mainnet

X1 is SVM-compatible, so it uses Solana CLI tools. Set your CLI to X1 mainnet:

````bash
# Install Solana CLI if you dont have it
# Note: release.anza.xyz is the official Anza/Solana installer
# See https://docs.anza.xyz/cli/install for details
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"

# Set to X1 mainnet
solana config set --url https://rpc.mainnet.x1.xyz
```


### 1. Set Environment Variables
```bash
export PINATA_JWT="your_pinata_jwt_here"
export X1_RPC_URL="https://rpc.mainnet.x1.xyz"
```

### 2. Create a Wallet Keypair
```bash
solana-keygen new --outfile x1_vault_cli/wallet.json --no-bip39-passphrase

# View your wallet address
solana address --keypair x1_vault_cli/wallet.json

# Check your balance
solana balance --keypair x1_vault_cli/wallet.json --url https://rpc.mainnet.x1.xyz
```

> ⚠️ **Keep wallet.json safe. Never commit it to GitHub. This is your encryption key.**

### 3. Fund Your Wallet

**Mainnet:** Transfer XN tokens to your wallet address from an exchange or existing wallet.

---

## Usage

### Backup
```bash
node x1-vault-memory/src/backup.js
```

Output:
```
Archive checksum: a1b2c3d4e5f6...
Backup uploaded, CID: QmExampleCID123456789abcdefghijklmnopqrstuv
X1 Transaction: 5h1XWikXsqVoDEnK54DbG5Jurxnwqf5puVD5FL28JByCBhatCk7X2mnMCyipLvYmsNDjdrvvmDtQZpPRZuwWqccV
Explorer: https://explorer.mainnet.x1.xyz/tx/...
Logged backup CID to vault-log.json
```

**Features:**
- ✅ SHA-256 checksum generated before encryption
- ✅ Checksum stored in encrypted payload for integrity verification
- ✅ CID anchored to X1 blockchain with transaction hash

### Restore
```bash
# Full restore
node x1-vault-memory/src/restore.js <CID>

# Selective restore (only memory folder)
node x1-vault-memory/src/restore.js <CID> --only memory/
```

**Features:**
- ✅ Automatic integrity verification (checksum must match)
- ✅ Aborts with error if archive is corrupted
- ✅ Selective restore — restore specific paths without overwriting identity files

### List Backups
```bash
node x1-vault-memory/src/list.js
```

Shows numbered list of all backups with timestamps and anchor status.

### Heartbeat Check
```bash
node x1-vault-memory/src/heartbeat.js
```

Self-healing check:
- Verifies SOUL.md and memory/ exist and aren't empty
- Auto-restores from latest backup if issues detected
- Run this on agent startup for self-healing memory

### Shell Wrappers
```bash
bash x1-vault-memory/scripts/backup.sh
bash x1-vault-memory/scripts/restore.sh <CID>
```

---

## CID Tracking

Every backup is logged to vault-log.json:
```json
[
  {
    "timestamp": "2026-02-16T09:48:38.207Z",
    "cid": "QmExampleCID123456789abcdefghijklmnopqrstuv"
  }
]
```

CIDs are also recorded on-chain. Check your wallet's transaction history on the [X1 Explorer](https://explorer.mainnet.x1.xyz).

---

## Automation
```bash
# Cron job - daily at 2am
0 2 * * * cd /path/to/workspace && node x1-vault-memory/src/backup.js >> /var/log/vault-backup.log 2>&1
```

---

## Files Backed Up

| File | Purpose |
|------|---------|
| IDENTITY.md | Agent name, persona, vibe |
| SOUL.md | Personality, instructions, expertise |
| USER.md | User profile and preferences |
| TOOLS.md | Environment-specific notes |
| memory/*.md | Daily memory logs |

---

## Security

- 🔐 Encrypted with AES-256-GCM using your wallet's secret key
- 🔑 Only your keypair can decrypt
- 📡 Stored on IPFS, not a single server
- ⛓️ CID recorded on X1 blockchain via Memo Program for permanence
- 🚫 Never share your wallet.json or PINATA_JWT

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Encryption | AES-256-GCM |
| IPFS Storage | Pinata API (JWT auth) |
| Blockchain | X1 (SVM-compatible L1) |
| Runtime | Node.js |
| Archiving | tar (npm) |

---

## About X1

[X1](https://x1.xyz) is a high-performance, SVM-compatible Layer-1 blockchain.

- **Docs:** [docs.x1.xyz](https://docs.x1.xyz)
- **Explorer:** [explorer.mainnet.x1.xyz](https://explorer.mainnet.x1.xyz)
- **Testnet RPC:** https://rpc.testnet.x1.xyz
- **Mainnet RPC:** https://rpc.mainnet.x1.xyz

---

## License

MIT

---

**Built by [Lokoweb3](https://github.com/Lokoweb3) with Loko_AI 🦞**
