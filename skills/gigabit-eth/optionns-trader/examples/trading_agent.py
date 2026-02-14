"""
Complete example of how to use the Optionns Trader skill in your agent.

This shows the full flow from registration to executing trades with on-chain settlement.
"""
import json
import requests
from pathlib import Path

# Add script directory to path to import signer
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from signer import sign_and_submit_transaction


class OptionnsTradingAgent:
    """Example agent that trades sports options via Optionns API."""
    
    def __init__(self, api_key: str, keypair_path: str):
        self.api_key = api_key
        self.keypair_path = Path(keypair_path).expanduser()
        self.api_base = "https://api.optionns.com"
        self.rpc_url = "https://api.devnet.solana.com"
    
    def _api_call(self, method: str, endpoint: str, data: dict = None):
        """Make authenticated API call."""
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        url = f"{self.api_base}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    def get_live_games(self, sport: str = "NBA"):
        """Fetch live games."""
        return self._api_call("GET", f"/v1/sports/events?sport={sport}")
    
    def get_quote(self, token_id: str, underlying: float, strike: float, 
                  quantity: int = 5, expiry_minutes: int = 5):
        """Get option quote."""
        return self._api_call("POST", "/v1/vault/quote", {
            "token_id": token_id,
            "underlying_price": underlying,
            "strike": strike,
            "option_type": "call",
            "sport": "nba",
            "quantity": quantity,
            "expiry_minutes": expiry_minutes
        })
    
    def execute_trade(self, quote_id: str, game_id: str, game_title: str,
                      token_id: str, underlying: float, strike: float,
                      quantity: int, wallet: str):
        """
        Execute a trade and settle on-chain.
        
        Returns:
            dict with tx_signature, position_id, and other trade details
        """
        # Step 1: Call buy endpoint (returns unsigned transaction)
        buy_response = self._api_call("POST", "/v1/vault/buy", {
            "quote_id": quote_id,
            "token_id": token_id,
            "game_id": game_id,
            "game_title": game_title,
            "sport": "nba",
            "underlying_price": underlying,
            "strike": strike,
            "option_type": "call",
            "quantity": quantity,
            "expiry_minutes": 5,
            "barrier_type": "lead_margin_home",
            "barrier_target": 10,
            "barrier_direction": "above",
            "user_pubkey": wallet,
            "user_ata": wallet  # Can be same as pubkey for devnet
        })
        
        # Step 2: Sign and submit the transaction
        tx_signature = sign_and_submit_transaction(
            unsigned_tx=buy_response['unsigned_tx'],
            blockhash=buy_response['blockhash'],
            keypair_path=str(self.keypair_path),
            rpc_url=self.rpc_url
        )
        
        return {
            "tx_signature": tx_signature,
            "position_id": buy_response['position_id'],
            "position_pda": buy_response.get('position_pda'),
            "explorer_url": f"https://explorer.solana.com/tx/{tx_signature}?cluster=devnet"
        }
    
    def get_positions(self):
        """Fetch your active positions."""
        return self._api_call("GET", "/v1/vault/positions")


def main():
    """Example usage."""
    # Initialize agent
    agent = OptionnsTradingAgent(
        api_key="YOUR_API_KEY",
        keypair_path="~/.config/optionns/agent_keypair.json"
    )
    
    # 1. Find live games
    games = agent.get_live_games("NBA")
    print(f"Found {len(games.get('data', {}).get('live', []))} live games")
    
    # 2. Get a quote
    quote = agent.get_quote(
        token_id="token_401584123",
        underlying=0.55,
        strike=0.50,
        quantity=5
    )
    print(f"Quote: {quote['premium']} USDC premium")
    
    # 3. Execute trade
    result = agent.execute_trade(
        quote_id=quote['quote_id'],
        game_id="401584123",
        game_title="Lakers vs Celtics",
        token_id="token_401584123",
        underlying=0.55,
        strike=0.50,
        quantity=5,
        wallet="YOUR_SOLANA_WALLET"
    )
    
    print(f"✅ Trade executed!")
    print(f"Position ID: {result['position_id']}")
    print(f"Tx Signature: {result['tx_signature']}")
    print(f"Explorer: {result['explorer_url']}")
    
    # 4. Check positions
    positions = agent.get_positions()
    print(f"Active positions: {len(positions.get('positions', []))}")


if __name__ == "__main__":
    main()
