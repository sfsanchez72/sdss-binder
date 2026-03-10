#!/bin/bash

set -e

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

DRY_RUN=false
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=true
fi

TMPDIR=$(mktemp -d)
REPO_URL="https://github.com/andycasey/sdss-binder.git"
EXCLUDE_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/exclude.txt"
INCLUDE_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/include.txt"

log "Temporary folder: $TMPDIR"

git clone --branch main --depth 1 "$REPO_URL" "$TMPDIR" > /dev/null 2>&1

cd "$TMPDIR"

if [ -f "$EXCLUDE_FILE" ]; then
    cp "$EXCLUDE_FILE" exclude.txt
    N_EXCLUDED=$(grep -c '[^[:space:]]' exclude.txt || true)
    log "Loaded $N_EXCLUDED excluded emails from exclude.txt"
else
    touch exclude.txt
    log "No exclude.txt found; proceeding without exclusions."
fi

if [ -f "$INCLUDE_FILE" ]; then
    cp "$INCLUDE_FILE" include.txt
    N_INCLUDED=$(grep -c '[^[:space:]]' include.txt || true)
    log "Loaded $N_INCLUDED forced-include emails from include.txt"
else
    touch include.txt
    log "No include.txt found; proceeding without forced inclusions."
fi

AUTH_RESPONSE=$(curl https://soji.sdss.utah.edu/collaboration/api/login \
    -s -c soji.cookies \
    --data-raw "url=https%3A%2F%2Fsoji.sdss.utah.edu%2Fcollaboration%2Fpeople%2Faccounts%2Fbrowse&username=$SDSS_ICDB_USERNAME&password=$SDSS_ICDB_PASSWORD")

if echo "$AUTH_RESPONSE" | grep -q '"authenticated": "True"'; then
    log "Authentication successful."
else
    log "Authentication failed."
    cd /
    rm -rf "$TMPDIR"
    exit 1
fi

curl https://soji.sdss.utah.edu/collaboration/api/people/browse/category%3Dpeople/topic%3Daccounts/subtopic%3Dcontacts \
    -s -b soji.cookies > soji.json

EXCLUDE_JSON=$(awk 'NF' exclude.txt | awk '{print tolower($0)}' | jq -R . | jq -s .)

jq -r --argjson excludes "$EXCLUDE_JSON" '
    .results[]
    | select(.fi_binder_account != null and .fi_binder_account != "")
    | select(
        (.fi_binder_account | ascii_downcase | endswith("@gmail.com")) or
        ((.fi_binder_account | ascii_downcase) != ((.email // "") | ascii_downcase))
      )
    | select(
        (
            ((.email // "")          | ascii_downcase | IN($excludes[])) or
            ((.fi_binder_account)    | ascii_downcase | IN($excludes[])) or
            ((.contacts // [])       | map(ascii_downcase) | any(IN($excludes[])))
        ) | not
      )
    | .fi_binder_account
' soji.json > users_base.txt

{ cat users_base.txt; awk 'NF' include.txt; } \
    | awk '!seen[tolower($0)]++' \
    | awk 'BEGIN{print "users:"} {print "- " $0}' > users.yaml

if ! diff -q users.yaml .public_binder > /dev/null 2>&1; then
    ADDED=$(diff .public_binder users.yaml | grep '^>' | grep -v '^> users:' | sed 's/^> - //' | sort)
    REMOVED=$(diff .public_binder users.yaml | grep '^<' | grep -v '^< users:' | sed 's/^< - //' | sort)
    N_ADDED=$(echo "$ADDED" | grep -c . || true)
    N_REMOVED=$(echo "$REMOVED" | grep -c . || true)
    log "users.yaml differs from .public_binder (+${N_ADDED} added, -${N_REMOVED} removed)."
    if [ -n "$ADDED" ]; then
        echo "$ADDED" | while read -r u; do log "  + $u"; done
    fi
    if [ -n "$REMOVED" ]; then
        echo "$REMOVED" | while read -r u; do log "  - $u"; done
    fi
    if [ "$DRY_RUN" = true ]; then
        log "Dry run — skipping commit and push."
    else
        cp users.yaml .public_binder
        git add .public_binder
        git commit -m "Update .public_binder from ICDB"
        git push origin main
        log "Pushed updated .public_binder to main."
    fi
else
    log "No changes detected."
fi

cd /
#rm -rf "$TMPDIR"
