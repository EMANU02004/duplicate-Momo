#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m http.server "${FRONTEND_PORT:-8080}"
