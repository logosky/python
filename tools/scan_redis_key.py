#!/usr/bin/env python
# coding=utf-8

import redis
import sys
import time
import logging
import os
import getopt

def log_init():
    logger = logging.getLogger('scan_redis')
    logger.setLevel(logging.INFO)
    Logname = 'scan_redis.log'
    fh = logging.FileHandler(Logname)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def usage():
    print('''\
-h\t redis ip
-p\t redis port
''')

def readCmdLinePara():
    global ip,port,logger
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["ip=","port="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for op,val in opts:
        if op in ('-h','--ip'):
            ip = val
        if op in ('-p','--port'):
            port = val
    logger.info('scan redis ip:%s port:%s' % (ip, port))

def connect_redis(redis_ip, redis_port):
    conn = redis.Redis(redis_ip, redis_port, 0, "pwd123")

    return conn

if __name__ == '__main__':
    global ip,port,logger
    logger = log_init()
    readCmdLinePara()
    cursor = 0
    matchs = ("test:*", "tk:*", "hkey*")
    count = 10
    
    try:
        client = connect_redis(ip, port)

        for match in matchs:
            while True:
                scan_res = client.scan(cursor, match, count)
                cursor = scan_res[0]

                for k in scan_res[1]:
                    # client.delete(k)
                    logger.info("find key: %s", k)

                time.sleep(0.01)
                if 0 == cursor:
                    break

    except Exception as ex:
        logger.info("redis exception: %s",str(ex))

    else:
        logger.info('find all keys completely')
    
    
    
