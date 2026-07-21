#!/bin/sh
set -eu

environment=${1:?environment test or main is required}
case "$environment" in test|main) ;; *) echo "environment must be test or main" >&2; exit 2 ;; esac
project="piaoliu-$environment"
compose_file="infra/compose.$environment.yml"
env_file="infra/env/$environment.env"
test -f "$env_file" || { echo "missing $env_file; copy and edit the matching .example first" >&2; exit 2; }
docker compose -p "$project" --env-file "$env_file" -f "$compose_file" config >/dev/null
docker compose -p "$project" --env-file "$env_file" -f "$compose_file" up -d --build
docker compose -p "$project" --env-file "$env_file" -f "$compose_file" ps
