import baostock as bs
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt

def computeMACD(code, startdate, enddate):
    login_result = bs.login(user_id='anonymous', password='123456')
    print(login_result)
    # 获取股票日 K 线数据
    rs = bs.query_history_k_data(code,
                                 "date,code,close,tradeStatus",
                                 start_date=startdate,
end_date=enddate,
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
        #TODO 加入微信触发提醒
        if ((df3.iloc[i, 0] >= df3.iloc[i, 1]) & (df3.iloc[i + 1, 0] <=
                                              df3.iloc[i + 1, 1])):
           print("MACD 死叉的日期:" + df3.index[i + 1])
           # TODO 加入微信触发提醒

    plt.show()
    df.to_csv("/Users/zou/PycharmProjects/weiyl_919/macd.csv", encoding='gbk')

    bs.logout()

    return (dif, dea, hist)


if __name__ == '__main__':
    code = 'sh.000001'
    startdate = '2017-03-01'
    enddate = '2019-09-01'
    (dif, dea, hist) = computeMACD(code, startdate, enddate)