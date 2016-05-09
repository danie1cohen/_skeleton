#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '_skeleton',
    'author': '_user_name',
    'url': '_download_url',
    'download_url': '_download_url',
    'author_email': '_user_email',
    'version': '0.1.0',
    'install_requires': [],
    'packages': ['_skeleton'],
    'scripts': [],
    'name': '_skeleton'
}

setup(**config)
