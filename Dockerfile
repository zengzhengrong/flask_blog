FROM zengzhengrong889/ubuntu:1804
MAINTAINER zengzhengrong
ENV PYTHONUNBUFFERED 1

# COPY sources.list /etc/apt/sources.list
WORKDIR /web
COPY . /web

RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN export FLASK_APP=run.py

RUN rm /etc/nginx/sites-enabled/*

COPY flask_nginx.conf /etc/nginx/sites-enabled/







