#!/usr/bin/python
#coding:UTF-8

import sys
import os
import getopt

reload(sys)
sys.setdefaultencoding( "utf-8" )

def read_group(file_name, group_set):
    with open(file_name,'r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            line=line.strip('\n')
            
            group_set.add(str(line))
            #print("%s" % line)
            
def read_room_guild(room_guild):
    #file fomert
    #rid,gid
    with open('anchor_guild_info.csv','r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            line=line.strip('\n')
            items = line.split(',')
            
            k = items[0]
            v = items[1]
            room_guild[int(k)] = int(v)
    
def read_guild_info(guild_info):
    #file fomert
    #gid,ggid
    with open('simple_guild.csv','r') as fp:
        while 1:
            line = fp.readline()
            if not line:
                break
            line=line.strip('\n')
            items = line.split(',')
            k = items[0]
            v = items[1]
            if v.strip():
                guild_info[int(k)] = str(v)
            
def write_result(file_name, data, set_data):
    fp = open(file_name,'w')
    for k,v in data.items():
        if v in set_data:
            line = "%d,%s\n" %(k, v)
            fp.write(line)
    fp.close()
    
def main():
    set_a = set()
    set_b = set()
    set_c = set()
    set_d = set()
    
    # read all group guilds
    read_group('GroupA.txt', set_a)
    print("GroupA size:%d" % len(set_a))
    
    read_group('GroupB.txt', set_b)
    print("GroupB size:%d" % len(set_b))
    
    read_group('GroupC.txt', set_c)
    print("GroupC size:%d" % len(set_c))
    
    read_group('GroupD.txt', set_d)
    print("GroupD size:%d" % len(set_d))
    
    if "123123" in set_a:
        print("true")
    else:
        print("false")
        
    # read room_guild
    room_guild = {}
    read_room_guild(room_guild)
    #for k,v in room_guild.items():
    #    print("k:%d,v:%d" % (k,v))
    print("room_guild size:%d" % len(room_guild))
    
    # read simple_guild
    guild_info = {}
    read_guild_info(guild_info)
    #for k,v in guild_info.items():
    #    print("k:%d,v:%s" % (k,v))
    print("guild_info size:%d" % len(guild_info))

    all_room_to_guild = {}
    for k,v in room_guild.items():
        if guild_info.has_key(v):
            all_room_to_guild[k] = guild_info[v]
    print("all_room_to_guild size:%d" % len(all_room_to_guild))
    
    write_result('result_a.txt', all_room_to_guild, set_a)
    write_result('result_b.txt', all_room_to_guild, set_b)
    write_result('result_c.txt', all_room_to_guild, set_c)
    write_result('result_d.txt', all_room_to_guild, set_d)
            
if __name__ == "__main__":
    '''
    entry
    '''
    main()
    
