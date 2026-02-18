const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const tar = require('tar');
const https = require('https');
const { execSync } = require('child_process');

// Helper to download file from Pinata gateway
function downloadFromPinata(cid, destPath) {
  return new Promise((resolve, reject) => {
    const url = `https://gateway.pinata.cloud/ipfs/${cid}`;
    const file = fs.createWriteStream(destPath);
    https.get(url, response => {
      if (response.statusCode !== 200) {
        return reject(new Error(`Failed to download CID ${cid}, status ${response.statusCode}`));
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close(() => resolve());
      });
    }).on('error', err => {
      fs.unlinkSync(destPath);
      reject(err);
    });
  });
}

async function restoreBackup(cid) {
  const encryptedPath = path.resolve(__dirname, 'downloaded.enc');
  await downloadFromPinata(cid, encryptedPath);

  // Load wallet secret key
  const walletPath = path.resolve(__dirname, '../..', 'x1_vault_cli', 'wallet.json');
  const wallet = JSON.parse(fs.readFileSync(walletPath, 'utf8'));
  const secretKey = Buffer.from(wallet.secretKey);
  const key = crypto.createHash('sha256').update(secretKey).digest();
  
  // Read encrypted file and auth tag (last 16 bytes for GCM)
  const data = fs.readFileSync(encryptedPath);
  const authTag = data.slice(data.length - 16);
  const encryptedData = data.slice(0, data.length - 16);
  const iv = encryptedData.slice(0, 12);
  const ciphertext = encryptedData.slice(12);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  
  // Write decrypted payload
  const payloadPath = path.resolve(__dirname, 'payload.tar');
  fs.writeFileSync(payloadPath, decrypted);
  console.log('Decrypted payload extracted');

  // Extract payload to get archive + checksum
  const tempDir = path.resolve(__dirname, 'temp_restore');
  if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir);
  
  await tar.x({ file: payloadPath, cwd: tempDir });
  console.log('Payload extracted');

  // Read checksum and verify
  const checksumPath = path.join(tempDir, 'checksum.txt');
  const archivePath = path.join(tempDir, 'backup.tar.gz');
  
  if (!fs.existsSync(checksumPath) || !fs.existsSync(archivePath)) {
    throw new Error('Payload missing checksum.txt or backup.tar.gz');
  }
  
  const expectedChecksum = fs.readFileSync(checksumPath, 'utf8').trim();
  const archiveBuffer = fs.readFileSync(archivePath);
  const actualChecksum = crypto.createHash('sha256').update(archiveBuffer).digest('hex');
  
  console.log('Expected checksum:', expectedChecksum);
  console.log('Actual checksum:', actualChecksum);
  
  if (expectedChecksum !== actualChecksum) {
    console.error('ERROR: Checksum mismatch! Archive may be corrupted.');
    console.error('Expected:', expectedChecksum);
    console.error('Got:', actualChecksum);
    process.exit(1);
  }
  
  console.log('✓ Checksum verified — archive integrity confirmed');

  // Extract archive to workspace
  const cwd = path.resolve(__dirname, '../..');
  await tar.x({ file: archivePath, cwd });
  console.log('Backup restored to workspace');
  
  // Cleanup temp files
  fs.rmSync(tempDir, { recursive: true });
  fs.unlinkSync(payloadPath);
}

// Parse arguments
const cid = process.argv[2];
const onlyFlag = process.argv.indexOf('--only');
const onlyPath = onlyFlag !== -1 && process.argv[onlyFlag + 1] ? process.argv[onlyFlag + 1] : null;

if (!cid) {
  console.error('Usage: node restore.js <CID> [--only <path>]');
  console.error('Example: node restore.js QmAbC123 --only memory/');
  process.exit(1);
}

async function restoreBackup(cid, onlyPath) {
  const encryptedPath = path.resolve(__dirname, 'downloaded.enc');
  await downloadFromPinata(cid, encryptedPath);

  // Load wallet secret key
  const walletPath = path.resolve(__dirname, '../..', 'x1_vault_cli', 'wallet.json');
  const wallet = JSON.parse(fs.readFileSync(walletPath, 'utf8'));
  const secretKey = Buffer.from(wallet.secretKey);
  const key = crypto.createHash('sha256').update(secretKey).digest();
  
  // Read encrypted file and auth tag (last 16 bytes for GCM)
  const data = fs.readFileSync(encryptedPath);
  const authTag = data.slice(data.length - 16);
  const encryptedData = data.slice(0, data.length - 16);
  const iv = encryptedData.slice(0, 12);
  const ciphertext = encryptedData.slice(12);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);
  const decrypted = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  
  // Write decrypted payload
  const payloadPath = path.resolve(__dirname, 'payload.tar');
  fs.writeFileSync(payloadPath, decrypted);
  console.log('Decrypted payload extracted');

  // Extract payload to get archive + checksum
  const tempDir = path.resolve(__dirname, 'temp_restore');
  if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir);
  
  await tar.x({ file: payloadPath, cwd: tempDir });
  console.log('Payload extracted');

  // Read checksum and verify
  const checksumPath = path.join(tempDir, 'checksum.txt');
  const archivePath = path.join(tempDir, 'backup.tar.gz');
  
  if (!fs.existsSync(checksumPath) || !fs.existsSync(archivePath)) {
    throw new Error('Payload missing checksum.txt or backup.tar.gz');
  }
  
  const expectedChecksum = fs.readFileSync(checksumPath, 'utf8').trim();
  const archiveBuffer = fs.readFileSync(archivePath);
  const actualChecksum = crypto.createHash('sha256').update(archiveBuffer).digest('hex');
  
  console.log('Expected checksum:', expectedChecksum);
  console.log('Actual checksum:', actualChecksum);
  
  if (expectedChecksum !== actualChecksum) {
    console.error('ERROR: Checksum mismatch! Archive may be corrupted.');
    console.error('Expected:', expectedChecksum);
    console.error('Got:', actualChecksum);
    process.exit(1);
  }
  
  console.log('✓ Checksum verified — archive integrity confirmed');

  // Extract archive to workspace
  const cwd = path.resolve(__dirname, '../..');
  
  if (onlyPath) {
    // Selective restore — only extract matching path
    console.log(`Restoring only: ${onlyPath}`);
    
    // List files in archive and filter
    const files = await tar.list({ file: archivePath });
    const matchingFiles = files.filter(f => f.startsWith(onlyPath));
    
    if (matchingFiles.length === 0) {
      console.error(`No files found matching: ${onlyPath}`);
      process.exit(1);
    }
    
    console.log(`Found ${matchingFiles.length} matching files`);
    await tar.x({ file: archivePath, cwd, filter: (p) => p.startsWith(onlyPath) });
    console.log(`Restored ${onlyPath} to workspace`);
  } else {
    // Full restore
    await tar.x({ file: archivePath, cwd });
    console.log('Backup restored to workspace');
  }
  
  // Cleanup temp files
  fs.rmSync(tempDir, { recursive: true });
  fs.unlinkSync(payloadPath);
}

restoreBackup(cid, onlyPath).catch(err => {
  console.error('Restore failed:', err);
  process.exit(1);
});
