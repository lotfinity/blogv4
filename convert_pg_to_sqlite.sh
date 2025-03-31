#!/bin/bash
set -e

# Configuration variables
DATABASE_NAME="dentiboard"
DATABASE_USER="postgres"
DATABASE_PASSWORD="lofa12345"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
PROJECT_PATH="/home/lotfikan/Desktop/dentidelil"

# Output SQLite file path
SQLITE_FILE="${PROJECT_PATH}/${DATABASE_NAME}.sqlite"

# Construct the PostgreSQL connection string
PG_CONN="postgresql://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_NAME}"

echo "Starting conversion of PostgreSQL database '${DATABASE_NAME}' to SQLite."
echo "PostgreSQL connection: ${PG_CONN}"
echo "SQLite output file: ${SQLITE_FILE}"

# Run pgloader to perform the conversion
pgloader "${PG_CONN}" "sqlite:///${SQLITE_FILE}"

echo "Conversion completed successfully. SQLite database is located at ${SQLITE_FILE}"
