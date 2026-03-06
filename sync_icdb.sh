#!/bin/bash

set -e

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

DRY_RUN=false
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN=true
fi

TMPDIR=$(mktemp -d)
REPO_URL="git@github.com:andycasey/sdss-binder.git"

log "Temporary folder: $TMPDIR"

git clone --branch main --depth 1 "$REPO_URL" "$TMPDIR" > /dev/null 2>&1

cd "$TMPDIR"

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

grep -o '"fi_binder_account": "[^"]*"' soji.json | grep -o '"[^"]*"$' | tr -d '"' | awk 'BEGIN{print "users:"} {print "- " $0}' > users.yaml

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
rm -rf "$TMPDIR"
