#!/bin/bash
# OpenclawCash CLI Tool
# Usage: ./agentwalletapi.sh <command> [options]
#
# Requirements: curl (jq optional for pretty output)
# Sensitive env var: AGENTWALLETAPI_KEY (in .env)
#
# Commands:
#   wallets                     List all wallets
#   wallet <walletId|walletLabel> [chain]   Get one wallet detail with balances
#   create <label> [network] [--yes]    Create a wallet (default network: sepolia)
#   import <label> <network> [privateKey] [--yes]   Import wallet (network: mainnet|solana-mainnet)
#   transactions <walletId> [chain]     List merged transaction history for a wallet
#   balance <walletId> [token] [chain]  Check balances for a wallet
#   transfer <walletId> <to> <amount> [token] [chain] [--yes]   Send native/token transfer
#   tokens [network] [chain]            List supported tokens (default: mainnet)
#   quote <network> <tokenIn> <tokenOut> <amountInBaseUnits> [chain]   Get swap quote
#   swap <walletId> <tokenIn> <tokenOut> <amountInBaseUnits> [slippage] [chain] [--yes]
#   approve <walletId> <tokenAddress> <spender> <amountBaseUnits> [chain] [--yes]   Approve ERC-20 allowance

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

if ! command -v curl >/dev/null 2>&1; then
    echo "Error: curl is required but not installed."
    exit 1
fi

BASE_URL="${AGENTWALLETAPI_URL:-https://openclawcash.com}"

FORCE_RISKY=0
FILTERED_ARGS=()
for arg in "$@"; do
    if [ "$arg" = "--yes" ]; then
        FORCE_RISKY=1
    else
        FILTERED_ARGS+=("$arg")
    fi
done
set -- "${FILTERED_ARGS[@]}"
COMMAND="$1"

json_escape() {
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

require_uint() {
    NAME="$1"
    VALUE="$2"
    if ! [[ "$VALUE" =~ ^[0-9]+$ ]]; then
        echo "Error: $NAME must be an unsigned integer."
        exit 1
    fi
}

require_decimal() {
    NAME="$1"
    VALUE="$2"
    if ! [[ "$VALUE" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
        echo "Error: $NAME must be a number."
        exit 1
    fi
}

pretty_print_json() {
    if command -v jq >/dev/null 2>&1; then
        jq . 2>/dev/null || cat
    else
        cat
    fi
}

confirm_risky_action() {
    ACTION="$1"
    if [ "$FORCE_RISKY" -eq 1 ]; then
        return 0
    fi

    if [ ! -t 0 ]; then
        echo "Error: $ACTION is a high-risk action. Re-run with --yes to confirm."
        exit 1
    fi

    echo "WARNING: $ACTION can move funds or import sensitive keys."
    echo "Target API host: $BASE_URL"
    printf "Type YES to continue: "
    read -r ANSWER
    if [ "$ANSWER" != "YES" ]; then
        echo "Cancelled."
        exit 1
    fi
}

case "$COMMAND" in
    wallets)
        curl -s -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            "$BASE_URL/api/agent/wallets" | pretty_print_json
        ;;

    wallet)
        SELECTOR="$2"
        CHAIN="$3"
        if [ -z "$SELECTOR" ]; then
            echo "Usage: agentwalletapi.sh wallet <walletId|walletLabel> [chain]"
            exit 1
        fi
        if echo "$SELECTOR" | grep -Eq '^[0-9]+$'; then
            URL="$BASE_URL/api/agent/wallet?walletId=$SELECTOR"
        else
            URL="$BASE_URL/api/agent/wallet?walletLabel=$(printf '%s' "$SELECTOR" | sed 's/ /%20/g')"
        fi
        if [ -n "$CHAIN" ]; then
            URL="$URL&chain=$CHAIN"
        fi
        curl -s -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            "$URL" | pretty_print_json
        ;;

    create)
        confirm_risky_action "Wallet creation"
        LABEL="$2"
        NETWORK="${3:-sepolia}"
        if [ -z "$LABEL" ]; then
            echo "Usage: agentwalletapi.sh create <label> [network] [--yes]"
            echo "  network options: sepolia | mainnet | solana-devnet | solana-testnet | solana-mainnet"
            exit 1
        fi
        BODY="{\"label\":\"$(json_escape "$LABEL")\",\"network\":\"$NETWORK\"}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/wallets/create" | pretty_print_json
        ;;

    import)
        confirm_risky_action "Wallet import"
        LABEL="$2"
        NETWORK="$3"
        PRIVATE_KEY="$4"
        if [ -z "$LABEL" ] || [ -z "$NETWORK" ]; then
            echo "Usage: agentwalletapi.sh import <label> <network> [privateKey] [--yes]"
            echo "  network options: mainnet | solana-mainnet"
            exit 1
        fi
        if [ -z "$PRIVATE_KEY" ]; then
            if [ ! -t 0 ]; then
                echo "Error: private key missing. Provide as argument or run interactively to be prompted."
                exit 1
            fi
            printf "Enter private key (input hidden): "
            stty -echo
            read -r PRIVATE_KEY
            stty echo
            echo ""
        fi
        BODY="{\"label\":\"$(json_escape "$LABEL")\",\"network\":\"$NETWORK\",\"privateKey\":\"$(json_escape "$PRIVATE_KEY")\"}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/wallets/import" | pretty_print_json
        ;;

    transactions)
        WALLET_ID="$2"
        CHAIN="$3"
        if [ -z "$WALLET_ID" ]; then
            echo "Usage: agentwalletapi.sh transactions <walletId> [chain]"
            exit 1
        fi
        require_uint "walletId" "$WALLET_ID"
        URL="$BASE_URL/api/agent/transactions?walletId=$WALLET_ID"
        if [ -n "$CHAIN" ]; then
            URL="$URL&chain=$CHAIN"
        fi
        curl -s -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            "$URL" | pretty_print_json
        ;;

    balance)
        WALLET_ID="$2"
        TOKEN_FILTER="$3"
        CHAIN="$4"
        if [ -z "$WALLET_ID" ]; then
            echo "Usage: agentwalletapi.sh balance <walletId> [token] [chain]"
            exit 1
        fi
        require_uint "walletId" "$WALLET_ID"
        BODY="{\"walletId\": $WALLET_ID"
        if [ -n "$TOKEN_FILTER" ]; then
            BODY="$BODY, \"token\": \"$(json_escape "$TOKEN_FILTER")\""
        fi
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$(json_escape "$CHAIN")\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/token-balance" | pretty_print_json
        ;;

    transfer)
        confirm_risky_action "Transfer"
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
        require_uint "walletId" "$WALLET_ID"
        BODY="{\"walletId\": $WALLET_ID, \"to\": \"$(json_escape "$TO")\", \"amount\": \"$(json_escape "$AMOUNT")\""
        if [ "$TOKEN" != "ETH" ]; then
            BODY="$BODY, \"token\": \"$(json_escape "$TOKEN")\""
        fi
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$(json_escape "$CHAIN")\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/transfer" | pretty_print_json
        ;;

    tokens)
        NETWORK="${2:-mainnet}"
        CHAIN="$3"
        URL="$BASE_URL/api/agent/supported-tokens?network=$NETWORK"
        if [ -n "$CHAIN" ]; then
            URL="$URL&chain=$CHAIN"
        fi
        curl -s "$URL" | pretty_print_json
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
        BODY="{\"tokenIn\":\"$(json_escape "$TOKEN_IN")\",\"tokenOut\":\"$(json_escape "$TOKEN_OUT")\",\"amountIn\":\"$(json_escape "$AMOUNT_IN")\""
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$(json_escape "$CHAIN")\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/quote?network=$NETWORK" | pretty_print_json
        ;;

    swap)
        confirm_risky_action "Swap"
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
        require_uint "walletId" "$WALLET_ID"
        require_decimal "slippage" "$SLIPPAGE"
        BODY="{\"walletId\":$WALLET_ID,\"tokenIn\":\"$(json_escape "$TOKEN_IN")\",\"tokenOut\":\"$(json_escape "$TOKEN_OUT")\",\"amountIn\":\"$(json_escape "$AMOUNT_IN")\",\"slippage\":$SLIPPAGE"
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$(json_escape "$CHAIN")\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/swap" | pretty_print_json
        ;;

    approve)
        confirm_risky_action "Token approval"
        WALLET_ID="$2"
        TOKEN_ADDRESS="$3"
        SPENDER="$4"
        AMOUNT="$5"
        CHAIN="$6"
        if [ -z "$WALLET_ID" ] || [ -z "$TOKEN_ADDRESS" ] || [ -z "$SPENDER" ] || [ -z "$AMOUNT" ]; then
            echo "Usage: agentwalletapi.sh approve <walletId> <tokenAddress> <spender> <amountBaseUnits> [chain]"
            exit 1
        fi
        require_uint "walletId" "$WALLET_ID"
        BODY="{\"walletId\":$WALLET_ID,\"tokenAddress\":\"$(json_escape "$TOKEN_ADDRESS")\",\"spender\":\"$(json_escape "$SPENDER")\",\"amount\":\"$(json_escape "$AMOUNT")\""
        if [ -n "$CHAIN" ]; then
            BODY="$BODY, \"chain\": \"$(json_escape "$CHAIN")\""
        fi
        BODY="$BODY}"
        curl -s -X POST \
            -H "X-Agent-Key: $AGENTWALLETAPI_KEY" \
            -H "Content-Type: application/json" \
            -d "$BODY" \
            "$BASE_URL/api/agent/approve" | pretty_print_json
        ;;

    *)
        echo "OpenclawCash CLI Tool"
        echo ""
        echo "Usage: agentwalletapi.sh <command> [options]"
        echo ""
        echo "Commands:"
        echo "  wallets                                    List all wallets"
        echo "  wallet <walletId|walletLabel> [chain]              Get one wallet detail with balances"
        echo "  create <label> [network] [--yes]                   Create wallet (default network: sepolia)"
        echo "  import <label> <network> [privateKey] [--yes]      Import wallet (mainnet|solana-mainnet)"
        echo "  transactions <walletId> [chain]                    List wallet transaction history"
        echo "  balance <walletId> [token] [chain]                 Check balances"
        echo "  transfer <walletId> <to> <amount> [token] [chain] [--yes]  Send native/token transfer"
        echo "  tokens [network] [chain]                           List supported tokens"
        echo "  quote <network> <tokenIn> <tokenOut> <amountInBaseUnits> [chain]  Get swap quote"
        echo "  swap <walletId> <tokenIn> <tokenOut> <amountInBaseUnits> [slippage] [chain] [--yes]  Execute swap"
        echo "  approve <walletId> <tokenAddress> <spender> <amountBaseUnits> [chain] [--yes]  Approve allowance"
        echo ""
        echo "Examples:"
        echo "  agentwalletapi.sh wallets"
        echo "  agentwalletapi.sh create 'Ops Wallet' sepolia --yes"
        echo "  agentwalletapi.sh import 'Treasury Imported' mainnet --yes"
        echo "  agentwalletapi.sh transactions 2"
        echo "  agentwalletapi.sh balance 2"
        echo "  agentwalletapi.sh transfer 2 0xRecipient 0.01 --yes"
        echo "  agentwalletapi.sh transfer 2 0xRecipient 100 USDC --yes"
        echo "  agentwalletapi.sh tokens mainnet"
        echo "  agentwalletapi.sh quote mainnet WETH USDC 10000000000000000"
        echo "  agentwalletapi.sh swap 2 ETH USDC 10000000000000000 0.5 --yes"
        echo "  agentwalletapi.sh approve 2 0xA0b86991... 0xSpender... 1000000000 --yes"
        ;;
esac
