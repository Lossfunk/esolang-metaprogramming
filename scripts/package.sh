#!/usr/bin/env bash
# Package the supplementary tree as supplementary_code.zip with NO macOS
# extended attributes, NO __MACOSX/ resource forks, and NO .DS_Store files.
# `xattr -cr` only clears the live filesystem; macOS may reapply
# com.apple.provenance later. The reliable defense is `zip -X` plus an
# explicit exclude list for AppleDouble metadata.
#
# Usage: bash scripts/package.sh [output_path]

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SUPP_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
OUT="${1:-$SUPP_ROOT/supplementary_code.zip}"

cd "$( dirname "$SUPP_ROOT" )"
BASE="$( basename "$SUPP_ROOT" )"

# Belt-and-braces: clear xattrs, drop .DS_Store, drop bytecode caches.
xattr -cr "$SUPP_ROOT" 2>/dev/null || true
find "$SUPP_ROOT" -name ".DS_Store" -delete 2>/dev/null || true
find "$SUPP_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$SUPP_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true

rm -f "$OUT"
zip -X -r "$OUT" "$BASE" \
    -x "*/.DS_Store" \
    -x "*/__pycache__/*" \
    -x "*/.venv/*" \
    -x "*/harness_state.json" \
    -x "*/export.json" \
    -x "*/logs/*" \
    -x "*/.git/*" >/dev/null

echo "Wrote $OUT"
echo "Bytes: $(wc -c <"$OUT" | tr -d ' ')"
echo "Top-level entries:"
unzip -l "$OUT" | head -20
