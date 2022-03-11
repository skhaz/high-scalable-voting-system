#!/usr/bin/env bash

set -e

if [ -n "$RABBITMQ_HOST" ]; then
  wait-for-it.sh "$RABBITMQ_HOST:${RABBITMQ_PORT:-5672}"
fi

if [ -n "$REDIS_HOST" ]; then
  wait-for-it.sh "$REDIS_HOST:${REDIS_PORT:-6379}"
fi

exec "$@"