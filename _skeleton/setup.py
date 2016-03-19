#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    u'description': u'_skeleton',
    u'author': u'_user_name',
    u'url': u'_download_url',
    u'download_url': u'_download_url',
    u'author_email': u'_user_email',
    u'version': u'0.1',
    u'install_requires': [u'nose'],
    u'packages': [u'_skeleton'],
    u'scripts': [],
    u'name': u'_skeleton'
}

setup(**config)
