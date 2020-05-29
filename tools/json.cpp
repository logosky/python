#!/usr/bin/env python
# coding=utf-8

import sys
import getopt
import json

sys.path.append("./")

def main():
    file_name = 'hb.dat'
    print("file_name:[%s]" % file_name)
    
    total = 0

    with open(file_name, 'r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            line = line.strip('\n')
            if line == '':
                continue

            print("line:%s" % line)
            
            result = json.loads(line)
            serie_one = result['data']
            data = serie_one[0]
            
            print("data cnt:%d" % len(data))
            for val in data:
                if str(val).isdigit():
                    total += val
                    
    
if __name__ == "__main__":
    main()
