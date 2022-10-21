FROM python:3.10-alpine AS base

ENV DB_USER=teste
ENV DB_PASSWORD=teste123
ENV DB_NAME=teste
ENV DB_PORT=3306
ENV DB_ADDRESS=postgresql

RUN apk add build-base
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

FROM base as packages

USER root

ADD requirements.txt /work/requirements.txt
WORKDIR /work

RUN pip install -r requirements.txt

FROM packages

ADD . /work
WORKDIR /work

USER appuser

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0"]
