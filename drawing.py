import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
import os
from PyQt5 import QtCore
import sys

from PyQt5.QtCore import *

mainUI = "_uiFiles/draw.ui"


class MainDialog(QDialog):
    def __init__(self):
        file_path = "image/i.png"
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        if os.path.exists(file_path):
            os.remove(file_path)
        QDialog.__init__(self, None)
        uic.loadUi(mainUI, self)
        self.okBtn.clicked.connect(self.save)
        self.okBtn.setStyleSheet('''
            QPushButton{

            font: 25pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: rgb(210, 230, 255);
            color: rgb(0,0,0);
            text-align: bottom;
            }
            QPushButton:hover{
            font: 25pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: #535c68;
            color: rgb(255, 255, 255);
            }
            QPushButton:pressed{
            background-color: rgb(255, 255, 255);
            border-style: inset;
            color: rgb(0,0,0);
            }              

        '''
                                    )
        self.clearBtn.clicked.connect(self.clear)
        self.clearBtn.setStyleSheet('''
                    QPushButton{

                    font: 25pt "이순신 돋움체 M";
                    border-radius: 20px;
                    background-color: rgb(210, 230, 255);
                    color: rgb(0,0,0);
                    text-align: bottom;
                    }
                    QPushButton:hover{
                    font: 25pt "이순신 돋움체 M";
                    border-radius: 20px;
                    background-color: #535c68;
                    color: rgb(255, 255, 255);
                    }
                    QPushButton:pressed{
                    background-color: rgb(255, 255, 255);
                    border-style: inset;
                    color: rgb(0,0,0);
                    }              

                '''
                                    )

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 15
        self.brush_color = Qt.black
        self.last_point = QPoint()

        self.brushBtn.setCheckable(True)

        # setting calling method by button
        self.brushBtn.clicked.connect(self.changeColor)

        # setting default color of button to light-grey
        self.brushBtn.setStyleSheet("background-color : lightgrey")
        self.brushBtn.setStyleSheet('''
                                                    QPushButton{
                                                    background-color: transparent;
                                                    border-image:url("image/eraser.png");
                                                    }


                                                '''
                                    )

        # show all the widgets

        # self.checkBox.
        self.update()

    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    def changeColor(self):

        # if button is checked
        if self.brushBtn.isChecked():
            self.brush_color = Qt.white
            self.brush_size = 100
            # setting background color to light-blue
            self.brushBtn.setStyleSheet("background-color : lightblue")
            self.brushBtn.setStyleSheet('''
                                                                QPushButton{
                                                                background-color: transparent;
                                                                border-image:url("image/pen.png");
                                                                }


                                                            '''
                                        )

        # if it is unchecked
        else:
            self.brush_color = Qt.black
            self.brush_size = 15
            # set background color back to light-grey
            self.brushBtn.setStyleSheet('''
                                                                QPushButton{
                                                                background-color: transparent;
                                                                border-image:url("image/eraser.png");
                                                                }


                                                            '''
                                        )

    def save(self):
        # fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        fpath = "image/i.png"

        if fpath:
            self.image.save(fpath)

        self.accept()

    def clear(self):
        self.image.fill(Qt.white)
        self.update()


app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

app.exec_()
