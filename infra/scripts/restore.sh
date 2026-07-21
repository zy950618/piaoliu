#!/bin/sh
set -eu

environment=${1:?environment test or main is required}
backup_dir=${2:?backup directory is required}
case "$environment" in test|main) ;; *) echo "environment must be test or main" >&2; exit 2 ;; esac
test -f "$backup_dir/database.dump"
project="piaoliu-$environment"
compose_file="infra/compose.$environment.yml"
docker compose -p "$project" -f "$compose_file" up -d postgres redis minio
docker compose -p "$project" -f "$compose_file" stop nginx backend worker scheduler >/dev/null 2>&1 || true
docker compose -p "$project" -f "$compose_file" exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '\''$POSTGRES_DB'\'' AND pid <> pg_backend_pid();"' >/dev/null
docker compose -p "$project" -f "$compose_file" exec -T postgres sh -c 'dropdb -U "$POSTGRES_USER" --if-exists "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB"'
docker compose -p "$project" -f "$compose_file" exec -T postgres sh -c 'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists' < "$backup_dir/database.dump"
if test -f "$backup_dir/redis.rdb"; then docker compose -p "$project" -f "$compose_file" cp "$backup_dir/redis.rdb" redis:/data/dump.rdb; fi
if test -d "$backup_dir/minio-data"; then docker compose -p "$project" -f "$compose_file" cp "$backup_dir/minio-data/." minio:/data; fi
docker compose -p "$project" -f "$compose_file" restart redis minio
docker compose -p "$project" -f "$compose_file" up -d backend worker scheduler nginx
