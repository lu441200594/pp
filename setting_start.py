from resource.ui.ui_logic import UiLogic
import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets


class create_qt(QtWidgets.QMainWindow, UiLogic):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        UiLogic.__init__(self)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = create_qt()
    win.show()
    sys.exit(app.exec())
