from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import re
import time
import winsound
import sys

#TODO : REDO ALL THE THREADS AS QTHREADS, SIGNALS AND SLOTS
#TODO : USE online_browser instead of online_label
#TODO : /i to invite someone to private room and add ***pm** to msg

def play_sound(arg):
        if arg == "pm":
                winsound.PlaySound("resources/pm.wav", winsound.SND_FILENAME)
        elif arg=="ring":
                winsound.PlaySound("resources/ring.wav", winsound.SND_FILENAME)
        elif arg=="server":
                winsound.PlaySound("resources/server.wav",winsound.SND_FILENAME)


class Ui_MainWindow(object):
        def __init__(self, client_socket, name, addr, host, port):
                self.client_socket = client_socket
                self.name = name
                self.addr = addr
                self.host = host
                self.port = port

        def setupUi(self, MainWindow):
                MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowMinimizeButtonHint)
                MainWindow.setWindowIcon(QtGui.QIcon('resources/icon.ico'))
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(550, 518)
                MainWindow.setFixedSize(550,518)
                MainWindow.setStyleSheet("QMainWindow{\n"
                "background-color:white;\n"
                "}\n"
                "\n"
                "#btn_dis{\n"
                "background-color: #d9f1ff;\n"
                "}\n"
                "\n"
                "")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.label_whosonline = QtWidgets.QLabel(self.centralwidget)
                self.label_whosonline.setGeometry(QtCore.QRect(396, 150, 101, 16))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.label_whosonline.setFont(font)
                self.label_whosonline.setObjectName("label_whosonline")
                self.label_personalinfo = QtWidgets.QLabel(self.centralwidget)
                self.label_personalinfo.setGeometry(QtCore.QRect(397, 80, 151, 21))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.label_personalinfo.setFont(font)
                self.label_personalinfo.setObjectName("label_personalinfo")
                self.btn_send = QtWidgets.QPushButton(self.centralwidget)
                self.btn_send.setGeometry(QtCore.QRect(10, 450, 381, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.btn_send.setFont(font)
                self.btn_send.setObjectName("btn_send")
                self.label_my_address = QtWidgets.QLabel(self.centralwidget)
                self.label_my_address.setGeometry(QtCore.QRect(410, 122, 171, 16))
                self.label_my_address.setObjectName("label_my_address")
                self.label_my_name = QtWidgets.QLabel(self.centralwidget)
                self.label_my_name.setGeometry(QtCore.QRect(410, 102, 151, 16))
                self.label_my_name.setObjectName("label_my_name")
                self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
                self.lineEdit.setGeometry(QtCore.QRect(10, 400, 381, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.lineEdit.setFont(font)
                self.lineEdit.setObjectName("lineEdit")
                self.chat_browser = QtWidgets.QTextBrowser(self.centralwidget)
                self.chat_browser.setGeometry(QtCore.QRect(10, 10, 381, 391))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.chat_browser.setFont(font)
                self.chat_browser.setAutoFillBackground(True)
                self.chat_browser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                self.chat_browser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
                self.chat_browser.setOverwriteMode(False)
                self.chat_browser.setObjectName("chat_browser")

                # Online Browser
                # self.online_browser = QtWidgets.QTextBrowser(self.centralwidget)
                # self.online_browser.setGeometry(QtCore.QRect(400, 170, 141, 271))
                # self.online_browser.setLineWrapMode(QtWidgets.QTextBrowser.NoWrap)
                # self.online_browser.setObjectName("online_browser")

                # Label
                # self.online_label = QtWidgets.QLabel(self.centralwidget)
                # self.online_label.setGeometry(QtCore.QRect(400, 170, 141, 271))
                # self.online_label.setObjectName("online_label")

                # Scroll Area + Label
                self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
                self.scrollArea.setGeometry(QtCore.QRect(400, 170, 141, 271))
                self.scrollArea.setStyleSheet("background-color:white;")
                self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                self.scrollArea.setObjectName("scrollArea")
                self.scrollAreaWidgetContents = QtWidgets.QWidget()
                self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 130, 265))
                self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
                self.online_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                self.online_label.setGeometry(QtCore.QRect(3, 3, 0, 0))
                self.online_label.setObjectName("online_label")

                self.label_server_address = QtWidgets.QLabel(self.centralwidget)
                self.label_server_address.setGeometry(QtCore.QRect(410, 32, 150, 16))
                self.label_server_address.setObjectName("label_server_address")
                self.label_serverinfo = QtWidgets.QLabel(self.centralwidget)
                self.label_serverinfo.setGeometry(QtCore.QRect(397, 10, 200, 21))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.label_serverinfo.setFont(font)
                self.label_serverinfo.setObjectName("label_serverinfo")
                self.label_server_port = QtWidgets.QLabel(self.centralwidget)
                self.label_server_port.setGeometry(QtCore.QRect(410, 52, 121, 16))
                self.label_server_port.setObjectName("label_server_port")
                self.btn_dis = QtWidgets.QPushButton(self.centralwidget)
                self.btn_dis.setGeometry(QtCore.QRect(400, 450, 141, 41))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.btn_dis.setFont(font)
                self.btn_dis.setObjectName("btn_dis")
                self.label_8 = QtWidgets.QLabel(self.centralwidget)
                self.label_8.setGeometry(QtCore.QRect(518, 153, 47, 13))
                self.label_8.setObjectName("label_8")
                self.line = QtWidgets.QFrame(self.centralwidget)
                self.line.setGeometry(QtCore.QRect(400, 65, 141, 20))
                self.line.setFrameShape(QtWidgets.QFrame.HLine)
                self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line.setObjectName("line")
                self.line_2 = QtWidgets.QFrame(self.centralwidget)
                self.line_2.setGeometry(QtCore.QRect(400, 135, 141, 20))
                self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
                self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.line_2.setObjectName("line_2")
                MainWindow.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 21))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "Chat Room"))
                self.label_whosonline.setText(_translate("MainWindow", "Who\'s Online?"))
                self.label_personalinfo.setText(_translate("MainWindow", "Personal Informations"))
                self.btn_send.setStatusTip(_translate("MainWindow", "Press Enter"))
                self.btn_send.setText(_translate("MainWindow", "Send"))
                self.btn_send.setShortcut(_translate("MainWindow", "Return" or "Enter"))
                self.label_my_address.setText(_translate("MainWindow", "address"))
                self.label_my_name.setText(_translate("MainWindow", "name"))
                self.lineEdit.setPlaceholderText(_translate("MainWindow", "Type here.. /h to see all the commands."))

                self.chat_browser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
                self.chat_browser.setPlaceholderText(_translate("MainWindow", "Feels lonely up here.."))

                # self.online_browser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                # "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                # "p, li { white-space: pre-wrap; }\n"
                # "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                # "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
                # self.online_browser.setPlaceholderText(_translate("MainWindow", "No one is online.."))

                self.label_server_address.setText(_translate("MainWindow", "Address"))
                self.label_serverinfo.setText(_translate("MainWindow", "Server Informations"))
                self.label_server_port.setText(_translate("MainWindow", "Port"))
                self.btn_dis.setStatusTip(_translate("MainWindow", "Type /q"))
                self.btn_dis.setText(_translate("MainWindow", "Disconnect"))
                MainWindow.setTabOrder(self.lineEdit, self.btn_send)
                self.label_8.setText(_translate("MainWindow", f"0/10"))
                self.btn_send.clicked.connect(self.send)
                self.btn_dis.clicked.connect(self.disconnect)
                self.label_server_address.setText("Host : "+self.host)
                self.label_server_port.setText("Port : "+str(self.port))
                self.label_my_name.setText("Name : "+self.name)
                self.label_my_address.setText(self.addr)

                Thread(target=self.receive, daemon=True).start()

                self.people_online = 0
                self.people_names = ""
                self.update_bool = True

                Thread(target=self.update, daemon=True).start()

        def show_commands(self):
                self.lineEdit.clear()
                msg = QtWidgets.QMessageBox()
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                msg.setWindowTitle("Commands")
                msg.setText("<p><span style=\" color: #ff0000;\">/q</span> : To Quit<br><span style=\" color: #ff0000;\">/ra</span> : To Ring everyone<br><span style=\" color: #ff0000;\">/r name</span> : To Ring name<br><span style=\" color: #ff0000;\">/p (name) text</span> : To send private message<br><span style=\" color: #ff0000;\">/h</span> : Show Commands<br><span style=\" color: #ff0000;\">/c</span> : Show Credits</p>")
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msg.setWindowIcon(QtGui.QIcon("resources/icon.ico"))
                msg.exec_()

        def show_credits(self):
                self.lineEdit.clear()
                msg = QtWidgets.QMessageBox()
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                msg.setWindowTitle("Credits")
                msg.setText("<span style=\" color: #0000FF;\">I</span><span style=\" color: #800080;\">n</span><span style=\" color: #000000;\">f</span><span style=\" color: #32CD32;\">r</span><span style=\" color: #008000;\">e<span style=\" color: #ff00f0;\">e</span><span style=\" color: #ffc0cb;\">z</span><span style=\" color: #FFA500;\">y</span>")
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msg.setWindowIcon(QtGui.QIcon("resources/icon.ico"))
                msg.exec_()

        def send(self):
                msg = self.lineEdit.text()

                if msg.startswith("/h"):
                        self.show_commands()
                elif msg.startswith("/c"):
                        self.show_credits()
                elif msg.startswith("/q"):
                        self.client_socket.send(b"/q")
                        self.client_socket.close()
                        sys.exit()
                else:
                        self.client_socket.send(msg.encode())
                        self.lineEdit.clear()

        def scrollDown(self):
                time.sleep(0.1)
                self.chat_browser.verticalScrollBar().setValue(self.chat_browser.verticalScrollBar().maximum())

        def disconnect(self):
                self.client_socket.send(b"/q")
                self.client_socket.close()
                sys.exit()

        def receive(self):

                while True:
                        try:
                                pattern_number = re.compile(r"#/#(\d+)##")
                                pattern_result = re.compile(r"\*/\*(.*)\*\*")
                                pattern_name = re.compile(r"\'([\d\w\s]*)\'")

                                msg = self.client_socket.recv(1024).decode()

                                # Server message
                                if "******server******" in msg and "#/#" not in msg and "*/*" not in msg and "******ring******" not in msg:
                                        Thread(target=play_sound, args=("server",), daemon=True).start()
                                        server_msg = (msg.split("******server******")[0])
                                        self.chat_browser.append(server_msg)
                                        Thread(target=self.scrollDown, daemon=True).start()

                                # Ringing message
                                if "******ring******" in msg and "#/#" not in msg and "*/*" not in msg and "******server******" not in msg:
                                        Thread(target=play_sound, args=("ring",), daemon=True).start()
                                        self.chat_browser.append(msg.split("******ring******")[0])
                                        Thread(target=self.scrollDown, daemon=True).start()

                                # Private message
                                if "******pm******" in msg and "#/#" not in msg and "*/*" not in msg and "******server******" not in msg and "******ring******" not in msg:
                                        Thread(target=play_sound, args=("pm",), daemon=True).start()
                                        self.chat_browser.append(msg.split("******pm******")[0])
                                        Thread(target=self.scrollDown, daemon=True).start()

                                # Normal message
                                if "#/#" not in msg and "*/*" not in msg and "******ring******" not in msg and "******server******" not in msg and "******pm******" not in msg:
                                        self.chat_browser.append(msg)
                                        Thread(target=self.scrollDown, daemon=True).start()

                                try:
                                        self.people_online = pattern_number.findall(msg)[0]
                                        self.result = pattern_result.findall(msg)[0]
                                        self.people_names = pattern_name.findall(self.result)

                                except IndexError:
                                        continue
                        except OSError:
                                break

        def update(self):
                while self.update_bool:
                        time.sleep(0.1)
                        self.label_8.setText(f"{self.people_online}/20")
                        for name in self.people_names:
                                if name not in self.online_label.text().splitlines():
                                        self.online_label.setText(self.online_label.text()+'\n'+name)
                                        self.online_label.adjustSize()
                                        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
                        try:
                                for nm in self.online_label.text().splitlines():
                                        if nm not in self.people_names:
                                                self.online_label.setText(self.online_label.text()[:self.online_label.text().index(nm)].strip() + self.online_label.text()[self.online_label.text().index(nm)+len(nm):].strip())
                                                self.online_label.adjustSize()
                                                self.scrollArea.setWidget(self.scrollAreaWidgetContents)
                        except ValueError:
                                continue

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())