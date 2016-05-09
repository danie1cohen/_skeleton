#!/usr/bin/env python
"""
This fab file is for deploying new code and remotely managing the machines code
is installed on.
"""
from __future__ import print_function
import os
from datetime import datetime

from fabric.api import run, env, cd, prefix, put, sudo, local


env.host_string = 'administrator@gelsons'
env.user = 'administrator'
env.key_filename = 'U:\\.ssh\\id_rsa'

REPO_URL = 'git@deltaco:usc-cu/_skeleton.git'
INSTALL_PATH = '/opt/_skeleton'


def uname():
    """
    Gets the uname from the remote machine.
    """
    run('uname -s')

def deploy():
    """Deploys new code and handles the commands that must follow"""
    folder = datetime.now().strftime('%Y%m%d%H%M%S')
    with cd(INSTALL_PATH):
        run('git clone %s %s' % (REPO_URL, folder))
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
    increment_version()

def create():
    """
    Does initial folder setup.
    """
    local('ssh-copy-id -i %s %s' % (env.key_filename, env.host_string))
    put('_skeleton/settings.py')
    sudo(
        'mkdir %(path)s && chown %(user)s:%(user)s %(path)s' % {
            'path': INSTALL_PATH,
            'user':env.user
            }
        )
    with cd(INSTALL_PATH), prefix('workon _skeleton'):
        run('git clone %s initialdeployment' % GIT_REPO)
        run('ln -s %s/initialdeployment %s/current' % (INSTALL_PATH,
                                                       INSTALL_PATH))
        run('mv ~/settings.py %s/current/_skeleton/settings.py' % INSTALL_PATH)
        run('pip install -r current/requirements.txt')

def bootstrap():
    """
    Bootstrapping will install system dependencies (we leave python dependencies
    to the deployment process, since they can change .
    """
    put('bootstrap.sh')
    sudo('chmod +x bootstrap.sh && ./bootstrap.sh')

def oneoff():
    with cd(INSTALL_PATH + '/current'), prefix('workon _skeleton'):
        run('python _skeleton/_skeleton.py')

def increment_version():
    """Increments setup.py to the next version."""
    if os.path.exists('setup.py'):
        with open('setup.py', 'r') as infile:
            lines = infile.readlines()
        with open('setup.py', 'w') as outfile:
            for line in lines:
                if 'version' in line:
                    line = increment_last(line)
                outfile.write(line)
    else:
        print('No setup.py file found!')

def increment_last(line):
    """Takes the setup.py version line and returns an incremented one."""
    key, val = line.split(':')
    val = val.replace("'", '').replace('"', '').replace(',', '')
    vals = [int(v.strip()) for v in val.split('.')]
    vals[-1] = vals[-1] + 1
    version_plus = '.'.join([str(val) for val in vals])
    print('Incrementing setup.py to version: %s' % version_plus)
    line = "%s: '%s',\n" % (key, version_plus)
    return line
