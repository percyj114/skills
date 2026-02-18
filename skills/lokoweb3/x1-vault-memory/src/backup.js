const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const tar = require('tar');
const { uploadToIPFS } = require('./upload');
const { anchorCID } = require('./anchor');

// Paths to backup (go up 2 levels to reach workspace root)
const filesToBackup = [
  'IDENTITY.md',
  'SOUL.md',
  'USER.md',
  'TOOLS.md',
];
const memoryDir = path.resolve(__dirname, '../..', 'memory');

async function createBackup() {
  // Prepare log entry early
  const entry = { timestamp: new Date().toISOString() };
  
  // Create a temporary tar.gz archive
  const archivePath = path.resolve(__dirname, 'backup.tar.gz');
  const tarFiles = filesToBackup.map(f => path.resolve(__dirname, '..', f));
  // Include memory directory
  const cwd = path.resolve(__dirname, '../..');
  await tar.c(
    {
      gzip: true,
      file: archivePath,
      cwd,
    },
    [...filesToBackup, 'memory']
  );

  // Generate SHA-256 hash of archive before encryption
  const archiveBuffer = fs.readFileSync(archivePath);
  const checksum = crypto.createHash('sha256').update(archiveBuffer).digest('hex');
  const checksumPath = path.resolve(__dirname, 'checksum.txt');
  fs.writeFileSync(checksumPath, checksum);
  console.log('Archive checksum:', checksum);

  // Create payload with archive + checksum
  const payloadPath = path.resolve(__dirname, 'payload.tar');
  await tar.c(
    {
      file: payloadPath,
      cwd: __dirname,
    },
    ['backup.tar.gz', 'checksum.txt']
  );

  // Load wallet secret key
  const walletPath = path.resolve(__dirname, '../..', 'x1_vault_cli', 'wallet.json');
  const wallet = JSON.parse(fs.readFileSync(walletPath, 'utf8'));
  const secretKey = Buffer.from(wallet.secretKey);
  // Derive symmetric key from secretKey using SHA-256
  const key = crypto.createHash('sha256').update(secretKey).digest();
  const iv = crypto.randomBytes(12); // for AES-256-GCM
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const input = fs.createReadStream(payloadPath);
  const encryptedPath = archivePath + '.enc';
  const output = fs.createWriteStream(encryptedPath);
  input.pipe(cipher).pipe(output);
  await new Promise((res, rej) => {
    output.on('finish', () => {
      // Append auth tag
      const authTag = cipher.getAuthTag();
      fs.appendFileSync(encryptedPath, authTag);
      res();
    });
    output.on('error', rej);
  });

  // Upload encrypted backup to Pinata
  const cid = await uploadToIPFS(encryptedPath);
  entry.cid = cid;
  console.log('Backup uploaded, CID:', cid);

  // Anchor CID to X1 blockchain
  try {
    const { signature, explorerUrl } = await anchorCID(cid, walletPath);
    console.log('X1 Transaction:', signature);
    console.log('Explorer:', explorerUrl);
    entry.txHash = signature;
    entry.explorerUrl = explorerUrl;
  } catch (err) {
    console.error('X1 anchoring failed (backup still saved to IPFS):', err.message);
  }

  // Prepare log entry
  const logPath = path.resolve(__dirname, '../..', 'vault-log.json');
  let log = [];
  if (fs.existsSync(logPath)) {
    log = JSON.parse(fs.readFileSync(logPath, 'utf8'));
  }
  log.push(entry);
  fs.writeFileSync(logPath, JSON.stringify(log, null, 2));
  console.log('Logged backup CID to vault-log.json');
}

createBackup().catch(err => {
  console.error('Backup failed:', err);
  process.exit(1);
});
