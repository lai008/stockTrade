#!/usr/bin/env python3

from pynput.mouse import Controller
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel
from PyQt5.QtCore import QRect, QThread,  pyqtSignal, QObject
import datetime

import sys

class BackendThread(QObject):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    # 处理业务逻辑
    def run(self):
        mouse = Controller()
        while True:
            # 给信号update_date发送数据
            self.update_date.emit("(%d, %d)" % mouse.position)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

    def setupUi(self, mainwindow):
        self.centralwidget = QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")

        self.txtLabel = QLabel("", self.centralwidget)
        self.txtLabel.setGeometry(QRect(20, 10, 100, 20))

        mainwindow.setCentralWidget(self.centralwidget)

    def run(self):
        self.backend = BackendThread()
        # 连接信号，绑定update_date信号对应的槽为handleDisplay方法
        self.backend.update_date.connect(self.handleDisplay)

        # 创建线程
        self.thread = QThread()
        # 将backend对象转移到子线程thread中
        self.backend.moveToThread(self.thread)

        # 开始线程
        self.thread.started.connect(self.backend.run)
        self.thread.start()

    # 将当前时间输出到文本框
    def handleDisplay(self, data):
        self.txtLabel.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.move(0, 0)
    MainWindow.resize(110, 40)
    ui = Example()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.run()
    sys.exit(app.exec_())