#! /bin/sh

apk add --update \
 python \
 python-dev \
 py-pip \
 build-base


pip install flask
pip install flask_cors

cd /usr/bin/

python users.py
