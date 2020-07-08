FROM python:3.8.3-slim

RUN apt-get update -y && apt-get install redis-server -y

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python -m pip install --no-cache -r requirements.txt

COPY docker-entrypoint.sh /

COPY main.py .

ENTRYPOINT ["/docker-entrypoint.sh"]