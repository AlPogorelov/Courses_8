bash
#!/bin/sh

# Ожидание доступности PostgreSQL через pg_isready
until pg_isready -h db -U ${POSTGRES_USER}; do
  echo "Ждем, когда PostgreSQL запустится..."
  sleep 1
done

echo "PostgreSQL доступен!"