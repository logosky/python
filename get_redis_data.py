#!/usr/bin/env python
# coding: utf-8

import redis
import struct
import json
import sys

sys.path.append("./")

def conn_redis_impl(host, port, auth, db = 0):
    r = redis.Redis(host, port, db, auth)
    return r

def get_redis_config(env):
    if env == "dev":
        redis_config = dev_redis
    elif env == "test":
        redis_config = test_redis 

    if redis_config is None:
        print('get_redis_config failed. env:%s' % (env))
        return None

    return redis_config

def conn_redis(env):
    redis_config = get_redis_config(env)
    if redis_config is None:
        print('conn_redis.get_redis_config failed. env:%s' % (env))
        return None

    r = conn_redis_impl(redis_config['host'],
            redis_config['port'],
            redis_config['password'])
    return r

def get_redis_data(r, env):
    if r is None:
        print 'get_redis_data param error. redis is none'
        return False

    redis_key = "test_key"
    if redis_key is None:
        print('get_redis_data.redis_key failed. env:%s' % (env))
        return False

    dict_data = r.hgetall(redis_key)
    data_res = []
    for (field_key, field_value) in dict_data.items():
        one_item = {}
        one_item[field_key] = field_value
        data_res.append(one_item)

    json_data = json.dumps(data_res, indent = 1)
    print json_data

    return True

call_function = {'get_redis_data' : get_redis_data}

dev_redis = {'host': '192.168.0.1',
    'port': 1000,
    'password': '',
    'prefix': 'dev_'
}

test_redis = {'host': '192.168.0.2',
    'port': 2000,
    'password': '',
    'prefix': 'test_'
}

ENV = ['dev', 'test']
OPT = ['get_redis_data']

def usage():
    cmd = sys.argv[0]
    
    print("%s [dev |test] get_redis_data \n" % cmd)
    
def check_param(argv):
    argc = len(argv)
    if argc < 3:
        return False

    if argv[1] not in ENV:
        return False

    if argv[2] not in OPT:
        return False

    return True
    
def main():
    if not check_param(sys.argv):
        usage()
        return None

    (env, cmd) = (sys.argv[1], sys.argv[2])

    r = conn_redis(env)

    result = call_function[cmd](r, env)

if __name__ == "__main__":
    main()

