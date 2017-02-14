#!/usr/bin/env python
"""
This fab file is for deploying new code and remotely managing already deployed
code.
"""
from __future__ import print_function
import os
from datetime import datetime

from fabric.api import *


env.host_string = '_env_host_string'
env.user = '_env_user'
env.key_filename = '_env_key_filename'
env.install_path = '/opt/_skeleton'
env.current = '/opt/_skeleton/current'
env.repo = '_download_url'
env.build = datetime.now().strftime('%Y%m%d%H%M%S')
env.settings = '_skeleton/settings.py'


def deploy():
    """Deploys new code and handles the commands that must follow"""
    with cd('%(install_path)s' % env):
        run('git clone %(repo)s %(build)s' % env)
        run('cp current/%(settings)s %(build)s/%(settings)s' % env)
        with cd('%(build)s' % env), prefix('workon _skeleton'):
            run('pip install -U pip')
            run('pip install -r requirements.txt')
            run('nosetests -v')
            # if tests pass, change symlink
            remove = 'rm -rf %(current)s' % env
            replace = 'ln -sfn %(install_path)s/%(build)s %(current)s' % env
            run(remove + ' && ' + replace)
    increment_version()

def oneoff():
    """Run _skeleton as a one off process."""
    with cd('%(current)s' % env), prefix('workon _skeleton'):
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
    return "%s: '%s',\n" % (key, version_plus)

def deployed_version():
    """
    Return the version of the current deployed code.
    """
    run('cat %(current)s/setup.py | grep -i version' % env)

def uname():
    """
    Gets the uname from the remote machine.
    """
    run('uname -s')

def chmod_settings():
    """Restrict file access for settings file."""
    with cd(env['current']):
        sudo('chmod 700 %(settings)s' % env)
