# -*- coding: utf-8 -*-
import baostock as bs
import pandas as pd
import talib as ta
#ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
import matplotlib.pyplot as plt


def computeRSI(code, startdate, enddate):
    """计算证券在起止时间内的 RSI 指标。
    :param code:证券代码
    :param startdate:起始日期
    :param enddate:截止日期
    :return:
"""

    login_result = bs.login(user_id='anonymous', password='123456')
    print(login_result.error_msg)
    # 获取股票日 K 线数据,adjustflag 复权状态(1:后复权， 2:前复权，3: 不复权)
    rs = bs.query_history_k_data(code, "date,code,close,tradeStatus",
                                 start_date=startdate, end_date=enddate,
                                 frequency="d", adjustflag="3")
    # 打印结果集
    result_list = []
    while (rs.error_code == '0') & rs.next():
          # 获取一条记录，将记录合并在一起
          result_list.append(rs.get_row_data())
    df_init = pd.DataFrame(result_list, columns=rs.fields)
    # 剔除停盘数据
    df_status = df_init[df_init['tradeStatus'] == '1']

    df_status['close'] = df_status['close'].astype(float)

    rsi_12days = ta.RSI(df_status['close'], timeperiod=12)
    rsi_6days = ta.RSI(df_status['close'], timeperiod=6)
    rsi_24days = ta.RSI(df_status['close'], timeperiod=24)
    df_status['rsi_6days'] = rsi_6days
    df_status['rsi_12days'] = rsi_12days
    df_status['rsi_24days'] = rsi_24days


    # RSI 超卖和超买
    rsi_buy_position = df_status['rsi_6days'] > 80
    rsi_sell_position = df_status['rsi_6days'] < 20

    df_status.loc[rsi_buy_position[(rsi_buy_position == True) &
                                   (rsi_buy_position.shift() == False)].index, '超买'] = '超买'
    # TODO 加入微信触发提醒
    df_status.loc[rsi_sell_position[(rsi_sell_position == True) &
                                    (rsi_sell_position.shift() == False)].index, '超卖'] = '超卖'
    # TODO 加入微信触发提醒
    return df_status


if __name__ == '__main__':
   code = "sh.000858"
   startdate = "2017-01-01"
   enddate = "2019-07-01"
   df = computeRSI(code, startdate, enddate)
   df2 = df[['date', 'rsi_6days', 'rsi_12days', 'rsi_24days']]

   df2.index = df['date']
   df2.plot(title='RSI')
   plt.show()
   df.to_csv("/Users/zou/PycharmProjects/weiyl_919/rsi.csv", encoding='gbk')