#!/usr/bin/env python
# coding=utf-8

import math
import time
import platform

import sys
# To python2, reload function is build-in
# To python3, reload function is not build-in function, it need be imported.
from imp import reload
reload(sys)

PYTHON_VERSION = platform.python_version()
print("PYTHON_VERSION: %s \n%s" % (PYTHON_VERSION, time.ctime()))

if PYTHON_VERSION.startswith('2.'):
    sys.setdefaultencoding('utf-8') 
    # python3 has not this function because it need not, it used the code of this file
    # print(sys.getdefaultencoding())

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
from download import Download
from urllib import urlencode

import traceback

logdir = os.path.join(os.path.dirname(__file__), '../log')
log = os.path.join(os.path.dirname(__file__), '../log/client.log')
if not os.path.exists(logdir): 
    os.mkdir(logdir)
with open(log, 'w') as f:
    f.write(str(datetime.today()) + '\n')

class SimpleHTTPClient(object):
    '''Simple HTTP Client'''
    def __init__(self, ip=None, port=None, url=None):
        self.__current_path = os.getcwd()
        self.__store_path = self.__current_path + r'/download_' + str(date.today())

        if not os.path.exists(self.__store_path):
            os.mkdir(self.__store_path)

        self.__ip = '127.0.0.1' if ip == None else ip
        self.__port = '8000' if port == None else port
        self.__real_url_head = 'http://' + self.__ip + ':' + self.__port
        if url:
            try:
                self.__real_url_head = urlencode(url)
            except TypeError:
                self.__real_url_head = url
        self.__req = requests.Session()

        #  原网页编码,一般是服务器的系统编码,
        #  如何获得? requests.encoding
        self.__decode_type = None
        # 要编码成当前系统的编码
        # self.__encode_type = 'utf-8' if 'linux' in sys.platform else 'gbk'
        # 当前系统的编码
        self.__encode_type = sys.getfilesystemencoding() if \
                sys.getfilesystemencoding() != 'mbcs' else 'gbk'
        # All Dirs Count
        self.__target_dir_count = 0
        # All Files Count
        self.__target_file_count = 0
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
        html = html_requsets_obj.content\
                .decode(self.__decode_type)\
                .encode(self.__encode_type)
        # 所有的url
        urls = re.findall(r'<li><a href="(.+)">', html)
        # 所有的文件夹名和文件名
        files_or_directorys = re.findall(r'">(.+)</a>', html)
        # url和文件名一对一
        files_urls = list(zip(files_or_directorys, urls))

        files_urls_list = []
        for each in files_urls:
            each = list(each)
            each[0] = each[0].replace('?', '')
            if each[0].startswith('.git'):
                continue
            # Directory
            if each[0].endswith('/'):
                # Target Dirs Count
                self.__target_dir_count += 1
                sys.stdout.write('[ %s ] Files Count %d; Dirs Count: %d\r' % (time.ctime(), self.__target_file_count, self.__target_dir_count))
                sys.stdout.flush()
                # Create new directory
                if not os.path.exists(self.__store_path + dir + each[0]):
                    os.mkdir(self.__store_path + dir + each[0])

                for deep_fu in self.get_html_recursion(url + each[1], dir + each[0]):
                    files_urls_list.append(deep_fu)
                continue

            each[0] = dir + each[0]
            each[1] = url.replace(self.__real_url_head, '') + each[1]
            files_urls_list.append(each)
            # Count Files
            self.__target_file_count += 1
            # Calculate Target Files Size
            head = requests.head(self.__real_url_head + each[1])
            if not head.ok:
                break
            self.__target_file_size += int(head.headers.get('Content-Length'))

            sys.stdout.write('[ %s ] Files Count %d; Dirs Count: %d\r' % (time.ctime(), self.__target_file_count, self.__target_dir_count))
            # Show Files Count
            sys.stdout.write('Files Count %d; Dirs Count: %d \r' % (self.__target_file_count, self.__target_dir_count))
            sys.stdout.flush()

        return files_urls_list

    def exits(self, filepath):
        return os.path.isfile(self.__store_path + filepath)

    def download(self, file_url, file_path, number):
        download = Download()
        download_url = download.download
        url = self.__real_url_head + file_url
        path = self.__store_path + file_path
        file_name = path.split('/').pop()
        file_name_size = len(file_name)
        file_path = path[:-file_name_size-1]
        (target_size, real_size) = download_url(url, file_name, file_path, int(number), self.__files_number)
        self.__real_file_size += real_size
        
    def myrun(self):
        files_urls = self.get_html_recursion(self.__real_url_head, '')
        print('\n\nThe Number of All The Files is: %s' % str(len(files_urls)))
        self.__files_number = len(files_urls)
        print('Log: %s\n' % log)

        i = 1
        exits_num = 1
        for each in files_urls:
            if self.exits(each[0]):
                exists_file_size = os.path.getsize(self.__store_path + each[0])
                download_size = int(requests.head(self.__real_url_head + each[1]).headers.get('Content-Length'))
                try:
                    if exists_file_size == download_size:
                        print("%d - %s Exists." % (exits_num, each[0].split('/').pop()))
                        exits_num += 1
                    else:
                        print("%d - %s modify size from %dbit -> %dbit." % (exits_num, 
                            each[0].split('/').pop(), exists_file_size, download_size))
                        self.download(each[1], each[0], i)
                    i += 1
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
        print('\n\nThe Number of All The Dirs : %d' % (self.__target_dir_count))
        print('The Number of All The Files : %s' % str(len(files_urls)))
        if self.__target_file_size > 0:
            print('The Size Of All Files : %.2f%s / %3.2f%s [ %.2f%% ]' % \
                  (file_size, \
                   file_size_unit, \
                   target_size, \
                   file_size_unit, \
                   self.__real_file_size * 100 / float(self.__target_file_size), \
                  ))
        else:
            print('The Size Of All Files : %.2f%s / %3.2f%s [ %.2f%% ]' % \
                  (file_size, \
                   file_size_unit, \
                   target_size, \
                   file_size_unit, \
                   100,\
                  ))
        print('Log: %s\n' % log)

if __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) >= 4:
        print("Usage:\n\t %s IPAddr Port" % (sys.argv[0]))
        print('\t %s URL' % sys.argv[0])
        exit(-1)

    if sys.argv[1].startswith('http'):
        OO = SimpleHTTPClient(url=sys.argv[1])
        OO.myrun()
    else:
        OO = SimpleHTTPClient(sys.argv[1], sys.argv[2])
        OO.myrun()
