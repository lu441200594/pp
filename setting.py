from resource.window import Ui_MainWindow
from PyQt5 import QtWidgets, uic, QtCore, QtGui, QtWebEngine
import sys
# from p_test import apscheduler_test


class create_qt(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = create_qt()
    win.show()
    # apscheduler_test.test()
    sys.exit(app.exec())
