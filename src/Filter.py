
import math
import Control
import DbControler
import logging
import time
class AbstractStockInfo(object):
    def __init__(self,**kwarg):
        self.index_list = ['po_StockCode','po_StockName','po_StockMuch','po_SellMuch','po_CostMoney','po_NowMoney','po_Market','po_PL','po_PLRatio']
    def _get_stock_list(self,**kwarg):
        pass
    def _get_stock_info(self,**kwarg):
        pass
    def update_stock_info(self,**kwarg):
        try:
            self._format_property()
            self._format_stock()
            self._format_entrust()
            # self._format_deal_record()
        except Exception as e:
            logging.exception('erorr msg')
            
#         self._upload_stocks()
        

class HengXingStockInfo(AbstractStockInfo):
    def __init__(self,stock_info_block,property_block,entrust_block,finish_book_block,sec_hold_user,user_id):
        self.user_id = user_id 
        self.sec_hold_user  = sec_hold_user

        #资金信息块
        self.property_block = property_block
        #交易委托块
        self.entrust_block = entrust_block
        #交易完成委托块
        self.finish_book_block = finish_book_block
        #持仓股票块 
        self.stock_info_block = stock_info_block
        
        #当前持仓股票指标
        self.cur_index_list = ['sec_code',
                               #证券代码
                               'sec_name',
                               #证券数量
                               'sec_amount',
                               #可卖数量
                               'sec_trade_amount',
                               #成本价
                               'sec_cost_price',
                               #当前价
                               'sec_cur_price',
                               #最新市值
                               'sec_latest_market_val',
                               #累计浮动盈亏
                               'sec_cfpl',
                               #无费用盈亏
                               'sec_ncpl',
                               #盈亏比例
                               'sec_plr',
                               #股东代码
                               'sec_share_holder_code',
                               #交易所代码
                               'sec_exchange_code',
                               #成本价类型
                               'sec_cost_type',
                               #(参数)操作数据
                               'sec_action_data',
                               #句柄
                               'sec_handler',
                               #保留信息
                               'sec_reference_information' ,]
        #当前相应账户的持仓类别
        self.cur_property_list = [
                                   #'币种' 
                                   'pro_type',
                                   #'资金余额' 
                                   'pro_amount',
                                   #'可用资金'
                                   'pro_use',
                                   #'冻结资金' 
                                   'pro_freezed',
                                   #'可取资金' 
                                   'pro_avail',
                                   #'总资产' 
                                   'pro_total',
                                   #'最新市值'
                                   'pro_now',
                                   #'利息' 
                                   'pro_rec',
                                   #'提示信息0'
                                   'information',
                                   #'保留信息'
                                   'reserve_information',
                                  ]
        #当前用户成交股票信息
        self.cur_trade_list = [
                               #'成交时间' 
                               'tr_time',
                               #'证券代码' 
                               'tr_code',
                               #'证券名称' 
                               'tr_name',
                               #'买卖标志'
                               'tr_side',
                               #'买卖标志' 
                               'tr_flag',
                               #'成交价格' 
                               'tr_price',
                               #'成交数量' 
                               'tr_amount',
                               #'成交金额' 
                               'tr_cost',
                               #'成交编号' 
                               'tr_suc_code',
                               #'委托编号' 
                               'tr_en_code',
                               #'股东代码' 
                               'tr_mrkt_code',
                               #'帐号类别' 
                               'tr_type',
                               #'成交类型'
                               'tr_suc_type',
                               #'保留信息',
                               'tr_ref_information',
                               ]
        #当前委托信息
        self.cur_entrust_list = [
                                #'委托时间' 
                                'en_time',
                                #'证券代码' 
                                'en_code',
                                #'证券名称' 
                                'en_name',
                                #'买卖标志' 
                                'en_side_1',
                                #'买卖标志' 
                                'en_side_2',
                                #'委托类别'
                                'en_type',
                                #'状态说明' 
                                'en_status',
                                #'委托价格' 
                                'en_price',
                                #'委托数量' 
                                'en_amount',
                                #'委托编号' 
                                'en_number',
                                #'成交价格' 
                                'en_deal_price',
                                #'成交数量' 
                                'en_deal_amount',
                                #'委托方式' 
                                'en_way',
                                #'委托属性' 
                                'en_pro',
                                #'股东代码' 
                                'en_user_code',
                                #'帐号类别' 
                                'en_count_type',
                                #'交易所代码' 
                                'en_tr',
                                #'撤单标志' 
                                'en_quit',
                                #'(参数)操作数据' 
                                'en_data',
                                #'句柄'
                                'en_handler',
                                #'保留信息'
                                'en_ref_data',
                                 ]
        #当前股票名称
        self.stock_list = []
        #当前所有股票块
        self.all_stock_info = {}
        #当前所有持仓信息
        self.property_info = {}
        #当前委托列表
        self.entrust_list = []
        #当前委托块
        self.all_entrust_info = {}
        #当日成交列表
        self.deal_list = []
        #当日成交列表明细
        self.all_deal_info = {}
        



    def _format_stock(self,**kwargs):
        start = 2 
        step = int(self.stock_info_block[0])
        count = int(self.stock_info_block[1]) + 1

        if count == 1:
            logging.debug("no hold stock")
        else:
            for col in range(count):
                tmp_stock = {}
                if col == 0:
                    continue
                else:
                    start += step  
                    for row in range(step):
                        if self.stock_info_block[start+row] == '':
                            tmp_stock[self.cur_index_list[row]] = 0
                        else:
                            tmp_stock[self.cur_index_list[row]] = self.stock_info_block[start+row]
    #                 Control.post_single_position(self.sec_hold_user,out_str)
                    self.stock_list.append(tmp_stock['sec_code'])
                    self.all_stock_info[tmp_stock['sec_code']] = tmp_stock
            stock_info_list = [] 
            for code in self.stock_list:
                out_stock = {}
                out_stock['po_StockCode'] = self.all_stock_info[code]['sec_code']
                out_stock['po_StockName'] = self.all_stock_info[code]['sec_name'].encode('utf-8').decode('utf-8')
                out_stock['po_StockMuch'] = self.all_stock_info[code]['sec_amount']
                out_stock['po_Inventory'] = self.all_stock_info[code]['sec_amount']
                out_stock['po_SellMuch'] = self.all_stock_info[code]['sec_trade_amount']
                out_stock['po_CostMoney'] = self.all_stock_info[code]['sec_cost_price']
                out_stock['po_NowMoney'] = self.all_stock_info[code]['sec_cur_price']
                out_stock['po_Market'] = self.all_stock_info[code]['sec_latest_market_val']
                out_stock['po_PL'] = self.all_stock_info[code]['sec_cfpl']
                out_stock['po_PLRatio'] = self.all_stock_info[code]['sec_plr']
                stock_info_list.append(out_stock)
            DbControler.insert_position_table(stock_info_list,self.user_id)
            print("inserted position table")
            logging.debug("inserted position table")
 
    #格式化相应资金持仓情况
    def _format_property(self,**kwargs):
        start = 2 
        step = int(self.property_block[0])
        count = int(self.property_block[1]) + 1
        tmp_property = {}
        if count == 1:
            logging.debug("no property")
        else:
            for col in range(count):
                if col == 0:
                    continue
                else:
                    start += step
                    for row in range(step):
                        if self.property_block[start+row] == '':
                            tmp_property[self.cur_property_list[row]] = 0
                        else:
                            tmp_property[self.cur_property_list[row]] = self.property_block[start+row]
                    self.property_info = tmp_property
                property_info_list = []
                out_property = {}
                # 恒泰证券资金信息没有反馈盈亏比例
                out_property['fu_PL'] = self.property_info['pro_type']
                out_property['fu_GetMoney'] = self.property_info['pro_avail']
                out_property['fu_Market'] = self.property_info['pro_now']
                out_property['fu_AvailableMoney'] = self.property_info['pro_use']
                out_property['fu_Total'] = self.property_info['pro_total']
                # out_property['af_Name'] = self.sec_hold_user
                # out_property['af_Type_Id'] = '3'#self.property_info['pro_type']
                # out_property['af_Interests'] = self.property_info['pro_now']
                # out_property['af_AvailableMoney'] = self.property_info['pro_use']
                # out_property['af_Position'] = self.property_info['pro_freezed']
                # out_property['af_PL'] = '0'

                property_info_list.append(out_property)
                DbControler.insert_fund_table(property_info_list,self.user_id)
                logging.debug("inserted accountfunds table")
                print("inserted accountfunds table")

    #格式化相应成交信息
    def _format_deal_record(self,**kwargs):
        start = 2 
        step = int(self.finish_book_block[0])
        count = int(self.finish_book_block[1]) + 1
        if count == 1:
            logging.debug("no trade")
        else:
            for col in range(count):
                tmp_finish_book = {}
                if col == 0:
                    continue
                else:
                    start += step
                    for row in range(step):
                        if self.finish_book_block[start+row] == '':
                            tmp_finish_book[self.cur_trade_list[row]] = 0
                        else:
                            tmp_finish_book[self.cur_trade_list[row]] = self.finish_book_block[start+row]
                    self.deal_list.append(tmp_finish_book['tr_code'])
                    self.all_deal_info[tmp_finish_book['tr_code']] = tmp_finish_book
                deal_info_list = [] 
                for record in self.deal_list:
                    out_deal = {}
                    out_deal['dr_Date'] = time.strftime("%Y-%m-%d")
                    raw_time = self.all_deal_info[record]['tr_time']
                    out_deal['dr_Time'] = raw_time[:2] + ":" + raw_time[2:4] + ":" + raw_time[4:]
                    out_deal['dr_StockCode'] = self.all_deal_info[record]['tr_code']
                    out_deal['dr_StockName'] = self.all_deal_info[record]['tr_name']
                    out_deal['dr_SignId'] = self.all_deal_info[record]['tr_side']
                    out_deal['dr_EntrustMoney'] = self.all_deal_info[record]['tr_price']
                    out_deal['dr_EntrustMuch'] = self.all_deal_info[record]['tr_amount']
                    out_deal['dr_EntrustNumber'] = self.all_deal_info[record]['tr_en_code']
                    out_deal['dr_DealMoney'] = self.all_deal_info[record]['tr_cost']
                    out_deal['dr_DealMuch'] = self.all_deal_info[record]['tr_amount']
                    out_deal['dr_SumMoney'] = self.all_deal_info[record]['tr_cost']
                    deal_info_list.append(out_deal)
                DbControler.insert_dealrecord_table(deal_info_list,self.user_id)
                logging.debug("inserted recordlist table")
                print("inserted recordlist table")
#                 logging.debug("inserted accountfunds table")

    #格式化相应的交易明细
    def _format_entrust(self,**kwargs):
        start = 2 
        step = int(self.entrust_block[0])
        count = int(self.entrust_block[1]) + 1
        print(self.entrust_block)
        if count == 1:
            logging.debug("no entrust")
        else:
            for col in range(count):
                tmp_entrust = {}
                if col == 0:
                    continue
                else:
                    start += step
                    for row in range(step):
#                         print(self.cur_entrust_list[row])
                        if self.entrust_block[start+row] == '':
                            tmp_entrust[self.cur_entrust_list[row]] = 'null' 
                        else:
                            tmp_entrust[self.cur_entrust_list[row]] = self.entrust_block[start+row]
                    self.entrust_list.append(tmp_entrust['en_number'])
                    self.all_entrust_info[tmp_entrust['en_number']] = tmp_entrust
            entrust_info_list = []
            for entrust in self.entrust_list:
                out_entrust = {}
                out_entrust['et_Date'] = time.strftime("%Y-%m-%d") 
                out_entrust['et_OperateDate'] = time.strftime("%Y-%m-%d")
                raw_time = self.all_entrust_info[entrust]['en_time']
                out_entrust['et_OperateTime'] = raw_time[:2] + ":" + raw_time[2:4] + ":" + raw_time[4:]
                out_entrust['et_StockCode'] = self.all_entrust_info[entrust]['en_code']
                out_entrust['et_StockName'] = self.all_entrust_info[entrust]['en_name']
                out_entrust['et_SignId'] = self.all_entrust_info[entrust]['en_side_1']
                out_entrust['et_Money'] = self.all_entrust_info[entrust]['en_price']
                out_entrust['et_Much'] = self.all_entrust_info[entrust]['en_amount']
                out_entrust['et_Number'] = self.all_entrust_info[entrust]['en_number']
                out_entrust['et_DealMuch'] = '1'
                out_entrust['et_DealMoney'] = '1'
                out_entrust['et_DanMuch'] = '1'
                out_entrust['et_Status'] = '1'
                entrust_info_list.append(out_entrust)
            DbControler.insert_entrust_table(entrust_info_list,self.user_id)
            print("inserted entrust table")
            logging.debug("inserted entrust table")


class ChangJiangStockInfo(AbstractStockInfo):
    def __init__(self, stock_info_block, property_block, entrust_block, finish_book_block,sec_hold_user, user_id):#
        self.user_id = user_id
        self.sec_hold_user = sec_hold_user
        # 资金信息块
        self.property_block = property_block
        # # 交易委托块
        self.entrust_block = entrust_block
        # # 交易完成委托块
        self.finish_book_block = finish_book_block


        self.cur_index_list = ['sec_code',  # '证券代码'
                               'sec_name',  # '证券名称'
                               'sec_amount',  # '证券数量'
                               'sec_trade_amount',  # '可卖数量'
                               'sec_buy_today_amount',  # '今买持仓'
                               'sec_sell_today_amount',  #'今卖持仓'
                               'sec_cur_rcc',  # '参考成本价'
                               'sec_cur_price',  # '当前价'
                               'sec_cur_lmv',  # '参考市值'
                               'sec_rpl',  # '参考盈亏'
                               'sec_rpl_ratio',  # '参考盈亏比例(%)'
                               'sec_share_code',  # '股东代码'
                               'sec_account_type',  # '帐号类别'
                               'sec_exchange_code',  # '交易所代码'
                               'sec_reference_information'  # '保留信息'
                               ]
        # 当前相应账户的持仓类别

        self.cur_property_list = [
                                    # '币种'
                                    'pro_type',
                                    # '资金余额'
                                    'pro_amount',
                                    # '可用资金'
                                    'pro_use',
                                    # '冻结资金'
                                    'pro_freezed',
                                    # '可取资金'
                                    'pro_avail',
                                    # '参考市值',
                                    'pro_now',
                                    # '总资产'
                                    'pro_total',
                                    # '操作标志',
                                    'pro_action_label',
                                    #'提示信息3',
                                    'pro_ref_info_3',
                                    #'提示信息4',
                                    'pro_ref_info_4',
                                    # '提示信息5',
                                    'pro_ref_info_5',
                                    # '保留信息'
                                    'reserve_information',
                                    ]
        # 当前委托信息

        self.cur_entrust_list = [
            # '委托时间'
            'en_time',
            # '证券代码'
            'en_code',
            # '证券名称'
            'en_name',
            # '买卖标志'
            'en_side_1',
            # '买卖标志'
            'en_side_2',
            # '委托类别'
            'en_type',
            # '状态说明'
            'en_status',
            # '委托价格'
            'en_price',
            # '委托数量'
            'en_amount',
            # '成交价格'
            'en_deal_price',#'成交数量', '委托方式', '报价方式', '委托编号', '股东代码', '帐号类别', '交易所代码',, '保留信息'
            # '成交数量'
            'en_deal_amount',
            # '委托方式'
            'en_way',
            # '报价方式
            'en_order_way',
            # '委托编号'
            'en_number',
            # '股东代码'
            'en_user_code',
            # '废单原因',
            'en_cancel_re'
            # '帐号类别'
            'en_count_type',
            # '交易所代码'
            'en_tr',
            # '显示颜色'
            'en_color',
            #'(参数)操作数据',
            'en_ref_data',
            #'句柄',
            'en_handler',
            # '保留信息'
            'en_ref_data',
        ]
        # 当前用户成交股票信息

        self.cur_trade_list = [
            # '成交时间'
            'tr_time',
            # '证券代码'
            'tr_code',
            # '证券名称'
            'tr_name',
            # '买卖标志'
            'tr_side',
            # '买卖标志'
            'tr_flag',
            # '状态说明',
            'tr_ref_status'
            # '成交价格'
            'tr_price',
            # '成交数量'
            'tr_amount',
            # '成交金额'
            'tr_cost',
            # '成交编号'
            'tr_suc_code',
            # '委托编号'
            'tr_en_code',
            # '股东代码'
            'tr_mrkt_code',
            # '帐号类别'
            'tr_type',
            #'显示颜色',
            'tr_color',
            # '(参数)操作数据'
            'tr_ref_data',
            # '句柄',
            'tr_handler',
            # '保留信息',
            'tr_ref_information',
        ]
        # 当前股票名称
        self.stock_list = []
        # 当前所有股票块
        self.all_stock_info = {}
        # 当前所有持仓信息
        self.property_info = {}
        # 当前委托列表
        self.entrust_list = []
        # 当前委托块
        self.all_entrust_info = {}
        # 当日成交列表
        self.deal_list = []
        # 当日成交列表明细
        self.all_deal_info = {}

        self.stock_info_block = stock_info_block

    def _format_stock(self, **kwargs):
        start = 2
        step = int(self.stock_info_block[0])
        count = math.floor(len(self.stock_info_block) / step)
        if count == 1:
            print('no position')
            logging.debug('no position')
            return
        for col in range(count):
            tmp_stock = {}
            if col == 0:
                continue
            else:
                start += step
                for row in range(step):
                    if self.stock_info_block[start + row] == '':
                        tmp_stock[self.cur_index_list[row]] = 0
                    else:
                        tmp_stock[self.cur_index_list[row]] = self.stock_info_block[start + row]
                self.stock_list.append(tmp_stock['sec_code'])
                self.all_stock_info[tmp_stock['sec_code']] = tmp_stock
        stock_info_list = []
        for code in self.stock_list:
            out_stock = {}
            out_stock['po_StockCode'] = self.all_stock_info[code]['sec_code']
            out_stock['po_StockName'] = self.all_stock_info[code]['sec_name'].encode('utf-8').decode('utf-8')
            out_stock['po_StockMuch'] = self.all_stock_info[code]['sec_amount']
            out_stock['po_Inventory'] = self.all_stock_info[code]['sec_amount']
            out_stock['po_SellMuch'] = self.all_stock_info[code]['sec_trade_amount']
            out_stock['po_CostMoney'] = self.all_stock_info[code]['sec_cur_rcc']
            out_stock['po_NowMoney'] = self.all_stock_info[code]['sec_cur_price']
            out_stock['po_Market'] = self.all_stock_info[code]['sec_cur_lmv']
            out_stock['po_PL'] = self.all_stock_info[code]['sec_rpl']
            out_stock['po_PLRatio'] = self.all_stock_info[code]['sec_rpl_ratio']
            stock_info_list.append(out_stock)
        DbControler.insert_position_table(stock_info_list, self.user_id)
        print("inserted position table")
        logging.debug("inserted position table")

    # 格式化相应资金持仓情况
    def _format_property(self, **kwargs):
        start = 2
        step = int(self.property_block[0])
        count = int(self.property_block[1]) + 1
        tmp_property = {}
        if count == 1:
            logging.debug("no property")
        else:
            for col in range(count):
                if col == 0:
                    continue
                else:
                    start += step
                    for row in range(step):
                        if self.property_block[start + row] == '':
                            tmp_property[self.cur_property_list[row]] = 0
                        else:
                            tmp_property[self.cur_property_list[row]] = self.property_block[start + row]
                    self.property_info = tmp_property
                property_info_list = []
                out_property = {}

                out_property['fu_PL'] = self.property_info['pro_type']

                out_property['fu_GetMoney'] = self.property_info['pro_avail']

                out_property['fu_Market'] = self.property_info['pro_now']

                out_property['fu_AvailableMoney'] = self.property_info['pro_use']
                out_property['fu_Total'] = self.property_info['pro_total']


                property_info_list.append(out_property)
                DbControler.insert_fund_table(property_info_list, self.user_id)
                logging.debug("inserted accountfunds table")
                print("inserted accountfunds table")

        # 格式化相应的交易明细

    def _format_entrust(self, **kwargs):
        start = 2
        step = int(self.entrust_block[0])
        count = int(self.entrust_block[1]) + 1
        print(self.entrust_block)
        if count == 1:
            print("no entrust")
            logging.debug("no entrust")
        else:
            for col in range(count):
                tmp_entrust = {}
                if col == 0:
                    continue
                else:
                    start += step
                    for row in range(step):
                        #                         print(self.cur_entrust_list[row])
                        if self.entrust_block[start + row] == '':
                            tmp_entrust[self.cur_entrust_list[row]] = 'null'
                        else:
                            tmp_entrust[self.cur_entrust_list[row]] = self.entrust_block[start + row]
                    self.entrust_list.append(tmp_entrust['en_number'])
                    self.all_entrust_info[tmp_entrust['en_number']] = tmp_entrust
            entrust_info_list = []
            for entrust in self.entrust_list:
                out_entrust = {}
                out_entrust['et_Date'] = time.strftime("%Y-%m-%d")
                out_entrust['et_OperateDate'] = time.strftime("%Y-%m-%d")
                raw_time = self.all_entrust_info[entrust]['en_time']
                out_entrust['et_OperateTime'] = raw_time[:2] + ":" + raw_time[2:4] + ":" + raw_time[4:]
                out_entrust['et_StockCode'] = self.all_entrust_info[entrust]['en_code']
                out_entrust['et_StockName'] = self.all_entrust_info[entrust]['en_name']
                out_entrust['et_SignId'] = self.all_entrust_info[entrust]['en_side_1']
                out_entrust['et_Money'] = self.all_entrust_info[entrust]['en_price']
                out_entrust['et_Much'] = self.all_entrust_info[entrust]['en_amount']
                out_entrust['et_Number'] = self.all_entrust_info[entrust]['en_number']
                out_entrust['et_DealMuch'] = '1'
                out_entrust['et_DealMoney'] = '1'
                out_entrust['et_DanMuch'] = '1'
                out_entrust['et_Status'] = '1'
                entrust_info_list.append(out_entrust)
            DbControler.insert_entrust_table(entrust_info_list, self.user_id)
            print("inserted entrust table")
            logging.debug("inserted entrust table")

    # 格式化相应成交信息
    def _format_deal_record(self, **kwargs):
        start = 2
        step = int(self.finish_book_block[0])
        count = int(self.finish_book_block[1]) + 1
        if count == 1:
            print("no trade")
            logging.debug("no trade")
        else:
            for col in range(count):
                tmp_finish_book = {}
                if col == 0:
                    continue
                else:
                    start += step
                    for row in range(step):
                        if self.finish_book_block[start + row] == '':
                            tmp_finish_book[self.cur_trade_list[row]] = 0
                        else:
                            tmp_finish_book[self.cur_trade_list[row]] = self.finish_book_block[start + row]
                    self.deal_list.append(tmp_finish_book['tr_code'])
                    self.all_deal_info[tmp_finish_book['tr_code']] = tmp_finish_book
                deal_info_list = []
                for record in self.deal_list:
                    out_deal = {}
                    out_deal['dr_Date'] = time.strftime("%Y-%m-%d")
                    raw_time = self.all_deal_info[record]['tr_time']
                    out_deal['dr_Time'] = raw_time[:2] + ":" + raw_time[2:4] + ":" + raw_time[4:]
                    out_deal['dr_StockCode'] = self.all_deal_info[record]['tr_code']
                    out_deal['dr_StockName'] = self.all_deal_info[record]['tr_name']
                    out_deal['dr_SignId'] = self.all_deal_info[record]['tr_side']
                    out_deal['dr_EntrustMoney'] = self.all_deal_info[record]['tr_price']
                    out_deal['dr_EntrustMuch'] = self.all_deal_info[record]['tr_amount']
                    out_deal['dr_EntrustNumber'] = self.all_deal_info[record]['tr_en_code']
                    out_deal['dr_DealMoney'] = self.all_deal_info[record]['tr_cost']
                    out_deal['dr_DealMuch'] = self.all_deal_info[record]['tr_amount']
                    out_deal['dr_SumMoney'] = self.all_deal_info[record]['tr_cost']
                    deal_info_list.append(out_deal)
                DbControler.insert_dealrecord_table(deal_info_list, self.user_id)
                logging.debug("inserted recordlist table")
                print("inserted recordlist table")
#                 logging.debug("inserted accountfunds table")
