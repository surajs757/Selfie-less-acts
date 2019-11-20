#! /bin/sh

apk add --update \
 python \
 python-dev \
 py-pip \
 build-base


pip install flask
pip install flask_cors
pip install requests

cd /usr/bin/

python acts.py
