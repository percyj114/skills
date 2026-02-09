#!/usr/bin/env node
// Fetch Safe info (owners/threshold/nonce) from the Transaction Service REST API.
// Uses plain HTTP — no SDK needed for read-only queries.
import { addCommonOptions, cmd, fetchJson, resolveTxServiceUrl } from './safe_lib.mjs';

const program = addCommonOptions(
  cmd('safe_info', 'Fetch Safe info (owners/threshold/nonce) from Transaction Service')
)
  .requiredOption('--safe <address>', 'Safe address')
  .parse();

const opts = program.opts();
const baseUrl = resolveTxServiceUrl(opts);
const url = `${baseUrl}/v1/safes/${opts.safe}/`;

const data = await fetchJson(url);
process.stdout.write(JSON.stringify(data, null, 2) + '\n');
