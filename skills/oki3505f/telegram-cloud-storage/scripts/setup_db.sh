#!/bin/bash
# setup_db.sh - Prepare the Postgres database for Pentaract

# Check if psql is available
if ! command -v psql &> /dev/null
then
    echo "psql could not be found. Please install postgresql@15."
    exit 1
fi

# Create user and database
# Note: Assumes the current OS user has permissions to run createuser/createdb or access postgres via peer auth
psql -d postgres -c "CREATE USER pentaract WITH PASSWORD 'pentaract' CREATEDB;"
psql -d postgres -c "CREATE DATABASE pentaract OWNER pentaract;"

echo "Database 'pentaract' created successfully."
