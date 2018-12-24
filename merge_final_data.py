#!/usr/bin/python
#coding:UTF-8

#merge data from 'merge_file_dat.py' result
import sys
import os
import getopt

reload(sys)
sys.setdefaultencoding( "utf-8" )

def read_group(file_name, dict_data):
    with open(file_name,'r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            line=line.strip('\n')
            
            items = line.split(',')
            k = items[0]
            v = items[1]
            dict_data[int(k)] = str(v)
    
def main():
    rooms_a = {}
    rooms_b = {}
    rooms_c = {}
    rooms_d = {}
    
    read_group('result_a.txt', rooms_a)
    read_group('result_b.txt', rooms_b)
    read_group('result_c.txt', rooms_c)
    read_group('result_d.txt', rooms_d)
    print("a size:%d" % len(rooms_a))
    
    fp = open('flow_log.txt', 'r')
    wfp = open('result.txt', 'a')
    while 1:
        line = fp.readline()
        if not line:
            break;
        line=line.strip('\n')
        res_a = line.split(' ')
        ak = res_a[0]
        av = res_a[1]
        #print("ak %s %s" % (ak, av))
        res_b = ak.split('@=')
        bk = res_b[0]
        bv = res_b[1]
        #print("bk %s %s" % (bk, bv))
        if rooms_a.has_key(int(bv)):
            new_line = "%s club_id@=%s zone@=1\n" % (line, rooms_a[int(bv)])
            wfp.write(new_line)
        elif rooms_b.has_key(int(bv)):
            new_line = "%s club_id@=%s zone@=2\n" % (line, rooms_b[int(bv)])
            wfp.write(new_line)
        elif rooms_c.has_key(int(bv)):
            new_line = "%s club_id@=%s zone@=3\n" % (line, rooms_c[int(bv)])
            wfp.write(new_line)
        elif rooms_d.has_key(int(bv)):
            new_line = "%s club_id@=%s zone@=4\n" % (line, rooms_d[int(bv)])
            wfp.write(new_line)
    fp.close()
    wfp.close()
    
if __name__ == "__main__":
    '''
    entry
    '''
    main()
    
