#!/bin/bash
set -e

cd /usr/src/app/finances-automation

if [ "$1" == "app" ]; then
    finances-automation

elif [ "$1" == "test" ]; then
    pytest finances_automation/tests/ --junit-xml=/test-reports/junit.xml

else:
    exec "$@"

fi
