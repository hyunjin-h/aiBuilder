from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import urllib.request
import json

form_text=uic.loadUiType('_uiFiles/textInput.ui')[0]

class TextDialog(QDialog,form_text):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self):
        super(TextDialog, self).__init__()
        self.initUI()
        self.show()

        # self.text = ""
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def initUI(self):
        self.setupUi(self)
        self.textCheck.clicked.connect(self.quit_text)

    def quit_text(self):

        self.text = str(self.textEdit.toPlainText())
        self.close()






