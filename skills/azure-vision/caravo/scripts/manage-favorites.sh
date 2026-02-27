#!/usr/bin/env bash
# Caravo - Local Favorites Manager
# Manage local favorites at ~/.caravo/favorites.json

set -euo pipefail

FAVORITES_DIR="$HOME/.caravo"
FAVORITES_FILE="$FAVORITES_DIR/favorites.json"
BASE_URL="${CARAVO_URL:-https://caravo.ai}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
err() { echo -e "${RED}Error:${NC} $*" >&2; exit 1; }
info() { echo -e "${GREEN}$*${NC}"; }
warn() { echo -e "${YELLOW}$*${NC}"; }

# Validate tool_id: alphanumeric, hyphens, underscores, dots, and one optional slash for namespaced IDs
validate_tool_id() {
  local tool_id="$1"
  if [[ ! "$tool_id" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*(\/[a-zA-Z0-9][a-zA-Z0-9._-]*)?$ ]]; then
    err "Invalid tool_id '$tool_id'. Must be alphanumeric with hyphens/underscores/dots, optionally namespaced (e.g., 'flux-schnell' or 'alice/imagen-4')"
  fi
  if [[ ${#tool_id} -gt 100 ]]; then
    err "tool_id too long (${#tool_id} chars, max 100)"
  fi
}

# Validate favorites JSON file is readable and .favorites is an array
validate_file() {
  if ! jq -e '.favorites | type == "array"' "$FAVORITES_FILE" >/dev/null 2>&1; then
    err "Favorites file is corrupted. Delete and re-init:\n  rm $FAVORITES_FILE && $0 init"
  fi
}

# Check dependencies
check_deps() {
  command -v jq >/dev/null 2>&1 || err "jq is required. Install: brew install jq (macOS) or apt install jq (Linux)"
}

# Initialize favorites file
init() {
  if [[ -f "$FAVORITES_FILE" ]]; then
    warn "Favorites file already exists at $FAVORITES_FILE"
    return 0
  fi
  mkdir -p "$FAVORITES_DIR"
  echo '{"version":"1.0.0","favorites":[]}' > "$FAVORITES_FILE"
  info "✓ Created favorites file at $FAVORITES_FILE"
}

# List all favorites, optionally validating against server with --validate flag
list() {
  [[ -f "$FAVORITES_FILE" ]] || err "No favorites file. Run: $0 init"
  validate_file
  local count=$(jq -r '.favorites | length' "$FAVORITES_FILE")
  if [[ "$count" -eq 0 ]]; then
    warn "No favorites yet. Add one: $0 add <tool_id>"
    return 0
  fi
  info "Your favorites ($count):"
  local idx=0
  local invalid_count=0
  while IFS= read -r tool_id; do
    ((idx++))
    if [[ "${1:-}" == "--validate" ]]; then
      if verify_tool_exists "$tool_id"; then
        printf "%2d. %s\n" "$idx" "$tool_id"
      else
        printf "%2d. %s ${RED}(not found on server)${NC}\n" "$idx" "$tool_id"
        ((invalid_count++))
      fi
    else
      printf "%2d. %s\n" "$idx" "$tool_id"
    fi
  done < <(jq -r '.favorites[]' "$FAVORITES_FILE")
  if [[ "$invalid_count" -gt 0 ]]; then
    warn "\n$invalid_count favorite(s) not found on server. Use '$0 remove <tool_id>' to clean up."
  fi
}

# Verify a tool_id exists on the server (returns 0 if valid, 1 if not)
verify_tool_exists() {
  local tool_id="$1"
  local http_code
  http_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/tools/$tool_id")
  [[ "$http_code" == "200" ]]
}

# Add a favorite
add() {
  local tool_id="${1:-}"
  [[ -n "$tool_id" ]] || err "Usage: $0 add <tool_id>"
  validate_tool_id "$tool_id"
  [[ -f "$FAVORITES_FILE" ]] || init
  validate_file

  # Check if already exists
  if jq -e --arg id "$tool_id" '.favorites | index($id)' "$FAVORITES_FILE" >/dev/null; then
    warn "$tool_id is already in favorites"
    return 0
  fi

  # Verify tool exists on the server before adding
  if ! verify_tool_exists "$tool_id"; then
    err "Tool '$tool_id' not found on the server. Check the tool ID and try again."
  fi

  # Add and deduplicate
  if jq --arg id "$tool_id" '.favorites += [$id] | .favorites |= unique' \
    "$FAVORITES_FILE" > "$FAVORITES_FILE.tmp"; then
    mv "$FAVORITES_FILE.tmp" "$FAVORITES_FILE"
    info "✓ Added $tool_id to favorites"
  else
    rm -f "$FAVORITES_FILE.tmp"
    err "Failed to update favorites file"
  fi
}

# Remove a favorite
remove() {
  local tool_id="${1:-}"
  [[ -n "$tool_id" ]] || err "Usage: $0 remove <tool_id>"
  validate_tool_id "$tool_id"
  [[ -f "$FAVORITES_FILE" ]] || err "No favorites file"
  validate_file

  # Check if exists before removing
  if ! jq -e --arg id "$tool_id" '.favorites | index($id)' "$FAVORITES_FILE" >/dev/null 2>&1; then
    warn "$tool_id is not in favorites"
    return 0
  fi

  if jq --arg id "$tool_id" '.favorites -= [$id]' \
    "$FAVORITES_FILE" > "$FAVORITES_FILE.tmp"; then
    mv "$FAVORITES_FILE.tmp" "$FAVORITES_FILE"
    info "✓ Removed $tool_id from favorites"
  else
    rm -f "$FAVORITES_FILE.tmp"
    err "Failed to update favorites file"
  fi
}

# Check if a tool is favorited
check() {
  local tool_id="${1:-}"
  [[ -n "$tool_id" ]] || err "Usage: $0 check <tool_id>"
  validate_tool_id "$tool_id"
  [[ -f "$FAVORITES_FILE" ]] || { echo "No"; return 1; }
  validate_file

  if jq -e --arg id "$tool_id" '.favorites | index($id)' "$FAVORITES_FILE" >/dev/null; then
    echo "Yes"
    return 0
  else
    echo "No"
    return 1
  fi
}

# Sync from server to local
sync_from_server() {
  local api_key="${CARAVO_API_KEY:-}"
  [[ -n "$api_key" ]] || err "CARAVO_API_KEY is required for sync"

  info "Fetching favorites from server..."
  local response=$(curl -s -H "Authorization: Bearer $api_key" \
    "$BASE_URL/api/favorites")

  # Extract tool IDs
  local ids=$(echo "$response" | jq -r '.data[]?.id // empty')
  [[ -n "$ids" ]] || { warn "No favorites on server"; return 0; }

  # Build favorites array
  local favorites_array=$(echo "$ids" | jq -R -s 'split("\n") | map(select(length > 0))')

  # Update local file
  [[ -f "$FAVORITES_FILE" ]] || init
  jq --argjson favs "$favorites_array" '.favorites = $favs' \
    "$FAVORITES_FILE" > "$FAVORITES_FILE.tmp" && \
    mv "$FAVORITES_FILE.tmp" "$FAVORITES_FILE"

  local count=$(echo "$ids" | wc -l | xargs)
  info "✓ Synced $count favorites from server to local"
}

# Sync from local to server
sync_to_server() {
  local api_key="${CARAVO_API_KEY:-}"
  [[ -n "$api_key" ]] || err "CARAVO_API_KEY is required for sync"
  [[ -f "$FAVORITES_FILE" ]] || err "No local favorites file"
  validate_file

  info "Uploading favorites to server..."
  local count=0
  local skipped=0
  while IFS= read -r tool_id; do
    # Validate tool_id format before sending
    if [[ ! "$tool_id" =~ ^[a-zA-Z0-9][a-zA-Z0-9._/-]*$ ]] || [[ ${#tool_id} -gt 100 ]]; then
      warn "Skipping invalid tool_id: $tool_id"
      ((skipped++))
      continue
    fi
    # Use jq to safely JSON-encode the tool_id
    local json_body
    json_body=$(jq -n --arg id "$tool_id" '{"tool_id":$id}')
    curl -s -X POST "$BASE_URL/api/favorites" \
      -H "Authorization: Bearer $api_key" \
      -H "Content-Type: application/json" \
      -d "$json_body" > /dev/null
    ((count++))
  done < <(jq -r '.favorites[]' "$FAVORITES_FILE")

  info "✓ Uploaded $count favorites to server"
  [[ "$skipped" -eq 0 ]] || warn "Skipped $skipped invalid entries"
}

# Show usage
usage() {
  cat <<EOF
Caravo - Local Favorites Manager

Usage:
  $0 init                    Initialize empty favorites file
  $0 list [--validate]        List all favorites (--validate checks server)
  $0 add <tool_id>          Add a favorite
  $0 remove <tool_id>       Remove a favorite
  $0 check <tool_id>        Check if tool is favorited
  $0 sync-from-server       Download server favorites to local (requires API key)
  $0 sync-to-server         Upload local favorites to server (requires API key)

Examples:
  $0 init
  $0 add flux-schnell
  $0 add alice/imagen-4
  $0 list
  $0 check flux-schnell
  $0 remove flux-schnell
  $0 sync-from-server

Environment Variables:
  CARAVO_API_KEY            API key for server sync (optional)
  CARAVO_URL                Base URL (default: https://caravo.ai)

File Location: ~/.caravo/favorites.json
EOF
}

# Main function
main() {
  check_deps

  local cmd="${1:-}"
  case "$cmd" in
    init) init ;;
    list) list "${2:-}" ;;
    add) add "${2:-}" ;;
    remove) remove "${2:-}" ;;
    check) check "${2:-}" ;;
    sync-from-server) sync_from_server ;;
    sync-to-server) sync_to_server ;;
    -h|--help|help|"") usage ;;
    *) err "Unknown command: $cmd. Run '$0 help' for usage." ;;
  esac
}

main "$@"
