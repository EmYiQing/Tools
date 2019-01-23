# -*- coding:utf-8 -*-
import threading
import time
import Queue

exit_flag = 0
queue_lock = threading.Lock()
work_queue = Queue.Queue(10)
thread_list = ["Thread-1", "Thread-2", "Thread-3"]
name_list = ["one", "two", "three", "four", "five"]
threads = []
thread_id = 1


class MyThread(threading.Thread):
    def __init__(self, thread__id, name, queue):
        threading.Thread.__init__(self)
        self.thread__id = thread__id
        self.name = name
        self.queue = queue

    def run(self):
        print "Starting:" + self.name
        process_data(self.name, self.queue)
        print "Exiting:" + self.name


def process_data(thread_name, queue):
    while not exit_flag:
        queue_lock.acquire()
        if not work_queue.empty():
            data = queue.get()
            queue_lock.release()
            print "%s processing %s" % (thread_name, data)
        else:
            queue_lock.release()
        time.sleep(2)


for t in thread_list:
    thread = MyThread(thread_id, t, work_queue)
    thread.start()
    threads.append(thread)
    thread_id += 1

queue_lock.acquire()
for word in name_list:
    work_queue.put(word)
queue_lock.release()

while not work_queue.empty():
    pass

exit_flag = 1

for t in threads:
    t.join()
