#!/usr/bin/env bash
set -euo pipefail

echo "Applying RAD-637 fix commits..."

if [[ -f handoff/RAD-637.bundle ]]; then
  git fetch handoff/RAD-637.bundle HEAD
fi

git cherry-pick 79ec946 797a9df 081094e 383c637 e06be26 2ed75af c7e3f38

echo "Done. Next:"
echo "  git push origin HEAD"
echo "  Verify workflow: Blog Date Visibility -> jekyll-future-date-guard"
