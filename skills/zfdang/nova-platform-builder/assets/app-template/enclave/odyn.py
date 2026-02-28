"""
odyn.py — Odyn Internal API wrapper.
Auto-switches between production (localhost:18000) and mock (odyn.sparsity.cloud:18000).
Copy this file as-is; do not modify the base URL logic.
"""
from __future__ import annotations
import base64, json, os
from typing import Any
import httpx

IN_ENCLAVE = os.getenv("IN_ENCLAVE", "false").lower() == "true"
_BASE = "http://localhost:18000" if IN_ENCLAVE else "http://odyn.sparsity.cloud:18000"


class OdynError(Exception):
    pass


class Odyn:
    def __init__(self, timeout: float = 15.0):
        self._c = httpx.Client(base_url=_BASE, timeout=timeout)

    # ── Identity ───────────────────────────────────────────────────────────────
    def eth_address(self) -> dict:
        return self._get("/v1/eth/address")

    # ── Signing ────────────────────────────────────────────────────────────────
    def sign_message(self, payload: dict) -> dict:
        return self._post("/v1/eth/sign", {"data": json.dumps(payload)})

    def sign_transaction(self, tx: dict) -> dict:
        return self._post("/v1/eth/sign-tx", {"transaction": tx})

    # ── Randomness ─────────────────────────────────────────────────────────────
    def get_random_bytes(self, length: int = 32) -> bytes:
        r = self._get(f"/v1/random?length={length}")
        return base64.b64decode(r["random"])

    # ── Attestation ────────────────────────────────────────────────────────────
    def get_attestation(self, user_data: bytes | None = None) -> dict:
        body: dict[str, Any] = {}
        if user_data:
            body["user_data"] = base64.b64encode(user_data).decode()
        return self._post("/v1/attestation", body)

    # ── Encryption ─────────────────────────────────────────────────────────────
    def encryption_public_key(self) -> dict:
        return self._get("/v1/encryption/public_key")

    def encrypt(self, plaintext: bytes, client_pubkey: str) -> dict:
        return self._post("/v1/encryption/encrypt", {
            "plaintext": base64.b64encode(plaintext).decode(),
            "client_public_key": client_pubkey,
        })

    def decrypt(self, ciphertext: str, nonce: str, tag: str) -> bytes:
        r = self._post("/v1/encryption/decrypt", {"ciphertext": ciphertext, "nonce": nonce, "tag": tag})
        return base64.b64decode(r["plaintext"])

    # ── S3 Storage ─────────────────────────────────────────────────────────────
    def s3_put(self, key: str, value: bytes) -> dict:
        return self._post("/v1/s3/put", {"key": key, "value": base64.b64encode(value).decode()})

    def s3_get(self, key: str) -> bytes:
        return base64.b64decode(self._post("/v1/s3/get", {"key": key})["value"])

    def s3_list(self, prefix: str = "") -> list[str]:
        return self._post("/v1/s3/list", {"prefix": prefix}).get("keys", [])

    def s3_delete(self, key: str) -> dict:
        return self._post("/v1/s3/delete", {"key": key})

    # ── KMS ────────────────────────────────────────────────────────────────────
    def kms_derive_key(self, app_id: int, context: str) -> dict:
        return self._post("/v1/kms/derive", {"app_id": app_id, "context": context})

    # ── Internals ──────────────────────────────────────────────────────────────
    def _get(self, path: str) -> dict:
        try:
            r = self._c.get(path)
        except httpx.RequestError as e:
            raise OdynError(f"GET {path}: {e}") from e
        if not r.is_success:
            raise OdynError(f"GET {path} → {r.status_code}: {r.text[:300]}")
        return r.json()

    def _post(self, path: str, body: dict) -> dict:
        try:
            r = self._c.post(path, json=body)
        except httpx.RequestError as e:
            raise OdynError(f"POST {path}: {e}") from e
        if not r.is_success:
            raise OdynError(f"POST {path} → {r.status_code}: {r.text[:300]}")
        return r.json()
