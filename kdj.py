# -*- coding: utf-8 -*-
import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def computeKDJ(code, startdate, enddate):
    login_result=bs.login(user_id='anonymous', password='123456')
    print(login_result.error_msg)


    # 获取股票日K线数据
    rs=bs.query_history_k_data(code,
                                 "date,code,high,close,low,tradeStatus",
                                 start_date=startdate, end_date=enddate,
                                 frequency="d", adjustflag="3")

    # 打印结果集
    result_list=[]

    while (rs.error_code == '0') & rs.next():
           # 获取一条记录，将记录合并在一起
           result_list.append(rs.get_row_data())
    df_init = pd.DataFrame(result_list, columns=rs.fields)
    # 剔除停盘数据
    df_status = df_init[df_init['tradeStatus'] == '1']

    low = df_status['low'].astype(float)
    del df_status['low']
    df_status.insert(0, 'low', low)
    high = df_status['high'].astype(float)
    del df_status['high']
    df_status.insert(0, 'high', high)
    close = df_status['close'].astype(float)
    del df_status['close']
    df_status.insert(0, 'close', close)

    # 计算KDJ指标,前9个数据为空
    low_list = df_status['low'].rolling(window=9).min()
    high_list = df_status['high'].rolling(window=9).max()

    rsv = (df_status['close'] - low_list) / (high_list - low_list) * 100

    df_data = pd.DataFrame()
    df_data['K'] = rsv.ewm(com=2).mean()
    df_data['D'] = df_data['K'].ewm(com=2).mean()
    df_data['J'] = 3 * df_data['K'] - 2 * df_data['D']
    #2019-9-24

    #取enddate的J值
    df_J=df_data['J'].tolist()
    print(df_J[-1])



    #
    df_data.index = df_status['date'].values
    df_data.index.name = 'date'
    # 删除空数据
    df_data = df_data.dropna()
    #计算KDJ指标金叉、死叉情况
    df_data['KDJ_金叉死叉'] = ''
    kdj_position = df_data['K'] > df_data['D']
    df_data.loc[kdj_position[(kdj_position == True) &
    (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
    # TODO 加入微信触发提醒
    df_data.loc[kdj_position[(kdj_position == False) &
    (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'
    # TODO 加入微信触发提醒

    df_data.plot(title='KDJ')

    #plt.show()
    bs.logout()
    #return (df_data)
    return (df_J)


if __name__ == '__ma' \
               'in__':
   code = 'sz.000858'
   startdate = '2017-01-01'
   #enddate = '2019-08-14'
   today = datetime.datetime.now().strftime('%Y%m%d')
   enddate = f'{today[0:4]}-{today[4:6]}-{today[6:8]}'


   #df = computeKDJ(code,startdate,enddate)
   KDJ_J=computeKDJ(code,startdate,enddate)

   for KDJ_J in KDJ_J:

      if KDJ_J > 100:
          print(KDJ_J)

   # 保存到文件中
   #df.to_csv("/Users/zou/PycharmProjects/weiyl_919/KDJ.csv", encoding='gbk')
