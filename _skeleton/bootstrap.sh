#!/bin/bash
export TZ=America/Los_Angeles
export DEBIAN_FRONTEND=noninteractive

echo "cd /vagrant/" > /home/vagrant/.profile

apt-get update
apt-get -y install build-essential libssl-dev libffi-dev python-dev python-pip
apt-get -y --no-install-recommends install git-core

pip install ansible markupsafe
