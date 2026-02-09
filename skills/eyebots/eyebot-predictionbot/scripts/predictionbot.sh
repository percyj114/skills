#!/bin/bash
API_BASE="${EYEBOT_API:-${EYEBOT_API}}"
curl -s -X POST "${API_BASE}/api/predictionbot" -H "Content-Type: application/json" -d "{\"request\": \"$*\", \"auto_pay\": true}"
