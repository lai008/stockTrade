import baostock as bs
import pandas as pd
import talib as ta
#https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
import matplotlib.pyplot as plt

def computeMACD(code, startdate, enddate):
    login_result = bs.login(user_id='anonymous', password='123456')
    print(login_result)
    # 获取股票日 K 线数据
    rs = bs.query_history_k_data(code,
                                 "date,code,close,tradeStatus",
                                 start_date=startdate,
end_date=enddate,
                                 # frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、
                                 # 5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；
                                 # 指数没有分钟线数据；周线每周最后一个交易日才可以获取，
                                 # 月线每月最后一个交易日才可以获取。
                                 frequency="d", adjustflag="3")
    # 打印结果集
    result_list = []

    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        result_list.append(rs.get_row_data())
    df = pd.DataFrame(result_list, columns=rs.fields)
    # 剔除停盘数据
    df2 = df[df['tradeStatus'] == '1']
    # 获取 dif,dea,hist，它们的数据类似是 tuple，且跟 df2 的 date 日期一一对应
    # 记住了 dif,dea,hist 前 33 个为 Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    # 这里计算的 hist 就是 dif-dea,而很多证券商计算的 MACD=hist*2=(dif-dea)*2


    dif, dea, hist = ta.MACD(df2['close'].astype(
        float).values, fastperiod=12, slowperiod=26, signalperiod=9)
    df3 = pd.DataFrame({'dif': dif[33:], 'dea': dea[33:], 'hist':
    hist[33:]},
                         index = df2['date'][33:], columns = ['dif', 'dea',
    'hist'])
    df3.plot(title='MACD')



    # 寻找 MACD 金叉和死叉
    datenumber = int(df3.shape[0])
    for i in range(datenumber - 1):
        if((df3.iloc[i, 0] <= df3.iloc[i, 1]) & (df3.iloc[i + 1, 0] >= df3.iloc[i + 1, 1])):
           print("MACD 金叉的日期:" + df3.index[i + 1])
           #print( df3.iloc[i,0])
           #print( df3.iloc[i+1,0]) #DIF
           #print( df3.iloc[i+1,1]) #DEA
           # 金叉向前移動3日的波動率
           i = i - 3
           # DIF/DEA 波動率計算
           print("DIF/DEA 波動率:")
           print(df3.iloc[i+1,0]/ df3.iloc[i+1,1])

          # df_data.loc[kdj_position[(kdj_position == True) &
          #   (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'

        if ((df3.iloc[i, 0] >= df3.iloc[i, 1]) & (df3.iloc[i + 1, 0] <=
                                              df3.iloc[i + 1, 1])):
           print("MACD 死叉的日期:" + df3.index[i + 1])
           #死叉向前移動3日的波動率
           i=i-3
           #DIF/DEA 波動率計算
           print("DIF/DEA 波動率:")
           print(df3.iloc[i + 1, 0] / df3.iloc[i + 1, 1])

    plt.show()
    df.to_csv("/Users/zou/PycharmProjects/weiyl_919/macd.csv", encoding='gbk')

    bs.logout()

    return (dif, dea, hist)


if __name__ == '__main__':
    code = 'sz.000858'
    startdate = '2017-03-01'
    enddate = '2019-09-01'
    (dif, dea, hist) = computeMACD(code, startdate, enddate)