import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('pp')
        self.setGeometry(100, 100, 900, 900)
        self.browser = QWebEngineView()
        # 加载外部的web界面
        # self.browser.load(QUrl('http://10.4.15.210:8080/authorityManger/Login'))
        self.browser.load(QUrl('http://p_test.alltobid.com/moni/gerenlogin.html'))
        self.browser.set
        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exit(app.exec_())
