#!/usr/bin/env python
# coding=utf-8

import platform
import sys
import os

PYTHON_VERSION = platform.python_version()
COMMAND = '{python_version} -m {server} {argv}'
file_path = os.path.dirname(__file__)

# SYS PATH
#sys.path.append(os.path.join(file_path, '..'))
#from server.server_python2 import test

def usage(command):
    print('Usage:')
    print('\t%s Port(Default 8000)' % command)
    print('\t%s --prefix=path/to/dir(Default Port 8000)' % command)
    print('\t%s Port --prefix=path/to/dir\n' % command)

if __name__ == '__main__':
    '''main'''
    usage(sys.argv[0])
    if len(sys.argv) > 3:
        exit(-1)

    argvs = ' '
    prefix = ''
    for argv in sys.argv:
        if argv != sys.argv[0] and '--prefix=' not in argv:
            argvs += (argv + ' ')

        if '--prefix=' in argv:
            prefix = argv

    #Current Dir
    if prefix != '':
        chdir = prefix.strip().replace('--prefix=', '')
        chdir = chdir.replace('~', os.environ.get('HOME'))
        os.chdir(chdir)
    print(PYTHON_VERSION)
    print('Current Directory: %s\n' % os.getcwd())

if PYTHON_VERSION.startswith('3'):
    COMMAND = COMMAND.format(python_version='python', server='http.server', argv=argvs)
else:
    COMMAND = COMMAND.format(python_version='python', server='SimpleHTTPServer', argv=argvs)

os.system(COMMAND)
