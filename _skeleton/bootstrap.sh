#!/bin/bash
export TZ=America/Los_Angeles
export DEBIAN_FRONTEND=noninteractive

echo "
# aliases
alias provision=\"cd /vagrant/playbook && ansible-playbook dev.yml --vault-password-file ~/.vault\"
alias deploy=\"cd /vagrant/playbook && ansible-playbook prod.yml --vault-password-file ~/.vault\"

cd /vagrant/
workon _skeleton" > /home/vagrant/.profile

echo "# dev cleanup
find /home/vagrant/ -name .vault -exec rm {} \\;
find /vagrant/ -name \"*.retry\" -exec rm {} \\;
" >> /home/vagrant/.logout

echo "source ~/.logout" >> ~/.bash_logout


apt-get update
apt-get -y install vim tree build-essential libssl-dev libffi-dev python-dev python-pip
apt-get -y --no-install-recommends install git-core

pip install ansible==2.3.2 markupsafe

chown -R vagrant:vagrant /home/vagrant
