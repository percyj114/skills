---
name: pinata-api
description: Pinata IPFS API for file storage, groups, gateways, signatures, x402 payments, and AI-powered vector search.
homepage: https://pinata.cloud
metadata: {"openclaw": {"emoji": "📌", "requires": {"env": ["PINATA_JWT", "GATEWAY_URL"]}, "primaryEnv": "PINATA_JWT"}}
---

# Pinata API

Access the Pinata IPFS storage API. Upload files, manage groups, create gateways, add signatures, set up x402 payments, and perform AI-powered vector search.

Repo: https://github.com/PinataCloud/pinata-api-skill

## Authentication

All requests require a Pinata JWT in the Authorization header:

```
Authorization: Bearer $PINATA_JWT
```

**Environment Variables:**

- `PINATA_JWT` (required) - Your Pinata API JWT token. Get one at [app.pinata.cloud/developers/api-keys](https://app.pinata.cloud/developers/api-keys)
- `GATEWAY_URL` (required) - Your Pinata gateway domain (e.g., `your-gateway.mypinata.cloud`). Find yours at [app.pinata.cloud/gateway](https://app.pinata.cloud/gateway)
- `GATEWAY_KEY` (optional) - Gateway key for accessing public IPFS content not tied to your Pinata account. See [Gateway Access Controls](https://docs.pinata.cloud/gateways/gateway-access-controls#gateway-keys)

### Test Authentication

```bash
curl -s https://api.pinata.cloud/data/testAuthentication \
  -H "Authorization: Bearer $PINATA_JWT"
```

## Base URLs

- **API:** `https://api.pinata.cloud`
- **Uploads:** `https://uploads.pinata.cloud`

## Common Parameters

- `network` - IPFS network: `public` (default) or `private`
- Pagination uses `limit` and `pageToken` query parameters

## Files

### Search Files

```bash
GET /v3/files/{network}?name=...&cid=...&mimeType=...&limit=...&pageToken=...
```

```bash
curl -s "https://api.pinata.cloud/v3/files/public?limit=10" \
  -H "Authorization: Bearer $PINATA_JWT"
```

Query parameters (all optional): `name`, `cid`, `mimeType`, `limit`, `pageToken`

### Get File by ID

```bash
GET /v3/files/{network}/{id}
```

```bash
curl -s "https://api.pinata.cloud/v3/files/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### Update File Metadata

```bash
PUT /v3/files/{network}/{id}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/files/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"name": "new-name", "keyvalues": {"key": "value"}}'
```

### Delete File

```bash
DELETE /v3/files/{network}/{id}
```

```bash
curl -s -X DELETE "https://api.pinata.cloud/v3/files/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### Upload File

```bash
POST https://uploads.pinata.cloud/v3/files
```

Uses `multipart/form-data`. Do **not** set `Content-Type` manually — let the HTTP client set the boundary.

```bash
curl -s -X POST "https://uploads.pinata.cloud/v3/files" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -F "file=@/path/to/file.png" \
  -F "network=public" \
  -F "group_id={group_id}" \
  -F 'keyvalues={"key":"value"}'
```

```javascript
const fs = require('fs');
const FormData = require('form-data');

const form = new FormData();
form.append('file', fs.createReadStream('/path/to/file.png'));
form.append('network', 'public');

const response = await fetch('https://uploads.pinata.cloud/v3/files', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${process.env.PINATA_JWT}` },
  body: form,
});
```

```python
import os, requests

response = requests.post(
    'https://uploads.pinata.cloud/v3/files',
    headers={'Authorization': f'Bearer {os.environ["PINATA_JWT"]}'},
    files={'file': open('/path/to/file.png', 'rb')},
    data={'network': 'public'},
)
```

Optional form fields: `network`, `group_id`, `keyvalues` (JSON string)

## Groups

### List Groups

```bash
GET /v3/groups/{network}?name=...&limit=...&pageToken=...
```

```bash
curl -s "https://api.pinata.cloud/v3/groups/public?limit=10" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### Create Group

```bash
POST /v3/groups/{network}
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/groups/public" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-group"}'
```

### Get Group

```bash
GET /v3/groups/{network}/{id}
```

### Update Group

```bash
PUT /v3/groups/{network}/{id}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/groups/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"name": "updated-name"}'
```

### Delete Group

```bash
DELETE /v3/groups/{network}/{id}
```

### Add File to Group

```bash
PUT /v3/groups/{network}/{groupId}/ids/{fileId}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/groups/public/{groupId}/ids/{fileId}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### Remove File from Group

```bash
DELETE /v3/groups/{network}/{groupId}/ids/{fileId}
```

## Gateway & Downloads

### Create Private Download Link

```bash
POST /v3/files/private/download_link
```

Creates a temporary signed URL for accessing private files.

```bash
curl -s -X POST "https://api.pinata.cloud/v3/files/private/download_link" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://'"$GATEWAY_URL"'/files/{cid}",
    "expires": 600,
    "date": '"$(date +%s)"',
    "method": "GET"
  }'
```

- `url` (required) - Full gateway URL: `https://{GATEWAY_URL}/files/{cid}`
- `expires` (optional) - Seconds until expiry (default: 600)
- `date` (required) - Current Unix timestamp in seconds
- `method` (required) - HTTP method, typically `"GET"`

### Create Signed Upload URL

```bash
POST https://uploads.pinata.cloud/v3/files/sign
```

Creates a pre-signed URL for client-side uploads (no JWT needed on the client).

```bash
curl -s -X POST "https://uploads.pinata.cloud/v3/files/sign" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "date": '"$(date +%s)"',
    "expires": 3600
  }'
```

Optional fields: `max_file_size` (bytes), `allow_mime_types` (array), `group_id`, `filename`, `keyvalues`

## Signatures

EIP-712 signatures for verifying content authenticity.

### Add Signature

```bash
POST /v3/files/{network}/signature/{cid}
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/files/public/signature/{cid}" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"signature": "0x...", "address": "0x..."}'
```

### Get Signature

```bash
GET /v3/files/{network}/signature/{cid}
```

### Delete Signature

```bash
DELETE /v3/files/{network}/signature/{cid}
```

## Pin By CID

Pin existing IPFS content by its CID (public network only).

### Pin a CID

```bash
POST /v3/files/public/pin_by_cid
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/files/public/pin_by_cid" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"cid": "bafybeig..."}'
```

Optional fields: `name`, `group_id`, `keyvalues`, `host_nodes` (array of multiaddrs)

### Query Pin Requests

```bash
GET /v3/files/public/pin_by_cid?order=ASC&status=...&cid=...&limit=...&pageToken=...
```

### Cancel Pin Request

```bash
DELETE /v3/files/public/pin_by_cid/{id}
```

## x402 Payment Instructions

Create payment instructions for monetizing IPFS content using the x402 protocol with USDC on Base.

**USDC Contract Addresses:**
- Base mainnet: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Base Sepolia (testnet): `0x036CbD53842c5426634e7929541eC2318f3dCF7e`

**Important:** The `amount` field uses the smallest USDC unit (6 decimals). For example, $1.50 = `"1500000"`.

### Create Payment Instruction

```bash
POST /v3/x402/payment_instructions
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/x402/payment_instructions" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Payment",
    "description": "Pay to access this content",
    "payment_requirements": [{
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "pay_to": "0xYOUR_WALLET_ADDRESS",
      "network": "base",
      "amount": "1500000"
    }]
  }'
```

- `name` (required) - Display name
- `description` (optional) - Description
- `payment_requirements` (required) - Array with `asset` (USDC address), `pay_to` (wallet), `network` (`"base"` or `"base-sepolia"`), `amount` (smallest unit string)

### List Payment Instructions

```bash
GET /v3/x402/payment_instructions?limit=...&pageToken=...&cid=...&name=...&id=...
```

### Get Payment Instruction

```bash
GET /v3/x402/payment_instructions/{id}
```

### Delete Payment Instruction

```bash
DELETE /v3/x402/payment_instructions/{id}
```

### Associate CID with Payment

```bash
PUT /v3/x402/payment_instructions/{id}/cids/{cid}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/x402/payment_instructions/{id}/cids/{cid}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### Remove CID from Payment

```bash
DELETE /v3/x402/payment_instructions/{id}/cids/{cid}
```

## Vectorize (AI Search)

Generate vector embeddings for files and perform semantic search across groups.

### Vectorize a File

```bash
POST https://uploads.pinata.cloud/v3/vectorize/files/{file_id}
```

```bash
curl -s -X POST "https://uploads.pinata.cloud/v3/vectorize/files/{file_id}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### Delete File Vectors

```bash
DELETE https://uploads.pinata.cloud/v3/vectorize/files/{file_id}
```

### Query Vectors (Semantic Search)

```bash
POST https://uploads.pinata.cloud/v3/vectorize/groups/{group_id}/query
```

```bash
curl -s -X POST "https://uploads.pinata.cloud/v3/vectorize/groups/{group_id}/query" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"text": "search query here"}'
```

## Notes

- All JSON endpoints require `Content-Type: application/json`
- File uploads use `multipart/form-data` — do not set Content-Type manually
- Pagination: use `pageToken` from the previous response to get the next page
- Network defaults to `public` if not specified
- Gateway URLs follow the pattern `https://{GATEWAY_URL}/files/{cid}`

## Resources

- [Pinata Documentation](https://docs.pinata.cloud)
- [API Keys](https://app.pinata.cloud/developers/api-keys)
- [Gateway Setup](https://docs.pinata.cloud/gateways)
- [x402 Protocol](https://docs.pinata.cloud/x402)
- [Source (GitHub)](https://github.com/PinataCloud/pinata-api-skill)
