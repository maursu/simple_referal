FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

COPY . /referal
WORKDIR /referal

RUN pip install --no-cache-dir -r requirments.txt
