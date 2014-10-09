#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# site-packages path
sys.path.append('./site-packages')

import requests
import re
import os
import time
from datetime import date

class SimpleHTTPClient(object):
    '''Simple HTTP Client'''
    def __init__(self, ip=None, port=None, decode_type=None, encode_type=None):
        self.__current_path = os.getcwd()
        self.__store_path = self.__current_path + r'/download_' + str(date.today())

        if not os.path.exists(self.__store_path):
            os.mkdir(self.__store_path)

        self.__ip = '127.0.0.1' if ip == None else ip# default
        self.__port = '8000' if port == None else port
        self.__real_url_head = 'http://' + self.__ip + ':' + self.__port
        self.__req = requests.Session()

        #self.__decode_type = 'utf-8' if decode_type == None else decode_type
        self.__decode_type = None
        self.__encode_type = 'utf-8' if 'linux' in sys.platform else 'gbk'

    def get_html_recursion(self, url, dir):
        
        if not url.endswith('/'):
            url = url + '/'

        if not dir.endswith('/'):
            dir = dir + '/'

        html_requsets_obj = requests.get(url + dir)
        self.__decode_type = html_requsets_obj.apparent_encoding
        html = html_requsets_obj.content
        # files_or_directorys = re.findall('<li><a href="(.*)">', html)
        files_or_directorys = re.findall('">(.*)</a>', html)
        
        files = []
        dirs = []
        for each in files_or_directorys:
            if each.startswith('.'):
                continue

            if not each.endswith('/'):
                # file 
                files.append(dir + each)
            else:
                # dir
                dirs.append(dir + each)
                # 
                (deepFiles, deepDirs) = self.get_html_recursion(url, dir + each)
                for each in deepFiles:
                    files.append(each)
                for each in deepDirs:
                    dirs.append(each)
            # time.sleep(1)

        return (files, dirs)

    def exits(self, filepath):
        return os.path.isfile(self.__store_path + filepath)

    def download(self, filepath):
        file = self.__req.get(self.__real_url_head + filepath).content
        with open(self.__store_path + filepath, 'wb') as fp:
            fp.write(file)
        
        # time.sleep(1)

    def myrun(self):
        (files, dirs) = self.get_html_recursion(self.__real_url_head, '')
        for each in dirs:
            path = self.__store_path + each
            path = path.decode(self.__decode_type).encode(self.__encode_type)
            if not os.path.exists(path):
                os.mkdir(path)

        print('The Number of All The Files is: %s\n\n' % str(len(files)))

        i = 1
        exits_num = 1
        for each in files:
            each = each.decode(self.__decode_type)
            if self.exits(each):
                print("%d - %s Exists." % (exits_num, each.split('/').pop()))
                exits_num += 1
                continue

            try:
                print("%s Downloading %s " % (str(i), each.split('/').pop()))
            except :
                pass

            i += 1
            self.download(each)
            # time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage:\n\t %s ip port [decode_type(default=auto detect)]" % (sys.argv[0]))
        exit(-1)
    if len(sys.argv) == 3:
        OO = SimpleHTTPClient(sys.argv[1], sys.argv[2])
        OO.myrun()
    elif len(sys.argv) == 4:
        OO = SimpleHTTPClient(sys.argv[1], sys.argv[2], sys.argv[3])
        OO.myrun()
