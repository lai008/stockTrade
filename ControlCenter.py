# -*- coding: utf-8 -*-
import sys
import ctypes
import inspect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton ,QTextEdit,QLabel
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from autoTrade import autoTrade
import datetime
import time
import threading
import target as tg
import kdj as kdj
import RSI as rsi
import Vol as vol
import scrapData as sD
import pandas as pd
import difflib as df


#根据value_counts（）结果画饼图
#phone=df.phone_operator.value_counts()
#df_phone=pd.DataFrame({'phone_operator':phone.index[1:],'fre':phone.values[1:]})

########## 加入线程  ###################
exitFlag = 0


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        print
        "Exiting " + self.name
        # imnow = time.strftime("%Y-%m-%d %H:%M:%S")
        # print(imnow)
        while True:
            imnow = time.strftime("%Y-%m-%d %H:%M:%S")
            print(imnow)
            time.sleep(1)



     #myThread2策略线程
class myThread2(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        print
        "Exiting2 " + self.name


        while True:

            code = 'sh.000001'
            today = datetime.datetime.now().strftime('%Y%m%d')
            startdate = '2017-01-01'
            enddate = f'{today[0:4]}-{today[4:6]}-{today[6:8]}'
            # 获取当前时间
            now_time = datetime.datetime.now()
            period = 1
            Vol=vol.computeVOL(code, startdate, enddate,period)
            print(Vol[-1])

            # rsi_6days = rsi.computeRSI(code, startdate, enddate)
            # print(rsi_6days[-1])



            # imnow = time.strftime("%Y-%m-%d %H:%M:%S")
            # print(imnow)
            # time.sleep(1)
            # print(now_time.time().hour)
            # print(now_time.time().minute)# 创建新线程
            print
            "Exiting Main Thread"
            # print(now_time.time().second)
            # print(now_time.time().hour+":"+now_time.time().second +":"+now_time.time().second())

            # 系统时间XX点XX分XX秒，触发策略启动
            if now_time.time().hour == 9 and now_time.time().minute == 37 and now_time.time().second == 00:
                #print('启动KDJ策略')
                # ##########KDJ策略体###########
                # #enddate不是交易日，测试会出现接收数据异常  list index out of range
                # # J = kdj.computeKDJ(code, startdate, enddate)
                # # 买入测试日期
                # #J = kdj.computeKDJ(code, startdate,'2019-09-26')
                # #卖出测试日期
                # J = kdj.computeKDJ(code, startdate,'2019-08-21')
                # print(J[-1])
                #
                # if J[-1] < 0:
                #     # work.button_start(QWidget)
                #     print('启动买入策略')
                #     autoTrade.buy(159928)
                #
                # print("交易成功")
                # ######################
                # if J[-1] > 100:
                #     # work.button_start(QWidget)
                #     print('启动卖出策略')
                #     autoTrade.sell(159928)
                #
                #
                # print("交易成功")
                # ######################

                print('启动RSI策略')
                ##########RSI策略体###########
                # enddate不是交易日，测试会出现接收数据异常  list index out of range
                #rsi_6days = rsi.computeRSI(code, startdate, enddate)
                # 买入测试日期
                # J = rsi.computeRSI(code, startdate,'2019-09-26')
                # 卖出测试日期
                rsi_6days = rsi.computeRSI(code, startdate, '2019-09-09')
                print(rsi_6days[-1])

                if rsi_6days[-1] < 20:
                    # work.button_start(QWidget)
                    print('启动买入策略')
                    autoTrade.buy(159928)

                print("交易成功")
                ######################
                if rsi_6days[-1] > 80:
                    # work.button_start(QWidget)
                    print('启动卖出策略')
                    autoTrade.sell(159928)

                print("交易成功")
                ######################


def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1





######################################


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

        button_scrapData = QPushButton("资金流入排名", self)
        button_scrapData.resize(100, 50)
        button_scrapData.move(430, 100)

        textEdit_code=QTextEdit("请输入代码",self)
        textEdit_code.resize(100,30)
        textEdit_code.move(630,30)
        textEdit_code

        imnow = time.strftime("%Y-%m-%d %H:%M:%S")
        print(imnow)
        time.sleep(1)

        label1 = QLabel(self)
        palette = QPalette()
        # palette.setColor(QPalette.window.Qt.blue)
        label1.setAutoFillBackground(True)
        label1.setPalette(palette)

        label1.setText(imnow)

        """按钮与鼠标点击事件相关联"""
        button_start.clicked.connect(self.button_start)
        button_stop.clicked.connect(self.button_stop)
        button_scrapData.clicked.connect(self.button_scrapData)



        self.show()

    # 功能设计
    def button_start(self):
        # sender = self.sender()
        # self.statusBar().showMessage(sender.text() + ' was pressed')
        print("启动交易")
        #autoTrade.buy();
        #autoTrade.buy(159928)
        autoTrade.sell(159928)


    def button_stop(self):
        print("暂停交易")
        #结束线程myThread
        terminator(myThread)
        # 结束线程myThread2
        terminator(myThread2)

        sys.exit(1)
        sys.exit(0)

    def button_scrapData(self):
        print("资金流入分布")
        sD.main()



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

def __async_raise(thread_Id, exctype):
        # 在子线程内部抛出一个异常结束线程
        # 如果线程内执行的是unittest模块的测试用例， 由于unittest内部又异常捕获处理，所有这个结束线程
        # 只能结束当前正常执行的unittest的测试用例， unittest的下一个测试用例会继续执行，只有结束继续
        # 向unittest中添加测试用例才能使线程执行完任务，然后自动结束。
        thread_Id = ctypes.c_long(thread_Id)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, None)
            raise SystemError("PyThreadState_SEtAsyncExc failed")

def terminator(thread):
        # 结束线程
        __async_raise(thread.ident, SystemExit)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # # 创建新线程
    #thread1 计时间线程
    thread1 = myThread(1, "Thread-1", 1)
    # thread2 交易策略线程
    thread2 = myThread2(2, "Thread-2", 1)
    #
    # # 开启线程
    #thread1.start()
    #thread2.start()
    #
    # print
    # "Exiting Main Thread"
    # 交易平台界面启动
    ex = work()


    # while True:
    #
    #
    #     code = 'sh.000001'
    #     today = datetime.datetime.now().strftime('%Y%m%d')
    #     startdate = '2017-01-01'
    #     enddate = f'{today[0:4]}-{today[4:6]}-{today[6:8]}'
    #     period = 1
    #
    #     #获取当前时间
    #     now_time = datetime.datetime.now()
    #     imnow = time.strftime("%Y-%m-%d %H:%M:%S")
    #     print(imnow)
    #     time.sleep(1)
    #     print(now_time.time().hour)
    #     print(now_time.time().minute)
    #     print(now_time.time().second)
    #     #print(now_time.time().hour+":"+now_time.time().second +":"+now_time.time().second())
    #
    #     # 系统时间16点19分00秒，触发事件 (如不触发， .second 要重新加载一下 )
    #     if now_time.time().hour == 14 and now_time.time().minute ==50 and now_time.time().second == 00:
    #         print('启动KDJ策略')
    #         ##########策略体###########
    #         KDJ = kdj.computeKDJ(code, startdate, enddate)
    #         J = kdj.computeKDJ(code, startdate, enddate)
    #         print(J[-1])
    #
    #         if J[-1] < 0:
    #             #work.button_start(QWidget)
    #             print('启动买入策略')
    #             autoTrade.buy(159928)
    #
    #         print("交易成功")
    #         ######################
    #         if J[-1] > 100:
    #             #work.button_start(QWidget)
    #             print('启动卖出策略')
    #             autoTrade.sell(159928)
    #
    #         print("交易成功")
    #         ######################

    sys.exit(app.exec_())




