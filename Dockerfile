FROM python:3.6.5-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY setup.py .

RUN pip install -e . --no-cache-dir

COPY . .

VOLUME /data

VOLUME /test-reports

CMD pytest finances_automation/tests/ \
    --cov=finances_automation \
    --cov-report html:test-reports/coverage_html \
    --junitxml=/test-reports/junit.xml
