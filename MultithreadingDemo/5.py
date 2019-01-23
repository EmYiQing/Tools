# -*- coding:utf-8 -*-
import urllib2
import time
from threading import Thread


class GetUrlThread(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):
        response = urllib2.urlopen(self.url)
        print self.url, response.getcode()


def get_responses():
    urls = [
        'https://www.baidu.com',
        'https://www.taobao.com',
        'https://www.cnblogs.com',
        'https://github.com',
        'https://www.jd.com'
    ]
    start = time.time()
    threads = []
    for url in urls:
        thread = GetUrlThread(url)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print "Time: % s" % (time.time() - start)


get_responses()
