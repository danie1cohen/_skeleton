#!/bin/bash

apt-get update -q
apt-get install -yq build-essential libssl-dev libffi-dev python3-dev python3-pip
apt-get install -yq --no-install-recommends git

# set python3 as primary python
ln -sfn `which python3` `which python`

pip3 install --upgrade pip
pip3 install pyopenssl ndg-httpsclient pyasn1

# set up virtual envs
pip3 install virtualenvwrapper

if [ -d "/vagrant" ]; then
    HOME_USER=vagrant
else
    HOME_USER=`SUDO_USER`
fi
echo 'source "/usr/local/bin/virtualenvwrapper.sh"
export WORKON_HOME="/opt/envs/"' > /home/$HOME_USER/.bash_profile
source /home/$HOME_USER/.bash_profile

if [ ! -d "/opt/envs"]; then
    mkdir /opt/envs
    chown -R $HOME_USER:$HOME_USER /opt/envs
fi
mkvirtualenv _skeleton


if [ -a "/vagrant" ]; then
    cd /vagrant
    pip3 install -r requirements.txt
fi
