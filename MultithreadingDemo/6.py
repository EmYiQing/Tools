# -*- coding:utf-8 -*-
from threading import Thread, Lock

lock = Lock()
some_var = 0


class IncrementThread(Thread):
    def run(self):
        global some_var
        lock.acquire()
        read_value = some_var
        print "线程%s中的some_var是%d" % (self.name, read_value)
        some_var = read_value + 1
        print "线程%s中的some_var增加后变成%d" % (self.name, some_var)
        lock.release()


def use_increment_thread():
    threads = []
    for i in range(50):
        thread = IncrementThread()
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print "在50次运算后some_var应该变成50"
    print "在50次运算后some_var实际值为:%d" % (some_var,)


use_increment_thread()
