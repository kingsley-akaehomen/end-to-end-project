#!/usr/bin/env bash
host="$1"
shift
until nc -z "$host" 5432; do
  echo "Waiting for $host:5432..."
  sleep 1
done
exec "$@"