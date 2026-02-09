#!/usr/bin/env node
// Execute a Safe tx onchain (requires enough confirmations already collected).
import Safe from '@safe-global/protocol-kit';
import SafeApiKit from '@safe-global/api-kit';

import {
  addCommonOptions, cmd, requirePrivateKey,
  resolveTxServiceUrl, resolveChainId
} from './safe_lib.mjs';

const program = addCommonOptions(
  cmd('safe_tx_execute', 'Execute a Safe tx onchain (requires enough confirmations)')
)
  .requiredOption('--safe <address>', 'Safe address')
  .requiredOption('--safe-tx-hash <hash>', 'Safe transaction hash')
  .parse();

const opts = program.opts();
const txServiceUrl = resolveTxServiceUrl(opts);
const chainId = resolveChainId(opts);
const rpcUrl = opts.rpcUrl;
if (!rpcUrl) throw new Error('Missing --rpc-url (or RPC_URL env var)');

const pk = requirePrivateKey();

const safeSdk = await Safe.init({
  provider: rpcUrl,
  signer: pk,
  safeAddress: opts.safe
});

const senderAddress = await safeSdk.getSafeProvider().getSignerAddress();

// Fetch the tx + its confirmations from the service
const apiKitConfig = { chainId, txServiceUrl };
if (opts.apiKey) apiKitConfig.apiKey = opts.apiKey;
const apiKit = new SafeApiKit(apiKitConfig);

const tx = await apiKit.getTransaction(opts.safeTxHash);

// Rebuild the Safe transaction from the service data
const safeTransaction = await safeSdk.createTransaction({
  transactions: [{
    to: tx.to,
    data: tx.data ?? '0x',
    value: String(tx.value ?? '0'),
    operation: tx.operation ?? 0
  }],
  options: {
    nonce: tx.nonce,
    safeTxGas: String(tx.safeTxGas ?? '0'),
    baseGas: String(tx.baseGas ?? '0'),
    gasPrice: String(tx.gasPrice ?? '0'),
    gasToken: tx.gasToken || '0x0000000000000000000000000000000000000000',
    refundReceiver: tx.refundReceiver || '0x0000000000000000000000000000000000000000'
  }
});

// Attach existing confirmations
for (const c of tx.confirmations ?? []) {
  if (c.signature) {
    safeTransaction.addSignature({
      signer: c.owner,
      data: c.signature,
      isContractSignature: false,
      staticPart: () => c.signature,
      dynamicPart: () => ''
    });
  }
}

const execResponse = await safeSdk.executeTransaction(safeTransaction);
const receipt = await execResponse.transactionResponse?.wait?.();

process.stdout.write(JSON.stringify({
  ok: true,
  safe: opts.safe,
  safeTxHash: opts.safeTxHash,
  executor: senderAddress,
  txHash: receipt?.hash || execResponse.hash
}, null, 2) + '\n');
