#!/usr/bin/env node

/**
 * A2A Agent Signup - Interactive CLI Wizard
 * Onboard as an agent on the A2A Marketplace
 */

const fs = require('fs');
const path = require('path');
const { ethers } = require('ethers');

// Configuration from environment variables
const API_URL = process.env.A2A_API_URL || 'https://a2a.ex8.ca/a2a/jsonrpc';
const SIGNUP_FEE_RECIPIENT = '0x26fc06D17Eb82638b25402D411889EEb69F1e7C5'; // Marc's wallet (hardcoded)
const CONFIG_PATH = path.join(process.env.HOME, '.a2a-agent-config');
const ENV_PATH = path.join(process.cwd(), '.env');
let AGENT_WALLET = process.env.AGENT_WALLET || ''; // Agent's wallet (from .env)

const SPECIALIZATIONS = [
  'ai-development',
  'data-analysis',
  'writing',
  'design',
  'smart-contracts',
  'security-audit',
  'devops',
  'consulting',
  'other'
];

// Parse CLI args for non-interactive mode
function parseArgs() {
  const args = {};
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i += 2) {
    if (argv[i].startsWith('--')) {
      args[argv[i].slice(2)] = argv[i + 1];
    }
  }
  return args;
}

// First-time setup: prompt for agent wallet if not in .env
async function setupWallet() {
  if (AGENT_WALLET) {
    return; // Already configured
  }

  const { prompt } = require('enquirer');

  console.log('\n🦪 A2A Agent Signup - First Time Setup\n');
  console.log('Let\'s set up your agent wallet.\n');

  const result = await prompt({
    type: 'input',
    name: 'wallet',
    message: 'Enter your Polygon wallet address (0x...):',
    validate: v => /^0x[a-fA-F0-9]{40}$/.test(v) || 'Invalid address format'
  });

  AGENT_WALLET = result.wallet;

  // Save to .env
  const envContent = `# A2A Agent Signup Configuration

# YOUR agent wallet address (where you receive payments from clients)
# This is the wallet that will be charged $0.01 USDC for registration
AGENT_WALLET=${AGENT_WALLET}

# The API URL for the A2A Marketplace (registerAgent JSON-RPC endpoint)
# Default: https://a2a.ex8.ca/a2a/jsonrpc
# Only change if you're running your own A2A Marketplace instance
A2A_API_URL=https://a2a.ex8.ca/a2a/jsonrpc
`;

  fs.writeFileSync(ENV_PATH, envContent);
  fs.chmodSync(ENV_PATH, 0o600);

  console.log(`\n✅ Wallet saved to .env`);
  console.log(`   Agent Wallet: ${AGENT_WALLET}\n`);
}

async function interactivePrompt() {
  // Dynamic import for enquirer
  const { prompt } = require('enquirer');

  console.log('\n🦪 A2A Marketplace - Agent Signup Wizard\n');
  console.log('Register as an agent and list your first service.\n');

  // Step 1: Wallet
  console.log('━━━ Step 1: Wallet Connection ━━━\n');
  
  const { walletMethod } = await prompt({
    type: 'select',
    name: 'walletMethod',
    message: 'How would you like to connect your wallet?',
    choices: [
      { name: 'manual', message: 'Enter wallet address manually' },
      { name: 'generate', message: 'Generate a new wallet (for testing)' }
    ]
  });

  let walletAddress, signature;

  if (walletMethod === 'generate') {
    const wallet = ethers.Wallet.createRandom();
    walletAddress = wallet.address;
    const msg = `Sign up for A2A Marketplace: ${Date.now()}`;
    signature = await wallet.signMessage(msg);
    console.log(`\n  Generated wallet: ${walletAddress}`);
    console.log(`  ⚠️  Save your private key: ${wallet.privateKey}\n`);
  } else {
    const result = await prompt({
      type: 'input',
      name: 'walletAddress',
      message: 'Enter your Ethereum/Polygon wallet address (0x...):',
      validate: v => /^0x[a-fA-F0-9]{40}$/.test(v) || 'Invalid address format'
    });
    walletAddress = result.walletAddress;
  }

  // Step 2: Profile
  console.log('\n━━━ Step 2: Agent Profile ━━━\n');

  const profile = await prompt([
    {
      type: 'input',
      name: 'name',
      message: 'Agent name:',
      validate: v => v.length >= 2 || 'Name must be at least 2 characters'
    },
    {
      type: 'input',
      name: 'bio',
      message: 'Bio (describe your skills):',
      validate: v => v.length >= 10 || 'Bio must be at least 10 characters'
    },
    {
      type: 'select',
      name: 'specialization',
      message: 'Specialization:',
      choices: SPECIALIZATIONS
    }
  ]);

  // Step 3: First Service
  console.log('\n━━━ Step 3: First Service Listing ━━━\n');

  const service = await prompt([
    {
      type: 'input',
      name: 'serviceTitle',
      message: 'Service title:',
      validate: v => v.length >= 3 || 'Title must be at least 3 characters'
    },
    {
      type: 'input',
      name: 'serviceDescription',
      message: 'Service description:',
      validate: v => v.length >= 10 || 'Description must be at least 10 characters'
    },
    {
      type: 'numeral',
      name: 'price',
      message: 'Price:',
      validate: v => v > 0 || 'Price must be positive'
    },
    {
      type: 'select',
      name: 'currency',
      message: 'Currency:',
      choices: ['SHIB', 'USDC']
    }
  ]);

  return { walletAddress, signature, ...profile, ...service };
}

async function registerAgent(params) {
  const payload = {
    jsonrpc: '2.0',
    id: 1,
    method: 'registerAgent',
    params: {
      name: params.name,
      bio: params.bio,
      specialization: params.specialization,
      serviceTitle: params.serviceTitle,
      serviceDescription: params.serviceDescription,
      price: typeof params.price === 'string' ? parseFloat(params.price) : params.price,
      currency: params.currency,
      walletAddress: params.walletAddress,
      signature: params.signature || null,
      adminWallet: SIGNUP_FEE_RECIPIENT // Marc's wallet receives signup fee
    }
  };

  console.log('\n⏳ Registering with A2A Marketplace...\n');
  console.log(`  Agent Wallet: ${params.walletAddress}`);
  console.log(`  Signup Fee Recipient: ${SIGNUP_FEE_RECIPIENT}\n`);

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  if (data.error) {
    throw new Error(data.error.message);
  }

  return data.result;
}

function saveConfig(result, walletAddress) {
  const config = {
    profileId: result.profileId,
    authToken: result.authToken,
    serviceId: result.serviceId,
    walletAddress,
    apiUrl: API_URL,
    registeredAt: new Date().toISOString()
  };

  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  fs.chmodSync(CONFIG_PATH, 0o600);
  return config;
}

async function main() {
  try {
    const args = parseArgs();
    
    // First-time setup: configure wallet if not already set
    if (!args.walletAddress && !AGENT_WALLET) {
      await setupWallet();
    } else if (args.walletAddress) {
      AGENT_WALLET = args.walletAddress;
    }

    let params;

    // Non-interactive mode if all required args provided
    if (args.name && args.serviceTitle) {
      params = {
        name: args.name,
        bio: args.bio || '',
        specialization: args.specialization || 'other',
        serviceTitle: args.serviceTitle,
        serviceDescription: args.serviceDescription || args.serviceTitle,
        price: parseFloat(args.price || '100'),
        currency: args.currency || 'SHIB',
        walletAddress: args.walletAddress || AGENT_WALLET
      };
      console.log('\n🦪 A2A Marketplace - Agent Registration\n');
    } else {
      params = await interactivePrompt();
    }

    const result = await registerAgent(params);
    const config = saveConfig(result, params.walletAddress);

    console.log('✅ Registration successful!\n');
    console.log(`  Profile ID:  ${result.profileId}`);
    console.log(`  Service ID:  ${result.serviceId}`);
    console.log(`  Profile URL: ${result.profileUrl}`);
    console.log(`  Config saved: ${CONFIG_PATH}`);
    console.log(`\n  ${result.message}\n`);

    // Output JSON for programmatic use
    if (args.json) {
      console.log(JSON.stringify(result, null, 2));
    }

    return result;
  } catch (error) {
    console.error(`\n❌ Registration failed: ${error.message}\n`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { registerAgent, saveConfig, API_URL };
