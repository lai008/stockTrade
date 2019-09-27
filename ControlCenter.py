# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton ,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from autoTrade import autoTrade
import datetime
import time

import target as tg
import kdj as kdj
import pandas as pd
import difflib as df


#根据value_counts（）结果画饼图
#phone=df.phone_operator.value_counts()
#df_phone=pd.DataFrame({'phone_operator':phone.index[1:],'fre':phone.values[1:]})

root = r'/Users/zou/PycharmProjects/weiyl_919/'
tg1=tg.getTarget(root)





class work(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "自动交易控制台"
        self.left = 300
        self.top = 300
        self.width = 820
        self.height = 500
        self.initUI()



    def initUI(self):
        # 主窗口
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # 各按钮显示设计
        button_start = QPushButton("启动交易", self)
        button_start.resize(100, 50)
        button_start.move(230, 30)

        button_stop = QPushButton("暂停交易", self)
        button_stop.resize(100, 50)
        button_stop.move(430, 30)

        textEdit_code=QTextEdit("请输入代码",self)
        textEdit_code.resize(100,30)
        textEdit_code.move(630,30)
        textEdit_code


        """按钮与鼠标点击事件相关联"""
        button_start.clicked.connect(self.button_start)
        button_stop.clicked.connect(self.button_stop)



        self.show()

    # 功能设计
    def button_start(self):
        # sender = self.sender()
        # self.statusBar().showMessage(sender.text() + ' was pressed')
        print("启动交易")
        #autoTrade.buy();
        autoTrade.sell(159928);


    def button_stop(self):
        print("暂停交易")
    #
    #     if J[-1] <100:
    #         self.button_start()



        # #print(tg.ma_8)
        # tg1.computeMACD(code,startdate,enddate,1,1,period)
        # print(tg1.get_MA8())
       # tg1.computeMA(code, startdate, enddate, 1, 1, period)
       # tg1.computeKDJ(code, startdate, enddate, 1, 1, period)
       # tg1.computeRSI(code, startdate, enddate, 1, 1, period)
       # tg1.computeVOL(code, startdate, enddate, 1, 1, period)




        # plt.rc('font', family='SimHei', size=13)
        # fig = plt.figure()
        # #plt.pie(df_phone.fre,labels=df_phone.phone_operator,autopct='%1.2f%%') #画饼图（数据，数据对应的标签，百分数保留两位小数点）
        #
        # plt.title("资金分布")
        # plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = work()
    code = 'sh.000001'
    today = datetime.datetime.now().strftime('%Y%m%d')
    startdate = '2017-01-01'
    enddate = f'{today[0:4]}-{today[4:6]}-{today[6:8]}'
    period = 1



    while True:
        now_time = datetime.datetime.now()
        imnow = time.strftime("%Y-%m-%d %H:%M:%S")
        print(imnow)
        time.sleep(1)
        print(now_time.time().hour)
        print(now_time.time().minute)
        print(now_time.time().second)
        #print(now_time.time().hour+":"+now_time.time().second +":"+now_time.time().second())

        # 系统时间16点19分00秒，触发事件 (如不触发， .second 要重新加载一下 )
        if now_time.time().hour == 15 and now_time.time().minute ==19 and now_time.time().second == 00:
            print('启动策略')
            ##########策略体###########
            KDJ = kdj.computeKDJ(code, startdate, enddate)
            J = kdj.computeKDJ(code, startdate, enddate)
            print(J[-1])

            if J[-1] < 0:
                work.button_start(QWidget)

            print("交易成功")
            ######################


    # 系统时间16点19分00秒，触发事件 (如不触发， .second 要重新加载一下 )
    # if now_time.time().hour == 22 and now_time.time().minute == 51 and now_time.time().second == 00:
    #     print('AAAAAAAAAA')
    sys.exit(app.exec_())




