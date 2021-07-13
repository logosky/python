#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

import struct
import sys

sys.path.append("./")

mongo_cfg = {'host': 'mongodb://mongo.local',
    'port': 100
}

def check_param(argv):
    argc = len(argv)
    print('argc:%d argv:%s' %(argc, argv))
    if argc < 3:
        return False
    return True
    
def usage():
    cmd = sys.argv[0]
    
    print("usage:%s start_time end_time\n" % cmd)
    
def process(start_time, end_time):
    print("start_time:%d end_time:%d\n" % (start_time, end_time))
    conn = MongoClient(mongo_cfg['host'], mongo_cfg['port'])
    db = conn.room_record
    room_record = db.room_record
    res_cnt = 0
    time_1 = 0
    time_3 = 0
    time_5 = 0
    time_10 = 0
    time_long = 0
    with open('result.dat', 'w+') as fp:
        record = {}
        for i in room_record.find({"$and": [{ "timestamp": {"$gte":start_time}}, {"timestamp": {"$lte":end_time} }]}):
            room = {}
            room_id = i['room_id']
            origin = i['origin']
            timestamp = i['timestamp']
            op_type = i['op_type']
            
            room['room_id'] = room_id
            room['origin'] = origin
            room['op_type'] = op_type
            room['timestamp'] = timestamp
            
            #print("room_id:%s origin:%s op_type:%d timestamp:%d\n" % (room_id, origin, op_type, timestamp))
            
            if op_type == 2 :
                record[room_id] = room
            elif op_type == 3:
                if room['room_id'] in record:
                    start_record = record[room_id]
                    duration = timestamp - start_record['timestamp']
                    if duration <= 60:
                        time_1 += 1
                    elif duration <= 180:
                        time_3 += 1
                    elif duration <= 300:
                        time_5 += 1
                    elif duration <= 600:
                        time_10 += 1
                    else:
                        time_long += 1
                    #print("=====>room_id:%s duration:%d\n" % (room_id, duration))
                    line = 'room_id \t%s \tduration \t%d \torigin:%s\n' % (room_id, duration, origin)
                    fp.write(str(line))
                    del record[room_id]

                    res_cnt += 1
                    if res_cnt % 100 == 0:
                        print(res_cnt)
    print('time1:%d time3:%d time5:%d time10:%d long:%d\n' % (time_1, time_3, time_5, time_10, time_long)) 

def main():
    if not check_param(sys.argv):
        usage()
        return None

    (start_time, end_time) = (sys.argv[1], sys.argv[2])
    
    process(int(start_time), int(end_time))

if __name__ == "__main__":
    main()
