#!/usr/bin/env python
# coding=utf-8

import platform
PYTHON_VERSION = platform.python_version()
import os
COMMAND = '{python_version} {server} {argv}'
import sys

if PYTHON_VERSION.startswith('3'):
    os.system(COMMAND.format(python_version='python', server='server.py', argv=sys.argv[1]))

else:
    os.system(COMMAND.format(python_version='python', server='SimpleHTTPServer.py', argv=sys.argv[1]))
