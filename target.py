# -*- coding: utf-8 -*-
import sys
import datetime
import baostock as bs
import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import os

class getTarget(object):
	"""docstring for getTarget"""
	def __init__(self, root):
		self.root = root
		login_result = bs.login(user_id='anonymous', password='123456')
		print(login_result)



	def get_Colse_price(self):
		#### 获取沪深A股历史K线数据 ####
		# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
		# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag


		today = datetime.datetime.now().strftime('%Y%m%d')
		startdate = '2017-01-01'
		enddate = f'{today[0:4]}-{today[4:6]}-{today[6:8]}'

		rs = bs.query_history_k_data_plus("sz.000001",
										  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
										  start_date=startdate, end_date=enddate,
										  frequency="d", adjustflag="3")
		#print('query_history_k_data_plus respond error_code:' + rs.error_code)
		#print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

		#### 打印结果集 ####
		data_list = []
		while (rs.error_code == '0') & rs.next():
			# 获取一条记录，将记录合并在一起
			data_list.append(rs.get_row_data())
		result = pd.DataFrame(data_list, columns=rs.fields)

		#### 结果集输出到csv文件 ####
		result.to_csv("/Users/zou/PycharmProjects/weiyl_919/history_k_data.csv", encoding="gbk", index=False)
		# 输出代码
		#print(data_list[-1][1])
		# 输出收盘价
		#print(data_list[-1][5])
		return float(data_list[-1][5])

	def get_close(self, code, startdate, enddate, is_show, is_refresh,period):
		login_result = bs.login(user_id='anonymous', password='123456')
		print(login_result.error_msg)
		# 获取股票日K线数据
		rs = bs.query_history_k_data(code,
									 "date,code,high,close,low,tradeStatus",
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

		low = df_status['low'].astype(float)
		del df_status['low']
		df_status.insert(0, 'low', low)
		high = df_status['high'].astype(float)
		del df_status['high']
		df_status.insert(0, 'high', high)
		close = df_status['close'].astype(float)
		del df_status['close']
		df_status.insert(0, 'close', close)

		return float(result_list[-1][3])

	def computeKDJ(self, code, startdate, enddate, is_show, is_refresh,period):
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

		df_data.index = df_status['date'].values
		df_data.index.name = 'date'
		# 删除空数据
		df_data = df_data.dropna()
		# 记录index切片list
		loc_list = range(len(df_data))[::period]
		df_data = df_data.iloc[loc_list,:]
		df_data.plot(title=f'KDJ_{period}day')
		#计算KDJ指标金叉、死叉情况
		df_data['KDJ_金叉死叉'] = ''
		kdj_position = df_data['K'] > df_data['D']
		df_data.loc[kdj_position[(kdj_position == True) &
		(kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
		df_data.loc[kdj_position[(kdj_position == False) &
		(kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'

		if is_show:
			plt.show()
		if is_refresh:
			df_data.to_csv(os.path.join(root,"KDJ.csv"), encoding='gbk')
		bs.logout()
		return (df_data)

	def computeMACD(self, code, startdate, enddate, is_show, is_refresh,period):
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
		df3 = pd.DataFrame({'dif': dif[33:], 'dea': dea[33:], 'hist': hist[33:]},
			index = df2['date'][33:], columns = ['dif', 'dea', 'hist'])

		loc_list = range(len(df3))[::period]
		df3 = df3.iloc[loc_list,:]
		df3.plot(title=f'MACD_{period}day')
		# 寻找 MACD 金叉和死叉
		datenumber = int(df3.shape[0])
		for i in range(datenumber - 1):
			if((df3.iloc[i, 0] <= df3.iloc[i, 1]) & (df3.iloc[i + 1, 0] >= df3.iloc[i + 1, 1])):
				print("MACD 金叉的日期:" + df3.index[i + 1])
				# df_data.loc[kdj_position[(kdj_position == True) &
				#   (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'

			if ((df3.iloc[i, 0] >= df3.iloc[i, 1]) & (df3.iloc[i + 1, 0] <= df3.iloc[i + 1, 1])):
				print("MACD 死叉的日期:" + df3.index[i + 1])
		# 记录index切片list


		if is_show:
			plt.show()
		if is_refresh:
			df.to_csv(os.path.join(root,"macd.csv"), encoding='gbk')
		bs.logout()

		return (dif, dea, hist)
	def computeRSI(self, code, startdate, enddate, is_show, is_refresh, period):
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
			start_date=startdate, end_date=enddate,frequency="d", adjustflag="3")
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

		loc_list = range(len(df_status))[::period]
		df_status = df_status.iloc[loc_list,:]


		# RSI 超卖和超买
		rsi_buy_position = df_status['rsi_6days'] > 80
		rsi_sell_position = df_status['rsi_6days'] < 20
		df_status.loc[rsi_buy_position[(rsi_buy_position == True) &
			(rsi_buy_position.shift() == False)].index, '超买'] = '超买'
		df_status.loc[rsi_sell_position[(rsi_sell_position == True) &
			(rsi_sell_position.shift() == False)].index, '超卖'] = '超卖'
		df_status = df_status[['date', 'rsi_6days', 'rsi_12days', 'rsi_24days']]

		df_status.index = df_status['date']
		df_status.plot(title=f'RSI_{period}day')
		if is_show:
			plt.show()
		if is_refresh:
			df_status.to_csv(os.path.join(root,"rsi.csv"), encoding='gbk')
		return df_status

	def computeMA(self,code,startdate,enddate,is_show, is_refresh, period):
		name_ = ['MA8','MA13','MA21','MA34','MA55']
		fb_list = [8,13,21,34,55]
		# 登陆系统
		lg = bs.login()
		# 显示登陆返回信息
		print('login respond error_code:'+lg.error_code)
		print('login respond  error_msg:'+lg.error_msg)

		# 详细指标参数，参见“历史行情指标参数”章节
		rs = bs.query_history_k_data_plus(code,
		    "date,close,volume,amount",
		    start_date=startdate, end_date=enddate, frequency="d")
		print('query_history_k_data_plus respond error_code:'+rs.error_code)
		print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

		# 打印结果集
		data_list = []
		while (rs.error_code == '0') & rs.next():
		    # 获取一条记录，将记录合并在一起
		    data_list.append(rs.get_row_data())
		result = pd.DataFrame(data_list, columns=rs.fields)
		# 结果集输出到csv文件
		result.to_csv(r"/Users/zou/PycharmProjects/weiyl_919/history_Index_k_data.csv", index=False)
		close = [float(x) for x in result['close']]


		for item in zip(name_,fb_list):
			result[item[0]] = ta.MA(np.array(close), timeperiod=item[1])
		result.index = result['date']
		result = result[name_]

		loc_list = range(len(result))[::period]
		result = result.iloc[loc_list,:]


        #????????
		print(result.iloc[600,[0]])

		result.plot(title=f'fb_ma_{period}day')
		if is_show:
			plt.show()
		if is_refresh:
			result.to_csv(os.path.join(root,'fb_ma.csv'), encoding='gbk')


		# 登出系统
		bs.logout()
		return result

	def get_MA8(self):
		ma_list = df_ma.iloc[-1, :].tolist()
		ma_8, ma_13, ma_21, ma_34, ma_55 = ma_list[0], ma_list[1], ma_list[2], ma_list[3], ma_list[4]
		return float(ma_8)


	def computeVOL(self,code,startdate,enddate,is_show, is_refresh, period):
		# 登陆系统
		lg = bs.login()
		# 显示登陆返回信息
		print('login respond error_code:'+lg.error_code)
		print('login respond  error_msg:'+lg.error_msg)

		# 详细指标参数，参见“历史行情指标参数”章节
		rs = bs.query_history_k_data_plus(code,
		    "date,volume,amount",
		    start_date=startdate, end_date=enddate, frequency="d")
		print('query_history_k_data_plus respond error_code:'+rs.error_code)
		print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

		# 打印结果集
		data_list = []
		while (rs.error_code == '0') & rs.next():
		    # 获取一条记录，将记录合并在一起
		    data_list.append(rs.get_row_data())
		result = pd.DataFrame(data_list, columns=rs.fields)
		result.index = result['date']
		result = result[['volume']]
		result['volume'] = result['volume'].astype(float)
		# print(result)
		# print(result)
		loc_list = range(len(result))[::period]
		result = result.iloc[loc_list,:]

		result.plot(title=f'fb_vol_{period}day')
		if is_show:
			plt.show()
		# 结果集输出到csv文件
		if is_refresh:
			result.to_csv(os.path.join(root,'fb_ma.csv'), encoding='gbk')
		# 登出系统
		bs.logout()
		return result
		
if __name__ == '__main__':

	# root = r'/Users/zou/PycharmProjects/weiyl_919/'
	# task = getTarget(root)
	# code = 'sz.000858'
	# startdate = '2017-01-01'
	# enddate = '2019-09-22'
	# period = 1


	root = r'/Users/zou/PycharmProjects/weiyl_919/'
	task = getTarget(root)
	code = 'sh.600809' \

	today = datetime.datetime.now().strftime('%Y%m%d')
	startdate = '2017-01-01'
	enddate = f'{today[0:4]}-{today[4:6]}-{today[6:8]}'
	period = 1

	# 计算KDJ,MACD,MA,VOL,MA，最后两个参数为 是否显示图 以及 是否更新数据。
	#df_kdj = task.computeKDJ(code,startdate,enddate,1, 1,period)
	#(dif, dea, hist) = task.computeMACD(code, startdate, enddate, 1, 1,period)
	#df_rsi = task.computeRSI(code, startdate, enddate,1, 1,period)
	df_ma = task.computeMA(code, startdate, enddate,1, 1,period)
	df_close=task.get_close(code, startdate, enddate,1, 1,period)
	df_vol=task.computeVOL(code, startdate, enddate,1, 1,period)
	ma_list = df_ma.iloc[-1,:].tolist()
	ma_8,ma_13,ma_21,ma_34,ma_55 = ma_list[0],ma_list[1],ma_list[2],ma_list[3],ma_list[4]
	# print("Ma-8：")
	print("MA8:")
	print(ma_8)
	print("收盘价：")
	print(df_close)
	print("前一交易日收盘股价／MA8 比率:")
	print(df_close/ma_8)

	#TODO 计算从 【 startdate 到 enddate 】 的所有 当天的收盘价／当天的MA8，存入一个list[]
	#TODO 计算这个list[]的最大值，以及最小值， 求平均值
	#print(getTarget(root).get_MA8())

	#print(getTarget(root).get_Colse_price()/getTarget(root).get_MA8())

	#print(Cloce_div_ma8)
	#df_vol = task.computeVOL(code, startdate, enddate,1, 1,period)
	#df_macd=task.computeMACD(code,startdate,enddate,1,1,period)


#print(df_ma)
