from PyQt5 import QtCore, QtGui, QtWidgets
from chat import Ui_MainWindow
import socket, sys, time

#TODO : ADD REGISTRATION AND LOGIN
#TODO : FIX USER LIMITATION

class C_MainWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        msg = QtWidgets.QMessageBox()
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        msg.setWindowTitle("Disconnection required.")
        msg.setText("Please click at Disconnect.")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg.setWindowIcon(QtGui.QIcon("resources/icon.ico"))
        msg.exec_()
        event.ignore()


class Ui_WelcomeWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowOpacity(0.9)
        MainWindow.setWindowIcon(QtGui.QIcon('resources/icon.ico'))

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(342, 180)
        MainWindow.setFixedSize(342,180)
        MainWindow.setStyleSheet("QMainWindow{\n"
                                 "background-color:white;\n"
                                 "}\n")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 351, 41))

        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setGeometry(QtCore.QRect(125, 145, 351, 41))
        self.label_info.setText("The server is closed.")
        self.label_info.setVisible(False)


        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setGeometry(QtCore.QRect(92, 40, 161, 20))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_name.setPlaceholderText("Name")

        self.lineEdit_address = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_address.setGeometry(QtCore.QRect(92, 70, 161, 20))
        self.lineEdit_address.setObjectName("lineEdit_address")
        self.lineEdit_address.setPlaceholderText("Server address")

        self.lineEdit_port = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_port.setGeometry(QtCore.QRect(92, 100, 161, 20))
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.lineEdit_port.setPlaceholderText("Server port")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(126, 130, 91, 23))
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat"))
        self.label.setText(_translate("MainWindow", "Welcome, Please enter the required informations"))
        self.pushButton.setText(_translate("MainWindow", "Proceed"))
        self.pushButton.setShortcut(_translate("MainWindow", "Return"))
        self.pushButton.clicked.connect(self.chat_init)

    def chat_init(self):
        HOST = self.lineEdit_address.text()
        PORT = self.lineEdit_port.text()

        if PORT.isdigit():
            PORT = int(PORT)
        else:
            PORT = 420

        if not HOST:
            HOST = "192.168.1.123"

        HOST = socket.gethostbyname(HOST)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            name = self.lineEdit_name.text()
            if name and HOST and PORT:

                client_socket.connect((HOST, PORT))
                client_socket.send(name.encode())
                addr = client_socket.recv(1024).decode()

                # time.sleep(0.5)
                # number = int(client_socket.recv(1024).decode())
                #
                # if number > 20:
                #     self.label_info.setText("The server is full.")
                #     self.label_info.adjustSize()
                #     self.label_info.setVisible(True)

                # else:
                self.window = C_MainWindow()
                self.ui = Ui_MainWindow(client_socket, name, addr=addr, host=HOST, port=PORT)
                self.ui.setupUi(self.window)
                self.window.show()

                MainWindow.hide()
            else:
                pass

        except Exception as er:
            print(str(er))
            self.label_info.setText("The server is closed.")
            self.label_info.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_WelcomeWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())