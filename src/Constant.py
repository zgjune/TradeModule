#encoding: utf-8
'''
Created on 2018年6月24日

@author: lxj
'''

#查询相关账号的信息代号
#用于Trader.query_positions
#查询所有资金情况
QUERY_PROPERTY = 104
#当日持股票
QUERY_STOCKS = 1114
#当日可用资金
QUERY_AVALIBLE_ON_NEWSTOCK_PROPERTY = 1156
#成交记录 
QUERY_FINISH_BOOK = 1108
#查询当日委托
QUERY_BOOK = 1102

#交易相应方向
#用于 Trader.send_order
SEND_BUY = 0
SEND_SELL = 1

#取消交易市场类型
#用于Trader.cancel_order
CANCEL_SH = 1
CANCEL_SZ = 2

#dll路径
DLL_PATH ="./JLAPI.dll"


#用户交易使用信息
TRADE_PORT = 7708

#券商IP
DONGBEI_IP = '113.105.77.163'
GUOJUN_IP = '114.141.165.219'

HENGTAI_IP = '202.99.230.133'

CHANGCHENG_IP = '219.133.95.102'



GUOSHENG_IP = '117.40.3.6'


DONGGUAN_IP = '218.16.124.5'

CHANGJIANG_IP = '59.173.7.38'

ZHONGTOU_IP = '61.144.233.115'


#用户的券商
DONGBEI_YYB = '0'
GUOJUN_YYB = '78'
HENGTAI_YYB = '0'
CHANGCHENG_YYB = '0'
DONGGUAN_YYB = '0'

GUOSHENG_YYB = '0'

CHANGJIANG_YYB = '0'
ZHONGTOU_YYB = '0'
#传输相关
POST_HEAD = "https://bs.novly.com/servlet/"
POST_POSITION = POST_HEAD + "TestService"


