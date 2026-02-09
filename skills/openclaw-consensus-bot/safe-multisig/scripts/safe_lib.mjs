import { Command } from 'commander';

// Chain slug → default public RPC URLs
const DEFAULT_RPCS = {
  mainnet: 'https://eth.llamarpc.com', ethereum: 'https://eth.llamarpc.com',
  optimism: 'https://mainnet.optimism.io', 'op-mainnet': 'https://mainnet.optimism.io',
  bsc: 'https://bsc-dataseed.binance.org', gnosis: 'https://rpc.gnosischain.com',
  polygon: 'https://polygon-rpc.com', base: 'https://mainnet.base.org',
  arbitrum: 'https://arb1.arbitrum.io/rpc', 'arbitrum-one': 'https://arb1.arbitrum.io/rpc',
  avalanche: 'https://api.avax.network/ext/bc/C/rpc', sepolia: 'https://rpc.sepolia.org',
  'base-sepolia': 'https://sepolia.base.org', 'optimism-sepolia': 'https://sepolia.optimism.io',
  'arbitrum-sepolia': 'https://sepolia-rollup.arbitrum.io/rpc'
};

// Chain slug → chainId mapping (common chains)
const CHAIN_IDS = {
  mainnet: 1n, ethereum: 1n,
  optimism: 10n, 'op-mainnet': 10n,
  bsc: 56n, gnosis: 100n,
  polygon: 137n, base: 8453n,
  arbitrum: 42161n, 'arbitrum-one': 42161n,
  avalanche: 43114n, sepolia: 11155111n,
  'base-sepolia': 84532n, 'optimism-sepolia': 11155420n,
  'arbitrum-sepolia': 421614n
};

export function addCommonOptions(cmd) {
  return cmd
    .option('--chain <slug>', 'Safe tx-service chain slug (e.g. base, base-sepolia, mainnet)')
    .option('--tx-service-url <url>', 'Override tx-service base URL')
    .option('--rpc-url <url>', 'RPC URL (required for signing/executing)', process.env.RPC_URL)
    .option('--api-key <key>', 'Safe Transaction Service API key', process.env.SAFE_TX_SERVICE_API_KEY)
    .option('--debug', 'Verbose logging');
}

// User-facing chain slug → Safe Transaction Service gateway slug
// Verified live 2026-02-08 against https://api.safe.global/tx-service/{slug}/api/v1/about/
const TX_SERVICE_SLUGS = {
  mainnet: 'eth', ethereum: 'eth',
  optimism: 'oeth', 'op-mainnet': 'oeth',
  bsc: 'bnb',
  gnosis: 'gno',
  polygon: 'pol',
  base: 'base',
  arbitrum: 'arb1', 'arbitrum-one': 'arb1',
  avalanche: 'avax',
  sepolia: 'sep',
  'base-sepolia': 'basesep',
};

export function resolveTxServiceUrl(opts) {
  if (opts.txServiceUrl) return opts.txServiceUrl.replace(/\/$/, '');
  if (!opts.chain) throw new Error('Missing --chain or --tx-service-url');
  const slug = TX_SERVICE_SLUGS[opts.chain.toLowerCase()];
  if (!slug) throw new Error(
    `Unknown chain "${opts.chain}" for Safe Transaction Service. ` +
    `Known: ${Object.keys(TX_SERVICE_SLUGS).join(', ')}. ` +
    `Or pass --tx-service-url directly.`
  );
  // URL must end with /api — SafeApiKit appends /v1/... paths
  return `https://api.safe.global/tx-service/${slug}/api`;
}

export function resolveChainId(opts) {
  if (opts.chain) {
    const id = CHAIN_IDS[opts.chain.toLowerCase()];
    if (!id) throw new Error(`Unknown chain slug "${opts.chain}". Known: ${Object.keys(CHAIN_IDS).join(', ')}`);
    return id;
  }
  throw new Error('Missing --chain (needed to resolve chainId)');
}

export function resolveRpcUrl(opts) {
  if (opts.rpcUrl) return opts.rpcUrl;
  if (process.env.RPC_URL) return process.env.RPC_URL;
  if (opts.chain) {
    const url = DEFAULT_RPCS[opts.chain.toLowerCase()];
    if (url) return url;
    throw new Error(`No default RPC URL for chain "${opts.chain}". Pass --rpc-url explicitly.`);
  }
  throw new Error('Missing --rpc-url or --chain (needed to resolve RPC URL)');
}

export function requirePrivateKey() {
  const pk = process.env.SAFE_SIGNER_PRIVATE_KEY;
  if (!pk) throw new Error('Missing SAFE_SIGNER_PRIVATE_KEY env var');
  return pk.startsWith('0x') ? pk : `0x${pk}`;
}

export async function fetchJson(url, { method = 'GET', headers = {}, body } = {}) {
  const res = await fetch(url, {
    method,
    headers: { 'content-type': 'application/json', ...headers },
    body: body ? JSON.stringify(body) : undefined
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status} ${res.statusText}: ${text.slice(0, 800)}`);
  }
  return res.json();
}

export function cmd(name, description) {
  const c = new Command();
  c.name(name);
  c.description(description);
  c.showHelpAfterError(true);
  c.showSuggestionAfterError(true);
  return c;
}
