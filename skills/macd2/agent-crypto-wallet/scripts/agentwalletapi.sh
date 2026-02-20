#!/bin/bash
# OpenclawCash CLI Tool
# Usage: ./agentwalletapi.sh <command> [options]
#
# Commands:
#   wallets                     List all wallets
#   transactions <walletId> [chain]     List merged transaction history for a wallet
#   balance <walletId> [token] [chain]  Check balances for a wallet
#   transfer <walletId> <to> <amount> [token] [chain]   Send native/token transfer
#   tokens [network] [chain]            List supported tokens (default: mainnet)
#   quote <network> <tokenIn> <tokenOut> <amountInBaseUnits> [chain]   Get swap quote
#   swap <walletId> <tokenIn> <tokenOut> <amountInBaseUnits> [slippage] [chain]
#   approve <walletId> <tokenAddress> <spender> <amountBaseUnits> [chain]   Approve ERC-20 allowance

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$SKILL_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found. Run setup first:"
    echo "  bash $SKILL_DIR/scripts/setup.sh"
    exit 1
fi

source "$ENV_FILE"

if [ -z "$AGENTWALLETAPI_KEY" ] || [ "$AGENTWALLETAPI_KEY" = "ag_your_api_key_here" ]; then
    echo "Error: API key not configured. Edit $ENV_FILE and set AGENTWALLETAPI_KEY."
    exit 1
fi

BASE_URL="${AGENTWALLETAPI_URL:-https://openclawcash.com}"
COMMAND="$1"

case "$COMMAND" in
    wallets)
        curl -s -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            "$BASE_URL/api/agent/wallets" | python3 -m json.tool 2>/dev/null || \
        curl -s -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            "$BASE_URL/api/agent/wallets"
        ;;

    transactions)
        WALLET_ID="$2"
        CHAIN="$3"
        if [ -z "$WALLET_ID" ]; then
            echo "Usage: agentwalletapi.sh transactions <walletId> [chain]"
            exit 1
        fi
        URL="$BASE_URL/api/agent/transactions?walletId=$WALLET_ID"
        if [ -n "$CHAIN" ]; then
            URL="$URL&chain=$CHAIN"
        fi
        curl -s -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            "$URL" | python3 -m json.tool 2>/dev/null || \
        curl -s -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            "$URL"
        ;;

    balance)
        WALLET_ID="$2"
        TOKEN_FILTER="$3"
        CHAIN="$4"
        if [ -z "$WALLET_ID" ]; then
            echo "Usage: agentwalletapi.sh balance <walletId> [token] [chain]"
            exit 1
        fi
        BODY="{\"walletId\": $WALLET_ID"
        if [ -n "$TOKEN_FILTER" ]; then
            BODY="$BODY, \"token\": \"$TOKEN_FILTER\""
        fi
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$CHAIN\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/token-balance" | python3 -m json.tool 2>/dev/null || \
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/token-balance"
        ;;

    transfer)
        WALLET_ID="$2"
        TO="$3"
        AMOUNT="$4"
        TOKEN="${5:-ETH}"
        CHAIN="$6"
        if [ -z "$WALLET_ID" ] || [ -z "$TO" ] || [ -z "$AMOUNT" ]; then
            echo "Usage: agentwalletapi.sh transfer <walletId> <to> <amount> [token] [chain]"
            echo "  token defaults to the wallet's native token (ETH/SOL) if not specified"
            exit 1
        fi
        BODY="{\"walletId\": $WALLET_ID, \"to\": \"$TO\", \"amount\": \"$AMOUNT\""
        if [ "$TOKEN" != "ETH" ]; then
            BODY="$BODY, \"token\": \"$TOKEN\""
        fi
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$CHAIN\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/transfer" | python3 -m json.tool 2>/dev/null || \
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/transfer"
        ;;

    tokens)
        NETWORK="${2:-mainnet}"
        CHAIN="$3"
        URL="$BASE_URL/api/agent/supported-tokens?network=$NETWORK"
        if [ -n "$CHAIN" ]; then
            URL="$URL&chain=$CHAIN"
        fi
        curl -s "$URL" | python3 -m json.tool 2>/dev/null || \
        curl -s "$URL"
        ;;

    quote)
        NETWORK="$2"
        TOKEN_IN="$3"
        TOKEN_OUT="$4"
        AMOUNT_IN="$5"
        CHAIN="$6"
        if [ -z "$NETWORK" ] || [ -z "$TOKEN_IN" ] || [ -z "$TOKEN_OUT" ] || [ -z "$AMOUNT_IN" ]; then
            echo "Usage: agentwalletapi.sh quote <network> <tokenIn> <tokenOut> <amountInBaseUnits> [chain]"
            exit 1
        fi
        BODY="{\"tokenIn\":\"$TOKEN_IN\",\"tokenOut\":\"$TOKEN_OUT\",\"amountIn\":\"$AMOUNT_IN\""
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$CHAIN\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/quote?network=$NETWORK" | python3 -m json.tool 2>/dev/null || \
        curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/quote?network=$NETWORK"
        ;;

    swap)
        WALLET_ID="$2"
        TOKEN_IN="$3"
        TOKEN_OUT="$4"
        AMOUNT_IN="$5"
        SLIPPAGE="${6:-0.5}"
        CHAIN="$7"
        if [ -z "$WALLET_ID" ] || [ -z "$TOKEN_IN" ] || [ -z "$TOKEN_OUT" ] || [ -z "$AMOUNT_IN" ]; then
            echo "Usage: agentwalletapi.sh swap <walletId> <tokenIn> <tokenOut> <amountInBaseUnits> [slippage] [chain]"
            exit 1
        fi
        BODY="{\"walletId\":$WALLET_ID,\"tokenIn\":\"$TOKEN_IN\",\"tokenOut\":\"$TOKEN_OUT\",\"amountIn\":\"$AMOUNT_IN\",\"slippage\":$SLIPPAGE"
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$CHAIN\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/swap" | python3 -m json.tool 2>/dev/null || \
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/swap"
        ;;

    approve)
        WALLET_ID="$2"
        TOKEN_ADDRESS="$3"
        SPENDER="$4"
        AMOUNT="$5"
        CHAIN="$6"
        if [ -z "$WALLET_ID" ] || [ -z "$TOKEN_ADDRESS" ] || [ -z "$SPENDER" ] || [ -z "$AMOUNT" ]; then
            echo "Usage: agentwalletapi.sh approve <walletId> <tokenAddress> <spender> <amountBaseUnits> [chain]"
            exit 1
        fi
        BODY="{\"walletId\":$WALLET_ID,\"tokenAddress\":\"$TOKEN_ADDRESS\",\"spender\":\"$SPENDER\",\"amount\":\"$AMOUNT\""
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$CHAIN\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/approve" | python3 -m json.tool 2>/dev/null || \
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/approve"
        ;;

    *)
        echo "OpenclawCash CLI Tool"
        echo ""
        echo "Usage: agentwalletapi.sh <command> [options]"
        echo ""
        echo "Commands:"
        echo "  wallets                                    List all wallets"
        echo "  transactions <walletId> [chain]                    List wallet transaction history"
        echo "  balance <walletId> [token] [chain]                 Check balances"
        echo "  transfer <walletId> <to> <amount> [token] [chain]  Send native/token transfer"
        echo "  tokens [network] [chain]                           List supported tokens"
        echo "  quote <network> <tokenIn> <tokenOut> <amountInBaseUnits> [chain]  Get swap quote"
        echo "  swap <walletId> <tokenIn> <tokenOut> <amountInBaseUnits> [slippage] [chain]  Execute swap"
        echo "  approve <walletId> <tokenAddress> <spender> <amountBaseUnits> [chain]  Approve allowance"
        echo ""
        echo "Examples:"
        echo "  agentwalletapi.sh wallets"
        echo "  agentwalletapi.sh transactions 2"
        echo "  agentwalletapi.sh balance 2"
        echo "  agentwalletapi.sh transfer 2 0xRecipient 0.01"
        echo "  agentwalletapi.sh transfer 2 0xRecipient 100 USDC"
        echo "  agentwalletapi.sh tokens mainnet"
        echo "  agentwalletapi.sh quote mainnet WETH USDC 10000000000000000"
        echo "  agentwalletapi.sh swap 2 ETH USDC 10000000000000000 0.5"
        echo "  agentwalletapi.sh approve 2 0xA0b86991... 0xSpender... 1000000000"
        ;;
esac
