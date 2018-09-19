#!/usr/bin/env bash

# Create a new PostgreSQL database storage cluster, start up a server for it and create a database there.

database=$1
database_storage_area=$2
user=$3

# Create database storage area and start server
initdb -D $database_storage_area
pg_ctl -D $database_storage_area start

# Create user database so future psql commands can be executed by them
createdb $user

# Create the required database
createdb $database

# Disconnect from server
pg_ctl -D $database_storage_area stop
