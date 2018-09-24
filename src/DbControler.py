#encoding: utf-8
'''
Created on 2018年7月24日

@author: Administrator
'''
#数据库ip
import pymysql
import sqlalchemy
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Numeric, BigInteger
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.session import sessionmaker
import time
import logging

db_ip = "112.74.48.66"
db_port = "3306"
#用户
db_user = "bs"
#密码
db_password = "baoshui"
#数据库名
db_name = "bs_user"
#目标路径
target_location = 'mysql+pymysql://'+db_user+':'+db_password+'@'+db_ip+':3306/'+db_name
#相应的数据库表名
tb_accountFund = "accountfunds"

DynamicBase = declarative_base(class_registry=dict())

engine = sqlalchemy.create_engine(target_location)


def insert_funds(property_list):
    pass

def delete_content(table_name,user_field,user_id):
    conn = engine.connect()
    try:
        delete_str  = "DELETE FROM "+ table_name +" WHERE "+ user_field + " = " + user_id
        conn.connect()
        conn.execute(delete_str)
    except Exception as e:
        logging.exception('erorr msg')
    finally:
        conn.close()

def delete_content_by_date(table_name,user_field,date_field,user_date,user_id):
    conn = engine.connect()
    try:
        delete_str = "DELETE FROM "+ table_name + " WHERE "+ user_field +" = "+ user_id +" AND " + date_field +  " = '"+ user_date + "'"
        conn.connect()
        conn.execute(delete_str)
    except Exception as e:
        logging.exception('erorr msg')
    finally:
        conn.close()

def delete_unordered_by_date(table_name,user_field,date_field,user_date,user_id):
    conn = engine.connect()
    try:
        delete_str = "DELETE FROM "+ table_name + " WHERE "+ user_field +" = "+ user_id +" AND " + date_field +  " = '"+ user_date + "'" +" AND " + 'et_Status' +  " = '"+ '1' + "'"
        conn.connect()
        conn.execute(delete_str)
    except Exception as e:
        logging.exception('erorr msg')
    finally:
        conn.close()

def insert_entrust_table(entrust_info_list,user_id):
    today = time.strftime("%Y-%m-%d")
    delete_content_by_date("entrust","et_UserId","et_Date",today,user_id)
    for entrust in entrust_info_list:
        val_name_sql = ''
        val_val_sql = ''
        val_name = []
        val_value = []
        for key,value in entrust.items():
            val_name.append(key)
            val_value.append(value)
        for i in range(len(val_name)):
            if i != len(val_name)-1:
                val_name_sql += val_name[i] + ","
            else:
                val_name_sql += val_name[i] + ", et_UserId"
        val_val_sql = "'" + val_value[0] + "', " +"'" + val_value[1]+"', '" + val_value[2] +"', '"+ val_value[3] + "', " + "'" + val_value[4]+"', "+ "'" + val_value[5]+"', "+ "'" + val_value[6]+"', "+ "'" + val_value[7]+"', "+ "'" + val_value[8]+"', " +"'" + val_value[9]+"', "+"'" + val_value[10]+"', "+"'" + val_value[11]+"', " +"'" + val_value[12]+"', "+ user_id
        insert_sql = "INSERT INTO entrust (" + val_name_sql + ") VALUES ("+val_val_sql + ")"
        conn = engine.connect()
        try:
            conn.connect()
            conn.execute(insert_sql)
        except Exception as e:
            logging.exception('erorr msg')
        finally:
            conn.close()
    
#插入成交表
def insert_dealrecord_table(deal_info_list,user_id):
    today = time.strftime("%Y-%m-%d")
    delete_content_by_date("dealrecord","dr_UserId","dr_Date",today,user_id)
    for deal in deal_info_list:
        val_name_sql = ''
        val_val_sql = ''
        val_name = []
        val_value = []
        for key,value in deal.items():
            val_name.append(key)
            val_value.append(value)
        for i in range(len(val_name)):
            if i != len(val_name)-1:
                val_name_sql += val_name[i] + ","
            else:
                val_name_sql += val_name[i] + ", dr_UserId"
        val_val_sql = "'" + val_value[0] + "', " +"'" + val_value[1]+"', '" + val_value[2] +"', '"+ val_value[3] + "', " + "'" + val_value[4]+"', "+ "'" + val_value[5]+"', "+ "'" + val_value[6]+"', "+ "'" + val_value[7]+"', "+ "'" + val_value[8]+"', " +"'" + val_value[9]+"', "+"'" + val_value[10]+"', " + user_id 
        insert_sql = "INSERT INTO dealrecord (" + val_name_sql + ") VALUES ("+val_val_sql + ")"
        conn = engine.connect()
        try:
            conn.connect()
            conn.execute(insert_sql)
        except Exception as e:
            logging.exception('erorr msg')
        finally:
            conn.close()

#插入持仓表
def insert_position_table(position_block,user_id):
#     delete_content('position','po_UserId',user_id)
    for stock in position_block:
        val_name_sql = ''
        val_val_sql = ''
        val_name = []
        val_value = []
        for key,value in stock.items():
            val_name.append(key)
            val_value.append(value)
        for i in range(len(val_name)):
            if i != len(val_name)-1:
                val_name_sql += val_name[i] + ","
            else:
                val_name_sql += val_name[i] + ", po_UserId"
        val_val_sql = "'" + val_value[0] + "', " +"'" + val_value[1]+"', " + val_value[2] +", "+ val_value[3] + ", " + val_value[4]+", "+ "'" + val_value[5]+"', "+ "'" + val_value[6]+"', "+ "'" + val_value[7]+"', "+ "'" + val_value[8]+"', "+ "'" + val_value[9]+"', " + user_id
        insert_sql = "INSERT INTO position (" + val_name_sql + ") VALUES ("+val_val_sql + ")"
        conn = engine.connect()
        try:
            conn.connect()
            conn.execute(insert_sql)
        except Exception as e:
            logging.exception('erorr msg')
        finally:
            conn.close()
#插入资金表
def insert_accountfunds_table(funds_block,user_id):    
    delete_content('accountfunds','af_UserId',user_id)
    for fund in funds_block:
        val_name_sql = ''
        val_val_sql = ''
        val_name = []
        val_value = []
        for key,value in fund.items():
            val_name.append(key)
            val_value.append(value)
        for i in range(len(val_name)):
            if i != len(val_name)-1:
                val_name_sql += val_name[i] + ","
            else:
                val_name_sql += val_name[i] + ", af_UserId"
        val_val_sql = "'" + val_value[0] + "', " + val_value[1]+", '" + val_value[2] +"', '"+ val_value[3] + "', " + "'" + val_value[4]+"', "+ "'" + val_value[5]+"', "+ user_id
        insert_sql = "INSERT INTO accountfunds (" + val_name_sql + ") VALUES ("+val_val_sql + ")"
        conn = engine.connect()
        try:
            conn.connect()
            conn.execute(insert_sql)
        except Exception as e:
            logging.exception('erorr msg')
        finally:
            conn.close()

#插入资金表(新)
def insert_fund_table(funds_block,user_id):
    delete_content('fund','userId',user_id)
    for fund in funds_block:
        val_name_sql = ''
        val_val_sql = ''
        val_name = []
        val_value = []
        for key,value in fund.items():
            val_name.append(key)
            val_value.append(value)
        for i in range(len(val_name)):
            if i != len(val_name)-1:
                val_name_sql += val_name[i] + ","
            else:
                val_name_sql += val_name[i] + ", userId"
        val_val_sql = "" + str(val_value[0])+ "," + str(val_value[1])+", " + str(val_value[2]) +", "+ str(val_value[3]) + ", " + str(val_value[4]) + ", "+ user_id
        insert_sql = "INSERT INTO fund (" + val_name_sql + ") VALUES ("+val_val_sql + ")"
        conn = engine.connect()
        try:
            conn.connect()
            conn.execute(insert_sql)
        except Exception as e:
            logging.exception('erorr msg')
        finally:
            conn.close()

def query_selected_stock(stock_list):
    list_len =  len(stock_list)
    query_range = '('
    for i in range(list_len):
        print(stock_list[i])
        if i == list_len -1:
            query_range = query_range + "'" + stock_list[i] + "')"
        else:
            query_range =  query_range + "'" + stock_list[i] + "',"
    query_sql = "SELECT * FROM position WHERE po_Id IN %s" %query_range

    conn = engine.connect()
    try:
        conn.connect()
        conn.execute(query_sql)
    except Exception as e:
        logging.exception('erorr msg')
    finally:
        conn.close()


#查询当前用户持仓
def query_user_position(userid):    
    query_sql = "SELECT * FROM position WHERE po_UserId = %s" %userid
    conn = engine.connect()
    try:
        conn.connect()
        res = conn.execute(query_sql)
        stockList = []
        for stock in res:
            stockList.append(stock[1])
        return stockList
    except Exception as e:
        logging.exception('erorr msg')
    finally:
        conn.close()
        if stockList:
            return stockList
        else:
            return None
    
#删除旧有持仓
def delete_old_position(userid,delete_position):
    for stock in delete_position:
        delete_sql ="DELETE FROM position WHERE po_UserId = %s AND po_StockCode = %s"  %(userid,stock)
        conn = engine.connect()
        try:
            conn.connect()
            res = conn.execute(delete_sql)
        except Exception as e:
            logging.exception('erorr msg')
        finally:
            conn.close()
    
#修改旧有持仓信息
def update_position_table(position_block,user_id):
    for stock in position_block:
        val_val_sql = ''
        val_name = []
        val_value = []
        for key,value in stock.items():
            val_name.append(key)
            val_value.append(value)
            
        val_val_sql = val_name[1]+"='" + val_value[1]+"', " + val_name[2] + "="+ val_value[2] +", "+ val_name[3] + "="+ val_value[3] + ", " + val_name[4] +"=" + val_value[4]+", " + val_name[5]+ "='" + val_value[5]+"', "+val_name[6] +" ='" + val_value[6]+"', "+val_name[7] + "='" + val_value[7]+"', "+ val_name[8] + "='" + val_value[8]+"', "+ val_name[9] + "='" + val_value[9]+"' " +"WHERE po_UserId = "+ user_id + " AND po_StockCode = '" + val_value[0] +"'"
        update_sql = "UPDATE position SET " + val_val_sql

        conn = engine.connect()
        try:
            conn.connect()
            conn.execute(update_sql)
        except Exception as e:
            logging.exception('erorr msg')
        finally:
            conn.close()




if __name__ == "__main__":
#     update_position_table([{'po_StockCode': '002198', 'po_StockName': '嘉应制药', 'po_StockMuch': '92900.00', 'po_Inventory': '92900.00', 'po_SellMuch': '92900.00', 'po_CostMoney': '6.503', 'po_NowMoney': '6.1100', 'po_Market': '567619.00', 'po_PL': '-36476.79', 'po_PLRatio': '-6.043'}], '30')
    query_sql = '''UPDATE position SET po_StockCode='002198', po_StockName='嘉应制药', po_StockMuch=92900.00, po_Inventory=92900.00, po_SellMuch=92900.00, po_CostMoney='6.503', po_NowMoney ='6.1100', 
                    po_Market='567619.00', po_PL='-36476.79', po_PLRatio='-6.043' WHERE po_UserId = 30 AND po_StockCode = '002198' '''
    conn = engine.connect()
    try:
        conn.connect()
        conn.execute(query_sql)
    except Exception as e:
        logging.exception('erorr msg')
    # delete_content("entrust","et_UserId", '3')
#     insert_fund_table([{'fu_PL': 0, 'fu_GetMoney': '708.76', 'fu_Market': '824766.00', 'fu_AvailableMoney': '708.76', 'fu_Total': '825474.76'}],'6')
    
    
    
    # res = query_selected_stock(['314','315'])
    # for r in res:
    #     print(r)
    # engine = sqlalchemy.create_engine(target_location)
    # conn = engine.connect()
#     conn.execute("insert into position (po_StockCode,po_StockName,po_StockMuch,po_SellMuch,po_CostMoney,po_NowMoney,po_Market,po_PL,po_PLRatio,po_UserId) values('1', '1', 1, 1, '1', '1', '1', '1', '1', 1)")
#     conn.execute("INSERT INTO accountfunds (af_Name,af_Type_Id,af_Interests,af_AvailableMoney,af_Position, af_UserId) VALUES ('67200134', 1, '755422.12', '51731.36', '0.00', 1)")
#     conn.execute("DELETE FROM position WHERE po_UserId = 1")
#     conn.execute("DELETE FROM dealrecord WHERE dealrecord.dr_UserId = 1 AND dealrecord.dr_Date > '2018-07-30'")
#     result = conn.execute("select * from position where po_Id in (314,315)")
#     today = time.strftime("%d%m%Y")
 
    # for r in result:
    #     #     print(r)
#         time.strptime(raw_time, format)
#         print(tmp_time)

#     delete_content('accountfunds','af_UserId','1')
#     content = [{'dr_Date': '2018-08-01', 'dr_Time': '14:17:02', 'dr_StockCode': '204001', 'dr_StockName': 'GC001', 'dr_SignId': '1', 'dr_EntrustMoney': '3.2950', 'dr_EntrustMuch': '7000.00', 'dr_EntrustNumber': '209', 'dr_DealMoney': '700000.00', 'dr_DealMuch': '7000.00', 'dr_SumMoney': '700000.00'}]
#     insertt_dealrecord_table(content, '1')
#     today = time.strftime("%Y-%m-%d")
#     delete_content_by_date("dealrecord","dr_UserId","dr_Date",today,"1")
#     content = [{'et_Date': '2018-07-31', 'et_OperateDate': '2018-07-31', 'et_OperateTime': '14:32:18', 'et_StockCode': '204001', 'et_StockName': 'GC001', 'et_SignId': '1', 'et_Money': '2.7700', 'et_Much': '7000.00', 'et_Number': '231', 'et_DealMuch': '7000.00','et_DealMoney':'0','et_DanMuch':'0','et_Status':'1'}]
#     insert_entrust_table(content,'1')
#     content = [{'po_StockCode': '600547', 'po_StockName': '山东黄金', 'po_StockMuch': '100', 'po_Inventory': '100', 'po_SellMuch': '100', 'po_CostMoney': '23.741', 'po_NowMoney': '24.0800', 'po_Market': '2408.00', 'po_PL': '8700.93', 'po_PLRatio': '1.428'}, {'po_StockCode': '888880', 'po_StockName': '标准券', 'po_StockMuch': '0', 'po_Inventory': '0', 'po_SellMuch': '0', 'po_CostMoney': '0.000', 'po_NowMoney': '100.0000', 'po_Market': '0.00', 'po_PL': '0.00', 'po_PLRatio': '0.000'}, {'po_StockCode': '002564', 'po_StockName': '天沃科技', 'po_StockMuch': '100', 'po_Inventory': '100', 'po_SellMuch': '100', 'po_CostMoney': '6.888', 'po_NowMoney': '7.0300', 'po_Market': '703.00', 'po_PL': '-5950.16', 'po_PLRatio': '2.062'}, {'po_StockCode': '300136', 'po_StockName': '信维通信', 'po_StockMuch': '100', 'po_Inventory': '100', 'po_SellMuch': '100', 'po_CostMoney': '32.954', 'po_NowMoney': '34.0300', 'po_Market': '3403.00', 'po_PL': '3590.38', 'po_PLRatio': '3.265'}, {'po_StockCode': '300143', 'po_StockName': '星普医科', 'po_StockMuch': '26', 'po_Inventory': '26', 'po_SellMuch': '26', 'po_CostMoney': '12.510', 'po_NowMoney': '8.9900', 'po_Market': '233.74', 'po_PL': '40944.89', 'po_PLRatio': '-28.137'}]
#     insert_position_table(content,'1')


#     conn.execute("insert into position (po_StockCode,po_StockName,po_StockMuch,po_SellMuch,po_CostMoney,po_NowMoney,po_Market,po_PL,po_PLRatio,po_UserId) values('1', '1', 1, 1, '1', '1', '1', '1', '1', 1)")



#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     all = session.query(User).filter_by().all()
#     print(all)
#     all = session.query(Position).filter_by().all()
#     print(all)
#     tmp_property = AccountFunds()
#     tmp_property.af_AvailableMoney= property_info['af_AvailableMoney']
#     tmp_property.af_Interests = property_info['af_Interests']
#     tmp_property.af_Name = property_info['af_Name']
#     tmp_property.af_Position = property_info['af_Position']
#     tmp_property.af_Type_Id = property_info['af_Type_Id']
#     tmp_property.af_UserId = property_info['af_UserId']

#     tmp_property.af_AvailableMoney= '51977.53'
#     tmp_property.af_Interests = '744065.40'
#     tmp_property.af_Name = '67200134'
#     tmp_property.af_Position = '0.00'
#     tmp_property.af_Type_Id = '0'
#     tmp_property.af_UserId = '67200134'
#     session.add(tmp_property)
#     session.commit()
#     session.close()