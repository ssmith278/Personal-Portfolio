# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /usr/src/app

ARG ONBUILD_SECRET_KEY="bananas"
ENV SECRET_KEY=${SECRET_KEY}

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
