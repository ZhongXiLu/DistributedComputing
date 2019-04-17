#!/usr/bin/env bash
# Get full directory name of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
for serviceDir in "${DIR}"/services/*/; do
    echo cp -r "${DIR}"/util "${serviceDir}"
    cp -r "${DIR}"/util "${serviceDir}"
done