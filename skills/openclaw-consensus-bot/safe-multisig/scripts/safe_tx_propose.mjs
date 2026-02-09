#!/usr/bin/env node
// Create + propose a Safe multisig tx via the Transaction Service.
// Uses @safe-global/protocol-kit (v6) + @safe-global/api-kit (v4).
import fs from 'node:fs';
import path from 'node:path';

import Safe from '@safe-global/protocol-kit';
import SafeApiKit from '@safe-global/api-kit';

import {
  addCommonOptions, cmd, fetchJson,
  requirePrivateKey, resolveTxServiceUrl, resolveChainId
} from './safe_lib.mjs';

const program = addCommonOptions(
  cmd('safe_tx_propose', 'Create + propose a Safe multisig tx via Transaction Service')
)
  .requiredOption('--tx-file <path>', 'Path to tx request JSON (see references/tx_request.schema.json)')
  .parse();

const opts = program.opts();
const txServiceUrl = resolveTxServiceUrl(opts);
const chainId = resolveChainId(opts);
const rpcUrl = opts.rpcUrl;
if (!rpcUrl) throw new Error('Missing --rpc-url (or RPC_URL env var)');

const pk = requirePrivateKey();

// Read tx request file
const txFilePath = path.resolve(process.cwd(), opts.txFile);
const req = JSON.parse(fs.readFileSync(txFilePath, 'utf8'));
if (!req.safe) throw new Error('tx-file missing required field: safe');
if (!Array.isArray(req.transactions) || req.transactions.length === 0)
  throw new Error('tx-file missing transactions[]');

// Init protocol-kit (v6 API: provider=rpcUrl, signer=privateKey)
const safeSdk = await Safe.init({
  provider: rpcUrl,
  signer: pk,
  safeAddress: req.safe
});

const senderAddress = await safeSdk.getSafeProvider().getSignerAddress();
if (!senderAddress) throw new Error('Could not derive signer address');

// If nonce not provided, fetch from service
let nonce = req.nonce;
if (nonce === undefined || nonce === null) {
  const safeInfo = await fetchJson(`${txServiceUrl}/v1/safes/${req.safe}/`);
  nonce = safeInfo.nonce;
}

const transactions = req.transactions.map(t => ({
  to: t.to,
  data: t.data || '0x',
  value: String(t.value ?? '0'),
  operation: t.operation ?? 0
}));

const safeTransaction = await safeSdk.createTransaction({ transactions, options: { nonce } });
const safeTxHash = await safeSdk.getTransactionHash(safeTransaction);

// Sign off-chain
const signedTx = await safeSdk.signTransaction(safeTransaction);

// Init api-kit (v4 API: chainId required, apiKey optional for self-hosted)
const apiKitConfig = { chainId, txServiceUrl };
if (opts.apiKey) apiKitConfig.apiKey = opts.apiKey;
const apiKit = new SafeApiKit(apiKitConfig);

await apiKit.proposeTransaction({
  safeAddress: req.safe,
  safeTransactionData: signedTx.data,
  safeTxHash,
  senderAddress,
  senderSignature: signedTx.encodedSignatures()
});

process.stdout.write(JSON.stringify({
  ok: true,
  safe: req.safe,
  safeTxHash,
  sender: senderAddress,
  nonce
}, null, 2) + '\n');
