#!/usr/bin/env python3
"""
signer.py — Helper for OpenClaw agents to sign and submit Solana transactions.

Usage in agent code:
    from signer import sign_and_submit_transaction
    
    # After receiving unsigned_tx from API
    tx_sig = sign_and_submit_transaction(
        unsigned_tx=response['unsigned_tx'],
        blockhash=response['blockhash'],
        keypair_path='~/.config/optionns/agent_keypair.json',
        rpc_url='https://api.devnet.solana.com'
    )
"""
import json
import base64
import time
from typing import Optional
from pathlib import Path
import urllib.request
import urllib.error


def sign_and_submit_transaction(
    unsigned_tx: str,
    blockhash: str,
    keypair_path: str,
    rpc_url: str = "https://api.devnet.solana.com",
    timeout: int = 30
) -> str:
    """
    Sign an unsigned Solana transaction and submit to RPC.
    
    Args:
        unsigned_tx: Base64-encoded unsigned transaction message
        blockhash: Recent blockhash
        keypair_path: Path to Solana keypair JSON file
        rpc_url: Solana RPC endpoint
        timeout: Max seconds to wait for confirmation
        
    Returns:
        Transaction signature on success
        
    Raises:
        Exception: If signing or submission fails
    """
    try:
        from solders.keypair import Keypair
        from solders.transaction import Transaction
        from solders.message import Message
    except ImportError:
        raise ImportError(
            "solders library required. Install with: pip install solders"
        )
    
    # Load keypair
    keypair_path = Path(keypair_path).expanduser()
    if not keypair_path.exists():
        raise FileNotFoundError(f"Keypair not found: {keypair_path}")
    
    with open(keypair_path, "r") as f:
        secret = json.load(f)
    
    kp = Keypair.from_bytes(bytes(secret))
    
    # Deserialize the unsigned message
    msg_bytes = base64.b64decode(unsigned_tx)
    msg = Message.from_bytes(msg_bytes)
    
    # Sign message and assemble Transaction
    sig = kp.sign_message(bytes(msg))
    tx = Transaction.populate(msg, [sig])
    
    # Serialize signed tx
    tx_bytes = bytes(tx)
    tx_b64 = base64.b64encode(tx_bytes).decode("ascii")
    
    # Submit via JSON-RPC
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [
            tx_b64,
            {"encoding": "base64", "preflightCommitment": "confirmed"}
        ]
    }).encode("utf-8")
    
    req = urllib.request.Request(
        rpc_url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise Exception(f"RPC request failed: {e}")
    
    if "error" in result:
        raise Exception(f"RPC error: {result['error']}")
    
    tx_sig = result.get("result", "")
    
    # Confirm the tx landed (poll for up to timeout seconds)
    for _ in range(timeout // 2):
        time.sleep(2)
        confirm_payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "getSignatureStatuses",
            "params": [[tx_sig], {"searchTransactionHistory": True}]
        }).encode("utf-8")
        
        confirm_req = urllib.request.Request(
            rpc_url,
            data=confirm_payload,
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(confirm_req, timeout=10) as resp:
                confirm_result = json.loads(resp.read().decode())
            
            statuses = confirm_result.get("result", {}).get("value", [None])
            if statuses and statuses[0] is not None:
                if statuses[0].get("err"):
                    raise Exception(f"Transaction failed on-chain: {statuses[0]['err']}")
                # Confirmed!
                return tx_sig
        except Exception:
            continue
    
    # Timed out waiting for confirmation
    raise Exception(f"Transaction submitted but not confirmed after {timeout}s: {tx_sig}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <keypair_file> <unsigned_tx_b64> <blockhash> [rpc_url]", file=sys.stderr)
        sys.exit(1)
    
    keypair_file = sys.argv[1]
    unsigned_b64 = sys.argv[2]
    blockhash_str = sys.argv[3]
    rpc_url = sys.argv[4] if len(sys.argv) > 4 else "https://api.devnet.solana.com"
    
    try:
        tx_sig = sign_and_submit_transaction(
            unsigned_tx=unsigned_b64,
            blockhash=blockhash_str,
            keypair_path=keypair_file,
            rpc_url=rpc_url
        )
        print(tx_sig)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
