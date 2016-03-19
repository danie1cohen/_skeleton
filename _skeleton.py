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

ORIGIN = u'_skeleton/_skeleton'

REPLACEMENTS = {
    u'_skeleton': PACKAGE_NAME,
    u'_user_name': u'Dan Cohen',
    u'_user_email': u'daniel.o.cohen@gmail.com',
    u'_download_url': u'dancohen.io'
}

def main(origin, package_name):
    """
    Replicate the folder _skeleton and rename everything with the new package
    name
    """
    print 'Creating package... %s ' % package_name
    os.mkdir(package_name)

    for root, dirs, files in os.walk(origin):
        for dir_ in dirs:
            dir_loc = os.path.join(
                package_name, dir_.replace(origin, package_name)
            )
            os.mkdir(dir_loc)
        for file_name in files:
            if file_name == '.DS_Store':
                continue
            old_loc = os.path.join(root, file_name)
            new_loc = old_loc.replace(origin, package_name)
            print new_loc
            old = open(old_loc, 'rb')
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
    print 'Done!'

if __name__ == "__main__":
    main(ORIGIN, PACKAGE_NAME)
