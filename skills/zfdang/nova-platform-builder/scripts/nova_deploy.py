#!/usr/bin/env python3
"""
nova_deploy.py — Deploy a Docker image to the Nova Platform and wait for it to go live.

Usage:
    python3 scripts/nova_deploy.py \
        --image docker.io/alice/my-app:latest \
        --port 8000 \
        --name "My App" \
        --api-key <nova-api-key> \
        [--poll-interval 15] \
        [--timeout 600]

Nova API key:  sparsity.cloud → Account → API Keys → Create

Output:
    App URL printed when status = running, e.g.:
        https://abc123.nova.sparsity.cloud

Fallback:
    If the API is unavailable, the script prints manual console steps.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any

try:
    import urllib.request
    import urllib.error
except ImportError:
    pass  # stdlib always available

NOVA_API_BASE = "https://console.sparsity.cloud/api/v1"
HEADERS_TEMPLATE = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# ── HTTP helpers (stdlib only — no pip install needed) ────────────────────────

def _request(
    method: str,
    path: str,
    api_key: str,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{NOVA_API_BASE}{path}"
    headers = {**HEADERS_TEMPLATE, "Authorization": f"Bearer {api_key}"}
    data = json.dumps(body).encode() if body else None

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason} → {url}\n{body_text}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error → {url}: {e.reason}") from e


def _post(path: str, api_key: str, body: dict[str, Any]) -> dict[str, Any]:
    return _request("POST", path, api_key, body)


def _get(path: str, api_key: str) -> dict[str, Any]:
    return _request("GET", path, api_key)


# ── Deployment steps ──────────────────────────────────────────────────────────

def create_app(name: str, image: str, port: int, api_key: str) -> dict[str, Any]:
    """Create the app entry in the Nova Console."""
    print(f"[1/3] Creating Nova app '{name}' with image {image} ...")
    result = _post(
        "/apps",
        api_key,
        {
            "name": name,
            "dockerImage": image,
            "listenPort": port,
        },
    )
    app_id = result.get("appId") or result.get("id")
    print(f"      App ID: {app_id}")
    return result


def trigger_deploy(app_id: str, api_key: str) -> None:
    """Trigger a deployment (provision enclave + start Odyn)."""
    print(f"[2/3] Triggering deployment for app {app_id} ...")
    _post(f"/apps/{app_id}/deploy", api_key, {})
    print("      Deployment triggered — waiting for enclave to start ...")


def wait_for_running(
    app_id: str,
    api_key: str,
    poll_interval: int,
    timeout: int,
) -> str:
    """Poll until status == 'running'. Returns the live appUrl."""
    print(f"[3/3] Polling status (every {poll_interval}s, timeout {timeout}s) ...")
    deadline = time.time() + timeout
    dots = 0

    while time.time() < deadline:
        try:
            data = _get(f"/apps/{app_id}", api_key)
        except RuntimeError as exc:
            print(f"\n      [warn] Poll error: {exc} — retrying ...")
            time.sleep(poll_interval)
            continue

        status = data.get("status", "unknown").lower()
        app_url = data.get("appUrl") or data.get("url") or ""

        print(f"  [{dots * '.':.<20}] status={status}", end="\r")
        dots += 1

        if status == "running" and app_url:
            print()
            return app_url

        if status in ("failed", "error"):
            print()
            logs = data.get("logs", "")
            raise RuntimeError(
                f"Deployment failed (status={status}).\nLogs:\n{logs}"
            )

        time.sleep(poll_interval)

    raise TimeoutError(
        f"App did not reach 'running' within {timeout}s.\n"
        f"Check Nova Console → Apps → {app_id} for logs."
    )


# ── Manual fallback ───────────────────────────────────────────────────────────

def print_manual_steps(image: str, port: int, name: str) -> None:
    print(
        f"""
[fallback] Nova API unreachable — complete deployment manually:

  1. Go to https://sparsity.cloud → Nova Console → Apps → Create App
  2. Fill in:
       Name:            {name}
       Docker Image:    {image}
       Listening Port:  {port}
  3. Click Deploy and wait for status = Running
  4. Copy the App URL from the console

The app will be live at the URL shown in the console.
"""
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy a Nova app and wait for it to go live")
    parser.add_argument("--image", required=True, help="Full Docker image ref, e.g. docker.io/alice/my-app:latest")
    parser.add_argument("--port", type=int, default=8000, help="App listening port (default: 8000)")
    parser.add_argument("--name", required=True, help="Human-readable app name")
    parser.add_argument("--api-key", required=True, help="Nova Console API key")
    parser.add_argument("--poll-interval", type=int, default=15, help="Poll interval in seconds (default: 15)")
    parser.add_argument("--timeout", type=int, default=600, help="Total wait timeout in seconds (default: 600)")
    args = parser.parse_args()

    try:
        # ── Create app ────────────────────────────────────────────────────────
        result = create_app(args.name, args.image, args.port, args.api_key)
        app_id = result.get("appId") or result.get("id")
        if not app_id:
            raise RuntimeError(f"No appId in create response: {result}")

        # ── Deploy ────────────────────────────────────────────────────────────
        trigger_deploy(app_id, args.api_key)

        # ── Wait ──────────────────────────────────────────────────────────────
        app_url = wait_for_running(
            app_id,
            args.api_key,
            args.poll_interval,
            args.timeout,
        )

        print(f"""
╔══════════════════════════════════════════════════════╗
║  ✅  Nova App is LIVE                                ║
╠══════════════════════════════════════════════════════╣
║  App ID  : {app_id:<42}║
║  URL     : {app_url:<42}║
╚══════════════════════════════════════════════════════╝

Verify:
  curl {app_url}/
  curl {app_url}/api/attestation
""")

    except RuntimeError as exc:
        print(f"\n[error] {exc}", file=sys.stderr)
        print_manual_steps(args.image, args.port, args.name)
        sys.exit(1)

    except TimeoutError as exc:
        print(f"\n[timeout] {exc}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n[cancelled]")
        sys.exit(0)


if __name__ == "__main__":
    main()
