#!/bin/bash
set -e

TEST_REPORTS_DIRECTORY=/test-reports

cd /usr/src/app/

if [ "$1" == "app" ]; then
    finances-automation

elif [ "$1" == "test" ]; then
    pytest finances_automation/tests/ \
    --junit-xml="$TEST_REPORTS_DIRECTORY"/junit.xml \
    --cov=finances_automation \
    --cov-report html:"$TEST_REPORTS_DIRECTORY"/coverage_html

else
    exec "$@"

fi
