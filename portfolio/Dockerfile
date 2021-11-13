# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

RUN --mount=type=secret,id=SECRET_KEY \
  export SECRET_KEY=$SECRET_KEY

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
