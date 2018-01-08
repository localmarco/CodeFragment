#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 23:59:57 2018
@author: marco
"""

# test module

class test1(object):
    def __init__(self):
        print "Test 1 Init..."

    def start(self, args = None):
        print "Test 1 Start ..."

    def __del__(self):
        print "Test 1 Del..."

