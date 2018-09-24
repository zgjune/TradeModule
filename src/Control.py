#encoding: utf-8
'''
Created on Jun 19, 2018

@author: liu
'''
import json
import uuid
import sys
import codecs
import mimetypes
import io
import requests
import Constant
base_url = "http://119.28.25.120/"
# base_url = "http://127.0.0.1:8000/"
update_deposite_url = base_url + "update/deposite/"
update_trade_url = base_url + "update/trade/"


class MultipartFormdataEncoder(object):
    def __init__(self):
        self.boundary = uuid.uuid4().hex
        self.content_type = 'multipart/form-data; boundary={}'.format(self.boundary)

    @classmethod
    def u(cls, s):
        if sys.hexversion < 0x03000000 and isinstance(s, str):
            s = s.decode('utf-8')
        if sys.hexversion >= 0x03000000 and isinstance(s, bytes):
            s = s.decode('utf-8')
        return s

    def iter(self, fields, files = None):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, file-type) elements for data to be uploaded as files
        Yield body's chunk as bytes
        """
        encoder = codecs.getencoder('utf-8')
        for (key, value) in fields:
            key = self.u(key)
            yield encoder('--{}\r\n'.format(self.boundary))
            yield encoder(self.u('Content-Disposition: form-data; name="{}"\r\n').format(key))
            yield encoder('\r\n')
            if isinstance(value, int) or isinstance(value, float):
                value = str(value)
            yield encoder(self.u(value))
            yield encoder('\r\n')
        if files != None:
            for (key, filename, fd) in files:
                key = self.u(key)
                filename = self.u(filename)
                yield encoder('--{}\r\n'.format(self.boundary))
                yield encoder(self.u('Content-Disposition: form-data; name="{}"; filename="{}"\r\n').format(key, filename))
                yield encoder('Content-Type: {}\r\n'.format(mimetypes.guess_type(filename)[0] or 'application/octet-stream'))
                yield encoder('\r\n')
                with fd:
                    buff = fd.read()
                    yield (buff, len(buff))
                yield encoder('\r\n')
        yield encoder('--{}--\r\n'.format(self.boundary))

    def encode(self, fields, files=None):
        body = io.BytesIO()
        for chunk, chunk_len in self.iter(fields, files):
            body.write(chunk)
        return self.content_type, body.getvalue()
    





#插入新持仓信息
#单只股票插入
#返回 boolean True标识执行成功 False失败
def insert_deposite_tb(single_deposite):
    if single_deposite == None:
        return False
    else:
        stock_deposite = {}
        single_stock = {}
        single_stock['sec_amount'] = single_deposite[1]
        single_stock['sec_price'] = single_deposite[2]
        single_stock['sec_hold_user'] = single_deposite[3]
        stock_deposite[single_deposite[0]] = single_stock
        deposite_json= json.dumps(stock_deposite)
        kv = {'content':deposite_json}
#         print(kv)
        resp = requests.get(update_deposite_url,params=kv)
        print(resp.text)
        return True


#插入相应下单信息
#对应单只股票下单
def insert_trade_tb(current_trade):
    if current_trade == None:
        return False
    else:
        temp_trade= {}
        send_trade = {}
        temp_trade['sec_amount'] = current_trade[1]
        temp_trade['sec_price'] = current_trade[2]
        temp_trade['sec_code'] = current_trade[3]
        temp_trade['sec_trade_user'] = current_trade[4]
        temp_trade['sec_trade_type'] = current_trade[5]
        send_trade[current_trade[0].__str__()] = temp_trade
        trade_json = json.dumps(send_trade)
        kv = {'content':trade_json}
        resp = requests.get(update_trade_url,params=kv)
        print(resp.text) 

#list_name 
def post_single_position(user_id,list_name,entity_list):
    data = {list_name:json.dumps(entity_list)}
    resp = requests.post("http://bs.novlyb.com/servlet/TestService",data=data)
    print(resp)
    if resp.status_code == 200:
        print(resp.text)
        

if __name__ == "__main__":
    
    post_single_position(1)

