# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\OneDrive\Parttime-Project\黄夏\prj\player\player.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_player(object):
    def setupUi(self, player):
        player.setObjectName("player")
        player.resize(757, 626)
        self.centralwidget = QtWidgets.QWidget(player)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBox_Com = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Com.setObjectName("comboBox_Com")
        self.horizontalLayout_3.addWidget(self.comboBox_Com)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_Baud = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Baud.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_Baud.setObjectName("lineEdit_Baud")
        self.horizontalLayout_3.addWidget(self.lineEdit_Baud)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButto_Files = QtWidgets.QPushButton(self.centralwidget)
        self.pushButto_Files.setObjectName("pushButto_Files")
        self.horizontalLayout_2.addWidget(self.pushButto_Files)
        self.pushButton_Clr = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Clr.setObjectName("pushButton_Clr")
        self.horizontalLayout_2.addWidget(self.pushButton_Clr)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget_List = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_List.setObjectName("tableWidget_List")
        self.tableWidget_List.setColumnCount(0)
        self.tableWidget_List.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget_List)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_Loop = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Loop.setChecked(True)
        self.checkBox_Loop.setObjectName("checkBox_Loop")
        self.horizontalLayout.addWidget(self.checkBox_Loop)
        self.checkBox_Keycheck = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_Keycheck.setChecked(True)
        self.checkBox_Keycheck.setObjectName("checkBox_Keycheck")
        self.horizontalLayout.addWidget(self.checkBox_Keycheck)
        self.pushButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.horizontalLayout.addWidget(self.pushButton_Start)
        self.pushButton_Quit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Quit.setObjectName("pushButton_Quit")
        self.horizontalLayout.addWidget(self.pushButton_Quit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.textEdit_Info = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Info.setMaximumSize(QtCore.QSize(16777215, 200))
        self.textEdit_Info.setReadOnly(True)
        self.textEdit_Info.setObjectName("textEdit_Info")
        self.verticalLayout.addWidget(self.textEdit_Info)
        player.setCentralWidget(self.centralwidget)

        self.retranslateUi(player)
        QtCore.QMetaObject.connectSlotsByName(player)

    def retranslateUi(self, player):
        _translate = QtCore.QCoreApplication.translate
        player.setWindowTitle(_translate("player", "串口视频播放工具"))
        self.label.setText(_translate("player", "串口："))
        self.label_2.setText(_translate("player", "波特率："))
        self.lineEdit_Baud.setText(_translate("player", "9600"))
        self.pushButto_Files.setText(_translate("player", "添加视频文件"))
        self.pushButton_Clr.setText(_translate("player", "清空列表"))
        self.checkBox_Loop.setText(_translate("player", "循环播放"))
        self.checkBox_Keycheck.setText(_translate("player", "相同键值不可打断"))
        self.pushButton_Start.setText(_translate("player", "开始"))
        self.pushButton_Quit.setText(_translate("player", "退出"))
        self.label_3.setText(_translate("player", "日志："))