#!/usr/bin/env bash

apt-get update

apt-get install -y build-essential libssl-dev libffi-dev python-dev python-pip
pip install --upgrade pip
pip install pyopenssl ndg-httpsclient pyasn1

pip install -r /vagrant/requirements.txt
