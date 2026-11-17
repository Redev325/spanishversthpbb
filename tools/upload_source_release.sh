#!/usr/bin/env bash
set -euo pipefail

repo="Redev325/spanishversthpbb"
archive="${1:-Bloodbath Spanish Mix PC [RTX].zip}"
tag="${2:-source-v1.0.0}"
asset_name="bloodbath-spanish-mix-source.zip"

if [[ ! -s "$archive" ]]; then
  echo "Source ZIP not found: $archive" >&2
  exit 1
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required. You can upload the ZIP through the repository Releases page instead." >&2
  exit 1
fi

if gh release view "$tag" --repo "$repo" >/dev/null 2>&1; then
  gh release upload "$tag" "$archive#$asset_name" --repo "$repo" --clobber
else
  gh release create "$tag" "$archive#$asset_name" \
    --repo "$repo" \
    --title "Bloodbath Spanish Mix source assets" \
    --notes "Original mod package used by the Psych Engine 0.7.3 HTML5 build workflow."
fi

echo "Uploaded $asset_name to $repo release $tag"
