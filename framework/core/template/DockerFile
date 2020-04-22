FROM python:3.8.2-alpine3.11

EXPOSE 8080 8081 443

RUN apk update && apk add gcc musl-dev libffi-dev libressl-dev bash build-base openrc nginx

RUN mkdir /apps && mkdir /apps/deployment

COPY requirements.txt /apps/requirements.txt

RUN pip install -r /apps/requirements.txt

RUN mkdir /apps/app
COPY app/ /apps/app/
COPY deployment/ /apps/deployment/

RUN mkdir /apps/files && \
    mkdir /apps/settings && \
    mkdir /apps/settings/env && \
    mkdir /apps/settings/secrets && \
    mkdir /apps/settings/test

RUN chmod +x /apps/deployment/startup/app.sh && \
    chmod +x /apps/deployment/startup/test.sh && \

WORKDIR /apps/app
