#!/bin/bash
export TZ=America/Los_Angeles
export DEBIAN_FRONTEND=noninteractive

echo "
# aliases
alias provision=\"cd /vagrant/playbook && ansible-playbook dev.yml --vault-password-file ~/.vault\"
alias deploy=\"cd /vagrant/playbook && ansible-playbook prod.yml --vault-password-file ~/.vault\"

cd /vagrant/
workon notifications" > /home/vagrant/.profile

echo "rm ~/.vault
rm /vagrant/playbook/*.retry " >> ~/.logout

echo "source ~/.logout" >> ~/.bash_logout


apt-get update
apt-get -y install build-essential libssl-dev libffi-dev python-dev python-pip
apt-get -y --no-install-recommends install git-core

pip install ansible markupsafe
