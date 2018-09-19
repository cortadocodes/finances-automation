#!/usr/bin/env bash

database=$1
database_storage_area=$2
user=$3

# Create database storage area and start server
initdb -D $database_storage_area
pg_ctl -D $database_storage_area start

# Create database for user so future psql commands can be executed by them
createdb $user

# Create the required database
createdb $database
