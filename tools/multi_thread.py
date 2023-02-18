#!/usr/bin/env python
#coding=utf-8

import sys
import time
import os
import requests
import json
import getopt
import threading

a = 0
b = 0

res = []
threads = []
n = 100
group = 8
process_cnt = 0

lock = threading.Lock()

def usage():
    print("args:")
    print(" -h or --help: for help")
    print(" -a or --aa: enable a")
    print(" -b or --bb= : set value for b")
    
def run(name, idx):
    global process_cnt
    print("run %s" % name)
    for i in range(0, n):
        if i % group == idx:
            lock.acquire()
            res.append(i)
            process_cnt += 1
            print("add:%d" % i)
            lock.release()
            
            time.sleep(1)
    
if __name__ == '__main__':
    for i in range(0, group):
        name = "thread_%d" % i
        t = threading.Thread(target = run, args = (name, i, ))
        t.start()
        threads.append(t)
        
    for i in range(0, group):
        threads[i].join()
        
    for i in range (0, n):
        print("res:%d" % res[i])
    
