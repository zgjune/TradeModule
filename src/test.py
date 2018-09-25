from BrokerType.DongBeiStockInfo import DongBeiStockInfo
from Trader import *
if __name__ == "__main__":
    #测试问题券商类型东北证券 
    #情况 荡数据库出现多条东北证券用户实例时候，将会导致相应信息错误 ，从而无法更新 
    #解决方案 将增加的多余券商类型用户资金情况实例 手动删除 
    tmp_trader = Trader(Constant.DONGBEI_IP,
                        Constant.TRADE_PORT,
                        '50506031',
                        '375228',
                        '0',
                        Constant.DONGBEI_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code='',
                        sz_code='',
                        )
    tmp_trader.query_positions(Constant.QUERY_STOCKS)
    stock_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
    tmp_trader.query_positions(Constant.QUERY_PROPERTY)
    property_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
    tmp_trader.query_positions(Constant.QUERY_BOOK)
    entrust_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
    tmp_trader.query_positions(Constant.QUERY_FINISH_BOOK)
    finish_book_input = tmp_trader.trader_Ree.value.decode('gbk', 'ignore').split('|')
    donbei_stock_info = DongBeiStockInfo(stock_input, property_input, entrust_input, finish_book_input,'50506031','30')
    donbei_stock_info.update_stock_info()