#!/bin/sh
set -eu

environment=${1:-test}
case "$environment" in test|main) ;; *) echo "environment must be test or main" >&2; exit 2 ;; esac
project="piaoliu-$environment"
compose_file="infra/compose.$environment.yml"
backup_dir=".local-workspace/backups/$environment/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$backup_dir"
docker compose -p "$project" -f "$compose_file" exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$backup_dir/database.dump"
docker compose -p "$project" -f "$compose_file" exec -T redis redis-cli --rdb /data/backup.rdb >/dev/null
docker compose -p "$project" -f "$compose_file" cp redis:/data/backup.rdb "$backup_dir/redis.rdb"
docker compose -p "$project" -f "$compose_file" cp minio:/data "$backup_dir/minio-data"
printf '%s\n' "$project" > "$backup_dir/environment.txt"
echo "$backup_dir"
