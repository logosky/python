#!/usr/bin/python
#coding:UTF-8

'''
读取多个txt文件，计算其中的数字之和
文件格式如下
4	148267
5	17
22	67647
'''
import sys
import os
import getopt

reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_files(path, files):
    all_files = os.listdir(path)
    #print("num:%d" % len(all_files))
    
    for f in all_files:
        if(os.path.isdir(path + '/' + f)):  
            # 排除隐藏文件夹
            if(f[0] == '.'):  
                pass  

        if(os.path.isfile(path + '/' + f)):  
            # 添加文件  
            files.append(f)
            #print("f:%s" % f)
    
def calc_data(rfp, file_name):
    double_set = set()
    
    double_set.add(5)
    double_set.add(830)
    double_set.add(831)
    
    total = 0
    
    with open('./data/' + file_name,'r') as fp:
        #print("\n[file:%s]" % file_name)
        while 1:
            line = fp.readline()
            if not line:
                break
            line=line.strip('\n')
            items = line.split('\t')
            
            k = items[0]
            v = items[1]
            #print("k:%s,v:%s" %(k,v))
            
            if int(k) in double_set:
                total += int(v) * 2
            else:
                total += int(v)
    file_names = file_name.split('.')
    rl = "%s,%d\n" % (file_names[0], total)
    rfp.write(rl)
    #print("%s,%d" % (file_names[0], total))
    
def main():
    files = []
    get_files("path", files)
    print("total file cnt:%d" % len(files))
    
    rfp = open('res.txt','a')
    for file in files:
        calc_data(rfp, file)
    rfp.close()
    
if __name__ == "__main__":
    '''
    entry
    '''
    main()
    
