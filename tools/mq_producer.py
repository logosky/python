import json
import struct
import socket
from collections import OrderedDict
import demjson
import time
import collections
import random
import sys


class MessageProtocalBase:
    def __init__(self):
        self._header = OrderedDict()
        self._body = ''

    def serialize_header(self):
        return json.dumps(self._header, separators=(',', ':'))

    def set_header(self, header):
        self._header = header

    def set_body(self, body):
        self._body = body

    def serialize_body(self):
        if len(self._body) > 0:
            return self._body
        else:
            return ''

    def encode(self):
        header_data = self.serialize_header()
        head_len = len(header_data)
        body_data = self.serialize_body()
        body_len = len(body_data)
        pack_len = head_len + body_len + 4
        req_format_str = '!II%ss%ss' % (head_len, body_len)
        req = struct.pack(req_format_str, pack_len, head_len, header_data.encode('utf-8'), body_data.encode('utf-8'))
        return req

    def decode(self, msg):
        pack_len = struct.unpack('!I', msg[0:4])[0]
        head_len = struct.unpack('!I', msg[4:8])[0]
        head = struct.unpack('%ss' % head_len, msg[8:head_len + 8])[0]
        head_json = demjson.decode(head)
        body_len = pack_len - head_len - 4
        body = struct.unpack('%ss' % body_len, msg[head_len + 8: head_len + body_len + 8])[0]
        body_json = ''
        if body_len > 0:
            body_json = demjson.decode(body)
        return head_json, body_json


class RouteInfoProctocal(MessageProtocalBase):
    def __init__(self, topic):
        super(RouteInfoProctocal, self).__init__()
        self._topic = topic
        self.build_header()

    def build_header(self):
        header = OrderedDict()
        ext_field = OrderedDict()
        ext_field['topic'] = self._topic
        header['code'] = 105
        header['extFields'] = ext_field
        header['flag'] = 0
        header['language'] = 'CPP'
        header['opaque'] = 4
        header['remark'] = ""
        header['serializeTypeCurrentRPC'] = 'JSON'
        header['version'] = 1
        self.set_header(header)


class SendProctocal(MessageProtocalBase):
    def __init__(self, topic, queue_id, body):
        super(SendProctocal, self).__init__()
        self._topic = topic
        self._queue_id = queue_id
        self.build_header()
        self.set_body(body)

    def build_header(self):
        header = OrderedDict()
        ext_field = self.build_ext_fields()
        header['code'] = 310
        header['extFields'] = ext_field
        header['flag'] = 0
        header['language'] = 'PYTHON'
        header['opaque'] = 2
        header['remark'] = ''
        header['serializeTypeCurrentRPC'] = 'JSON'
        header['version'] = 1
        self.set_header(header)

    def build_ext_fields(self):
        ext_field = OrderedDict()
        ext_field['a'] = 'handy_producer_group'
        ext_field['b'] = self._topic
        ext_field['c'] = 'TBW102'
        ext_field['d'] = 4
        ext_field['e'] = str(self._queue_id)
        ext_field['f'] = '0'
        ext_field['g'] = str(int(time.time()) * 1000)
        ext_field['h'] = '0'
        ext_field['i'] = ''
        ext_field['j'] = '0'
        ext_field['k'] = 'false'
        return ext_field


class BaseSocketClient:
    def __init__(self, host, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (host, port)
        con_res = self._sock.connect(addr)

    def send(self, msg):
        self._sock.send(msg)

    def recv(self):
        recv_str = b''
        try:
            while True:
                recv_data = self._sock.recv(1024)
                if not recv_data:
                    break
                recv_str += recv_data
                if len(recv_data) < 1024:
                    break
        except socket.error as e:
            print("recv error: %s" % e)

        return recv_str


class RocketMqClient(BaseSocketClient):
    def __init__(self, host, port, protocal):
        super(RocketMqClient, self).__init__(host, port)
        self._protocal = protocal

    def send_msg(self):
        msg = self._protocal.encode()
        self.send(msg)

    def recieve(self):
        msg = self.recv()
        if len(msg) == 0:
            print('no broker info recieve from nameserver!')
            return msg
        else:
            return self._protocal.decode(msg)

##BrokerInfo = collections.namedtuple('BrokerInfo', ['broker_name', 'host', 'port', 'queue_num'])

class BrokerInfo:
    def __init__(self):
        self.broker_name = ''
        self.host = ''
        self.port = 0
        self.queue_num = 0

class QueueInfo:
    def __init__(self):
        self.broker_name = ''
        self.queue_id = 0
        
class Producer:
    def __init__(self, host, port, topic):
        self._host = host
        self._port = port
        self._topic = topic
        self._broker_infos = dict()
        self._queue_infos = dict()

    def send_msg_by_random_queue(self, msg):
        self.get_broker_info()
        if len(self._broker_infos) == 0:
            print('get broker info from nameserver error!')
            return None
        self.send_msg(msg)
    
    def send_msg_by_hash_queue(self, msg, key):
        self.get_broker_info()
        if len(self._broker_infos) == 0:
            print('get broker info from nameserver error!')
            return None
        self.send_msg_by_hash(msg, key)
        
    def get_broker_info(self):
        route_pro = RouteInfoProctocal(self._topic)
        name_server_cli = RocketMqClient(self._host, self._port, route_pro)
        name_server_cli.send_msg()
        head, body = name_server_cli.recieve()
        if head['code'] != 0:
            print(head['remark'])
        if len(body) == 0:
            return None

        for broker_data in body['brokerDatas']:
            broker_info = BrokerInfo()
            broker_info.broker_name = broker_data['brokerName']
            host, port = broker_data['brokerAddrs'][0].split(':')
            broker_info.host = host
            broker_info.port = int(port)
            self._broker_infos[broker_info.broker_name] = broker_info
            
        i = 0
        for queue_data in body['queueDatas']:
            broker_name = queue_data['brokerName']
            broker_info = self._broker_infos.get(broker_name)
            if broker_info is None:
                continue
            broker_info.queue_num = queue_data['writeQueueNums']

            for j in range(broker_info.queue_num):
                queue_info = QueueInfo()
                queue_info.broker_name = broker_name
                queue_info.queue_id = j
                self._queue_infos[i] = queue_info
                i = i + 1


    def get_one_queue_by_random(self):
        broker_infos = []
        for broker in self._broker_infos.values():
            broker_infos.append(broker)
        random_broker = random.sample(broker_infos, 1)[0]
        return random_broker
    
    def get_one_queue_by_hash(self, key):
        queue_len = len(self._queue_infos) 
        queue_info = self._queue_infos[key%queue_len]
        broker_info = self._broker_infos.get(queue_info.broker_name)
        return broker_info, queue_info.queue_id

    def send_msg(self, msg):
        broker_info = self.get_one_queue_by_random()
        queue_id = random.randint(0, broker_info.queue_num - 1)
        send_pro = SendProctocal(self._topic, queue_id, msg)
        producer_cli = RocketMqClient(broker_info.host, broker_info.port, send_pro)
        producer_cli.send_msg()
        res = producer_cli.recieve()
        #print(res)

    def send_msg_by_hash(self, msg, key):
        broker_info, queue_id = self.get_one_queue_by_hash(key)
        #print(broker_info.broker_name, queue_id)
        send_pro = SendProctocal(self._topic, queue_id, msg)
        producer_cli = RocketMqClient(broker_info.host, broker_info.port, send_pro)
        producer_cli.send_msg()
        res = producer_cli.recieve()
        #print(res)

if __name__ == '__main__':
    if 5 != len(sys.argv) and 6 !=  len(sys.argv):
        print(sys.argv)
        print('param error, please check them! [host, port, topic, msg, key]')
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        topic = sys.argv[3]
        msg = sys.argv[4]
        key = 0
        if 6 == len(sys.argv) :
            key = int(sys.argv[5])
        # host = ''
        # port = 8000 
        # topic = 'test_topic'
        # msg = 'msg'
        app = Producer(host, port, topic)

        for i in range(10000):
            if key == 0:
                app.send_msg_by_random_queue(msg)
            else:
                app.send_msg_by_hash_queue(msg, key)

            print(i)

