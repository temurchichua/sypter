# pull official base image
FROM python:3.9.5-alpine

MAINTAINER Temur Chichua "contact@temurchichua.me"

# set work directory
WORKDIR .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV FLASK_ENV=development \
    FLASK_APP=manage

ENV GROUP_ID=1000 \
    USER_ID=1000

# install dependencies
RUN python -m pip install -U --force-reinstall pip
RUN apk update && \
    && rm -rf /var/cache/apk/*

COPY ./requirements.txt ./requirements.txt
COPY ./requirements ./requirements

RUN pip install -r requirements.txt

# copy project
COPY . .

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www