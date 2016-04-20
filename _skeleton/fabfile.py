#!/usr/bin/env python
"""
This fab file is for deploying new code and remotely managing the machines code
is installed on.
"""
from datetime import datetime

from fabric.api import run, env, cd, prefix, put, sudo

env.host_string = 'administrator@gelsons'
env.user = 'administrator'
env.key_filename = r'U:\.ssh\identity'

def uname():
    """
    Gets the uname from the remote machine.
    """
    run('uname -s')

def deploy():
    """Deploys new code and handles the commands that must follow"""
    folder = datetime.now().strftime('%Y%m%d%H%M%S')
    with cd('/opt/_skeleton'):
        run('git clone git@deltaco:usc-cu/_skeleton.git %s' % folder)
        # copy the settings files over
        run('cp current/_skeleton/settings.py %s/_skeleton/settings.py' % folder)
        with cd(folder), prefix('workon _skeleton'):
            run('pip install -U pip')
            run('pip install -r requirements.txt')
            run('nosetests')
            # if tests pass, change symlink
            remove = 'rm -rf /opt/_skeleton/current'
            replace = 'ln -sfn /opt/_skeleton/%s /opt/_skeleton/current'
            run(remove + ' && ' + replace % folder)

def create():
    """
    Does initial folder setup.
    """
    put('_skeleton/settings.py')
    sudo('mkdir /opt/_skeleton && chown administrator:administrator /opt/_skeleton')
    with cd('/opt/_skeleton'), prefix('workon _skeleton'):
        run('git clone git@deltaco:usc-cu/_skeleton.git initialdeployment')
        run('ln -s /opt/_skeleton/initialdeployment /opt/_skeleton/current')
        run('mv ~/settings.py /opt/_skeleton/current/_skeleton/settings.py')
        run('pip install -r current/requirements.txt')

def bootstrap():
    """
    Bootstrapping will install system dependencies (we leave python dependencies
    to the deployment process, since they can change .
    """
    put('bootstrap.sh')
    sudo('chmod +x bootstrap.sh && ./bootstrap.sh')
