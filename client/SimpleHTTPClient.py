#!/usr/bin/env python
# coding=utf-8

import platform
PYTHON_VERSION = platform.python_version()
print("PYTHON_VERSION: %s" % PYTHON_VERSION)

import sys
# To python2, reload function is build-in
# To python3, reload function is not build-in function, it need be imported.
from imp import reload
reload(sys)
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
from datetime import date
from download import download_url

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
        html = html_requsets_obj.content.decode(self.__decode_type)
        # files_or_directorys = re.findall('<li><a href="(.*)">', html)
        # files_or_directorys = re.findall('">(.*)</a>', html)
        compile = re.compile(r'">(.*)</a>')
        files_or_directorys = compile.findall(str(html))
        
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

    def download(self, filepath, number):
        # file = self.__req.get(self.__real_url_head + filepath).content
        # with open(self.__store_path + filepath, 'wb') as fp:
        #    fp.write(file)
        download_url(self.__real_url_head + filepath,
                    self.__store_path + filepath, 
                    number,)
        
        # time.sleep(1)

    def myrun(self):
        (files, dirs) = self.get_html_recursion(self.__real_url_head, '')
        
        print('\nThe Number of All The Directories is : %d\n' % len(dirs))
        print('The Number of All The Files is: %s\n' % str(len(files)))

        for each in dirs:
            path = self.__store_path + each
            #if PYTHON_VERSION.startswith('2'):
            #    path = path.decode(self.__decode_type).encode(self.__encode_type)
            #else:
            path = path.encode(self.__encode_type)

            if not os.path.exists(path):
                os.mkdir(path)

        i = 1
        exits_num = 1
        for each in files:
            # each = each.decode(self.__decode_type)
            if self.exits(each):
                print("%d - %s Exists." % (exits_num, each.split('/').pop()))
                exits_num += 1
                continue

            #try:
            #    print("%s Downloading %s " % (str(i), each.split('/').pop()))
            #except :
            #    pass
            # print('%s ' % str(i), )

            self.download(each, i)
            i += 1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:\n\t %s IPAddr Port" % (sys.argv[0]))
        exit(-1)

    OO = SimpleHTTPClient(sys.argv[1], sys.argv[2])
    OO.myrun()
