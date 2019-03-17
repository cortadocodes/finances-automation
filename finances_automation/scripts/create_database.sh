#!/usr/bin/env bash

# Create a new PostgreSQL storage cluster and database.


database="$1"
database_storage_area="$2"
user="$3"
overwrite="$4"


check_overwrite() {
    # Check if the user wishes for an existing database cluster to be overwritten.
    if [[ -d "$database_storage_area" ]] ; then
        case "$overwrite" in
            [Yy]* )
                # If they do, remove the existing cluster.
                remove_cluster;;
            [Nn]* )
                exit;;
        esac
    fi
}


database_exists() {
    # Check if a psql database with a given name exists.
    check_database_exists="$(psql -l -t | grep "$1" | wc -l)"
}


remove_cluster() {
    # Stop and remove a database cluster.
    pg_ctl -D "$database_storage_area" stop
    rm -r "$database_storage_area"
}


create_database() {
    # Create a database cluster and database, also creating a database for the username if required so that future
    # psql commands can be executed by them.
    initdb -D "$database_storage_area"
    pg_ctl -D "$database_storage_area" start

    if [[ ! $(database_exists $user) ]] ; then
        createdb "$user"
    fi

    createdb "$database"
    pg_ctl -D "$database_storage_area" stop
}


check_overwrite
create_database
