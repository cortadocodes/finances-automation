#!/usr/bin/env bash

database=$1
database_storage_area=$2

pg_ctl -D $database_storage_area start
createdb $database
