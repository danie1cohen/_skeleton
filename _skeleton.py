#! /usr/bin/env python
"""
This module automates setting up a new python project with the usual package
structure and whatever files you'd expect to be there.

Based on Learn Python the Hard Way's skeleton chapter:
http://learnpythonthehardway.org/book/ex46.html
"""
from sys import argv
import os


SCRIPT, PACKAGE_NAME = argv

PATH = u'_skeleton'
ORIGIN = u'_skeleton'

REPLACEMENTS = {
    u'_skeleton': PACKAGE_NAME,
    u'_user_name': u'Dan Cohen',
    u'_user_email': u'daniel.o.cohen@gmail.com',
    u'_download_url': u'dancohen.io'
}

def main():
    """
    Replicate the folder _skeleton and rename everything with the new package
    name
    """
    print 'Creating package... %s ' % PACKAGE_NAME
    os.mkdir(PACKAGE_NAME)

    for _, dirs, _ in os.walk(os.path.join(PATH, ORIGIN)):
        for dir_ in dirs:
            copy_dir(os.path.join(ORIGIN, dir_))

    copy_files(ORIGIN)

    print 'Done!'

def copy_dir(dir_):
    # copies a dir and dirs within it.
    dir_loc = dir_.replace(ORIGIN, PACKAGE_NAME)
    print 'Creating directory... %s' % dir_loc
    os.mkdir(dir_loc)

    copy_files(dir_)


def copy_files(dir_):
    for root, dirs, files in os.walk(os.path.join(PATH, dir_)):
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
