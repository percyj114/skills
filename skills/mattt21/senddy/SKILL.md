---
name: senddy
description: Create and manage private stablecoin wallets using Senddy's zero-knowledge protocol on Base. Use when building payment agents, bots, server-side apps, or any system that needs private USDC transfers. Covers @senddy/node for headless agents and @senddy/client for browser apps.
metadata: {"openclaw":{"requires":{"env":["SENDDY_API_KEY"]},"primaryEnv":"SENDDY_API_KEY","emoji":"🛡️","homepage":"https://www.senddy.com"}}
---

# Senddy Private Wallet

Build private stablecoin wallets with zero-knowledge proofs on Base.
Senddy lets agents and apps hold, transfer, and withdraw USDC privately —
no public on-chain linkage between deposits, transfers, and withdrawals.

## Quick Start (Headless Agent)

**5 steps to a working private wallet:**

```bash
npm install @senddy/node
```

```typescript
import { createSenddyAgent, toUSDC } from '@senddy/node';
import { randomBytes } from 'node:crypto';

// 1. Generate a seed (store this securely — it controls the wallet)
const seed = randomBytes(32);

// 2. Create the agent (only seed + apiKey required)
const agent = createSenddyAgent({
  seed,
  apiKey: process.env.SENDDY_API_KEY!,
});

// 3. Initialize (derives keys, loads WASM prover, first sync)
await agent.init();

// 4. Get your receive address
console.log('Address:', agent.getReceiveAddress()); // senddy1...

// 5. Check balance, transfer, withdraw
const balance = await agent.getBalance();
await agent.transfer('senddy1...recipient', toUSDC('5.00'));
await agent.withdraw('0xPublicAddress...', toUSDC('10.00'));
```

Set `SENDDY_API_KEY` in your environment. Get one at https://senddy.com.

## Configuration

### Minimal Config (recommended)

Only `seed` and `apiKey` are required. Everything else defaults to the
canonical Base mainnet deployment:

```typescript
createSenddyAgent({
  seed: Uint8Array,        // 32-byte secret (REQUIRED)
  apiKey: string,          // 'sk_live_...' (REQUIRED)
})
```

### Full Config (overrides)

```typescript
createSenddyAgent({
  seed: Uint8Array,
  apiKey: string,
  apiUrl: string,          // default: 'https://senddy.com/api/v1'
  chainId: number,         // default: 8453 (Base)
  rpcUrl: string,          // default: 'https://mainnet.base.org'
  pool: '0x...',           // default: canonical pool
  usdc: '0x...',           // default: canonical USDC
  permit2: '0x...',        // default: canonical Permit2
  subgraphUrl: string,     // default: canonical subgraph
  attestorUrl: string,     // override: bypass API gateway for attestor
  relayerUrl: string,      // override: bypass API gateway for relayer
  context: string,         // default: 'main' (for multi-agent from one seed)
  debug: boolean,          // default: false
})
```

### What the API Key Gates

The `apiKey` authenticates all requests through the Senddy API gateway:
- **Attestor** — ZK proof verification (TEE-based, off-chain)
- **Relayer** — Gas-sponsored transaction submission (you don't pay gas)
- **Usernames** — Resolve `senddy1...` addresses to human-readable names
- **Merkle tree** — Proof generation helper endpoints

## Operations

### Balance

```typescript
const balance = await agent.getBalance();
// { shares: bigint, estimatedUSDC: bigint, noteCount: number }
```

`estimatedUSDC` is in 6-decimal USDC units. `shares` are 18-decimal internal units.

### Transfer

```typescript
// Simple transfer
const result = await agent.transfer('senddy1...', toUSDC('25.00'));
// { txHash, shares, nullifierCount, circuit: 'spend' | 'spend9' }

// With memo (max 31 ASCII chars)
await agent.transfer('senddy1...', toUSDC('5.00'), { memo: 'Payment' });

// Anonymous (hide sender identity)
await agent.transfer('senddy1...', toUSDC('5.00'), { anonymous: true });
```

Auto-escalation: tries `spend` circuit (3 inputs), escalates to `spend9`
(9 inputs), and auto-consolidates if neither suffices.

### Withdraw

Withdraw to a public Ethereum address (USDC leaves the privacy pool):

```typescript
const result = await agent.withdraw('0x...', toUSDC('50.00'));
// { txHash, shares, to, circuit }
```

### Sync

State is synced automatically on `init()`. For long-running agents:

```typescript
// Manual sync
const result = await agent.sync();
// { newNotes, newSpent, unspentCount, durationMs }
```

### Consolidation

When notes fragment (many small UTXOs), consolidate them:

```typescript
const result = await agent.consolidate({ noteThreshold: 16 });
// { txHash, notesConsolidated, totalShares, needsMore }
```

### Receive Address

```typescript
const address = agent.getReceiveAddress(); // 'senddy1qw508d6q...'
```

Share this address to receive private transfers. It's derived from
your viewing public key and is deterministic for a given seed + context.

### Transaction History

```typescript
const txs = await agent.getTransactions({ limit: 50 });
// Array<{ id, type, shares, estimatedUSDC, counterparty, memo, timestamp, status }>
```

### Events

```typescript
agent.on('balanceChange', (balance) => { /* ... */ });
agent.on('sync', (result) => { /* ... */ });
agent.on('noteStrategy', (event) => { /* escalation/consolidation info */ });
agent.on('error', (err) => { /* ... */ });
```

## Multiple Agents from One Seed

Use the `context` parameter to derive different wallets from the same seed:

```typescript
const treasury = createSenddyAgent({ seed, apiKey, context: 'treasury' });
const payroll  = createSenddyAgent({ seed, apiKey, context: 'payroll' });
const tips     = createSenddyAgent({ seed, apiKey, context: 'tips' });
```

Each context produces different keys and a different receive address.

## Amounts

Always use `toUSDC()` to convert human-readable amounts:

```typescript
import { toUSDC } from '@senddy/node';

toUSDC('1.00')     // 1_000_000n
toUSDC('100')      // 100_000_000n
toUSDC('0.01')     // 10_000n
toUSDC(50)         // 50_000_000n
```

Raw amounts are in USDC's 6-decimal format (`bigint`).

## Address Validation

```typescript
import { isValidSenddyAddress } from '@senddy/node';

isValidSenddyAddress('senddy1qw508d6q...');  // true
isValidSenddyAddress('0x...');                // false
```

## Contract Addresses

```typescript
import { SHARED_CONTRACTS, V3_CONTRACTS } from '@senddy/node';

SHARED_CONTRACTS.USDC     // '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
SHARED_CONTRACTS.Permit2  // '0x000000000022D473030F116dDEE9F6B43aC78BA3'
V3_CONTRACTS.Pool         // '0x0b4e0C18e4005363A10a93cb30e0a11A88bee648'
```

## Cleanup

```typescript
agent.destroy(); // Zeros key material and cleans up resources
```

Always call `destroy()` when done (especially in short-lived processes).

## Gotchas

- **No deposits**: Agents can't deposit directly. Fund them by sending a
  private transfer from a funded wallet (browser app or another agent).
- **In-memory storage**: Notes are lost on process restart. The agent re-syncs
  from the subgraph on `init()`, so this is safe — just costs a few seconds.
- **First init downloads SRS**: The first `init()` downloads a ~16 MB
  structured reference string (cached for subsequent runs in Node.js).
- **Shares vs USDC**: Internal values are in 18-decimal shares. Use
  `balance.estimatedUSDC` and `toUSDC()` for human-readable amounts.

## Additional Resources

- For full type signatures and advanced composition, see [reference.md](reference.md)
- For copy-paste usage examples, see [examples.md](examples.md)