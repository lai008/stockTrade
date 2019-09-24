# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton ,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from autoTrade import autoTrade
import target as tg
import pandas as pd
import difflib as df


#根据value_counts（）结果画饼图
#phone=df.phone_operator.value_counts()
#df_phone=pd.DataFrame({'phone_operator':phone.index[1:],'fre':phone.values[1:]})

root = r'/Users/zou/PycharmProjects/weiyl_919/'
tg1=tg.getTarget(root)

code = 'sh.000001'
startdate = '2015-01-01'
enddate = '2019-09-22'
period = 1


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
        autoTrade.main();


    def button_stop(self):
        print("暂停交易")
        tg1.computeMACD(code,startdate,enddate,1,1,period)
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
    sys.exit(app.exec_())




