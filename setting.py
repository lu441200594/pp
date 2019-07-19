from resource.ui.ui_logic import UiLogic
from PyQt5 import QtWidgets
import sys


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
