#!/usr/bin/env python
# coding=utf-8

import math
import platform

import sys
# To python2, reload function is build-in
# To python3, reload function is not build-in function, it need be imported.
from imp import reload
reload(sys)

PYTHON_VERSION = platform.python_version()
print("PYTHON_VERSION: %s" % PYTHON_VERSION)

if PYTHON_VERSION.startswith('2.'):
    sys.setdefaultencoding('utf-8') 
    # python3 has not this function because it need not, it used the code of this file

# site-packages path
import os
sys.path.append('../site-packages')
sys.path.append('../../site-packages')
sys.path.append(os.path.dirname(__file__)+'/../site-packages')
sys.path.append(os.path.dirname(__file__)+'/../../site-packages')

import requests
import re
import os
from datetime import date, datetime
from download import download_url

import traceback

logdir = os.path.join(os.path.dirname(__file__), '../log')
log = os.path.join(os.path.dirname(__file__), '../log/client.log')
if not os.path.exists(logdir): 
    os.mkdir(logdir)
with open(log, 'w') as f:
    f.write(str(datetime.today()) + '\n')

class SimpleHTTPClient(object):
    '''Simple HTTP Client'''
    def __init__(self, ip=None, port=None):
        self.__current_path = os.getcwd()
        self.__store_path = self.__current_path + r'/download_' + str(date.today())

        if not os.path.exists(self.__store_path):
            os.mkdir(self.__store_path)

        self.__ip = '127.0.0.1' if ip == None else ip# default
        self.__port = '8000' if port == None else port
        self.__real_url_head = 'http://' + self.__ip + ':' + self.__port
        self.__req = requests.Session()

        self.__decode_type = None
        self.__encode_type = 'utf-8' if 'linux' in sys.platform else 'gbk'
        # All Files SIZE 
        self.__target_file_size = 0
        self.__real_file_size = 0

    def get_html_recursion(self, url, dir):
        
        if not url.endswith('/'):
            url = url + '/'

        if not dir.endswith('/'):
            dir = dir + '/'

        html_requsets_obj = requests.get(url)
        self.__decode_type = html_requsets_obj.encoding if html_requsets_obj.encoding != 'mbcs' else 'gbk'
        html = html_requsets_obj.content
        url_compile = re.compile(r'<li><a href="(.*)">')
        urls = url_compile.findall(str(html))

        compile = re.compile(r'">(.*)</a>')
        files_or_directorys = compile.findall(str(html))
        
        files_urls = list(zip(files_or_directorys, urls))
        files_urls_list = []

        for each in files_urls:
            each = list(each)
            each[0] = each[0].decode(self.__decode_type, 'ignore')

            # Not download .* files
            if each[0].startswith('.'):
                continue
            # Directory
            if each[0].endswith('/'):
                # Create new directory
                if not os.path.exists(self.__store_path + dir + each[0]):
                    os.mkdir(self.__store_path + dir + each[0])

                for deep_fu in self.get_html_recursion(url + each[1], dir + each[0]):
                    files_urls_list.append(deep_fu)

                continue
            each[0] = dir + each[0]
            each[1] = url.replace(self.__real_url_head, '') + each[1]
            files_urls_list.append(each)
            # Calculate Target Files Size
            self.__target_file_size += int(requests.head(self.__real_url_head + each[1]).headers.get('Content-Length', 0))

        return files_urls_list

    def exits(self, filepath):
        return os.path.isfile(self.__store_path + filepath)

    def download(self, file_url, file_path, number):
        url = self.__real_url_head + file_url
        path = self.__store_path + file_path
        percent = self.__real_file_size * 100 / float(self.__target_file_size)
        self.__real_file_size += download_url(url, path, number, log, percent)
        
        # time.sleep(1)

    def myrun(self):
        files_urls = self.get_html_recursion(self.__real_url_head, '')
        # print('\nThe Number of All The Directories is : %d\n' % len(dirs))
        print('The Number of All The Files is: %s' % str(len(files_urls)))
        print('Log: %s\n' % log)

        i = 1
        exits_num = 1
        for each in files_urls:
            if self.exits(each[0]):
                try:
                    print("%d - %s Exists." % (exits_num, each[0].split('/').pop()))
                    exits_num += 1
                except:
                    with open(log, 'a') as f:
                        traceback.print_exc(file=f)
                continue

            self.download(each[1], each[0], i)
            i += 1

        # Files Size
        file_size_unit = 'byte'
        file_size = 0.0
        target_size = 0.0
        if self.__target_file_size > math.pow(2, 30):
            file_size = self.__real_file_size / math.pow(2, 30)
            target_size = self.__target_file_size / math.pow(2, 30)
            file_size_unit = 'G'
        elif self.__target_file_size > math.pow(2, 20):
            file_size = self.__real_file_size / math.pow(2, 20)
            target_size = self.__target_file_size / math.pow(2, 20)
            file_size_unit = 'M'
        elif self.__target_file_size > math.pow(2, 10):
            file_size = self.__real_file_size / math.pow(2, 10)
            target_size = self.__target_file_size / math.pow(2, 10)
            file_size_unit = 'K'

        # Info
        print('\n\nThe Number of All The Files : %s' % str(len(files_urls)))
        print('The Size Of All Files : %.2f%s / %3.2f%s [ %.2f%% ]' % \
              (file_size, \
               file_size_unit, \
               target_size, \
               file_size_unit, \
               self.__real_file_size * 100 / float(self.__target_file_size), \
              ))
        print('Log: %s\n' % log)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:\n\t %s IPAddr Port" % (sys.argv[0]))
        exit(-1)

    OO = SimpleHTTPClient(sys.argv[1], sys.argv[2])
    OO.myrun()
