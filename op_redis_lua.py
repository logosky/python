#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from time import sleep

import redis
import time
from sys import argv
import random
import math

# 1. 读取lua脚本
with open('donate_break_gift.lua', 'rb') as f:
    lua_break_gift = f.read()

with open('donate_task_gift.lua', 'rb') as f:
    lua_task_gift = f.read()

host = '0.0.0.0'
port = 6000

r = redis.Redis(host=host, port=port, db=0, password=r"passwd")

# 载入lua脚本
keys_script = []
script_break_gift = r.register_script(lua_break_gift)
script_task_gift = r.register_script(lua_task_gift)

# 前置条件
uid = 100
rid = 200

# 清空redis的所有数据
# r.flushdb()

# 突破榜逻辑验证
argv_break_gift = [201701, 200, 10, 109]
script_break_gift(keys_script, argv_break_gift)

argv_break_gift = [201700, 200, 9, 110]
script_break_gift(keys_script, argv_break_gift)

argv_break_gift = [201700, 200, 1, 110]
script_break_gift(keys_script, argv_break_gift)

argv_break_gift = [201700, 200, 1, 110]
script_break_gift(keys_script, argv_break_gift)


# 任务逻辑验证
# 清空redis的所有数据
# r.flushdb()

# 设置config信息
key_config = "test_key"
hmDict = {'rk_level_2': 3,
        'rk_level_3': 3,
        'rk_level_4': 3,
        'rk_level_5': 3,
        'card_level_2': 20,
        'card_level_3': 40,
        'card_level_4': 60,
        'card_level_5': 80,
        'love_level_2': 1,
        'love_level_3': 2,
        'love_level_4': 2,
        'love_level_5': 200,
        'yuelao_level_2': 1,
        'yuelao_level_3': 3,
        'yuelao_level_4': 5,
        'yuelao_level_5': 7}
r.hmset(key_config, hmDict)

argv_task_gift = [uid, rid, 1, 1]
script_task_gift(keys_script, argv_task_gift)

argv_task_gift = [uid, rid, 1, 1]
script_task_gift(keys_script, argv_task_gift)

argv_task_gift = [uid, rid, 1, 1]
script_task_gift(keys_script, argv_task_gift)
