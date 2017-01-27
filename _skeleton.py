#!/usr/bin/env python3
"""_skeleton.py

This module automates setting up a new python project with the usual package
structure and whatever files you'd expect to be there.

Based on Learn Python the Hard Way's skeleton chapter:
http://learnpythonthehardway.org/book/ex46.html

Usage:
    _skeleton.py <package_name>
    _skeleton.py rename <current_name> <new_name>
"""
from __future__ import print_function
import os
import shutil
import sys

from docopt import docopt
import yaml


def hidden(path):
    """Returns true if some meaningful part of the path begins with a dot."""
    for part in path.split(os.path.sep):
        if part == '.':
            continue
        elif part.startswith('.'):
            return True
        elif part == '__pycache__':
            return True
    return False

def read_settings_yml():
    settings = os.path.expanduser('~/.skeleton.yml')
    if not os.path.exists(settings):
        raise ValueError("Found no settings file at %s" % settings)
    with open(settings, 'rb') as stream:
        settings_dict = yaml.load(stream)
    return settings_dict

def globalize(dict_):
    """
    Puts keys and values from an input dict into the globals space.
    (Uppercases the keys.)
    """
    for key, val in dict_.items():
        globals()[key.upper()] = val

def read_settings(args):
    if args['rename']:
        settings = {
            'package_name': args['<new_name>'],
            'path': '.',
            'origin': args['<current_name>'],
            'replacements': {
                args['<current_name>']: args['<new_name>']
            }
        }
    else:
        replacements = read_settings_yml()
        replacements['_skeleton'] = args['<package_name>']
        replacements['_Skeleton'] = ''.join([s.capitalize() for s in
                                             args['<package_name>'].split('_')])
        settings = {
            'package_name': args['<package_name>'],
            'path': os.path.dirname(__file__),
            'origin': '_skeleton',
        }
        for key, val in replacements.items():
            replacements[key] = val.replace(settings['origin'], settings['package_name'])

        settings['replacements'] = replacements
    globalize(settings)

def main(args):
    """
    Replicate the folder _skeleton and rename everything with the new package
    name
    """
    read_settings(args)

    print('Creating package... %s ' % PACKAGE_NAME)
    os.mkdir(PACKAGE_NAME)

    source_dir = os.path.join(PATH, ORIGIN)

    for root, dirs, _ in os.walk(source_dir):
        #print('Main walk')
        #print(root, dirs)
        if hidden(root):
            continue
        for dir_ in dirs:
            if hidden(dir_):
                continue
            new_dir = os.path.join(root, dir_)
            copy_dir(new_dir)

    #print('Copying end files')
    copy_files(ORIGIN, trim_leading=False)

    # copy the git tree, should one exist
    git_dir = os.path.join(source_dir, '.git')
    if os.path.exists(git_dir):
        print('Copying git tree.')
        shutil.copytree(git_dir, os.path.join(PACKAGE_NAME, '.git'))
    print('Done!')

def copy_dir(dir_):
    # copies a dir and dirs within it.
    dir_loc = trim_leading_skeleton(dir_)
    dir_loc = dir_loc.replace(ORIGIN, PACKAGE_NAME)
    if not os.path.exists(dir_loc):
        print('Creating directory... %s' % dir_loc)
        os.mkdir(dir_loc)

    copy_files(dir_)

def trim_leading_skeleton(string):
    pieces = string.split('_skeleton', 1)
    #print(pieces)
    string = pieces[1]
    while string.startswith('/') or string.startswith('\\'):
        string = string[1:]
    return string

def copy_files(dir_, trim_leading=True):
    #print('Copying files')
    for root, dirs, files in os.walk(os.path.join(PATH, dir_)):
        if hidden(root):
            continue
        #print(root, dirs, files)
        for dir_ in dirs:
            copy_dir(os.path.join(root, dir_))

        for filename in files:

            if filename == '.DS_Store': continue

            old_loc = os.path.join(root, filename)
            #print('old loc: %s' % old_loc)

            new_loc = trim_leading_skeleton(old_loc)
            new_loc = new_loc.replace(os.path.basename(ORIGIN), PACKAGE_NAME)

            #print('new loc: %s' % new_loc)
            if os.path.exists(new_loc):
                continue
            with open(old_loc, 'r') as old, open(new_loc, 'w') as new:
                print('Creating file... %s' % new_loc)
                for line in old:
                    for key, val in REPLACEMENTS.items():
                        if key in line:
                            line = line.replace(key, val)
                            #print('replaced %s with %s in line\n%s' % (key, val, line))
                    new.write(line)
                old.close()
                new.close()

if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
