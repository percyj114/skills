#!/usr/bin/env node
// Add an off-chain confirmation for a pending Safe tx.
import Safe from '@safe-global/protocol-kit';
import SafeApiKit from '@safe-global/api-kit';

import {
  addCommonOptions, cmd, requirePrivateKey,
  resolveTxServiceUrl, resolveChainId, resolveRpcUrl
} from './safe_lib.mjs';

const program = addCommonOptions(
  cmd('safe_tx_confirm', 'Add an off-chain confirmation for a Safe tx hash')
)
  .requiredOption('--safe <address>', 'Safe address')
  .requiredOption('--safe-tx-hash <hash>', 'Safe transaction hash')
  .parse();

const opts = program.opts();
const txServiceUrl = resolveTxServiceUrl(opts);
const chainId = resolveChainId(opts);
const pk = requirePrivateKey();

// protocol-kit needs a provider to talk to the chain (reads Safe state onchain)
// resolveRpcUrl uses --rpc-url, RPC_URL env, or derives from --chain
const provider = resolveRpcUrl(opts);

const safeSdk = await Safe.init({
  provider,
  signer: pk,
  safeAddress: opts.safe
});

const senderAddress = await safeSdk.getSafeProvider().getSignerAddress();

// Sign the tx hash
const sig = await safeSdk.signHash(opts.safeTxHash);

const apiKitConfig = { chainId, txServiceUrl };
if (opts.apiKey) apiKitConfig.apiKey = opts.apiKey;
const apiKit = new SafeApiKit(apiKitConfig);

await apiKit.confirmTransaction(opts.safeTxHash, sig.data);

process.stdout.write(JSON.stringify({
  ok: true,
  safe: opts.safe,
  safeTxHash: opts.safeTxHash,
  sender: senderAddress
}, null, 2) + '\n');
