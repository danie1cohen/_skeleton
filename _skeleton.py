#! /usr/bin/env python
"""_skeleton.py

This module automates setting up a new python project with the usual package
structure and whatever files you'd expect to be there.

Based on Learn Python the Hard Way's skeleton chapter:
http://learnpythonthehardway.org/book/ex46.html

Usage:
    _skeleton.py <package_name>
    _skeleton.py rename <current_name> <new_name>
"""
import os
import shutil

from docopt import docopt


args = docopt(__doc__)

if args['rename']:
    PACKAGE_NAME = args['<new_name>']
    PATH = '.'
    ORIGIN = args['<current_name>']
    REPLACEMENTS = {args['<current_name>']: args['<new_name>']}
else:
    PACKAGE_NAME = args['<package_name>']
    PATH = u'_skeleton'
    ORIGIN = u'_skeleton'
    REPLACEMENTS = {
        u'_skeleton': PACKAGE_NAME,
        u'_user_name': u'Dan Cohen',
        u'_user_email': u'daniel.o.cohen@gmail.com',
        u'_download_url': u'www.github.com/danie1cohen/_skeleton.git'
    }

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

def main():
    """
    Replicate the folder _skeleton and rename everything with the new package
    name
    """
    print 'Creating package... %s ' % PACKAGE_NAME
    os.mkdir(PACKAGE_NAME)

    source_dir = os.path.join(PATH, ORIGIN)

    for root, dirs, _ in os.walk(source_dir):
        if hidden(root):
            continue
        for dir_ in dirs:
            if hidden(dir_):
                continue
            print(root, dir_)
            copy_dir(os.path.join(ORIGIN, dir_))

    copy_files(ORIGIN)
    git_dir = os.path.join(source_dir, '.git')
    if os.path.exists(git_dir):
        print('Copying git tree.')
        shutil.copytree(git_dir, os.path.join(PACKAGE_NAME, '.git'))
    print 'Done!'

def copy_dir(dir_):
    # copies a dir and dirs within it.
    dir_loc = dir_.replace(ORIGIN, PACKAGE_NAME)
    print 'Creating directory... %s' % dir_loc
    os.mkdir(dir_loc)

    copy_files(dir_)


def copy_files(dir_):
    for root, dirs, files in os.walk(os.path.join(PATH, dir_)):
        if hidden(root):
            continue

        for file_name in files:
            if file_name == '.DS_Store': continue

            old_loc = os.path.join(PATH, os.path.join(dir_, file_name))
            new_loc = os.path.join(dir_, file_name).replace(
                os.path.basename(ORIGIN), PACKAGE_NAME
                )
            try:
                old = open(old_loc, 'rb')
            except IOError:
                pass
            else:
                print 'Creating file... %s' % new_loc
                new = open(new_loc, 'wb')
                for line in old:
                    for key in REPLACEMENTS:
                        try:
                            if key in line:
                                line = line.replace(key, REPLACEMENTS[key])
                        except UnicodeDecodeError:
                            pass
                    new.write(line)
                old.close()
                new.close()

if __name__ == "__main__":
    main()
