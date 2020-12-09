#!/usr/bin/env python
# coding: utf-8

import redis
import struct
import json
import sys

sys.path.append("./")

def invite(lua_script):
    keys = []
    args = [100, 101, 'mnick', 'micon', 200, 201, 'snick', 'sicon', 123456]

    reply = []
    reply = lua_script(keys, args)

    print("invite res:%s" % reply)

def cancel(lua_script):
    keys = []
    args = [100, 200]

    reply = []
    reply = lua_script(keys, args)

    print("cancel res:%s" % reply)

call_function = {'invite' : invite, 'cancel' : cancel}

redis_config = {'host': '1.1.1.1',
    'port': 6000,
    'password': ''
}

OPT = ['invite', 'cancel']

def check_param(argv):
    argc = len(argv)
    if argc < 2:
        return False
        
    if argv[1] not in OPT:
        return False
    return True
    
def main():
    if not check_param(sys.argv):
        print("invalid args \n")
        return None

    cmd = sys.argv[1]
    print("cmd : %s\n" % cmd)
    
    r = redis.Redis(redis_config['host'], redis_config['port'], 0, redis_config['password'])

    if cmd == 'clear':
        r.delete('#testkey')
        print("%s succ\n" % cmd)
        return None
    
    # 载入lua脚本
    lua_file = cmd + '.lua'
    with open(lua_file, 'rb') as f:
        test_lua = f.read()
    lua_script = r.register_script(test_lua)

    call_function[cmd](lua_script)

if __name__ == "__main__":
    main()

