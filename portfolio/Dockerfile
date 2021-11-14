# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN --mount=type=secret,id=SECRET_KEY \
    cat /run/secrets/SECRET_KEY > .env

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
