#!/bin/bash
set -e

echo "---> Waiting for database to become a available ..."
{
    until echo "SELECT 1" | psql "postgres://$DATABASE_USER:$DATABASE_PASS@$DATABASE_HOST:$DATABASE_PORT/$DATABASE_NAME" 2>&1 > /dev/null
    do
        echo "-- Waiting for database to become active ..."
        sleep 2
    done
}
echo "-- Database is now active ..."

echo "Apply database migrations"
python manage.py migrate

echo "Starting API Server"
python manage.py runserver 0.0.0.0:8000
