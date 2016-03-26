#!/usr/bin/env python
"""
This fab file is for deploying new code for the project to the machines wherein
it is hosted.
"""
from datetime import datetime

from fabric.api import run, env, cd, prefix

env.host_string = 'administrator@gelsons'
env.user = 'administrator'
env.key_filename = r'U:\.ssh\id_rsa'


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

def uname():
    """
    Gets the uname from the remote machine.
    """
    run('uname')
