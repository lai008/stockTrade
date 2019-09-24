# -*- coding: utf-8 -*-
import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节
rs = bs.query_history_k_data_plus("sz.000858",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2019-06-01', end_date='2019-09-18',
    frequency="d", adjustflag="3") #frequency="d"取日k线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)


#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
#### 结果集输出到csv文件 ####
result.to_csv("/Users/zou/PycharmProjects/weiyl_919/history_k_data.csv", encoding="gbk", index=False)
print(result)
#//////////////////////////////////////////////
#### 获取沪深A股估值指标(日频)数据 ####
# peTTM    滚动市盈率
# psTTM    滚动市销率
# pcfNcfTTM    滚动市现率
# pbMRQ    市净率
rs = bs.query_history_k_data_plus("sh.000858",
    "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
    start_date='2019-06-18', end_date='2019-09-18',
    frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
result_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    result_list.append(rs.get_row_data())
result = pd.DataFrame(result_list, columns=rs.fields)

#### 结果集输出到csv文件 ####
result.to_csv("/Users/zou/PycharmProjects/weiyl_919/PE_history_k_data.csv", encoding="gbk", index=False)
print(result)
#/////////////////////////////////////////////
#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
rs = bs.query_history_k_data_plus("sh.000858",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2019-06-18', end_date='2019-09-18',
    frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

#### 结果集输出到csv文件 ####
result.to_csv("/Users/zou/PycharmProjects/weiyl_919/history_k_data.csv", encoding="gbk", index=False)
print(result)
# 返回数据说明
# 参数名称	参数描述	算法说明
# date	交易所行情日期
# code	证券代码
# open	开盘价
# high	最高价
# low	最低价
# close	收盘价
# preclose	前收盘价	见表格下方详细说明
# volume	成交量（累计 单位：股）
# amount	成交额（单位：人民币元）
# adjustflag	复权状态(1：后复权， 2：前复权，3：不复权）
# turn	换手率	[指定交易日的成交量(股)/指定交易日的股票的流通股总股数(股)]*100%
# tradestatus	交易状态(1：正常交易 0：停牌）
# pctChg	涨跌幅（百分比）	日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%
# peTTM	滚动市盈率	(指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/归属母公司股东净利润TTM
# pbMRQ	市净率	(指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具)
# psTTM	滚动市销率	(指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价*截至当日公司总股本)/营业总收入TTM
# pcfNcfTTM	滚动市现率	(指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/现金以及现金等价物净增加额TTM
# isST	是否ST股，1是，0否



#////////////////////////////////////////////



#////////////////////////////////////////////
#### 登出系统 ####
bs.logout()