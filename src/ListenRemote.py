#encoding: utf-8
'''
Created on 2018年7月21日

@author: Administrator
'''
import socket,select,threading,sys
import Trader
from Trader import Trader 
import Constant
import DbControler
import time

from BrokerType.ChangChengStockInfo import ChangChengStockInfo

from BrokerType.GuoJunStockInfo import GuoJunStockInfo
from BrokerType.DongGuanStockInfo import DongGuanStockInfo
from BrokerType.DongBeiStockInfo import DongBeiStockInfo
from BrokerType.GuoShengStockInfo import GuoShengStockInfo
from BrokerType.ZhongTouStockInfo import ZhongTouStockInfo

import os
import multiprocessing
import logging

import re
from logging.handlers import TimedRotatingFileHandler
from Filter import HengXingStockInfo, ChangJiangStockInfo


#测试东北登陆
def test_dongbei_trader(user_name,user_password):
    tmp_trader = Trader(Constant.DONGBEI_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.DONGBEI_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code

def test_hengtai_trader(user_name,user_password):
    tmp_trader = Trader(Constant.HENGTAI_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.HENGTAI_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code

def test_guojun_trader(user_name,user_password):
    tmp_trader = Trader(Constant.GUOJUN_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.GUOJUN_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code

def test_changcheng_trader(user_name,user_password):
    tmp_trader = Trader(Constant.CHANGCHENG_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.CHANGCHENG_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code

def test_dongguan_trader(user_name,user_password):
    tmp_trader = Trader(Constant.DONGGUAN_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.DONGGUAN_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code


def test_guosheng_trader(user_name,user_password):
    tmp_trader = Trader(Constant.GUOSHENG_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.GUOSHENG_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code

def test_changjiang_trader(user_name,user_password):
    tmp_trader = Trader(Constant.CHANGJIANG_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.CHANGJIANG_YYB,
                        Constant.DLL_PATH,
                        "11.52",
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code

def test_zhongtou_trader(user_name,user_password):
    tmp_trader = Trader(Constant.ZHONGTOU_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.ZHONGTOU_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    user_code =  tmp_trader.login()
    return user_code



def parse_login_type(x, login_info):
    switcher = {
        '东北证券': test_dongbei_trader,
        '恒泰证券': test_hengtai_trader,
        '长城证券': test_changcheng_trader,
        '国君证券': test_guojun_trader,
        '东莞证券': test_dongguan_trader,
        '国盛证券': test_guosheng_trader,
        '长江证券': test_changjiang_trader,
        '中投证券': test_zhongtou_trader,
    }
    try:
        func = switcher.get(x)
        return func(login_info['userName'], login_info['password'])
    except Exception as e:
        return -1


#开启程序化交易
def excecute_auto_trade(login_info):
    pattern_stock = re.compile(r'[[](.*?)[]]')
    stock_query = re.findall(pattern_stock,login_info['stockList'])
    stock_set = stock_query[0].split(',')
    stocks_info = DbControler.query_selected_stock(stock_set)
    content = []
    for stock_info in stocks_info:
        today = time.strftime("%Y-%m-%d")
        tmp_entrust = {'et_Date': today,
                       'et_OperateDate': today,
                       'et_OperateTime': '00:00:00',
                       'et_StockCode': stock_info[1],
                       'et_StockName': stock_info[2],
                       'et_SignId': '1',
                       'et_Money': '0',
                       'et_Much': '0',
                       'et_Number': '0',
                       'et_DealMuch': '0',
                       'et_DealMoney':'0',
                       'et_DanMuch':'0',
                       'et_Status':'1'}
        content.append(tmp_entrust)
    logging.debug(stock_set)
    DbControler.insert_entrust_table(content,login_info['userId'])
#关闭程序化交易
def quit_auto_trade(login_info):
    today = time.strftime("%Y-%m-%d")
    DbControler.delete_content_by_date("entrust", "et_UserId", "et_Date", today,login_info['userId'])
def shut_down_auto_trade(login_info):
    pass

#处理相应的不同类型登陆者 
def login_dongbei_trader(user_name,user_password,user_id):
    try:
        tmp_trader = Trader(Constant.DONGBEI_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.DONGBEI_YYB,
                            Constant.DLL_PATH,
                            None,
                            sh_code='',
                            sz_code='',
                            )
        if not tmp_trader.login():
            return 2  # 代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        donbei_stock_info = DongBeiStockInfo(stock_input, property_input, entrust_input, finish_book_input, user_name,user_id)
        donbei_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行


def login_changcheng_trader(user_name,user_password,user_id):
    try:
        tmp_trader = Trader(Constant.CHANGCHENG_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.CHANGCHENG_YYB,
                            Constant.DLL_PATH,
                            None,
                            sh_code = '',
                            sz_code = '',
                            )
        if not tmp_trader.login():
            return 2  # 代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        hengxin_stock_info = ChangChengStockInfo(stock_input,property_input,entrust_input,finish_book_input,user_name,user_id)
        hengxin_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行



def login_guojun_trader(user_name,user_password,user_id):
    try:
        tmp_trader = Trader(Constant.GUOJUN_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.GUOJUN_YYB,
                            Constant.DLL_PATH,
                            None,
                            sh_code = '',
                            sz_code = '',
                            )
        if not tmp_trader.login():
            return 2  # 代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        guojun_stock_info = GuoJunStockInfo(stock_input,property_input,entrust_input,finish_book_input,user_name,user_id)
        guojun_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行
# 东莞证券
def login_dongguan_trader(user_name,user_password,user_id):
    try:
        tmp_trader = Trader(Constant.DONGGUAN_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.DONGGUAN_YYB,
                            Constant.DLL_PATH,
                            None,
                            sh_code = '',
                            sz_code = '',
                            )
        if not tmp_trader.login():
            return 2  # 代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        dongguan_stock_info = DongGuanStockInfo(stock_input,property_input,entrust_input,finish_book_input,user_name,user_id)
        dongguan_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行


def login_hengtai_trader(user_name,user_password,user_id):
    try:
        tmp_trader = Trader(Constant.HENGTAI_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.HENGTAI_YYB,
                            Constant.DLL_PATH,
                            None,
                            sh_code = '',
                            sz_code = '',
                            )
        if not tmp_trader.login():
            return 2  # 代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
        hengxin_stock_info = HengXingStockInfo(stock_input,property_input,entrust_input,finish_book_input,user_name,user_id)
        hengxin_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行


def login_changjiang_trader(user_name, user_password, user_id):
    try:
        tmp_trader = Trader(Constant.CHANGJIANG_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.CHANGJIANG_YYB,
                            Constant.DLL_PATH,
                            "11.52",
                            sh_code='',
                            sz_code='',
                            )
        if not tmp_trader.login():
            return 2  # 代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        changjiang_stock_info = ChangJiangStockInfo(stock_input, property_input, entrust_input, finish_book_input, user_name,user_id)
        changjiang_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行

def login_guosheng_trader(user_name, user_password, user_id):
    try:
        tmp_trader = Trader(Constant.GUOSHENG_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.GUOSHENG_YYB,
                            Constant.DLL_PATH,
                            None,
                            sh_code='',
                            sz_code='',
                            )
        if not tmp_trader.login():
            return 2     #代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        guosheng_stock_info = GuoShengStockInfo(stock_input, property_input, entrust_input, finish_book_input, user_name,user_id)
        guosheng_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行
def login_zhongtou_trader(user_name, user_password, user_id):
    try:
        tmp_trader = Trader(Constant.ZHONGTOU_IP,
                            Constant.TRADE_PORT,
                            user_name,
                            user_password,
                            '0',
                            Constant.ZHONGTOU_YYB,
                            Constant.DLL_PATH,
                            None,
                            sh_code='',
                            sz_code='',
                            )
        if not tmp_trader.login():
            return 2     #代表错误信息无法登陆
        tmp_trader.query_positions(Constant.QUERY_STOCKS)
        stock_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_PROPERTY)
        property_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_BOOK)
        entrust_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
        finish_book_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
        zhongtou_stock_info = ZhongTouStockInfo(stock_input, property_input, entrust_input, finish_book_input, user_name,user_id)
        zhongtou_stock_info.update_stock_info()
        return 1  # 代表执行成功
    except Exception as e:
        return 3  # 代表错误代码块执行

def parse_trader_type(x,login_info):
    switcher = {
        '东北证券':login_dongbei_trader,
        '恒泰证券':login_hengtai_trader,
        '长城证券':login_changcheng_trader,
        '国君证券': login_guojun_trader,
        '东莞证券': login_dongguan_trader,
        '国盛证券': login_guosheng_trader,
        '长江证券': login_changjiang_trader,
        '中投证券': login_zhongtou_trader,
    }
    try:
        func = switcher.get(x)
        return func(login_info['userName'], login_info['password'],login_info['userId'])
    except Exception as e:
        return 3

def notify_main(code,login_info):
    '''
        code 对应监听的端口
        login_info 为相应的获取数据
    '''
    if code == '8888':
        #登陆端口通信
        trader_type = login_info['type']
        logging.debug("login user %s %s" % (login_info['type'], login_info['userName']))
        status_code = parse_trader_type(trader_type, login_info)
        if status_code == 1:
            logging.debug('updated succeed')
            return 1
        elif status_code == 2:
            logging.debug('updated failed')
            return 2  #代表错误信息无法登陆
        elif status_code == 3:
            logging.debug('code error')
            return 3    #代表错误代码块执行

    elif code == '8000':
        trader_type = login_info['type']
        user_name = login_info['userName']
        user_password = login_info['password']
        logging.debug("auth user %s %s" % (login_info['type'], login_info['userName']))
        user_code = parse_login_type(trader_type, login_info)
        if user_code != 0:
            if user_code > 0:
                logging.debug('authentic succeed')
                return 1
            else:
                logging.debug('code error')
                return 3
        else:
            logging.debug('user authentic failed')
            return 2


    elif code == '8500':
        logging.debug('start auto trade')
        excecute_auto_trade(login_info)
        # create_start_widget(login_info)
    elif code == '8600':
        logging.debug('end auto trade')
        # create_stop_widget(login_info)
    return False

BASE_DIR = "./"

def listen_port(ip,port):

    _code_log_file = os.path.join(BASE_DIR, 'logs', 'port%s.log' %port) 
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=_code_log_file,
                filemode='w')
    strout = str(os.getpid()) + ip +" " + str(port) + "listen"
    logging.debug(strout)
    while True:
        host = ip
        port = port
        remote_addr = (host,port)
        try:
            client_socket = socket.socket()
            client_socket.connect(remote_addr)
            data = client_socket.recv(1024)
            recData = eval(data)
            if str(port) == '8888':
                login_str = '%s login connected' %recData['userName']
                print(login_str)
            elif str(port) == '8000':
                auth_str = '%s auth connected'  %recData['userName']
                print(auth_str)
            login_info = {}
            for key,value in recData.items():
                login_info[key] = value
            flag = notify_main(str(port), login_info)
            login_status = b''
            if str(port) == '8000' or str(port) == '8888':
                if flag == 1:  # 代表执行成功
                    login_status = b'SUCCESS\r'
                elif flag == 2:  # 代表错误信息无法登陆
                    login_status = b'FAILED\r'
                elif flag == 3:  # 代表错误代码块
                    login_status = b'ERROR\r'
            for i in range(1, 1024 - len(login_status) - 1):
                login_status += b'?'
            client_socket.send(login_status)
            client_socket.close()
        except Exception as e:
            pass



if __name__ == "__main__":
    
    ip = "112.74.48.66"
     # ip = socket.gethostname()
    #
    ports = [8888,8000,8500,8600]
    p1 = multiprocessing.Process(target=listen_port,args = (ip,ports[0]))
    p2 = multiprocessing.Process(target=listen_port,args = (ip,ports[1]))
    p3 = multiprocessing.Process(target=listen_port,args = (ip,ports[2]))
    p4 = multiprocessing.Process(target=listen_port,args = (ip,ports[3]))
    #
    p1.daemon = True
    p2.daemon = True
    p3.daemon = True
    p4.daemon = True
    #
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    #
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    # start_monitor()
    #listen_port("112.74.48.66", 8888)
