#!/bin/bash

apt-get update -q
apt-get install -y build-essential libssl-dev libffi-dev python3-dev python3-pip
apt-get install -y --no-install-recommends git

pip3 install --upgrade pip
pip3 install pyopenssl ndg-httpsclient pyasn1

# set up virtual envs
pip3 install virtualenvwrapper

if [ -d "/vagrant" ]; then
    echo "Setting home user to: vagrant"
    HOME_USER=vagrant
    # set python3 as primary python
    ln -sfn `which python3` `which python`
else
    echo "Setting home user to: `SUDO_USER`"
    HOME_USER=`SUDO_USER`
fi

echo 'source "/usr/local/bin/virtualenvwrapper.sh"
export WORKON_HOME="/opt/envs/"
cd /vagrant' >> /home/$HOME_USER/.bash_profile
source /home/$HOME_USER/.bash_profile

echo 'workon _skeleton' >> /home/$HOME_USER/.bash_profile

if [ ! -d "/opt/envs"]; then
    mkdir /opt/envs
fi
mkvirtualenv _skeleton

if [ -a "/vagrant" ]; then
    cd /vagrant
    pip3 install -r requirements.txt
fi

chown -R $HOME_USER:$HOME_USER /opt
