#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup (
    name = 'SimpleHTTP Server - Client',
    version = '1.0',
    description = 'SimpleHTTP Server - Client',
    url = 'http://dogeplan.com',
    license = 'LGPL',
    packages = find_packages(),
    script = ['client/SimpleHTTPClient.py', 'server/SimpleHTTPServer.py'],
    extras_require = {
        'requests': ['requests'],  
    },
    )
