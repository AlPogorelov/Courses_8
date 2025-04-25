#!/bin/sh

# Ожидание доступности PostgreSQL на порту 5432
until nc -z db 5432; do
  echo "Ждем, когда PostgreSQL запустится..."
  sleep 1
done

echo "PostgreSQL доступен!"