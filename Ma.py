import baostock as bs
import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import os


def computeMA(self, code, startdate, enddate, is_show, is_refresh, period):
    name_ = ['MA8', 'MA13', 'MA21', 'MA34', 'MA55']
    fb_list = [8, 13, 21, 34, 55]
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 详细指标参数，参见“历史行情指标参数”章节
    rs = bs.query_history_k_data_plus(code,
                                      "date,close,volume,amount",
                                      start_date=startdate, end_date=enddate, frequency="d")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 结果集输出到csv文件
    result.to_csv(r"/Users/zou/PycharmProjects/weiyl_919/history_Index_k_data.csv", index=False)
    close = [float(x) for x in result['close']]
    for item in zip(name_, fb_list):
        result[item[0]] = ta.MA(np.array(close), timeperiod=item[1])
    result.index = result['date']
    result = result[name_]

    loc_list = range(len(result))[::period]
    result = result.iloc[loc_list, :]
    # print(result)
    result.plot(title=f'fb_ma_{period}day')
    if is_show:
        plt.show()
    if is_refresh:
        result.to_csv(os.path.join(root, 'fb_ma.csv'), encoding='gbk')
    # 登出系统
    bs.logout()
    return result

if __name__ == '__main__':
	root = r'/Users/zou/PycharmProjects/weiyl_919/'
	task = getTarget(root)

	code = 'sz.000568'
	startdate = '2017-01-01'
	enddate = '2019-09-22'
	period = 1
	# 计算KDJ,MACD,MA,VOL,MA，最后两个参数为 是否显示图 以及 是否更新数据。

	df_ma = task.computeMA(code, startdate, enddate,1, 1,period)
