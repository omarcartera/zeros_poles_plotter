# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(718, 588)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btn_zero = QtGui.QPushButton(self.centralwidget)
        self.btn_zero.setGeometry(QtCore.QRect(20, 130, 98, 27))
        self.btn_zero.setObjectName(_fromUtf8("btn_zero"))
        self.btn_pole = QtGui.QPushButton(self.centralwidget)
        self.btn_pole.setGeometry(QtCore.QRect(20, 170, 98, 27))
        self.btn_pole.setObjectName(_fromUtf8("btn_pole"))
        self.lnd_zero_real = QtGui.QLineEdit(self.centralwidget)
        self.lnd_zero_real.setGeometry(QtCore.QRect(130, 130, 31, 27))
        self.lnd_zero_real.setObjectName(_fromUtf8("lnd_zero_real"))
        self.lnd_zero_img = QtGui.QLineEdit(self.centralwidget)
        self.lnd_zero_img.setGeometry(QtCore.QRect(170, 130, 31, 27))
        self.lnd_zero_img.setObjectName(_fromUtf8("lnd_zero_img"))
        self.lnd_pole_real = QtGui.QLineEdit(self.centralwidget)
        self.lnd_pole_real.setGeometry(QtCore.QRect(130, 170, 31, 27))
        self.lnd_pole_real.setObjectName(_fromUtf8("lnd_pole_real"))
        self.lnd_pole_img = QtGui.QLineEdit(self.centralwidget)
        self.lnd_pole_img.setGeometry(QtCore.QRect(170, 170, 31, 27))
        self.lnd_pole_img.setObjectName(_fromUtf8("lnd_pole_img"))
        self.circleWidget = QtGui.QWidget(self.centralwidget)
        self.circleWidget.setGeometry(QtCore.QRect(210, 10, 351, 341))
        self.circleWidget.setObjectName(_fromUtf8("circleWidget"))
        self.tfWidget = QtGui.QWidget(self.centralwidget)
        self.tfWidget.setGeometry(QtCore.QRect(20, 360, 661, 151))
        self.tfWidget.setObjectName(_fromUtf8("tfWidget"))
        self.btn_clear = QtGui.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(290, 520, 98, 27))
        self.btn_clear.setObjectName(_fromUtf8("btn_clear"))
        self.btn_browse = QtGui.QPushButton(self.centralwidget)
        self.btn_browse.setGeometry(QtCore.QRect(20, 50, 98, 27))
        self.btn_browse.setObjectName(_fromUtf8("btn_browse"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 340, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btn_up = QtGui.QPushButton(self.centralwidget)
        self.btn_up.setGeometry(QtCore.QRect(80, 230, 41, 27))
        self.btn_up.setObjectName(_fromUtf8("btn_up"))
        self.btn_down = QtGui.QPushButton(self.centralwidget)
        self.btn_down.setGeometry(QtCore.QRect(80, 290, 41, 27))
        self.btn_down.setObjectName(_fromUtf8("btn_down"))
        self.btn_left = QtGui.QPushButton(self.centralwidget)
        self.btn_left.setGeometry(QtCore.QRect(30, 260, 41, 27))
        self.btn_left.setObjectName(_fromUtf8("btn_left"))
        self.btn_right = QtGui.QPushButton(self.centralwidget)
        self.btn_right.setGeometry(QtCore.QRect(130, 260, 41, 27))
        self.btn_right.setObjectName(_fromUtf8("btn_right"))
        self.btn_ok = QtGui.QPushButton(self.centralwidget)
        self.btn_ok.setGeometry(QtCore.QRect(80, 260, 41, 27))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.lnd_accuracy = QtGui.QLineEdit(self.centralwidget)
        self.lnd_accuracy.setGeometry(QtCore.QRect(30, 230, 41, 27))
        self.lnd_accuracy.setObjectName(_fromUtf8("lnd_accuracy"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 210, 66, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(580, 30, 131, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 718, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Added by the magnificent omarcartera to allow plotting
        self.tfPlot = QtGui.QVBoxLayout(self.tfWidget)
        self.tfPlot.setObjectName(_fromUtf8("tfLayout"))
        #############################################################

        #Added by the magnificent omarcartera to allow plotting
        self.circlePlot = QtGui.QVBoxLayout(self.circleWidget)
        self.circlePlot.setObjectName(_fromUtf8("circleLayout"))
        #############################################################
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_zero.setText(_translate("MainWindow", "Add Zero", None))
        self.btn_pole.setText(_translate("MainWindow", "Add Pole", None))
        self.btn_clear.setText(_translate("MainWindow", "CLEAR!", None))
        self.btn_browse.setText(_translate("MainWindow", "Browse", None))
        self.label_2.setText(_translate("MainWindow", "Transfer Function", None))
        self.btn_up.setText(_translate("MainWindow", "↑", None))
        self.btn_down.setText(_translate("MainWindow", "↓", None))
        self.btn_left.setText(_translate("MainWindow", "←", None))
        self.btn_right.setText(_translate("MainWindow", "→", None))
        self.btn_ok.setText(_translate("MainWindow", "OK", None))
        self.label_3.setText(_translate("MainWindow", "Accuracy", None))
        self.label_4.setText(_translate("MainWindow", "Notification", None))

