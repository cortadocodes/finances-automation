#!/bin/bash
set -e


APPLICATION_ROOT=/usr/src/finances-automation/finances_automation
TEST_REPORTS_DIRECTORY=/test-reports


if [ "$1" == "app" ]; then
    finances-automation

elif [ "$1" == "test" ]; then
    pytest $APPLICATION_ROOT/tests/ \
    --junit-xml="$TEST_REPORTS_DIRECTORY"/junit.xml \
    --cov="$APPLICATION_ROOT" \
    --cov-report html

elif [ "$1" == "initialise" ]; then
    python3 "$APPLICATION_ROOT"/scripts/initialise_database.py

else
    exec "$@"

fi
