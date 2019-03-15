#!/usr/bin/env bash
# Get full directory name of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
docker-compose -f "${DIR}"/docker-compose-dev.yml up -d --build
