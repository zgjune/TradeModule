#encoding: utf-8
import ctypes 
from ctypes import windll, create_string_buffer, memmove, memset, c_char_p,c_float
import Constant
import threading
import time
import ThreadControl
from ThreadControl import ThreadPool as tp, ThreadPool

class Trader():
    def __init__(self,trader_ip,trader_port,trader_user,trader_password,trader_txword,trader_yyb,dll_path,trader_version = None,**kwargs):
        #使用的dll 设置系列参数
        self.dll = None
        self.trader_ip = trader_ip
        self.trader_port = trader_port
        self.trader_user= trader_user
        self.trader_psword= trader_password
        self.trader_txword= trader_txword
        self.trader_yyb= trader_yyb                         
        if trader_version == None:
            self.trader_version = "2.28"
        else:
            self.trader_version = trader_version
        #为 一块 String内存地址指针 ，用于保存各类信息的返回值
        self.trader_Ree = create_string_buffer(1024*1024)   #为Ree变量申请一个内存块，用于返回数据
        #登陆后生的 login_code 
        self.login_code = self.login()
        #用户股东代号用于交易send_order
        self.holder_number = {}
        #用户交易股票计划列表
        self.trade_stock_list = {}
        #用户交易账户下单历史
        #{股票代号:股票交易记录}
        self.trade_record_list = {}
        self._init_registration(dll_path)
#         print(kwargs)
        if kwargs:
            self.init_holder_number(kwargs['sh_code'],kwargs['sz_code'])
        #交易记录锁
        self.trade_record_lock = threading.RLock()
        #交易股票锁
        self.trade_stock_lock = threading.RLock()
        #线程池
        self.thread_pool = ThreadPool(5)
   
    #获取相应的股票交易列表
    def get_trade_stock_list(self):
        return self.trade_stock_list

    #设置相应的交易股票列表 
    def set_trade_stock_list(self,trade_stock_list):
        self.trade_stock_list = trade_stock_list

    #获取相应的交易股票
    #从相应的trade_stock_list中放回一个股票
    def get_trade_stock(self):
        self.trade_stock_lock.acquire()
        if len(self.trade_stock_list) != 0:
            trade_stock = self.trade_stock_list.popitem()
            self.trade_stock_lock.release()
            return trade_stock
        else:
            self.trade_record_lock.release()
            return False 
    #修改相应的trade_record_list
    def append_trade_record(self,book_order):
        self.trade_record_lock.acquire()
        book_config = {}
        book_config['stock_code'] = book_order['stock_code']
        book_config['side'] = book_order['side']
        self.trade_record_list[book_order['book_code']] = book_config
        self.trade_record_lock.release()

    #获得相应的交易记录
    def get_trade_record(self):
        self.trade_record_lock.acquire()
        book_info = self.trade_record_list.popitem()
        print(book_info[0])
        self.trade_record_lock.release()

    #交易股票
    def trade_single_stock(self):
        trade_stock = self.get_trade_stock()
        trade_config = trade_stock[1]
        trade_code = trade_stock[0]
        if trade_stock != False:
            #卖出股票
            stock_code = trade_stock[0]
            print(stock_code)
            stock_price = trade_config['price']
            stock_amount = trade_config['amount']
            book_config = {}
            print("stock_code:",stock_code,"stock_price:",stock_price,"stock_amount:",stock_amount)
            if trade_config['side'] == 0:
                #买入
                book_code = self.buy_stock(stock_code, stock_price, stock_amount)
                #获得相应下单的单号
                book_config['book_code'] = book_code
                book_config['side'] = 0 
                print("buy stock :",stock_code,stock_amount,time.time())
            else:
                #卖出 
                book_code = self.sell_stock(stock_code, stock_price, stock_amount)
                book_config['book_code'] = book_code
                book_config['side'] = 1
                book_config['stock_code'] = stock_code
                print("sell stock :",stock_code,stock_amount,time.time())
            self.append_trade_record(book_config)

    #执行交易计划
    def apply_trade_plan(self):
        for i in range(len(self.trade_stock_list)):
            self.thread_pool.run(func=self.trade_single_stock,args=())
        self.thread_pool.close()
    
    #取消当前所有交易
    def cancel_all_trade(self):
        for i in range(len(self.trade_record_list)):
            self.thread_pool.run(func=self.get_trade_record,args=())
        self.thread_pool.close()

    
    #查看相应的股票持仓
    #返回Boolean成功查询返回True 非False
    def query_positions(self,query_type):
        self.login_code = self.login()
        #清空信息缓存
        memset(ctypes.byref(self.trader_Ree),0x0,1024*1024)
        if self.login_code != None and self.login_code != 0:
            self.dll.JL_QueryData(self.login_code,bytes(str(self.trader_user), 'ascii'),query_type,self.trader_Ree)              # 这里是查询函数 104 是查询资金的编码，查询结果保存在Ree里
            if self.trader_Ree != None:
                self.trader_Ree.value.decode('gbk', 'ignore').split('|')
                return True
            else:
                pass
        return False

    #发送相应的下单命令
    #stock_code 交易股票代号
    #stock_price 交易股票价格
    #stock_amount 交易股票数量
    #trade_side 交易方向
    #holder_code 用户股东账号
    def send_order(self,stock_code,stock_price,stock_amount,trade_side,holder_code):
        if self.login_code == None:
            self.login_code = self.login()
        memset(ctypes.byref(self.trader_Ree),0x0,1024*1024)
        self.dll.JL_SendOrder(self.login_code,
                              trade_side,
                              bytes(self.trader_user, 'ascii'),
                              bytes(holder_code,'ascii'),
                              bytes(stock_code, 'ascii'),
                              stock_amount,
                              c_float(stock_price),
                              self.trader_Ree)
        result = self.trader_Ree.value.decode('gbk','ignore')
        return result

    #取消下单 
    #order_code 下单编号
    #exchange_type 交易市场
    def cancel_order(self,order_code,exchange_type):
        if self.login_code == None:
            self.login_code = self.login()
        memset(ctypes.byref(self.trader_Ree),0x0,1024*1024)
        cancel = self.dll.JL_CancelOrder(self.login_code,
                                         bytes(self.trader_user,'ascii'),
                                         bytes(order_code,'ascii'),
                                         exchange_type, 
                                         self.trader_Ree)
        return cancel 
   
    #购买股票 
    #stock_code 股票代号 
    #stock_price 购买价格 
    #stock_amount 购买数量 
    def buy_stock(self,stock_code,stock_price,stock_amount):
        if stock_code[0] == "3" or stock_code[0] == "0":
            holder_code = self.holder_number['SZ']
        else:
            holder_code = self.holder_number['SH']
            self.send_order(stock_code, stock_price, stock_amount,Constant.SEND_BUY, holder_code)
        return self.trader_Ree.value.decode('gbk','ignore')
        
    
    #卖出股票 
    #stock_code 股票代号 
    #stock_price 购买价格 
    #stock_amount 购买数量 
    def sell_stock(self,stock_code,stock_price,stock_amount):
        if stock_code[0] == "3" or stock_code[0] == "0":
            holder_code = self.holder_number['SZ']
        else:
            holder_code = self.holder_number['SH']
        book_order = self.send_order(stock_code, stock_price, stock_amount,Constant.SEND_SELL, holder_code)
        if type(book_order).__name__ == 'int':
            return book_order
        else:
            return False
    
    #获取当前价格买卖5档
    def get_stock_price(self,stock_code):
        memset(ctypes.byref(self.trader_Ree),0x0,1024*1024)
        if self.login_code == None:
            self.login_code = self.login()
        elif self.login_code == 0:
            return False
        else:
            res = self.dll.JL_GetPrice(self.login_code,bytes(stock_code,'ascii'),self.trader_Ree)
            if res == 1:
                return True
            else:
                return False

    #登陆帐号
    def login(self):
        try:
            #返回相应的用户账号
            login_user_code = self.dll.JL_Login(bytes(self.trader_ip, 'ascii'),
                                                self.trader_port,
                                                bytes(self.trader_version, 'ascii'), 
                                                bytes(self.trader_user, 'ascii'),
                                                bytes(self.trader_psword, 'ascii'),
                                                bytes(self.trader_txword, 'ascii'),
                                                bytes(self.trader_yyb, 'ascii'))
            return login_user_code
        except Exception as e:
            return None

    #注册相应用户信息 
    #dll_path 相应的注册dll路径
    #type 为加载的dll类型 
    def init_holder_number(self,sh_code='',sz_code=''):
        self.holder_number['SH'] = sh_code
        self.holder_number['SZ'] = sz_code
    
    #初始化函数 连接 相应dll
    def _init_registration(self,dll_path,type = None):
        #加载相应的dll
        if type == None:
            self.dll=windll.LoadLibrary(dll_path)     #载入DLL

    #退出登录    
    def quit_login(self):
        if self.login_code == '':
            return True
        else:
            jl_out = self.dll.JL_Out(self.login_code)
            if jl_out != '':
                return True
            else:
                return False