"""
This module contains a bare-bones VLC player class to play videos.
Adapted  from an example by Saveliy Yusufov, Columbia University, sy2685@columbia.edu
"""

import os
import sys
import platform
from time import sleep
import serial
import serial.tools.list_ports
import traceback
import codecs

from PyQt5 import Qt, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QHeaderView
from PyQt5.QtCore import QDir
from Ui_player import Ui_player
import vlc
from qt_material import apply_stylesheet


class Player(QtWidgets.QMainWindow):
    """Stripped-down PyQt5-based media player class
    """

    logSignal = QtCore.pyqtSignal(str)
    playSignal = QtCore.pyqtSignal(str)
    last_key = ""
    keycheck = True

    def __init__(self, loop, keycheck, baud, master=None):
        QtWidgets.QMainWindow.__init__(self, master)

        self.keycheck = keycheck

        self.com = "COM1"

        with open("configs.txt", "r", encoding="utf-8") as configs:
            lines = configs.readlines()
            for line in lines:
                self.com = line

        self.media_files = {}

        with open("files.txt", "r", encoding="utf-8") as files:
            lines = files.readlines()
            for line in lines:
                if len(line.rstrip("\n").rstrip("\r")) != 0:
                    self.media_files.update({line.split(",")[0]: line.split(",")[1].rstrip("\n").rstrip("\r")})

        self.showFullScreen()

        self.init_ui()

        if loop is True:
            vlc_options = [
                "--embedded-video",
                "--no-audio",
                "--autoscale",
                "--fullscreen",
                "--video-on-top",
                "--no-video-title-show",
                # "--repeat",
                "--input-repeat=65545",
                "--verbose -1",
                "--canvas-aspect 3:4",
                "--no-canvas-padd"
            ]
        else:
            vlc_options = [
                "--embedded-video",
                "--no-audio",
                "--autoscale",
                "--fullscreen",
                "--video-on-top",
                "--no-video-title-show",
                # "--repeat",
                # "--input-repeat=65545",
                "--verbose -1",
                "--canvas-aspect 3:4",
                "--no-canvas-padd"
            ]
        # Create a basic vlc instance
        self.instance = vlc.Instance(" ".join(vlc_options))
        # later used to store media object, for now blank
        self.media = None
        # Create an empty vlc media player
        self.player = self.instance.media_player_new()
        # self.mediaplayer = vlc.MediaPlayer()
        # Set to fullscreen
        # self.player.set_fullscreen(True)
        #
        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux":  # for Linux using the X Server
            self.player.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.player.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.player.set_nsobject(int(self.videoframe.winId()))

        self.playSignal.connect(self.play)

        # create a timer to refresh video
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.next_video)

        try:
            self.serial = serial.Serial(self.com, baud, timeout=0.5)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "打开串口失败", "{}".format(e))
            os._exit(0)
        if not self.serial.is_open:
            print("open failed")
        else:
            self.timer.start()
        # self.open_file('C://Users//BananaSuper//Desktop//meeting_01.mp4')

    def init_ui(self):
        """Set up the user interface
        """
        if platform.system() == "Darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()
        # set videoframe color
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        self.setCentralWidget(self.videoframe)

    def open_file(self, filename):
        """Open a media file in a MediaPlayer
        """
        if not filename:
            return
        # self.player.stop()
        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename)
        # Put the media in the media player
        self.player.set_media(self.media)
        # Parse the metadata of the file
        self.media.parse()
        # Start playing the video as soon as it loads
        self.player.play()

    def next_video(self):
        key = self.serial.readline().decode().strip()
        if(len(key) > 0):
            self.logSignal.emit("串口接收：" + str(key))
            self.playSignal.emit(str(key))
        return

    def play(self, key):
        # sleep(0.5)
        if key in self.media_files.keys():
            if self.last_key != key or self.keycheck is False:
                try:
                    if os.path.exists(self.media_files.get(key).rstrip("\n").rstrip("\r")):
                        self.open_file(self.media_files.get(key).rstrip("\n").rstrip("\r"))
                        self.logSignal.emit("播放视频文件：" + self.media_files.get(key).rstrip("\n").rstrip("\r"))
                    else:
                        self.logSignal.emit("视频文件不存在：" + self.media_files.get(key).rstrip("\n").rstrip("\r"))
                except Exception as e:
                    QtWidgets.QMessageBox.critical(None, "打开视频文件失败，键值： " + str(key), "{}".format(e))
            else:
                self.logSignal.emit("忽略键值： " + str(key))
            self.last_key = key
        else:
            self.logSignal.emit("打开视频文件失败，没有找到对应的键值： " + str(key))


class MyMainWindow(QMainWindow, Ui_player):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)

        self.old_hook = sys.excepthook
        sys.excepthook = self.excepthook

        com = "COM1"
        with open("configs.txt", "r", encoding="utf-8") as configs:
            lines = configs.readlines()
            for line in lines:
                com = line

        port_list = list(serial.tools.list_ports.comports())
        for comport in port_list:
            self.comboBox_Com.addItem(comport.device)
            if com == comport.device:
                self.comboBox_Com.setCurrentText(com)

        self.tableWidget_List.clear()
        self.tableWidget_List.setRowCount(0)
        self.tableWidget_List.setColumnCount(2)
        self.tableWidget_List.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_List.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_List.setHorizontalHeaderLabels(['键值', '文件路径'])
        self.index = 0
        with open("files.txt", "r", encoding="utf-8") as files:
            lines = files.readlines()
            for line in lines:
                if len(line.rstrip("\n").rstrip("\r")) != 0:
                    self.tableWidget_List.insertRow(self.index)
                    newItem = QTableWidgetItem(line.split(",")[0])
                    self.tableWidget_List.setItem(self.index, 0, newItem)
                    newItem = QTableWidgetItem(line.split(",")[1].rstrip("\n").rstrip("\r"))
                    self.tableWidget_List.setItem(self.index, 1, newItem)
                    self.index = self.index + 1

        self.port()
        self.comboBox_Com.currentTextChanged.connect(self.port)
        self.pushButto_Files.clicked.connect(self.add)
        self.pushButton_Clr.clicked.connect(self.clear)
        self.pushButton_Start.clicked.connect(self.start)
        self.pushButton_Quit.clicked.connect(self.quit)

    def port(self):
        _configF = open("configs.txt", "w")
        _configF.write(self.comboBox_Com.currentText())
        _configF.close()

    def add(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            _fileF = open("files.txt", "a", encoding='utf-8')
            _fileF.write(str(self.index + 1) + ",")
            _fileF.write(filenames[0].replace("/", "//"))
            _fileF.write("\n")
            _fileF.close()
            self.tableWidget_List.insertRow(self.index)
            newItem = QTableWidgetItem(str(self.index + 1))
            self.tableWidget_List.setItem(self.index, 0, newItem)
            newItem = QTableWidgetItem(filenames[0].replace("/", "//"))
            self.tableWidget_List.setItem(self.index, 1, newItem)
            self.index = self.index + 1

    def clear(self):
        self.index = 0
        _fileF = open("files.txt", "w")
        _fileF.write("")
        _fileF.close()
        self.tableWidget_List.clear()
        self.tableWidget_List.setRowCount(0)
        self.tableWidget_List.setColumnCount(2)
        self.tableWidget_List.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget_List.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_List.setHorizontalHeaderLabels(['键值', '文件路径'])

    def start(self):
        self.player = Player(self.checkBox_Loop.isChecked(), self.checkBox_Keycheck.isChecked(), int(self.lineEdit_Baud.text()))
        self.player.show()
        self.player.logSignal.connect(self.log)
        self.comboBox_Com.setEnabled(False)
        self.lineEdit_Baud.setEnabled(False)
        self.pushButto_Files.setEnabled(False)
        self.pushButton_Clr.setEnabled(False)
        self.checkBox_Loop.setEnabled(False)
        self.checkBox_Keycheck.setEnabled(False)
        self.pushButton_Start.setEnabled(False)

    def quit(self):
        self.close()
        os._exit(0)

    def log(self, msg):
        self.textEdit_Info.append(msg)

    def excepthook(self, exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        QtWidgets.QMessageBox.critical(None, "发生异常", "{}".format(tb))
        self.old_hook(exc_type, exc_value, exc_tb)
        sys.excepthook = self.old_hook
        os._exit(0)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        apply_stylesheet(app, theme='dark_teal.xml')
        myWin = MyMainWindow()
        myWin.show()
        sys.exit(app.exec_())
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "发生异常", "{}".format(e))
