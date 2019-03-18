FROM python:3.6.5

WORKDIR /usr/src/app

RUN apt update && apt install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY setup.py .

RUN pip install -e . --no-cache-dir

COPY . .

VOLUME /data

CMD finances-automation
