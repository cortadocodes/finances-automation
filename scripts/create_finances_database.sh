#!/usr/bin/env bash

# Create a new PostgreSQL database storage cluster, start up a server for it and create a database there.


database="finances"
database_storage_area="../data/database_cluster"
user="Marcus1"
overwrite="$1"


check_overwrite() {
    # If the cluster exists already, ask the user if they want to overwrite it
    if [ -d $database_storage_area ] ; then
        if [ "$overwrite" == "" ] ; then
            get_user_choice
        else
            case $overwrite in
                [Yy]* )
                    continue;;
                [Nn]* )
                    exit;;
            esac
        fi
        overwrite_cluster
    fi
}


get_user_choice() {
    while true; do
        read -p "Database cluster already exists: would you like to overwrite it? " overwrite
            case $overwrite in
                [Yy]* )
                    break;;
                [Nn]* )
                    exit;;
                * )
                    echo "Please answer yes or no:";;
        esac
    done
}


overwrite_cluster() {
    pg_ctl -D $database_storage_area stop
    rm -r $database_storage_area
}


create_database() {
    # Create database cluster
    initdb -D $database_storage_area

    # Start database server
    pg_ctl -D $database_storage_area start

    # Create user database so future psql commands can be executed by them
    createdb $user

    # Create the required database
    createdb $database

    # Stop server
    pg_ctl -D $database_storage_area stop
}


check_overwrite
create_database
