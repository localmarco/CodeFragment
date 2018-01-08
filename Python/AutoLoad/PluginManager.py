#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 23:58:39 2018
@author: marco
"""

import sys
import os
import config
import time
import WorkThread


class PluginManager(object):
    def __init__(self):
        ''' 初始化模块字典.
            字典格式: { name: 实例 }
        '''
        self.modules={}
        ''' 添加 plugin 目录为系统模块路径.'''
        if not os.path.isdir(config.PLUGIN_DIR):
            os.mkdir(config.PLUGIN_DIR)
        sys.path.append(config.PLUGIN_DIR)
        ''' 初始化线程池 '''
        self.wm = WorkThread.WorkManager(config.WORK_THREAD)
        ''' 加载插件模块 '''
        self.wm.add_job(self.load_plugins, None);

    def load_plugins(self, path = None):
        if path is None:
            path = config.PLUGIN_DIR
        for i in os.listdir(path):
            if os.path.isfile('./'+config.PLUGIN_DIR+'/'+i):
                m = i.split('.')
                if m[-1] in 'py':
                    if config.DEBUG:
                        print "load modue: %s"%(i)
                    i = __import__(m[0])
                    self.add_plugin(i)
                else:
                    print "[%s] is not module file."%(i)

    def add_plugin(self, m, name = None):
        name = name
        if name is None:
            name = m.__name__
        if name in self.modules:
            print "%s is exist..."%(name)
            return
        # 寻找模块
        module = getattr(m, name, None)
        if module is not None:
            # 初始化模块实例, 并放入字典
            self.modules[name] = module()
        else:
            print "Plugin is not match..."

    def remove_plugin(self, name):
        try:
            del self.modules[name]
        except Exception,e:
            print e

    def start(self):
        for i in self.modules:
            self.wm.add_job(self.modules[i].start(), None);

    def get_modules(self):
        return self.modules

    def wait_allcomplete(self):
        self.wm.wait_allcomplete()

if __name__ == '__main__':
    m = PluginManager()

    m.load_plugins()
    # 等待LOADING...
    time.sleep(1)
    print "Start----"
    m.start()
    m.wait_allcomplete()
    del m
    print "Done"
