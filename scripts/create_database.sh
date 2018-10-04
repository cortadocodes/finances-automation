#!/usr/bin/env bash

# Create a new PostgreSQL database storage cluster, start up a server for it and create a database there.


database="$1"
database_storage_area="$2"
user="$3"
overwrite="$4"


check_overwrite() {
    # If the cluster exists already, ask the user if they want to overwrite it
    if [ -d "$database_storage_area" ] ; then
        case "$overwrite" in
            [Yy]* )
                overwrite_cluster;;
            [Nn]* )
                exit;;
        esac
    fi
}


overwrite_cluster() {
    pg_ctl -D "$database_storage_area" stop
    rm -r "$database_storage_area"
}


create_database() {
    # Create database cluster
    initdb -D "$database_storage_area"

    # Start database server
    pg_ctl -D "$database_storage_area" start

    # If necessary, create user database so future psql commands can be executed by them
    user_database_exists="$(psql -l -t | grep "$database" | wc -l)"
    if [ ! $user_database_exists ] ; then
        createdb "$user"
    fi

    # Create the required database
    createdb "$database"

    # Stop server
    pg_ctl -D "$database_storage_area" stop
}


check_overwrite
create_database
