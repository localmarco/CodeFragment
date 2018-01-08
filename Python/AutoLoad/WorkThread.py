#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:47:43 2017
@author: marco
"""

import Queue
import threading
import time


class WorkManager(object):
    def __init__(self, t_max_num=5):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_thread_pool(t_max_num)

    def __init_thread_pool(self, t_max_num):
        for i in range(t_max_num):
            self.threads.append(WorkThread(self.work_queue))

    def add_job(self, func, args = None):
        self.work_queue.put((func, args))

    def check_queue(self):
        return self.work_queue.qsize()

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                func, args = self.work_queue.get(block=True, timeout=10)
                if func is not None:
                    func(args)
                self.work_queue.task_done()
            except Exception, e:
                print str(e)
                break


if __name__ == '__main__':
    def loop_thread(path):
        print "[D] Thread[%s] [%s]" % (threading.current_thread(), list(path))
        time.sleep(15)

    def do_work(path):
        print "[D] Thread[%s] [%s]" % (threading.current_thread(), list(path))
        time.sleep(0.5)
    work_manager = WorkManager(5)
    work_manager.add_job(loop_thread, "./1111", "2222")
    work_manager.add_job(do_work, "./1111", "2222")
    work_manager.wait_allcomplete()
    del work_manager
