#!usr/bin/env python
# coding=utf-8
# Author: zhezhiyong@163.com
# Created: 2015年12月11日 11:10:09
# 编辑器：pycharm3.4，python版本：2.66
"""
# TODO(purpose):Python多线程爬虫扫描器
"""

import os
import urllib2
import threading
import Queue
import time
import random

q = Queue.Queue()
threading_num = 5
domain_name = "http://www.yangqq.com"
# 百度蜘蛛浏览器
Baidu_spider = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
# 过滤不要的文件
exclude_file = ['.jpg', '.gif', '.css', '.png', '.js', '.scss']

# 代理服务器ip
proxy_list = [
    {'http': '61.185.219.126:3128'},
]

file_path = "G:\\work\\Workspaces\\pythonwork\\crawl\\test.txt"

# f = open(file_path, "r")
# lines = f.readlines()
# f.close()
#
# for line in lines:
#     print line
#     # 获取文件后缀名，去除过滤列表项
#     if os.path.splitext(line.rstrip())[1] not in exclude_file:
#         print line.rstrip()
#         q.put(line.rstrip())

# 以上代码优化
with open(file_path, "r") as lines:
    for line in lines:
        # print line
        # 获取文件后缀名，去除过滤列表项
        if os.path.splitext(line.rstrip())[1] not in exclude_file:
            # print line.rstrip()
            q.put(line.rstrip())


# 爬虫入口
def crawler():
    while not q.empty():
        path = q.get()
        # 类似http://127.0.0.1/login.php
        url = "%s%s" % (domain_name, path)
        print url
        # 从代理列表中随机获取一个代理地址
        # random_proxy = random.choice(proxy_list)
        # proxy_support = urllib2.ProxyHandler(random_proxy)
        # opener = urllib2.build_opener(proxy_support)
        # urllib2.install_opener(opener)

        headers = {}
        headers['User-Agent'] = Baidu_spider
        request = urllib2.Request(url, headers=headers)

        try:
            response = urllib2.urlopen(request)
            context = response.read()

            if len(context):
                print "Status [%s] - path: %s" % (response.code, path)
            response.close()
            time.sleep(1)
        except urllib2.HTTPError as e:
            print e.code, path
            pass


for i in range(threading_num):
    t = threading.Thread(target=crawler)
    t.start()
