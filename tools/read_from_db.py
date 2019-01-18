#!/usr/bin/python
#coding:UTF-8

import MySQLdb
import sys
import logging
import datetime
import os
import time
import getopt

reload(sys)
sys.setdefaultencoding( "utf-8" )

ComplexDBCfg = {
    'host':'192.168.1.1',
    'port':3600,
    'user':'d_user',
    'passwd':'d_password',
    'db':'d_test',
    'charset' : 'utf8',
    }

def get_data(fp, t):
    #连接数据库
    connDB = MySQLdb.connect(**ComplexDBCfg)
    curDB = connDB.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    
    try:
        sql = "select c_id, c_name, c_age from %s where " \
            "c_create_time>'2016-11-19 00:00:00' and c_create_time<'2016-12-10 00:00:00';" % t
        logging.debug(sql)
        curDB.execute(sql)
        rows = curDB.fetchall()
        
        num = 0
        for row in rows:
            c_id = row['c_id']
            c_name = row['c_name']
            c_age = row['c_age']

            line = "%s\t%s\t%s\n" % (c_id, c_name, c_age);
            fp.write(line)
            num += 1

        logging.debug("total:%d" % num)

    except MySQLdb.Error,e:
        logging.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))        

        curDB.close()
        connDB.close()
    return

def usage():
    print 'Usage: %s (opts)' % sys.argv[0]
    print '  -h --help                  help\n' \
          '  -g --get                   get data from db\n'
          
def main():
    logfile = sys.argv[0] + '.log'
    logging.basicConfig(filename = logfile, level = logging.DEBUG, filemode = 'w', format = '%(asctime)s - %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')
    
    options, args = getopt.getopt(sys.argv[1:], "hg", ['help', 'get'])
    get = False
    for name, value in options:
        if name in ('-h', '--help'):
            usage()
            return
        elif name in ('-g', '--get'):
            get = True
        else:
            usage()
            return
            
    if get:
        with open('res.txt','w') as fp:
            for i in range(0, 10):
                t="d_test.t_test_%s" % (i)
                get_data(fp,t)
                logging.debug("pro db:%s" % t)
    else:
        usage()

if __name__ == "__main__":
    '''
    连接DB，查询DB，写文件
    '''
    main()
    
