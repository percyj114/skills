# Nova Platform — Console API & Deployment Reference

## API Base URL

```
https://console.sparsity.cloud/api/v1
```

## Authentication

All requests: `Authorization: Bearer <api-key>`

Get API key: [sparsity.cloud](https://sparsity.cloud) → Account → API Keys → Create Key

## App Lifecycle Endpoints

### Create App

```
POST /apps
```
```json
{
  "name": "my-oracle",
  "dockerImage": "docker.io/alice/my-oracle:latest",
  "listenPort": 8000
}
```
Response:
```json
{
  "appId": "app_abc123",
  "status": "created",
  "createdAt": "2025-01-01T00:00:00Z"
}
```

### Deploy App

```
POST /apps/{appId}/deploy
```
Triggers enclave provisioning. Nova will:
- Pull the Docker image
- Build the EIF (Enclave Image File) via Enclaver
- Start the Nitro Enclave with Odyn as supervisor
- Register the enclave's Ethereum address on-chain

### Get App Status

```
GET /apps/{appId}
```
```json
{
  "appId": "app_abc123",
  "name": "my-oracle",
  "status": "running",
  "appUrl": "https://abc123.nova.sparsity.cloud",
  "enclaveAddress": "0xAbCd...",
  "createdAt": "...",
  "updatedAt": "..."
}
```

**Status values:**
| Status | Meaning |
|---|---|
| `created` | App registered, not yet deployed |
| `provisioning` | Nova is building the EIF |
| `starting` | Enclave is booting, Odyn initialising |
| `running` | App is live and accepting requests |
| `failed` | Deployment failed — check `logs` field |
| `stopped` | Manually stopped |

### List Apps

```
GET /apps
```
Returns `{"apps": [...]}` array of app objects.

### Stop / Delete App

```
POST /apps/{appId}/stop
DELETE /apps/{appId}
```

### Get App Logs

```
GET /apps/{appId}/logs?lines=100
```
Returns `{"logs": "...multiline text..."}`.

## Standard App Endpoints (served by your code)

Once running, these are available at `https://{appUrl}/`:

| Endpoint | Description |
|---|---|
| `GET /` | Health check — implement in main.py |
| `POST /.well-known/attestation` | Raw CBOR attestation (required by Nova registry) |
| `GET /api/attestation` | Base64 attestation (required by Nova registry) |
| Any `/api/*` route | Your business logic |

## Manual Console Deployment (fallback if API unavailable)

If `nova_deploy.py` fails, deploy manually:

1. **Open** [sparsity.cloud](https://sparsity.cloud) → sign in
2. **Nova Console** → Apps → **Create App**
3. Fill in:
   - **Name**: your app name
   - **Docker Image**: `docker.io/username/app-name:latest`
   - **Listening Port**: `8000` (must match `EXPOSE` in Dockerfile)
4. Click **Deploy** — provisioning takes 3–8 minutes
5. Status changes to **Running** → copy the **App URL**
6. Optional: click **Register** to add the app to the Nova App Registry (enables ZKP attestation pinning)

## enclaver.yaml (required for advanced deployments)

Include an `enclaver.yaml` in your repo/Docker image to configure:
- Egress allowlist (restrict outbound network access)
- Helios RPC (trustless multi-chain light client at `localhost:18545+`)
- KMS integration (Nova KMS + App Wallet)
- S3 persistent storage with optional KMS encryption
- API and Aux API ports

See `SKILL.md` for a full enclaver.yaml example with KMS, S3, and Helios.

Full reference: https://github.com/sparsity-xyz/enclaver/blob/sparsity/docs/enclaver.yaml

## Registry-based Trust (optional)

After deploying, register your app for ZKP verification:

```
POST /apps/{appId}/register
```

This stores `codeMeasurement`, `teePubkey`, and `appUrl` on-chain in the Nova App Registry contract (`0x58e41D71606410E43BDA23C348B68F5A93245461` on Base Sepolia).

Clients can then verify the enclave identity without trusting the Nova platform operator.
