#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m etl.run --xml "${1:-data/raw/momo.xml}" --export-only
