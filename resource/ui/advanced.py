# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'advanced.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_advanced(object):
    def setupUi(self, advanced):
        advanced.setObjectName("advanced")
        advanced.resize(400, 300)

        self.retranslateUi(advanced)
        QtCore.QMetaObject.connectSlotsByName(advanced)

    def retranslateUi(self, advanced):
        _translate = QtCore.QCoreApplication.translate
        advanced.setWindowTitle(_translate("advanced", "高级设置"))
