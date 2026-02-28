---
name: nova-app-builder
description: "Build and deploy Nova Platform apps (TEE apps on Sparsity Nova / sparsity.cloud). Use when a user wants to create a Nova app, write enclave application code, build it into a Docker image, and deploy it to the Nova Platform to get a live running URL. Handles the full lifecycle: scaffold, code, build, push, deploy, verify running. Triggers on requests like 'build me a Nova app', 'deploy to Nova Platform', 'create a TEE app on sparsity.cloud', 'I want to run an enclave app on Nova'."
---

# Nova App Builder

End-to-end workflow: understand the idea → scaffold → write code → build → push → deploy → confirm live URL.

## Architecture Overview

Nova apps run inside AWS Nitro Enclaves, managed by **Enclaver** (Sparsity edition) and supervised by **Odyn** (PID 1 inside the enclave). Key concepts:

- **Enclaver**: packages your Docker image into an EIF (Enclave Image File) and manages the enclave lifecycle.
- **Odyn**: supervisor inside the enclave; provides Internal API for signing, attestation, encryption, KMS, S3, and manages networking.
- **Nova Platform**: cloud platform at [sparsity.cloud](https://sparsity.cloud) — builds EIFs, runs enclaves, exposes app URLs.
- **Nova KMS**: distributed key management; enclave apps derive keys via `/v1/kms/derive`.

## Prerequisites (collect from user before starting)

- **App idea**: What does the app do?
- **Nova account + API key**: Sign up at [sparsity.cloud](https://sparsity.cloud) → Account → API Keys.
- **Git repo**: Nova Platform builds directly from a Git repo URL + branch.

> ⚠️ **Do NOT ask for Docker registry credentials or AWS S3 credentials.**
> Nova Platform handles the Docker build and image registry internally (Git-based build pipeline).
> S3 storage credentials are managed by the Enclaver/Odyn layer — the app only calls Internal API endpoints (`/v1/s3/*`). Users never touch AWS credentials.

## Full Workflow

### Step 1 — Scaffold the project

```bash
python3 scripts/scaffold.py \
  --name <app-name> \
  --desc "<one-line description>" \
  --port 8000 \
  --out <output-dir>
```

This copies the asset template into `<output-dir>/<app-name>/` and prints the file list.

Alternatively, fork [nova-app-template](https://github.com/sparsity-xyz/nova-app-template) — it's a production-ready starter with KMS, S3, App Wallet, E2E encryption, and a built-in React frontend.

### Step 2 — Write the app logic

Edit `enclave/main.py`. Key patterns:

**Minimal FastAPI app:**
```python
import os, httpx
from fastapi import FastAPI

app = FastAPI()
IN_ENCLAVE = os.getenv("IN_ENCLAVE", "false").lower() == "true"
ODYN_BASE = "http://127.0.0.1:18000" if IN_ENCLAVE else "http://odyn.sparsity.cloud:18000"

@app.get("/api/hello")
def hello():
    r = httpx.get(f"{ODYN_BASE}/v1/eth/address", timeout=10)
    return {"message": "Hello from TEE!", "enclave": r.json()["address"]}
```

**With App Wallet + KMS (from nova-app-template):**
```python
from kms_client import NovaKmsClient
import base64

kms = NovaKmsClient(endpoint=ODYN_BASE)

@app.get("/api/wallet")
def wallet():
    return kms.app_wallet_address()     # {"address": "0x...", "app_id": 0}

@app.post("/api/sign")
def sign(body: dict):
    return kms.app_wallet_sign(body["message"])   # {"signature": "0x..."}
```

**Dual-chain topology** (as in the template):
- **Auth/Registry chain**: Base Sepolia (84532) — KMS authorization & app registry
- **Business chain**: Ethereum Mainnet (1) — your business logic

Helios light-client RPC runs locally at `http://127.0.0.1:18545` (Base Sepolia) and `http://127.0.0.1:18546` (Mainnet).

Rules for enclave code:
- All outbound HTTP must use `httpx` (proxy-aware). Never use `requests` or `urllib` — they may bypass the egress proxy.
- Persistent state → use `/v1/s3/*` endpoints; the enclave filesystem is ephemeral.
- Secrets → derive via KMS (`/v1/kms/derive`); never from env vars or hardcoded.
- Test locally: `IN_ENCLAVE=false uvicorn main:app --port 8000` (Odyn calls hit the public mock).

### Step 3 — Configure enclaver.yaml

Key fields to update in your fork:

```yaml
version: v1
name: my-app
sources:
  app: my-app:latest
target: my-app-enclave:latest

ingress:
  - listen_port: 8000

egress:
  proxy_port: 10000
  allow:
    - "169.254.169.254"             # IMDS (required for S3/KMS)
    - "s3.us-east-1.amazonaws.com"
    - "api.example.com"

api:
  listen_port: 18000

kms_integration:
  enabled: true
  use_app_wallet: true
  kms_app_id: <YOUR_APP_ID>             # from Nova Portal
  nova_app_registry: "0x0f68E6..."      # Base Sepolia registry

helios_rpc:
  enabled: true
  chains:
    - name: "L2-base-sepolia"
      network_id: "84532"
      kind: "opstack"
      network: "base-sepolia"
      execution_rpc: "https://sepolia.base.org"
      local_rpc_port: 18545
    - name: "ethereum-mainnet"
      network_id: "1"
      kind: "ethereum"
      network: "mainnet"
      execution_rpc: "https://eth.llamarpc.com"
      local_rpc_port: 18546

storage:
  s3:
    enabled: true
    bucket: "my-app-data"
    prefix: "apps/my-app/"
    region: "us-east-1"
    encryption:
      mode: "kms"
```

Also update `enclave/config.py`: set `CONTRACT_ADDRESS`, `APP_ID`, `APP_VERSION_ID`.

### Step 4 — Commit & push to Git

No local Docker build needed. Nova Platform builds the image and EIF from your Git repo.

Just push your changes to the branch you'll specify in Step 5:

```bash
git add .
git commit -m "Initial Nova app"
git push origin main
```

### Step 5 — Deploy to Nova Platform (Portal-based)

1. Go to [sparsity.cloud](https://sparsity.cloud) → **Apps** → **Create App**
2. Fill in **Name** and **Description** → Submit → copy the **App ID**
3. Update `enclave/config.py` and `enclaver.yaml` with the App ID → push to Git
4. In the App page → **Builds/Versions** → **Create Build**:
   - Version Tag: e.g. `v1.0.0`
   - Git Repository: your fork URL
   - Git Branch: `main` (or commit hash)
5. Wait for build (Nova builds your Docker image → EIF via Enclaver → generates PCRs)
6. **Deployments** → **Create Deployment** → select the version → **Deploy**
   (No AWS credentials needed — Enclaver handles S3 access internally)
7. Status → `running` → copy the **App URL**

#### API-based deploy (alternative, if user has Nova API key)

```bash
python3 scripts/nova_deploy.py \
  --name "<app-name>" \
  --port 8000 \
  --api-key <nova-api-key>
```

This calls `POST /apps` + `POST /apps/{appId}/deploy`, then polls until `running` and prints the live URL. No Docker push needed — Nova pulls from Git.

### Step 6 — Verify the live app

```bash
# Health check
curl https://<appUrl>/

# Attestation (proves it's a real Nitro Enclave)
curl https://<appUrl>/api/attestation

# App Wallet address
curl https://<appUrl>/api/app-wallet
```

## Common Issues

| Symptom | Fix |
|---|---|
| `docker push` fails | `docker login` first |
| Deploy API returns 401 | Regenerate API key at sparsity.cloud |
| App stuck in `provisioning` >10 min | Check Nova Console logs; usually a Dockerfile CMD issue |
| `httpx` request fails inside enclave | Add domain to `egress.allow` in enclaver.yaml |
| S3 fails | Ensure `169.254.169.254` and S3 endpoint are in egress allow list |
| `/v1/kms/*` returns 400 | Check `kms_integration` config; requires `helios_rpc.enabled=true` for registry mode |
| App Wallet unavailable | Nova KMS unreachable or `use_app_wallet: true` missing in `kms_integration` |
| Proxy not respected | Switch from `requests`/`urllib` to `httpx` |

## Reference Files

- **`references/odyn-api.md`** — Full Odyn Internal API (signing, encryption, S3, KMS, App Wallet, attestation)
- **`references/nova-api.md`** — Nova Console REST API + manual console walkthrough

## Key URLs

- Nova Platform: https://sparsity.cloud
- Enclaver (Sparsity): https://github.com/sparsity-xyz/enclaver
- Nova App Template: https://github.com/sparsity-xyz/nova-app-template
- Enclaver Docs: [odyn.md](https://github.com/sparsity-xyz/enclaver/blob/sparsity/docs/odyn.md), [internal_api.md](https://github.com/sparsity-xyz/enclaver/blob/sparsity/docs/internal_api.md)
