# -*- coding:utf-8 -*-
from threading import Thread
import time


class CreateListThread(Thread):
    def __init__(self):
        self.entries = []
        Thread.__init__(self)

    def run(self):
        self.entries = []
        for i in range(10):
            time.sleep(1)
            self.entries.append(i)
        print self.entries


def use_create_list_thread():
    for i in range(3):
        t = CreateListThread()
        t.start()


use_create_list_thread()
