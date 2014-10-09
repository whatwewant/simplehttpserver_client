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
    '''简易客户端'''
    def __init__(self, ip=None, port=None):
        self.__current_path = '' # os.getcwd() + '/'
        self.__store_path = self.__current_path + './download' + str(date.today()) + '/'

        if not os.path.exists(self.__store_path):
            os.mkdir(self.__store_path)

        self.__ip = '127.0.0.1' if ip == None else ip# default
        self.__port = '8000' if port == None else port
        self.__real_url_head = 'http://' + self.__ip + ':' + self.__port
        self.__req = requests.Session()

        self.__html = None

    def get_html_recursion(self, url, dir):
        
        if not url.endswith('/'):
            url = url + '/'

        if not dir.endswith('/'):
            dir = dir + '/'

        html = requests.get(url + dir).content
        files_or_directorys = re.findall('<li><a href="(.*)">', html)
        
        files = []
        for each in files_or_directorys:
            if not each.endswith('/'):
                print "文件 " + dir + each
                files.append(dir + each)
            else:
                print("創建文件夾 " + self.__store_path + dir + each)
                print self.__store_path + dir + each

                #if not os.path.exists(self.__store_path + dir + each):
                    #os.mkdir(self.__store_path + dir + each)

                for more in self.get_html_recursion(url, dir + each):
                    files.append(more)
            time.sleep(1)

        return files

    def download(self, file):
        pass

    def run(self):
        files = self.get_html_recursion('http://127.0.0.1:8000', '.')
        #for each in files:
        #    print each
        #    time.sleep(1)

if __name__ == '__main__':
    OO = SimpleHTTPClient()
    OO.run()
