#!/usr/bin/env python
# coding=utf-8

import platform
PYTHON_VERSION = platform.python_version()
import os
COMMAND = '{python_version} {server} {argv}'
file_path = os.path.dirname(__file__)
import sys
argvs = ''
for argv in sys.argv:
    argvs += (argv + ' ')

if PYTHON_VERSION.startswith('3'):
    os.system(COMMAND.format(python_version='python', server=file_path+'/server_python3.py', argv=argvs))

else:
    os.system(COMMAND.format(python_version='python', server=file_path+'/server_python2.py', argv=argvs))
