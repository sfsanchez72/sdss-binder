#!/bin/bash

set -e

TMPDIR=$(mktemp -d)
REPO_URL="git@github.com:andycasey/sdss-binder.git"

echo "Cloning main branch into $TMPDIR..."
git clone --branch main --depth 1 "$REPO_URL" "$TMPDIR"

cd "$TMPDIR"

curl https://soji.sdss.utah.edu/collaboration/api/login \
    -c soji.cookies \
    --data-raw "url=https%3A%2F%2Fsoji.sdss.utah.edu%2Fcollaboration%2Fpeople%2Faccounts%2Fbrowse&username=$SDSS_ICDB_USERNAME&password=$SDSS_ICDB_PASSWORD"

curl https://soji.sdss.utah.edu/collaboration/api/people/browse/category%3Dpeople/topic%3Daccounts/subtopic%3Dcontacts \
    -b soji.cookies > soji.json

grep -o '"fi_binder_account": "[^"]*"' soji.json | grep -o '"[^"]*"$' | tr -d '"' | awk 'BEGIN{print "users:"} {print "- " $0}' > users.yaml

if ! diff -q users.yaml .public_binder > /dev/null 2>&1; then
    echo "users.yaml differs from .public_binder — updating..."
    cp users.yaml .public_binder
    git add .public_binder
    git commit -m "Update .public_binder from ICDB"
    git push origin main
    echo "Pushed updated .public_binder to main."
else
    echo "No changes detected."
fi

cd /
rm -rf "$TMPDIR"
echo "Done."
