#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup (
    name = 'SimpleHTTPServerClient',
    version = '2.0',
    description = 'SimpleHTTP Server - Client',
    url = 'http://dogeplan.com',
    license = 'LGPL',
    packages = find_packages(),
    scripts = ['client/SimpleHTTPClient.py', 
               'server/HTTPServer.py',
               'server/server_python2.py',
               'server/server_python3.py',
              ],
    extras_require = {
        'requests': ['requests'],  
        'download': ['download'],
    },
    )
