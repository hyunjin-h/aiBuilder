import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2


class Ui_MainWindow(object):
    cam_num=0
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("카메라")
        MainWindow.resize(1000, 1000)

        MainWindow.setMinimumSize(QtCore.QSize(1000, 1000))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 1000))
        MainWindow.setStyleSheet("QWidget#centralwidget{background-color:#89a3e3;}\n"
"")
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.cam_num=0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 80, 800, 600))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(685,720, 150, 100))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("border-radius:20px;\n"
"font: 14pt 'NanumSquare';\n"
"background-color: rgb(232, 100, 100);\n")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(175, 720, 150, 100))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("border-radius:20px;\n"
                                        "font: 14pt 'NanumSquare';\n"
"background-color: #e3d5ca;	\n"
"\n"
"color:#ffffff;\n")

        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(425, 900, 150, 50))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("border-radius:20px;\n"
"font: 12pt 'NanumSquare';\n"
"    background-color: #2f3640;\ncolor: #fff;\n"
                                       )
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(425,720,150,100))
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("border-radius:20px;\n"
                                        "font: 14pt 'NanumSquare';\n"
"background-color: #e3d5ca;	\n"
                                        )
        self.pushButton_4.setObjectName("pushButton_4")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 341, 31))
        self.label_2.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.cancel)

        self.pushButton_2.clicked.connect(lambda :self.start_video(1))

        self.pushButton_4.clicked.connect(lambda :self.start_video(0))
        self.pushButton_3.clicked.connect(self.salir)

        self.pushButton_2.setIcon(QIcon("image/webcam.png"))
        self.pushButton_2.setIconSize(QSize(70, 70));


        self.pushButton_3.setText("확인")
        self.pushButton_4.setIcon(QIcon("image/laptop.png"))
        self.pushButton_4.setIconSize(QSize(50,50));
        self.pushButton.setIcon(QIcon("image/cam_check.png"))
        self.pushButton.setIconSize(QSize(55,55));
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start_video(self,num):
        Ui_MainWindow.cam_num=num
        self.Work = Work()
        self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)

    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def cancel(self):
        self.label.clear()
        self.Work.stop()

    def salir(self):
        sys.exit()

    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    #     self.pushButton.setText(_translate("MainWindow", "📷"))
    #     self.pushButton_2.setIcon(_translate("MainWindow", "image/webcam.png"))
    #
    #     self.pushButton_3.setText(_translate("MainWindow", "확인"))
    #     self.pushButton_4.setText(_translate("MainWindow", "💻"))


class Work(QThread):
    Imageupd = pyqtSignal(QImage)
    def run(self):
        self.hilo_corriendo = True
        cap = cv2.VideoCapture(Ui_MainWindow.cam_num,cv2.CAP_DSHOW)
        while self.hilo_corriendo:
            ret, frame = cap.read()

            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(Image, 1)
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
                pic = convertir_QT.scaled(800,600, Qt.KeepAspectRatio)
                self.Imageupd.emit(pic)

        file = 'image/input_photo.jpg'
        cv2.imwrite(file,frame)
        print(file, ' saved')

    def stop(self):
        self.hilo_corriendo = False
        self.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())