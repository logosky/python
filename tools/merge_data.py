#!/usr/bin/env python
# coding=utf-8

import sys
import getopt
import struct

sys.path.append("./")

def usage():
    print ('Usage: %s <filename>' % sys.argv[0])
    print ('  -h --help                  help\n' \
            '  -f --file                process file\n')

def main(file_name):
    print("file_name:[%s]" % file_name)
    
    rid_set = set()
    exist_set = set()
    with open('result', 'r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            line = line.strip('\n')
            if line == '':
                continue
            exist_set.add(int(line))
    
    with open(file_name, 'r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            line = line.strip('\n')
            if line == '':
                continue

            #print("line:%s" % line)
            rid = int(line)
            if not rid in exist_set:
                rid_set.add(int(line))
            
    res_file = file_name + '_res'
    print("res_file:[%s]" % res_file)
    with open(res_file, 'w+') as fp:
        for rid in rid_set:
            #print("rid:%d" % rid)
            line = '%d\n' % rid
            fp.write(str(line))

if __name__ == "__main__":
    options, args = getopt.getopt(sys.argv[1:], "h-f:", ['help', 'file'])
    file_name = ''
    for name, value in options:
        if name in ('-h', '--help'):
            usage()
            exit()
        elif name in ('-f', '--file'):
            #print('n:%s v:%s' % (name, value))
            file_name = value
        else:
            usage()
            exit()
    main(file_name)
