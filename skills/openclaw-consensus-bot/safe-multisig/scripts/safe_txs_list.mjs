#!/usr/bin/env node
// List multisig transactions for a Safe. Uses plain HTTP — no SDK needed.
import { addCommonOptions, cmd, fetchJson, resolveTxServiceUrl } from './safe_lib.mjs';

const program = addCommonOptions(
  cmd('safe_txs_list', 'List multisig transactions for a Safe (queued + executed)')
)
  .requiredOption('--safe <address>', 'Safe address')
  .option('--limit <n>', 'Page size', '10')
  .option('--offset <n>', 'Offset', '0')
  .option('--executed <true|false>', 'Filter by executed status')
  .parse();

const opts = program.opts();
const baseUrl = resolveTxServiceUrl(opts);

const params = new URLSearchParams({ limit: opts.limit, offset: opts.offset });
if (opts.executed !== undefined) params.set('executed', opts.executed);

const url = `${baseUrl}/v1/safes/${opts.safe}/multisig-transactions/?${params}`;
const data = await fetchJson(url);
process.stdout.write(JSON.stringify(data, null, 2) + '\n');
